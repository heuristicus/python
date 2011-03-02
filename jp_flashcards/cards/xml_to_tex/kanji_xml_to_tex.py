#!/bin/usr/python

import sys


#!/usr/bin/python
from lxml.etree import parse
import lxml
import sys

def convert_xml(xml_file, tex_skeleton, out_file):
    """Converts an xml file containing vocabulary definitions created
    by vocab_reader.py to a tex file to create flashcards. Uses a txt
    file containing some tex code, with some placeholder values that
    are used to insert the data into the tex code.
    
    Arguments:
    - `xml_file`: The xml file to read from
    - `out_file`: The file to write tex data to.
    """
    try:
        xml_tree = parse(xml_file)
    except IOError:
        print 'The xml file specified doesn\'t exist.'
        sys.exit(1)
    except lxml.etree.XMLSyntaxError:
        print 'The xml file you chose isn\'t xml.'
        sys.exit(1)
    
    # Get a tex skeleton from file. This skeleton should contain the
    # tags <voc_details> <str_part> and <english>. These tags
    # will later be replaced with the data from the xml.
    tex_skeleton = open(tex_skeleton, 'r').read()
    
    # Get all the vocab definitions from the xml file. These contain
    # data required to put into each tex card.
    cards = xml_tree.findall('card')
    for card in cards:
        tags = get_tags(card)
        filled_skele = fill_tex_skeleton(tags, tex_skeleton)
        # append the filled definition to the file
        append_to_file(out_file, filled_skele.encode('utf-8'))        

def fill_tex_skeleton(tags, tex_skele):
    """Takes a dictionary of tags, and replaces strings which match
    those tags in a tex skeleton that has been read in, returning a
    copy of the modified skeleton.
    
    Arguments: 
    - `tags`: A dictionary of tags. Should contain keys
    which are the same as tags in the tex skeleton.

    - `tex_skele`: A tex skeleton containing tags (<[some text]>) to replace.
    """
    base_skele = tex_skele
    print tags
    for tag in tags.keys():
        skele = base_skele.replace(tag, tags[tag])
        if skele == base_skele:
            print 'The tex skeleton seems to be missing a tag. Not going to continue.'
            sys.exit(1)
    return skele

def get_tags(card):
    """Gets the tags required for filling in the tex definition. The
    tags are returned in a dictionary with the names <kanji>, <meanings>, <readings> and <definitions>. Each tag may or may not have
    some processing done to get it into the state that it is put into
    the dictionary in. The contents of these tags are then used by the write method to
    replace tags inside the tex skeleton.
    
    Arguments:
    - `card`: The card from which to retrieve tags. Should be an Element.
    """
    # Dictionary which will store tag data.
    tags = {}

    # No processing on the kanji, so just put it into the
    # dictionary as is.
    tags['<kanji>'] = card.find('kanji').text
    
    tags['<meanings>'] = process_meanings(card.find('meanings'))

    tags['<readings>'] = process_readings(card.find('readings'))

    tags['<definitions>'] = process_definitions(card.find(compounds))
    
    return tags
    
def process_meanings(meanings):
    """Processes the meanings of a kanji. These are contained inside
    the <meaning> tag, of which there can be many.
    
    Arguments:
    - `meanings`: An element containing the meanings of a kanji.
    """
    mean_set = meanings.findall('meaning')
    m_string = ''
    for meaning in mean_set:
        m_string += '\\textbf{%s}\n' %(meaning.text)
    # remove the newline character from the end of the last part of
    # the string. Can't be bothered to do this inside the loop.
    m_string = m_string[:-1]
    return m_string
    

def process_readings(readings):
    """Processes an element containing the meanings of a kanji. These
    contain the on and kun readings in the <on> and <kun> tags.
    
    Arguments:
    - `readings`:
    """
    el_list = []
    el_list.extend(readings.findall('kun'))
    el_list.extend(readings.findall('on'))
    
    read_string = ''
    for element in el_list:
        read_string += '%s\\\\\n' %(element.text)
    # Remove the two backslashes and newline from the end of the string.
    read_string = read_string[:-3]
    return read_string


def process_definitons(string_parts):
    """Processes a vocab definition consisting of various parts:
    preceding hiragana, the kanji, furigana for it, and lastly
    okurigana, and returns this as a string with tex commands in it to
    create the relevant furigana.
    
    Arguments:
    - `string_parts`: List of elements which contain parts of the japanese text.
    """
    comp_string = ''
    for part in string_parts:
        hiragana = part.find('hiragana')
        kanji = part.find('kanji')
        furigana = part.find('furigana')
        okurigana = part.find('okurigana')
        # Shitty way of doing this, but whatever. If the thing is
        # nonetype it sets it to an empty string, otherwise set to the
        # text inside.
        if hiragana == None:
            hiragana = ''
        else:
            hiragana = hiragana.text
        if kanji == None:
            kanji = ''
        else:
            kanji= kanji.text
        if okurigana == None:
            okurigana = ''
        else:
            okurigana = okurigana.text
        if furigana == None:
            furigana = ''
        else:
            furigana = furigana.text
        comp_string += '%s\\ruby{%s}{%s}%s'%(hiragana, kanji, furigana, okurigana)
    return comp_string
    
def append_to_file(filename, data):
    """Appends data to a file.
    """
    f = open(filename, 'a')
    f.write(data)

    
def main():
    """
    """
    args = sys.argv[1:]
    if len(args) != 3:
        print 'Usage <xml file><tex_skele_file><output file>'
    else:
        xml = args[0]
        skele = args[1]
        output = args[2]
        convert_xml(xml, skele, output)

if __name__ == '__main__':
    main()
