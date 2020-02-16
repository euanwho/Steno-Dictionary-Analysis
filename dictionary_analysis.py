import csv
from collections import Counter, defaultdict
from rtf_parser import RtfDictionary

class Dictionary():

  def __init__(self, file_name):
          self.dictionary = self.get_dictionary(file_name)
          self.duplicates = self.get_duplicates()

  def get_dictionary(self, file_name):
    """Return dictionary file as a dictionary"""
    if '.csv' in file_name:
      dictionary = defaultdict(list)
      with open(file_name) as dictionary_file:
          csv_reader = csv.reader(dictionary_file)
          for line in csv_reader:
            word, steno = line[0], tuple(line[1].split('/'))
            if word not in dictionary:
              dictionary[word] = [steno]
            else:
              dictionary[word].append(steno)
    elif '.rtf' in file_name:
      RtfDictionary = RtfDictionary()
      RtfDictionary.load(file_name)
      dictionary = RtfDictionary.reverse
    return dictionary

    
  def get_duplicates(self):
    """Return a list of dictionary entries that are duplicates"""
    key_counts = Counter(self.dictionary)
    duplicates = dict()
    for key, value in self.dictionary.items():
      if len(value) > 1:
        duplicates[key] = value
    return duplicates

class Analyser():
  
  @staticmethod  
  def get_briefs(Dictionary, WordList):
    """Return a list of words for which there is no one-stroker"""
    words_matched = []
    for word in WordList.word_list:
      if word in Dictionary.dictionary and len(Dictionary.dictionary[word][0]) > 1:
        words_matched.append(word)
    return words_matched

  @staticmethod
  def get_missing_words(Dictionary, WordList):
    """Return list of words that aren't in a dictionary as compared with a word list"""
    words_not_matched = []
    for word in WordList.word_list:
      if word not in Dictionary.dictionary:
        words_not_matched.append(word)
    return words_not_matched

class WordList():

  def __init__(self, file_name):
    self.word_list = self.get_word_list(file_name)

  def get_word_list(self, file_name):  
    """Return word list file as a list"""
    word_list = []
    with open(file_name) as word_list_file: 
        csv_reader = csv.reader(word_list_file)
        word_list = [line[0] for line in csv_reader]
    return word_list

def write(words_matched, output_file_name='words_to_brief'):
  """Produce a .txt file from a list of words"""
  with open(output_file_name, 'w') as wordlist_generated:
    for word in words_matched:
      wordlist_generated.write(word + '\n')
      
d = Dictionary('test_dictionary.csv')
w = WordList('test_word_list.csv')
a = Analyser()
print(a.get_briefs(d, w), a.get_missing_words(d, w))