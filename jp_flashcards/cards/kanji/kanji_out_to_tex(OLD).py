#!/usr/bin/python

import sys
import re
import os
import shutil

"""This script extracts data from a flashcard definition in the following form:

kanji (single character)|hiragana reading(up to 4)|kanji1,kanji2!kanji1hiragana,kanji2hiragana!english meaning!(max 3)"""

def parse_file(filename):
    """Parses a file containing a series of flashcard definitions in a specific format"""
    f = open(filename, 'rU')
    s = f.read()
    s = s.split('\n')
    latex_data = ''
    for string in s:
        #print '\nParsing %s'%(string) 
        latex_data += parse_string(string)
    return latex_data

def write_to_file(filename, data):
    f = open(filename, 'w')
    f.write(data)
    f.close()
    print 'Wrote data to %s'%(filename)

def append_to_file(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
    print 'Appended data to %s'%(filename)

def parse_string(string):
    """Parses a string containing data for a single flashcard into its various components"""
    print string
    block = string.split('|')
    kanji = block[0]
    meanings = block[1]
    readings = block[2]
    flashcard = []
    flashcard.append(kanji)
    flashcard.append(meanings.split(','))
    flashcard.append(readings.split(','))
    flashcard.append(get_defs(block[3]))
    return to_tex(flashcard)

def to_tex(flashcard):
    """Puts a flashcard into a specific tex layout"""
    kanji = flashcard[0]
    meaning = flashcard[1]
    hiragana = flashcard[2]
    definitions = flashcard[3]
    tex_string = '\\begin{flashcard}{%s}'%(flashcard[0])
    tex_string += '\n\\begin{tabular}{cc}\n\\begin{minipage}[b]{0.5\linewidth}\centering\n\\begin{tabular}{c}\n'
    

    ms = '' # meanings string
    fm = meaning[:-1] # all but the last meaning
    bm = meaning[-1:] # last meaning
    lastm = '\\textbf{%s}\n'%(bm[0])
    for meaning in fm:
        ms += '\\textbf{%s}\\\\\n'%(meaning)
    tex_string +=  ms + lastm
    tex_string += '\\end{tabular}\n\\end{minipage}\n\\hspace{-1cm}\n&\\begin{minipage}[b]{0.5\\linewidth}\\centering\n\\fontsize{18pt}\n\\selectfont\n\\begin{tabular}{c}\n'
    

    hs = '' # hiragana string
    fh = hiragana[:-1] # all but the last hiragana
    lh = hiragana[-1:] # last hiragana
    lasth = '%s\n'%(lh[0])
    for hiragana in fh:
        hs += '%s\\\\\n'%(hiragana)
    tex_string += hs + lasth
    tex_string += '\\end{tabular}\n\\end{minipage}\n\\vspace*{0.1cm}\n\\end{tabular}\n\\fontsize{12pt} \\selectfont\n\\begin{tabular}{l}\n'
    
    # add definitions to tex string
    for i in range(len(definitions)):
        if i == len(definitions) - 1:
            tex_string += '%s\n'%(definitions[i])
        else:
            tex_string += '%s\\\\\n'%(definitions[i])
    
    tex_string += '\\end{tabular}\n\\end{flashcard}\n\n'
    return tex_string
    
def get_defs(def_block):
    """Splits a block of definitions into three separate definitions"""
    defs = def_block.split('!')
    n_defs = len(defs)/3
    split_defs = []
    for i in range(n_defs):
        split_defs.append(to_tex_def(defs[:3]))
        del defs[:3]
    return split_defs
    
def to_tex_def(definition):
    kanji = definition[0].split(',')
    hiragana = definition[1].split(',')
    romaji = definition[2]
    #print kanji, hiragana, romaji
    if len(kanji) == len(hiragana):
        defstring = ''
        for part in range(len(kanji)):
            kstring = kanji[part]
            hstring = hiragana[part]
            if len(kstring)>3: # the kanji is not by itself in the string
                #print kstring, len(kstring), hstring, len(hstring)
                diff = len(hstring) - len(kstring) + 3
                #print diff
                knji = kstring[:3]
                if diff is 0:
                    furigana = hstring[:3]
                    nokori = hstring[-3:]
                else:
                    furigana = hstring[:diff]
                    nokori = hstring[diff:] # left over characters after kanji
                    #print knji, furigana, nokori
                defstring = defstring + r'\ruby{%s}{%s}%s'%(knji, furigana, nokori)
                #print defstring
            else: 
                defstring = defstring + r'\ruby{%s}{%s}'%(kstring, hstring)
        print defstring
    else:        
        print 'A length error is present in definition %s.  Exiting.'%(''.join(definition)) 
        sys.exit(1)

    return r'\df{%s}{%s}'%(defstring, romaji)

def main():
    args = sys.argv[1:]
    if not args:
        print "usage: [--write] source_file [destination_file]"
        sys.exit(1)
    
    if args[0] == '--write':
        write = True
        del args[0]
    else:
        write = False
    source_file = args[0]
    dest_file = args[1]
    del args[0:2]
    
    # Runs the program.
    parsed_data = parse_file(source_file)
    if write:
        write_to_file(dest_file, parsed_data)
    else:
        append_to_file(dest_file, parsed_data)


if __name__ == '__main__':
    main()
