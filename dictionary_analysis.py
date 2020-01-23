import csv
import pickle

def get_dictionary(file_name):
  """Return dictionary file as a dictionary"""
  dictionary = []
  with open(file_name) as dictionary_file:
      csv_reader = csv.reader(dictionary_file)
      dictionary = [{'English': line[0], 'Steno': line[1], 'Translates': line[2]} for line in csv_reader]

  def dict_sort(dictionary): # function take s value as parameter 
    return int(dictionary['Translates'])

  dictionary = sorted(dictionary, key=dict_sort) # key takes function

  return dictionary

def get_word_list(file_name):  
  """Return word list file as a list"""
  word_list = []
  with open(file_name) as word_list_file: 
      csv_reader = csv.reader(word_list_file)
      word_list = [line[0] for line in csv_reader]

  return word_list

def get_briefs(dictionary_file_name, word_list_file_name):
  """Return a list of words for which there is no one-stroker"""
  dictionary, word_list = get_dictionary(dictionary_file_name), get_word_list(word_list_file_name)

  words_matched = []
  words_unmatched = []
  for word in word_list:
    for entry in dictionary:
      if word == entry['English'] and '/' in entry['Steno']:
        words_matched.append(word)
      elif word == entry['English'] and '/' not in entry['Steno']:
        words_unmatched.append(word)

  words_matched = [word for word in words_matched if word not in words_unmatched]
        
  return words_matched

def get_missing_words(dictionary_file_name, word_list_file_name):
  """Return list of words that aren't in a dictionary as compared with a word list"""
  dictionary, word_list = get_dictionary(dictionary_file_name), get_word_list(word_list_file_name)

  words_not_matched = []
  for word in word_list:
    for entry in dictionary:
        if word == entry['English']:
          break
    else:
      words_not_matched.append(word)

  return words_not_matched

def write_list(words_matched, output_file_name='words_to_brief'):
  """Produce a .txt file from a list of words"""
  with open(output_file_name + '.txt', 'w') as wordlist_generated:
    for word in words_matched:
      wordlist_generated.write(word + '\n')

def pickle_object(obj, file_name):
  with open(file_name, 'wb') as pickled_file:
    pickle.dump(obj, pickled_file)

def unpickle_object(obj, file_name):
  with open(file_name, 'rb') as unpickled_object:
    pickle.load(unpickled_object)

## Todo: 
## write function to detect conflicts - compare these against a word list
## take in two-item tuple/list and check that they are written differently 