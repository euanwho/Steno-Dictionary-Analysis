import pytest
import dictionary_analysis
import filecmp
import os

def test_get_dictionary():
    assert(dictionary_analysis.get_dictionary('test_dictionary.csv') == [{'English': 'zodiac', 'Steno': 'STKPWHRO-ED', 'Translates': '0'}, {'English': 'zodiac', 'Steno': 'STKPWHRO-ED/KWRA-K', 'Translates': '0'}, 
{'English': 'Bayesian', 'Steno': 'PWA-EUZ/KWRA-PB', 'Translates': '1'}, {'English': 'paralyzed', 'Steno': 'PRA-LDZ', 'Translates': '3'}, {'English': 'cognizant', 'Steno': 'KO-G/TPH-EUFPBT', 'Translates': '5'}, {'English': 'dysfunctionally', 'Steno': 'STKP*-UBLGZ', 'Translates': '5'}, {'English': 'sidelines', 'Steno': 'STKHRAO-EUPBZ', 'Translates': '5'}, {'English': 'inconceivably', 'Steno': 'SKA-EFBL', 'Translates': 
'7'}, {'English': 'causality', 'Steno': 'KA-UFLT', 'Translates': '12'}, {'English': 'along the lines of', 'Steno': 'HRAO-FLTS', 'Translates': '15'}, {'English': 'Glaswegian', 'Steno': 'TKPWHRA-PBLG', 'Translates': '16'}, {'English': 'floppy', 'Steno': 'TPHRO-EUP', 'Translates': '18'}, {'English': 'altruistic', 'Steno': 'TRAO*-UFBG', 'Translates': '23'}, {'English': 'third degree', 'Steno': 'THR-RGD', 'Translates': '24'}, {'English': 'what sort of', 'Steno': 'SWHAO-FRT', 'Translates': '33'}, {'English': 'explicitly', 'Steno': 'SPHR*-EUFLS', 'Translates': 
'88'}])

def test_get_word_list():
    assert(dictionary_analysis.get_word_list('test_word_list.csv') == ['cognizant', 'Bayesian', 'antidisestablishmentarianism', 'Euan'])

def test_get_briefs():
    dictionary = dictionary_analysis.get_dictionary('test_dictionary.csv')
    word_list = dictionary_analysis.get_word_list('test_word_list.csv')
    assert(dictionary_analysis.get_briefs(dictionary, word_list) == ['cognizant', 'Bayesian'])

def test_get_missing_words():
    dictionary = dictionary_analysis.get_dictionary('test_dictionary.csv')
    word_list = dictionary_analysis.get_word_list('test_word_list.csv')
    assert(dictionary_analysis.get_missing_words(dictionary, word_list) == ['antidisestablishmentarianism', 'Euan'])

def test_get_duplicates():
    dictionary = dictionary_analysis.get_dictionary('test_dictionary.csv')
    assert(dictionary_analysis.get_duplicates(dictionary) == {'zodiac': [{'English': 'zodiac', 'Steno': 'STKPWHRO-ED', 'Translates': '0'}, {'English': 'zodiac', 'Steno': 'STKPWHRO-ED/KWRA-K', 'Translates': '0'}]})

def test_write_brief_list():
    words_matched = ['himself', 'employee', 'yesterday', 'landscape', 'regime', 'custom', 'vitamin']
    dictionary_analysis.write_brief_list(words_matched, 'test_brief_list.txt')
    assert(filecmp.cmp('test_brief_list.txt', 'premade_brief_list.txt'))  
    os.remove('test_brief_list.txt')   

if __name__ == '__main__':
    pytest.main()