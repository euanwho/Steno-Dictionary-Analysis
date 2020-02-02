import codecs
import inspect
import re
import collections

# TODO: Move dictionary format somewhere more canonical than formatting.
from formatting import META_RE

# A regular expression to capture an individual entry in the dictionary.
DICT_ENTRY_PATTERN = re.compile(r'(?s)(?<!\\){\\\*\\cxs (?P<steno>[^}]+)}' + 
                                r'(?P<translation>.*?)(?:(?<!\\)(?:\r\n|\n))*?'+
                                r'(?=(?:(?<!\\){\\\*\\cxs [^}]+})|' +
                                r'(?:(?:(?<!\\)(?:\r\n|\n)\s*)*}\s*\Z))')

class TranslationConverter:
    """Convert an RTF/CRE translation into plover's internal format."""
    
    def __init__(self, styles={}):
        self.styles = styles
        
        def linenumber(f):
            return f[1].__code__.co_firstlineno
        
        handler_funcs = inspect.getmembers(self, inspect.ismethod)
        handler_funcs.sort(key=linenumber)
        handlers = [self._make_re_handler(f.__doc__, f)
                    for name, f in handler_funcs 
                    if name.startswith('_re_handle_')]
        handlers.append(self._match_nested_command_group)
        def handler(s, pos):
            for handler in handlers:
                result = handler(s, pos)
                if result:
                    return result
            return None
        self._handler = handler
        self._command_pattern = re.compile(
            r'(\\\*)?\\([a-z]+)(-?[0-9]+)?[ ]?')
        self._multiple_whitespace_pattern = re.compile(r'([ ]{2,})')
        # This poorly named variable indicates whether the current context is
        # one where commands can be inserted (True) or not (False).
        self._whitespace = True
    
    def _make_re_handler(self, pattern, f):
        pattern = re.compile(pattern)
        def handler(s, pos):
            match = pattern.match(s, pos)
            if match:
                newpos = match.end()
                result = f(match)
                return (newpos, result)
            return None
        return handler

    def _re_handle_escapedchar(self, m):
        r'\\([-\\{}])'
        return m.group(1)
        
    def _re_handle_hardspace(self, m):
        r'\\~'
        return '{^ ^}'
        
    def _re_handle_dash(self, m):
        r'\\_'
        return '-'
        
    def _re_handle_escaped_newline(self, m):
        r'\\\r|\\\n'
        return '{#Return}{#Return}'
        
    def _re_handle_infix(self, m):
        r'\\cxds ([^{}\\\r\n]+)\\cxds ?'
        return '{^%s^}' % m.group(1)
        
    def _re_handle_suffix(self, m):
        r'\\cxds ([^{}\\\r\n ]+)'
        return '{^%s}' % m.group(1)

    def _re_handle_prefix(self, m):
        r'([^{}\\\r\n ]+)\\cxds ?'
        return '{%s^}' % m.group(1)

    def _re_handle_commands(self, m):
        r'(\\\*)?\\([a-z]+)(-?[0-9]+)? ?'
        
        command = m.group(2)
        arg = m.group(3)
        if arg:
            arg = int(arg)
        
        if command == 'cxds':
            return '{^}'
        
        if command == 'cxfc':
            return '{-|}'

        if command == 'cxfl':
            return '{>}'

        if command == 'par':
            self.seen_par = True
            return '{#Return}{#Return}'
            
        if command == 's':
            result = []
            if not self.seen_par:
                result.append('{#Return}{#Return}')
            style_name = self.styles.get(arg, '')
            if style_name.startswith('Contin'):
                result.append('{^    ^}')
            return ''.join(result)

        # Unrecognized commands are ignored.
        return ''

    def _re_handle_simple_command_group(self, m):
        r'{(\\\*)?\\([a-z]+)(-?[0-9]+)?[ ]?([^{}]*)}'
        
        ignore = bool(m.group(1))
        command = m.group(2)
        contents = m.group(4)
        if contents is None:
            contents = ''

        if command == 'cxstit':
            # Plover doesn't support stitching.
            return self(contents)
        
        if command == 'cxfing':
            prev = self._whitespace
            self._whitespace = False
            result = '{&' + contents + '}'
            self._whitespace = prev
            return result
            
        if command == 'cxp':
            prev = self._whitespace
            self._whitespace = False
            contents = self(contents)
            if contents is None:
                return None
            self._whitespace = prev
            stripped = contents.strip()
            if stripped in ['.', '!', '?', ',', ';', ':']:
                return '{' + stripped + '}'
            if stripped == "'":
                return "{^'}"
            if stripped in ['-', '/']:
                return '{^' + contents + '^}'
            # Show unknown punctuation as given.
            return '{^' + contents + '^}'
        
        if command == 'cxsvatdictflags' and 'N' in contents:
            return '{-|}'
        
        # unrecognized commands
        if ignore:
            return ''
        else:
            return self(contents)

    def _re_handle_eclipse_command(self, m):
        r'({[^\\][^{}]*})'
        return m.group()

    # caseCATalyst doesn't put punctuation in \cxp so we will treat any 
    # isolated punctuation at the beginning of the translation as special.
    def _re_handle_punctuation(self, m):
        r'^([.?!:;,])(?=\s|$)'
        if self._whitespace:
            result = '{%s}' % m.group(1)
        else:
            result = m.group(1)
        return result

    def _re_handle_text(self, m):
        r'[^{}\\\r\n]+'
        text = m.group()
        if self._whitespace:
            text = self._multiple_whitespace_pattern.sub(r'{^\1^}', text)
        return text

    def _get_matching_bracket(self, s, pos):
        if s[pos] != '{':
            return None
        end = len(s)
        depth = 1
        pos += 1
        while pos != end:
            c = s[pos]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            if depth == 0:
                break
            pos += 1
        if pos < end and s[pos] == '}':
            return pos
        return None

    def _get_command(self, s, pos):
        return self._command_pattern.match(s, pos)

    def _match_nested_command_group(self, s, pos):
        startpos = pos
        endpos = self._get_matching_bracket(s, pos)
        if endpos is None:
            return None

        command_match = self._get_command(s, startpos + 1)
        if command_match is None:
            return None

        ignore = bool(command_match.group(1))
        command = command_match.group(2)
        
        if command == 'cxconf':
            pos = command_match.end()
            last = ''
            while pos < endpos:
                if s[pos] in ['[', '|', ']']:
                    pos += 1
                    continue
                if s[pos] == '{':
                    command_match = self._get_command(s, pos + 1)
                    if command_match is None:
                        return None
                    if command_match.group(2) != 'cxc':
                        return None
                    cxc_end = self._get_matching_bracket(s, pos)
                    if cxc_end is None:
                        return None
                    last = s[command_match.end():cxc_end]
                    pos = cxc_end + 1
                    continue
                return None
            return (endpos + 1, self(last))
            
        if ignore:
            return (endpos + 1, '')
        else:
            return (endpos + 1, self(s[command_match.end():endpos]))

    def __call__(self, s):
        self.seen_par = False
        
        pos = 0
        tokens = []
        handler = self._handler
        end = len(s)
        while pos != end:
            result = handler(s, pos)
            if result is None:
                return None
            pos = result[0]
            token = result[1]
            if token is None:
                return None
            tokens.append(token)
        return ''.join(tokens)

STYLESHEET_RE = re.compile(r'(?s){\\s([0-9]+).*?((?:\b\w+\b\s*)+);}')

def load_stylesheet(s):
    """Returns a dictionary mapping a number to a style name."""
    return {int(k): v for k, v in STYLESHEET_RE.findall(s)}

HEADER = ("{\\rtf1\\ansi{\\*\\cxrev100}\\cxdict{\\*\\cxsystem Plover}" +
          "{\\stylesheet{\\s0 Normal;}}\r\n")

def format_translation(t):
    t = ' '.join([x.strip() for x in META_RE.findall(t) if x.strip()])
    
    t = re.sub(r'{\.}', r'{\\cxp. }', t)
    t = re.sub(r'{!}', r'{\\cxp! }', t)
    t = re.sub(r'{\?}', r'{\\cxp? }', t)
    t = re.sub(r'{\,}', r'{\\cxp, }', t)
    t = re.sub(r'{:}', r'{\\cxp: }', t)
    t = re.sub(r'{;}', r'{\\cxp; }', t)
    t = re.sub(r'{\^}', r'\\cxds ', t)
    t = re.sub(r'{\^([^^}]*)}', r'\\cxds \1', t)
    t = re.sub(r'{([^^}]*)\^}', r'\1\\cxds ', t)
    t = re.sub(r'{\^([^^}]*)\^}', r'\\cxds \1\\cxds ', t)
    t = re.sub(r'{-\|}', r'\\cxfc ', t)
    t = re.sub(r'{>}', r'\\cxfls ', t)
    t = re.sub(r'{ }', r' ', t)
    t = re.sub(r'{&([^}]+)}', r'{\\cxfing \1}', t)
    t = re.sub(r'{#([^}]+)}', r'\\{#\1\\}', t)
    t = re.sub(r'{PLOVER:([a-zA-Z]+)}', r'\\{PLOVER:\1\\}', t)
    t = re.sub(r'\\"', r'"', t)

    return t

STROKE_DELIMITER = '/'

_NUMBERS = set('0123456789')
_IMPLICIT_NUMBER_RX = re.compile('(^|[1-4])([6-9])')
NUMBER_KEY = lambda mod: mod.NUMBER_KEY
IMPLICIT_HYPHEN_KEYS = lambda mod: set(mod.IMPLICIT_HYPHEN_KEYS),
IMPLICIT_HYPHENS = lambda mod: {l.replace('-', '') for l in mod.IMPLICIT_HYPHEN_KEYS}

def normalize_stroke(stroke):
    letters = set(stroke)
    if letters & _NUMBERS:
        if NUMBER_KEY in letters:
            stroke = stroke.replace(NUMBER_KEY, '')
        # Insert dash when dealing with 'explicit' numbers
        m = _IMPLICIT_NUMBER_RX.search(stroke)
        if m is not None:
            start = m.start(2)
            return stroke[:start] + '-' + stroke[start:]
    if '-' in letters:
        if stroke.endswith('-'):
            stroke = stroke[:-1]
        ## changed his and I don't know what it does
        elif IMPLICIT_HYPHENS in letters:
            stroke = stroke.replace('-', '')
    return stroke

def normalize_steno(strokes_string):
    """Convert steno strings to one common form."""
    return tuple(normalize_stroke(stroke) for stroke
                 in strokes_string.split(STROKE_DELIMITER))

class StenoDictionary:
    """A steno dictionary.
    This dictionary maps immutable sequences to translations and tracks the
    length of the longest key.
    Attributes:
    longest_key -- A read only property holding the length of the longest key.
    timestamp -- File last modification time, used to detect external changes.
    """

    # False if class support creation.
    readonly = False

    def __init__(self):
        self._dict = {}
        self._longest_key_length = 0
        self._longest_listener_callbacks = set()
        self.reverse = collections.defaultdict(list)
        # Case-insensitive reverse dict
        self.casereverse = collections.defaultdict(list)
        self.filters = []
        self.timestamp = 0
        self.readonly = False
        self.enabled = True
        self.path = None

    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self.path)

    def __repr__(self):
        return str(self)

    @property
    def longest_key(self):
        """The length of the longest key in the dict."""
        return self._longest_key

    def __len__(self):
        return self._dict.__len__()

    def __iter__(self):
        return self._dict.__iter__()

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def clear(self):
        self._dict.clear()
        self.reverse.clear()
        self.casereverse.clear()
        self._longest_key = 0

    def items(self):
        return self._dict.items()

    def update(self, *args, **kwargs):
        assert not self.readonly
        iterable_list = [
            a.items() if isinstance(a, (dict, StenoDictionary))
            else a for a in args
        ]
        if kwargs:
            iterable_list.append(kwargs.items())
        if not self._dict:
            reverse = self.reverse
            casereverse = self.casereverse
            longest_key = self._longest_key
            assert not (reverse or casereverse or longest_key)
            self._dict = dict(*iterable_list)
            for key, value in self._dict.items():
                reverse[value].append(key)
                casereverse[value.lower()].append(value)
                key_len = len(key)
                if key_len > longest_key:
                    longest_key = key_len
            self._longest_key = longest_key
        else:
            for iterable in iterable_list:
                for key, value in iterable:
                    self[key] = value

    def __setitem__(self, key, value):
        assert not self.readonly
        if key in self:
            del self[key]
        self._longest_key = max(self._longest_key, len(key))
        self._dict[key] = value
        self.reverse[value].append(key)
        self.casereverse[value.lower()].append(value)

    def get(self, key, fallback=None):
        return self._dict.get(key, fallback)

    def __delitem__(self, key):
        assert not self.readonly
        value = self._dict.pop(key)
        self.reverse[value].remove(key)
        self.casereverse[value.lower()].remove(value)
        if len(key) == self.longest_key:
            if self._dict:
                self._longest_key = max(len(x) for x in self._dict)
            else:
                self._longest_key = 0

    def __contains__(self, key):
        return self.get(key) is not None

    def reverse_lookup(self, value):
        return set(self.reverse[value])

    def casereverse_lookup(self, value):
        return set(self.casereverse[value])

    @property
    def _longest_key(self):
        return self._longest_key_length

    @_longest_key.setter
    def _longest_key(self, longest_key):
        if longest_key == self._longest_key_length:
            return
        self._longest_key_length = longest_key
        for callback in self._longest_listener_callbacks:
            callback(longest_key)

    def add_longest_key_listener(self, callback):
        self._longest_listener_callbacks.add(callback)

    def remove_longest_key_listener(self, callback):
        self._longest_listener_callbacks.remove(callback)


class RtfDictionary(StenoDictionary):

    def load(self, filename):
        with open(filename, 'rb') as fp:
            s = fp.read().decode('cp1252')
        def parse():
            styles = load_stylesheet(s)
            converter = TranslationConverter(styles)
            for m in DICT_ENTRY_PATTERN.finditer(s):
                steno = normalize_steno(m.group('steno'))
                translation = m.group('translation')
                converted = converter(translation)
                if converted is not None:
                    yield steno, converted
        self.update(parse())

    def save(self, filename):
        with open(filename, 'wb') as fp:
            writer = codecs.getwriter('cp1252')(fp)
            writer.write(HEADER)
            for s, t in self.items():
                s = '/'.join(s)
                t = format_translation(t)
                entry = "{\\*\\cxs %s}%s\r\n" % (s, t)
                writer.write(entry)
            writer.write("}\r\n")

dic = RtfDictionary()
dic.load('PD.rtf')
