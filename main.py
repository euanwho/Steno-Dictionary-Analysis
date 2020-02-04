from dictionary_analysis import *
import sys

dictionary_file = sys.argv[1]
word_list_file = sys.argv[2]
dictionary = get_dictionary(dictionary_file)
word_list = get_word_list(word_list_file)

with open('Dictionary Analysis Results.txt', 'w') as results:
    results.write('Briefs to be made: \n')
    briefs = get_briefs(dictionary, word_list)
    for i, brief in enumerate(briefs):
        results.write(f' {i+1}:  {brief} \n')

    results.write('Duplicate entries found in dictionary: \n')
    duplicates = get_duplicates(dictionary)
    for i, duplicate in enumerate(duplicates):
        results.write(f' {i+1}:  {duplicate} \n')

    results.write('Words missing in dictionary: \n')    
    missing_words = get_missing_words(dictionary, word_list)
    for i, missing_word in enumerate(missing_words):
        results.write(f' {i+1}:  {missing_word} \n')
