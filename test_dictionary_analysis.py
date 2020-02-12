import pytest
import dictionary_analysis
import filecmp
import os

def test_get_dictionary():
    assert(dictionary_analysis.get_dictionary('test_dictionary.csv') == {'along the lines of': [('HRAO-FLTS',)], 'altruistic': [('TRAO*-UFBG',)], 'Bayesian': [('PWA-EUZ', 'KWRA-PB')], 
'causality': [('KA-UFLT',)], 'cognizant': [('KO-G', 'TPH-EUFPBT')], 'dysfunctionally': [('STKP*-UBLGZ',)], 'explicitly': [('SPHR*-EUFLS',)], 'floppy': [('TPHRO-EUP',)], 'Glaswegian': [('TKPWHRA-PBLG',)], 'inconceivably': [('SKA-EFBL',)], 'paralyzed': [('PRA-LDZ',)], 'sidelines': 
[('STKHRAO-EUPBZ',)], 'third degree': [('THR-RGD',)], 'what sort of': [('SWHAO-FRT',)], 'zodiac': [('STKPWHRO-ED',), ('STKPWHRO-ED', 'KWRA-K')]})

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
    assert(dictionary_analysis.get_duplicates(dictionary) == {'zodiac': [('STKPWHRO-ED',), ('STKPWHRO-ED', 'KWRA-K')]})

def test_write_brief_list():
    words_matched = ['himself', 'employee', 'yesterday', 'landscape', 'regime', 'custom', 'vitamin']
    dictionary_analysis.write_brief_list(words_matched, 'test_brief_list.txt')
    assert(filecmp.cmp('test_brief_list.txt', 'premade_brief_list.txt'))  
    os.remove('test_brief_list.txt')   

if __name__ == '__main__':
    pytest.main()