import re
CASE_CAP_FIRST_WORD = 'cap_first_word'
CASE_LOWER = 'lower'
CASE_LOWER_FIRST_CHAR = 'lower_first_char'
CASE_TITLE = 'title'
CASE_UPPER = 'upper'
CASE_UPPER_FIRST_WORD = 'upper_first_word'

SPACE = ' '
META_ATTACH_FLAG = '^'
META_CAPITALIZE = '-|'
META_CARRY_CAPITALIZATION = '~|'
META_COMMAND = 'PLOVER:'
META_COMMAS = (',', ':', ';')
META_CUSTOM = ':'
META_GLUE_FLAG = '&'
META_KEY_COMBINATION = '#'
META_LOWER = '>'
META_MODE = 'MODE:'
META_RETRO_CAPITALIZE = '*-|'
META_RETRO_FORMAT = '*('
META_RETRO_LOWER = '*>'
META_RETRO_UPPER = '*<'
META_STOPS = ('.', '!', '?')
META_UPPER = '<'
MODE_CAMEL = 'CAMEL'
MODE_CAPS = 'CAPS'
MODE_LOWER = 'LOWER'
MODE_RESET = 'RESET'
MODE_RESET_CASE = 'RESET_CASE'
MODE_RESET_SPACE = 'RESET_SPACE'
MODE_SET_SPACE = 'SET_SPACE:'
MODE_SNAKE = 'SNAKE'
MODE_TITLE = 'TITLE'

META_ESCAPE = '\\'
RE_META_ESCAPE = '\\\\'
META_START = '{'
META_END = '}'
META_ESC_START = META_ESCAPE + META_START
META_ESC_END = META_ESCAPE + META_END

META_RE = re.compile(r"""(?:%s%s|%s%s|[^%s%s])+ # One or more of anything
                                                # other than unescaped { or }
                                                #
                                              | # or
                                                #
                     %s(?:%s%s|%s%s|[^%s%s])*%s # Anything of the form {X}
                                                # where X doesn't contain
                                                # unescaped { or }
                      """ % (RE_META_ESCAPE, META_START, RE_META_ESCAPE,
                             META_END, META_START, META_END,
                             META_START,
                             RE_META_ESCAPE, META_START, RE_META_ESCAPE,
                             META_END, META_START, META_END,
                             META_END),
                     re.VERBOSE)