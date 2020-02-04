from dictionary_analysis import *
import sys

dictionary_file = sys.argv[1]
word_list_file = sys.argv[2]

with open('Dictionary Analysis Results.txt', 'w') as results:
    results.write('Briefs to be made: \n')
    briefs = get_briefs(dictionary_file, word_list_file)
    for i, brief in enumerate(briefs):
        results.write(f' {i+1}:  {brief} \n')

    results.write('Duplicate entries found in dictionary: \n')
    duplicates = get_duplicates(dictionary_file)
    for i, duplicate in enumerate(duplicates):
        results.write(f' {i+1}:  {duplicate} \n')

    results.write('Words missing in dictionary: \n')    
    missing_words = get_missing_words(dictionary_file, word_list_file)
    for i, missing_word in enumerate(missing_words):
        results.write(f' {i+1}:  {missing_word} \n')
