# -*- coding: utf-8 -*-
"""
This is a translation script for Japanese, English, Chinese and Spanish.

Usage:
    python translate_ja_en_zh_es.py 'phrase'
    The phrase should be enclosed in single or double quotations

Output:
    translated phrase and pronouncitation
"""

import io, sys
from py_translator import Translator
import pandas as pd

# set encoding utf-8 to prevent text garbling in Japanese or Chinese
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def to_japanese(translator_obj, input_phrase):
    translated_phrase = translator_obj.translate(input_phrase, dest='ja')
    print('In Japanese: %s' % translated_phrase.text)
    return translated_phrase

def to_english(translator_obj, input_phrase):
    translated_phrase = translator_obj.translate(input_phrase, dest='en')
    print('In English: %s' % translated_phrase.text)
    return translated_phrase

def to_chinese_simplified(translator_obj, input_phrase):
    translated_phrase = translator_obj.translate(input_phrase, dest='zh-CN')
    if translated_phrase.src == 'zh-CN':
        print('Pronounciation: %s' % translated_phrase.pronunciation)
    else:    
        print('In Simplified Chinese: %s Pronounciation: %s' % (translated_phrase.text, translated_phrase.pronunciation))
    return translated_phrase

def to_spanish(translator_obj, input_phrase):
    translated_phrase = translator_obj.translate(input_phrase, dest='es')
    print('In Spanish: %s' % translated_phrase.text)
    return translated_phrase

def translate(input_phrase):
    translator = Translator()

    # detect language type of input phrase
    detect_result = translator.detect(input_phrase)
    language_type = detect_result.lang

    # define data frame
    trans_phrase_array = [''] * 5
    colmuns_list = ['English', 'Japanese', 'Spanish', 'Chinese', 'Ch_Prns']

    print('Language type: %s' % language_type)

    # switch translation process depend on language type
    if 'ja' in language_type: # Japanese
        print('Input phrase is Japanese')
        phrase_in_zh          = to_chinese_simplified(translator, input_phrase)
        trans_phrase_array[0] = to_english(translator, input_phrase).text
        trans_phrase_array[1] = input_phrase
        trans_phrase_array[2] = to_spanish(translator, input_phrase).text
        trans_phrase_array[3] = phrase_in_zh.text
        trans_phrase_array[4] = phrase_in_zh.pronunciation
    elif 'zh-CN' in language_type: # Chinese(Simplified)
        print('Input phrase is Simplified Chinese')
        phrase_in_zh          = to_chinese_simplified(translator, input_phrase)
        trans_phrase_array[0] = to_english(translator, input_phrase).text
        trans_phrase_array[1] = to_japanese(translator, input_phrase).text
        trans_phrase_array[2] = to_spanish(translator, input_phrase).text
        trans_phrase_array[3] = phrase_in_zh.text
        trans_phrase_array[4] = phrase_in_zh.pronunciation
    elif 'en' in language_type: # English
        print('Input phrase is English')
        phrase_in_zh          = to_chinese_simplified(translator, input_phrase)
        trans_phrase_array[0] = input_phrase
        trans_phrase_array[1] = to_japanese(translator, input_phrase).text
        trans_phrase_array[2] = to_spanish(translator, input_phrase).text
        trans_phrase_array[3] = phrase_in_zh.text
        trans_phrase_array[4] = phrase_in_zh.pronunciation
    elif 'es' in language_type: # Spanish
        print('Input phrase is Spanish')
        phrase_in_zh          = to_chinese_simplified(translator, input_phrase)
        trans_phrase_array[0] = to_english(translator, input_phrase).text
        trans_phrase_array[1] = to_japanese(translator, input_phrase).text
        trans_phrase_array[2] = input_phrase
        trans_phrase_array[3] = phrase_in_zh.text
        trans_phrase_array[4] = phrase_in_zh.pronunciation
    else:
        print('Input phrase should be Japanese, English, Chinese or Spanish')
    
    # write in csv
    # df_trans_phrase = pd.DataFrame(index=[], columns=colmuns_list)
    df_trans_phrase = pd.read_csv('phrase_translation_database.csv', encoding='utf-8-sig', index_col=0)
    sr_trans_phrase = pd.Series(trans_phrase_array, index=colmuns_list, name=input_phrase)
    df_trans_phrase = df_trans_phrase.append(sr_trans_phrase)
    df_trans_phrase.to_csv('phrase_translation_database.csv', encoding='utf-8-sig')

if __name__ == '__main__':
    # get command line input
    argv     = sys.argv
    argv_len = len(argv)

    # check there is an input phrase
    if argv_len == 2:
        input_phrase = argv[1]
    else:
        print("please input phrase you want to translate.")
        print("Usage: python translate_ja_en_zh_es.py 'phrase'")
        print("The phrase should be enclosed in single or double quotations")
        input_phrase = ''
    
    # read database csv file
    # df_trans_db = pd.read_csv('phrase_translation_database.csv')
    # print(df_trans_db)

    # translation
    if input_phrase:
        translate(input_phrase)