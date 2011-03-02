#!/bin/python
# coding=<utf-8>

import sys
import re
sys.path.append('../dict/') # adds the dict directory to the places where python searches for modules
import dict_access
from dict_access import dictAccessor


VALID_TSU_STRINGS = ['tt', 'kk','cc','pp', 'ss']
dic = dictAccessor()
alph = 0 # part of the dictionary tuple to get.  0 = hiragana, 1 = katakana


def convert(arg_list):
    global dic
    #for key in sorted(dic.get_dict(), key=lambda l: len(l)):
        #print '%s %s'%(key, dic.get_key(key))
        
    return convert_string(' '.join(arg_list))

def to_katakana(string):
    global alph
    alph = 1
    return convert_string(string)

def to_hiragana(string):
    global alph
    alph = 0
    return convert_string(string)

def convert_string(arg_string):
    conv_str = insert_small_tsu(arg_string) # adds small tsu
    
    for i in sorted(range(1,4), reverse=True): # replaces strings of length 3, then 2, then 1
        conv_str = rep_str_len(conv_str, i)
        
    return conv_str

def insert_small_tsu(string):
    """Finds repeated letters in the input string and converts to small tsu, if valid.
    """
    global dic
    global VALID_TSU_STRINGS
    global alph
    ed_str = string
    for key in VALID_TSU_STRINGS:
        rep = dic.get_key(key)[alph] # gets a hiragana or katakana char to replace the var with
        ed_str = ed_str.replace(key, rep) # replaces the var if it exists in the string with the value of the key in the dict.
               
    return ed_str

def rep_str_len(string, rep_len):
    """Replaces strings of length rep_len with the values of keys in the dictionary
    that match rep_len.
    """
    global dic
    global alph
    ed_str = string
    for key in dic.get_keys_len(rep_len): # loops through keys of rep_len in the dictionary
        rep = dic.get_key(key)[alph] # gets a hiragana or katakana char to replace the var with
        ed_str = ed_str.replace(key, rep) # replaces each roman string that matches a key, if it exists, with the katakana or hiragana character of that key

    return ed_str  

def main():
    global alph

    args = sys.argv[1:]
    if len(args) == 0:
        print 'No arguments entered.'
        sys.exit(1)
    if args[0] == '-k':
        alph = 1
        del args[0]
    
    string = args[:]

    print convert(string)


if __name__ == '__main__':
    main()
