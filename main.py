from dictionary_analysis import get_briefs, get_missing_words
print(get_briefs('data.csv', 'word_list.csv'))
print(get_missing_words('data.csv', 'missing_words.csv'))