#!/bin/usr/python

import utilities.roman_converter as r_conv
import utilities.furigana_creator as furi_cre
import kanji_xml as k_xml
import sys
import codecs

from datetime import datetime

def read_data():
    """Reads a set of data required to make up the definition of a kanji"""
    kanji = raw_input('Enter kanji.\n') # Kanji for the flashcard
    meanings = raw_input('Enter meanings separated by spaces.  If a definition has spaces, use underscores (_) instead.\n') # Meanings of the kanji in english
    #readings = raw_input('Enter readings of the kanji in hiragana or katakana, separated by spaces.  Inserting a backslash between two similar readings will separate them.\n') # Readings of kanji in hiragana for kun and katakana for on
    print 'If a reading has kanji that lead into it, use a \"-\".  For furigana separation, use \'--\'.  For kanji which have kanji that follow, use \'---\'.'
    kun = raw_input('Enter kun reading of the kanji in the hepburn romanisation, separated by spaces.  Leave blank if there is none.\n') # kun readings of kanji
    on = raw_input('Enter on reading of the kanji in hepburn romanisation, separated by spaces.  Leave blank if there is none.\n') # on reading of the kanji
    kun = r_conv.to_hiragana(kun) # converts hepburn to hiragana
    on = r_conv.to_katakana(on) # converts hepburn to katakana
    if len(kun) == 0:
        readings = on
    elif len(on) == 0:
        readings = kun
    elif len(on) == 0 and len(kun) == 0:
        print 'You\'ve not entered a reading.  Have another go.'
        return read_data()
    else:
        readings = kun + ' ' + on
    # This is the part that does the most work.
    k_comp = furi_cre.get_list()
    definitions = []
    definitions.extend([kanji, meanings, readings, k_comp])
    print 'Definition added: \n%s'%(definitions)
    return definitions

def cont_dialogue():
    next = raw_input('Another? (y/n)')
    if next == 'y' or next == 'yes' or next == '':
        return True
    elif next == 'n' or next == 'no':
        return False
    else:
        print 'Enter y, yes, n or no'
        return cont_dialogue()

def main():
    args = sys.argv[1:]
    if len(args) is 1:
        out_file = args[0]
    elif len(args) is 0:
        # creates a filename to use to output data to if a filename is not provided.
        now = datetime.now()
        now = now.strftime('%Y-%m-%d_%H:%M:%S')
        out_file = 'kanji_definitions_%s.xml'%(now)
    else:
        print 'Usage: [filename]'
        sys.exit(1)
       
    while 1:
        k_list = read_data() # read data from command line and return a string
        # Converts the list into an xml snippet and writes it to a file
        k_xml.write_xml(k_list, out_file)
        cont = cont_dialogue() # ask whether to repeat for a different kanji
        if cont is False: break
    print 'Wrote data to %s'%(out_file)
            
if __name__ == '__main__':
    main()
