import csv
import pickle
import profile
from collections import Counter, defaultdict
import pprint

def get_dictionary(file_name):
  """Return dictionary file as a dictionary"""
  dictionary = defaultdict(list)
  with open(file_name) as dictionary_file:
      csv_reader = csv.reader(dictionary_file)
      for line in csv_reader:
        strokes = tuple(line[1].split('/'))
        dictionary[line[0]] = [strokes]
  return dictionary

def get_word_list(file_name):  
  """Return word list file as a list"""
  word_list = []
  with open(file_name) as word_list_file: 
      csv_reader = csv.reader(word_list_file)
      word_list = [line[0] for line in csv_reader]
  return word_list

def get_briefs(dictionary, word_list):
  """Return a list of words for which there is no one-stroker"""
  words_matched = []
  for word in word_list:
    if word in dictionary and len(dictionary[word][0]) > 1:
      words_matched.append(word)
  return words_matched

def get_missing_words(dictionary, word_list):
  """Return list of words that aren't in a dictionary as compared with a word list"""
  words_not_matched = []
  for word in word_list:
    if word not in dictionary:
      words_not_matched.append(word)
  return words_not_matched

def get_duplicates(dictionary):
  """Return a list of dictionary entries that are duplicates"""
  key_counts = Counter(entry['English'] for entry in dictionary)
  duplicates = dict()
  for entry in dictionary:
    if key_counts[entry['English']] > 1 and entry['English'] not in duplicates:
      duplicates[entry['English']] = [entry]
    elif key_counts[entry['English']] > 1 and entry['English'] in duplicates:
      duplicates[entry['English']].append(entry)  
  return duplicates

def write_brief_list(words_matched, output_file_name='words_to_brief'):
  """Produce a .txt file from a list of words"""
  with open(output_file_name, 'w') as wordlist_generated:
    for word in words_matched:
      wordlist_generated.write(word + '\n')

def pickle_object(obj, file_name):
  with open(file_name, 'wb') as pickled_file:
    pickle.dump(obj, pickled_file)

def unpickle_object(obj, file_name):
  with open(file_name, 'rb') as unpickled_object:
    pickle.load(unpickled_object)

## Todo: 
# make any functions generators?
# make get_duplicates better
