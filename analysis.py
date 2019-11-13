import csv

dictionary = []
word_list = []
words_matched = []
words_to_brief = []

with open('data.csv') as dictionary_file:
    csv_reader = csv.reader(dictionary_file)

    for line in csv_reader:
      dictionary.append({'English': line[0], 'Steno': line[1], 'Translates': line[2]})

with open('wordList.csv') as word_list_file:
    csv_reader = csv.reader(word_list_file)
    for line in csv_reader:
      word_list.append(line[0])

for word in word_list:
  for entry in dictionary:
      if word == entry['English']:
        words_matched.append(word)
      if entry['Steno'].find('/'):
        words_to_brief.append({'English': entry['English'], 'Steno': entry['Steno']})
        

print(words_to_brief)

print(dictionary[2])