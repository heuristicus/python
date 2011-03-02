#!/bin/python

import sys
import pickle

DEFAULT_DICT_LOC = '../dict/kanadict.dict'
kana_dict = {}

def find_dict(filename = None):
    global kana_dict
    global DEFAULT_DICT_LOC
    
    if filename == None:
        try:
            dict_file = open(DEFAULT_DICT_LOC,'rb')
            kana_dict = pickle.load(dict_file)
            dict_file.close()
            if isinstance(kana_dict, dict):
                print 'Loaded a file at default dict location which seems to be a dictionary.' 
            else: 
                print 'Loaded something from the default location, but it doesn\'t seem to be a dictionary.  Not going to continue.'
                sys.exit(1)
        except IOError:
            c = raw_input('Couldn\'t locate dict file at default location %s.  Want to tell me where it is? (y/n)\n'%(DEFAULT_DICT_LOC))
            if c == 'n':
                print 'Ok, exiting.'
                sys.exit(1)
                if c == 'y':
                    f_loc = raw_input('Where\'s the dictionary?\n')
                    print 'Ok, attempting to open dictionary at %s...'%(f_loc)
                    find_dict(f_loc)
                else:
                    print 'Don\'t understand.  Exiting.'
                    sys.exit(1)
            else:
                try:
                    dict_file = open(filename, 'rb')
                    kana_dict = pickle.load(dict_file)
                    dict_file.close()
                    if isinstance(kana_dict, dict):
                        print 'Loaded a file at specified location which seems to be a dictionary.'
                    else: 
                        print 'Loaded something from the specified location, but it doesn\'t seem to be a dictionary.  Not going to continue.'
                        dict_file.close()
                        sys.exit(1)
                except IOError:
                    print 'The file doesn\'t seem to exist.  Exiting.'
                    sys.exit(1)

class dictAccessor:

    def get_hiragana(self, key):
        return kana_dict[key][0]
    
    def get_katakana(self, key):
        return kana_dict[key][1]
    
    def get_key(self, key):
        return kana_dict[key]
    
    def get_dict(self):
        return kana_dict

    def get_keys_len(self, length):
        comp_dic = {}
        for key in kana_dict:
            if len(key) == length:
                comp_dic[key] = kana_dict[key]
        
        return comp_dic
    
    def __init__(self):
        find_dict()
