#!usr/bin/python
"""This script checks whether an input character is katakana (k), hiragana (k)
or kanji (j).  The program prints a string of characters representing which alphabet the character at that location is in.  i.e. if the first character of the returned string is h, then the first character is hiragana, and so on."""

import sys
import unicodedata

def which_alph(str_):
    """Returns a string indicating which japanese alphabet each
    character of the received string is in.  
    """
    s = str_.decode('utf-8')
    
    a_str = ''
    for char in s:
        r = get_alph(char)
        a_str += r 
    return a_str
        
def get_alph(char):
    """Gets the alphabet for a specific character
    
    Arguments:
    - `char`: Character to check.
    """
    h_val = ord(char)
    
    if h_val >= 12352 and h_val <= 12447:
        return 'h'
    elif h_val >= 12448 and h_val <= 12543:
        return 'k'
    elif h_val >= 19968 and h_val <= 40895:
        return 'j'
    else:
        return 'x'


def main():
    """Called when this script is run.  Will not execute if this
    script is called by another.
    """
    args = sys.argv[1:]
    
    if not args:
        print 'No arguments received.'
        sys.exit(1)
    if len(args) == 1:
        which_alph(args[0])
    else:
        print 'Only takes one argument.'
        sys.exit(1)


if __name__ == '__main__':
    main()
