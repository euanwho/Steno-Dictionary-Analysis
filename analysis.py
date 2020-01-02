import csv

dictionary = []
word_list = []
words_matched = []

# Open the dictionary and store it in the var dictionary
with open('data.csv') as dictionary_file:
    csv_reader = csv.reader(dictionary_file)
    dictionary = [{'English': line[0], 'Steno': line[1], 'Translates': line[2]} for line in csv_reader]
  
# Open the word list against we will check the dictionary and store it in the var word_list
with open('wordList.csv') as word_list_file: 
    csv_reader = csv.reader(word_list_file)
    word_list = [line[0] for line in csv_reader]

# Add the words for which there isn't a one-stroker to word_matched
for word in word_list:
  for entry in dictionary:
      if word == entry['English'] and '/' in entry['Steno']:
        words_matched.append(word)
      
def dict_sort(dictionary): # function take s value as parameter 
  return int(dictionary['Translates'])

dictionary = sorted(dictionary, key=dict_sort) # key takes function
print(words_matched)
##print(dictionary)