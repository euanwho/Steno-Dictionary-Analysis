import pytest
import dictionary_analysis

def test_get_dictionary():
    assert(dictionary_analysis.get_dictionary('test_dictionary.csv') == [{'English': 'zodiac', 'Steno': 'STKPWHRO-ED', 'Translates': '0'}, {'English': 'zodiac', 'Steno': 'STKPWHRO-ED/KWRA-K', 'Translates': '0'}, 
{'English': 'Bayesian', 'Steno': 'PWA-EUZ/KWRA-PB', 'Translates': '1'}, {'English': 'paralyzed', 'Steno': 'PRA-LDZ', 'Translates': '3'}, {'English': 'cognizant', 'Steno': 'KO-G/TPH-EUFPBT', 'Translates': '5'}, {'English': 'dysfunctionally', 'Steno': 'STKP*-UBLGZ', 'Translates': '5'}, {'English': 'sidelines', 'Steno': 'STKHRAO-EUPBZ', 'Translates': '5'}, {'English': 'inconceivably', 'Steno': 'SKA-EFBL', 'Translates': 
'7'}, {'English': 'causality', 'Steno': 'KA-UFLT', 'Translates': '12'}, {'English': 'along the lines of', 'Steno': 'HRAO-FLTS', 'Translates': '15'}, {'English': 'Glaswegian', 'Steno': 'TKPWHRA-PBLG', 'Translates': '16'}, {'English': 'floppy', 'Steno': 'TPHRO-EUP', 'Translates': '18'}, {'English': 'altruistic', 'Steno': 'TRAO*-UFBG', 'Translates': '23'}, {'English': 'third degree', 'Steno': 'THR-RGD', 'Translates': '24'}, {'English': 'what sort of', 'Steno': 'SWHAO-FRT', 'Translates': '33'}, {'English': 'explicitly', 'Steno': 'SPHR*-EUFLS', 'Translates': 
'88'}]

def test_get_word_list():
    assert(dictionary_analysis.get_word_list('test_word_list.csv') == ['cognizant', 'Bayesian', 'antidisestablishmentarianism', 'Euan'])

def test_get_briefs():
    assert(dictionary_analysis.get_briefs('test_dictionary.csv', 'test_word_list.csv') == ['cognizant', 'Bayesian'])

def test_get_missing_words():
    assert(dictionary_analysis.get_missing_words('test_dictionary.csv', 'test_word_list.csv') == ['antidisestablishmentarianism', 'Euan'])

def test_get_duplicates():
    assert(dictionary_analysis.get_duplicates('test_dictionary.csv') == [{'English': 'zodiac', 'Steno': 'STKPWHRO-ED', 'Translates': '0'}, {'English': 'zodiac', 'Steno': 'STKPWHRO-ED/KWRA-K', 'Translates': '0'}])

def test_write_list():
    pass

## TODO: 
# write test_write_list

if __name__ == '__main__':
    pytest.main()