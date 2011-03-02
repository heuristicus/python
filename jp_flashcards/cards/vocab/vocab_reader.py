#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from lxml.etree import SubElement, Element
import utilities.furigana_creator as furi_cre
from utilities.xml_file_handler import xmlHandler
import traceback

HELP = 'This program allows you to enter vocabulary for entry onto flashcards. You will be asked to enter an english definition, a kanji compound, and the hiragana equivalent.\n\n The Japanese definitions should be split in a specific way. For example, if you wish to enter a definition for "I work at a company", then the Japanese equivalent with kanji is "私は会社で働いている". The hiragana for this is "わたしはかいしゃではたらいている". For ease of processing, definitions should be entered with spaces before each kanji. So, the above would become "私は 会 社で 働いている", with the hiragana version having spaces in the same place: "わたしは かい しゃで はたらいている". Basically, each part separated by spaces should only contain a single kanji.'
XML_HAND = ''


def read_vocab():
    """Loops forever and appends data to the xml root until the user
    exits the program."""
    global XML_ROOT
    while 1:
        try:
            eng_def = read_eng()
            jp_def = furi_cre.get_list()
            group = read_group()
            adj = read_adj()
            xml_def = def_to_xml(eng_def,jp_def,group)
            XML_HAND.add_element(xml_def)
            print 'Definition received.'
        except KeyboardInterrupt:
            XML_HAND.save_file()
            sys.exit(1)
        except Exception:
            print 'Something went wrong. Saving file and exiting.'
            exc_type, exc_value, exc_traceback = sys.exc_info()
            XML_HAND.save_file()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            sys.exit(1)
    
def read_eng():
    eng = raw_input('Enter the english definition of the word or compound. To exit the program, enter exit.\n')
    if eng == 'exit':
        global XML_ROOT
        XML_HAND.save_file()
        print 'Ok, exiting.'
        sys.exit(1)
    else:
        return eng

def read_group():
    grp = raw_input('Enter the verb group if this is a verb, otherwise press return.')
    if grp == 'exit':
        XML_HAND.save_file()
        print 'Ok, exiting.'
        sys.exit(1)
    else:
        return grp

def read_adj():
    """Reads an adjective from the commandline. Should be of a
    specific type - no, na or i. Will reject otherwise. Writing in in
    english or japanese is possible - result will be converted to
    japanese if it is english.
    """
    adj = raw_input('Enter the adjective type (の, な or い). Can be entered in english (no, na, i). These will be converted. If this isn\'t an adjective, just press return.\n')
    if adj == 'exit':
        XML_HAND.save_file()
        print 'Ok, exiting.'
        sys.exit(1)
    else:
        # Check if the adjective type is valid.
        if is_adj(adj):
            return convert_adj(adj)
        else:
            print '%s isn\'t an adjective type...try again.' %(adj)
            return read_adj()

def convert_adj(adj):
    """Converts an adjective ending written in English to one written in Japanese. Will not do anything to Japanese text.
    
    Arguments:
    - `adj`: Adjective to convert (if necessary)
    """
    if adj == 'i':
        return '\xe3\x81\x84'
    elif adj == 'na':
        return '\xe3\x81\xaa'
    elif adj == 'no':
        return '\xe3\x81\xae'
    else:
        return adj


def is_adj(adj):
    """Checks that an adjective entry is correct. Valid inputs are:
    no, na, i, の, な, い.
    
    Arguments:
    - `adj`: Adjective to check
    """
    valid = ['\xe3\x81\xae', '\xe3\x81\xaa', '\xe3\x81\x84', 'no', 'na', 'i']
    for val in valid:
        if adj == val:
            return True
    return False

def def_to_xml(eng, jp, grp, adj):
    # Root element for the definition
    def_root = Element('def')
    # Add english sub element
    english = SubElement(def_root, 'english')
    # Set the test in the sub element to be the english definition
    english.text = eng
    # Sub element to add the japanese definition to
    japanese = SubElement(def_root, 'japanese')
    # The japanese definition is made up of parts, which contain one kanji each.

    if jp[0] == -1:
            hiragana = SubElement(japanese, 'hiragana')
            hiragana.text = jp[1].decode('utf-8')
            if grp != '':                
                group = SubElement(japanese, 'group')
                group.text = grp
            if adj != '':
                adj = SubElement(japanese, 'adj_type')
                adj.text = adj
            return def_root
    else:
        for part in jp:
            str_part = SubElement(japanese, 'str_part')
            
            # Each part contains leading hiragana, a kanji, the furigana
            # of the kanji, and the trailing hiragana (4 bits, some of
            # which may be empty strings, if they do not exist.)
            if part[0] != '':
                lead_h = SubElement(str_part, 'hiragana')
                lead_h.text = part[0].decode('utf-8')
            if part[1] != '':
                kanji = SubElement(str_part, 'kanji')
                kanji.text = part[1].decode('utf-8')
            if part[2] != '':
                furi = SubElement(str_part, 'furigana')
                furi.text = part[2].decode('utf-8')
            if part[3] != '':
                okuri = SubElement(str_part, 'okurigana')
                okuri.text = part[3].decode('utf-8')
            if grp != '':
                group = SubElement(japanese, 'group')
                group.text = grp
            if adj != '':
                adj = SubElement(japanese, 'adj_type')
                adj.text = adj
        return def_root
    #print etree.tostring(def_root, pretty_print=True)
    
def main():
    global HELP
    global XML_HAND
    args = sys.argv[1:]
    if len(args) == 0:
        print 'You must enter a file to output to.'
        sys.exit(1)
    elif len(args) > 1:
        print 'Only one argument - file to output to.'
        sys.exit(1)
    else:
        filename = args[0]
    
    print HELP

    XML_HAND = xmlHandler(filename, 'deflist')
    read_vocab()

if __name__ == '__main__':
    main()
