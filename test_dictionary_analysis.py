import pytest
from dictionary_analysis import Dictionary, WordList, Analyser
import filecmp
import os

def test_get_dictionary():
    dictionary = Dictionary('test_dictionary.csv')
    assert(dictionary.dictionary == {'along the lines of': [('HRAO-FLTS',)], 'altruistic': [('TRAO*-UFBG',)], 'Bayesian': [('PWA-EUZ', 'KWRA-PB')], 
'causality': [('KA-UFLT',)], 'cognizant': [('KO-G', 'TPH-EUFPBT')], 'dysfunctionally': [('STKP*-UBLGZ',)], 'explicitly': [('SPHR*-EUFLS',)], 'floppy': [('TPHRO-EUP',)], 'Glaswegian': [('TKPWHRA-PBLG',)], 'inconceivably': [('SKA-EFBL',)], 'paralyzed': [('PRA-LDZ',)], 'sidelines': 
[('STKHRAO-EUPBZ',)], 'third degree': [('THR-RGD',)], 'what sort of': [('SWHAO-FRT',)], 'zodiac': [('STKPWHRO-ED',), ('STKPWHRO-ED', 'KWRA-K')]})

def test_get_word_list():
    word_list = WordList('test_word_list.csv')
    assert(word_list.word_list == ['cognizant', 'Bayesian', 'antidisestablishmentarianism', 'Euan'])

def test_get_briefs():
    dictionary = Dictionary('test_dictionary.csv')
    word_list = WordList('test_word_list.csv')
    analyser = Analyser()
    assert(analyser.get_briefs(dictionary, word_list) == ['cognizant', 'Bayesian'])

def test_get_missing_words():
    dictionary = Dictionary('test_dictionary.csv')
    word_list = WordList('test_word_list.csv')
    analsyer = Analyser()
    assert(Analyser.get_missing_words(dictionary, word_list) == ['antidisestablishmentarianism', 'Euan'])

def test_get_duplicates():
    dictionary = Dictionary('test_dictionary.csv')
    assert(dictionary.duplicates == {'zodiac': [('STKPWHRO-ED',), ('STKPWHRO-ED', 'KWRA-K')]})

def test_write_brief_list():
    word_list = WordList('test_word_list.csv')
    words_matched = ['himself', 'employee', 'yesterday', 'landscape', 'regime', 'custom', 'vitamin']
    word_list.write(words_matched, 'test_brief_list.txt')
    assert(filecmp.cmp('test_brief_list.txt', 'premade_brief_list.txt'))  
    os.remove('test_brief_list.txt')   

if __name__ == '__main__':
    pytest.main()