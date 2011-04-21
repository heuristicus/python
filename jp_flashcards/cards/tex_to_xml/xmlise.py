#!/usr/bin/python
"""This script is to be used in conjunction with extract_tex.py.  It
takes the output from that script and constructs an xml file from it.
"""

from lxml import etree
import utilities.alph_checker as alph_checker
import re

out_file = ''

def xmlise(extracted_cards, output_file):
    global out_file
    out_file = output_file
    
    xml_cards = []
    # makes an xml snippet out of each card and appends to a list
    for card in extracted_cards:
        xml_cards.append(do_xml(card))
    
    # Creates a root node for the whole set of cards.
    root = etree.Element('cardset')
    # Appends each card_root to the main root.
    for card in xml_cards:
        root.append(card)
    append_to_file(etree.tostring(root, pretty_print=True))
    #print etree.tostring(root, pretty_print=True)

def do_xml(card):
    """Puts a card into an xml format.
    
    Arguments:
    - `card`: Card to put into an xml format
    """
    # Creates a root element
    card_root = etree.Element('card')
    # Adds a kanji sub element
    kanji = etree.SubElement(card_root, 'kanji')
    # decodes the kanji from the card into unicode and sets it as the
    # text for the kanji node
    kanji.text = card[0].decode('utf-8')
    # Adds a node for the meanings
    meanings = etree.SubElement(card_root, 'meanings')
    # loops through the meanings in the card definition, makes child
    # nodes for each, and sets the text as that meaning.
    for meaning in card[1]:
        m = etree.SubElement(meanings, 'meaning')
        m.text = meaning
    # Adds a node for readings
    readings = etree.SubElement(card_root, 'readings')
    # loops through readings in the card definition, makes child nodes
    # for each and sets the text for the node as the reading.
    for reading in card[2]:
        # Uses another script method to find which alphabet the
        # reading is in, and strips out characters indicating
        # non-japanese text.
        alph_res = alph_checker.which_alph(reading).replace('x', '')
        # If the text is hiragana, create a kun reading node and
        # append the reading there. (Hiragana strings from
        # alph_checker contain at least one 'h'.
        if re.search('h+', alph_res):
            kun = etree.SubElement(readings, 'kun')
            kun.text = reading.decode('utf-8')
        # If the text is katakana, create an on reading node and
        # append the text to there.  (katakana string from
        # alph_checker contain at least one 'k'.
        elif re.search('k+', alph_res):
            on = etree.SubElement(readings, 'on')
            on.text = reading.decode('utf-8')
    # Creates a node for storing compounds
    compounds = etree.SubElement(card_root, 'compounds')
    # Loops through each compound in the card definition
    for compound in card[3]:
        # Creates a subtree for that compound
        comp = etree.SubElement(compounds, 'compound')
        tuples = compound[0]
        # Loops through the tuples of kanji, furigana and okurigana
        # that the compound contains
        for tuple_ in tuples:
            # Creates a node to store the individual kanji
            # details. The separation protocol in this program is that
            # the definition is separated by kanji present in the
            # string of japanese text. If a kanji has okurigana
            # following it, then this is grouped with the preceding
            # kanji. When the next kanji is encountered, this is
            # considered a new part of the japanese definition.
            jp_part = etree.SubElement(comp, 'jp_part')
            # Creates a node for the kanji
            c_kanji = etree.SubElement(jp_part, 'c_kanji')
            # Sets kanji text to the first part of the tuple
            c_kanji.text = tuple_[0].decode('utf-8')
            # Creates a node for the furigana
            furigana = etree.SubElement(jp_part, 'furigana')
            # Sets furigana text to the second part of the tuple
            furigana.text = tuple_[1].decode('utf-8')
            if tuple_[2]:
                # Creates a node for okurigana, if there is any in the
                # definition
                okurigana = etree.SubElement(jp_part, 'okurigana')
                # Sets okurigana text to the third part of the tuple 
                okurigana.text = tuple_[2].decode('utf-8')
        # Node for the english definition
        english = etree.SubElement(comp, 'english')
        english.text = compound[1]
            
            
    return card_root


def append_to_file(data):
    """Appends data to the output file.
    
    Arguments:
    - `data`: Data to write to file.
    """
    global out_file
    f = open(out_file, 'a')
    f.write(data)
    f.close()
    print 'Successfully wrote (appended) data to %s'%(out_file)



def main():
    print 'Not intended to be run like this (yet).'

if __name__ == '__main__':
    main()
