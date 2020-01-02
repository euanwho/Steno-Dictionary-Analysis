import csv
from operator import attrgetter

dictionary = []
word_list = []
words_matched = []
words_to_brief = []

with open('data.csv') as dictionary_file:
    csv_reader = csv.reader(dictionary_file)
    dictionary = [{'English': line[0], 'Steno': line[1], 'Translates': line[2]} for line in csv_reader]
  
with open('wordList.csv') as word_list_file: 
    csv_reader = csv.reader(word_list_file)
    word_list = [line[0] for line in csv_reader]

for word in word_list:
  is_in_dictionary = False
  for entry in dictionary:
      if word == entry['English']:
        is_in_dictionary = True
        words_matched.append(word)
      ##if entry['Steno'].find('/'):
      ##  words_to_brief.append({'English': entry['English'], 'Steno': entry['Steno']})"""

def d_sort(dictionary): # function take s value as parameter 
  return int(dictionary['Translates'])

dictionary = sorted(dictionary, key=d_sort) # key takes function
print(dictionary)