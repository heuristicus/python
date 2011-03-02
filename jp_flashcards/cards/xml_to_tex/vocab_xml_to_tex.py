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
    cards = xml_tree.findall('def')
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
    skele = tex_skele
    for tag in tags.keys():
        skele = skele.replace(tag, tags[tag])
    return skele

def get_tags(card):
    """Gets the tags required for filling in the tex definition. The
    tags are returned in a dictionary with the names <voc_details>  <vocab> and <english>. Each tag may or may not have
    some processing done to get it into the state that it is put into
    the dictionary in. The contents of these tags are then used by the write method to
    replace tags inside the tex skeleton.
    
    Arguments:
    - `card`: The card from which to retrieve tags. Should be an Element.
    """
    # Dictionary which will store tag data.
    tags = {}

    # No processing on the english definition, so just put it into the
    # dictionary as is.
    tags['<english>'] = card.find('english').text
    
    # The tag 'japanese' contains all the stuff that is needed for the
    # Japanese details
    japanese = card.find('japanese')
    
    vrb_grp = process_verb(japanese.find('group'))
    adj_type = process_adj(japanese.find('adj_type'))
    
    if vrb_grp:
        tags['<voc_details>'] = vrb_grp
    elif adj_type:
        tags['<voc_details>'] = adj_type
    else:
        tags['<voc_details>'] = ''

    # Get all the parts of the japanese text so that we can process
    # the data inside them
    str_parts = japanese.findall('str_part')
    # check if the list is empty, or whether we need to process the
    # stuff inside.
    if str_parts == []:
        # this card contains no kanji, so just put the hiragana in
        tags['<vocab>'] = japanese.find('hiragana').text
    else:
        # Need to process the data inside the string parts so that we
        # get some coherent text out.
        tags['<vocab>'] = process_vocab(str_parts)
    
    return tags
    
def process_vocab(string_parts):
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

def process_verb(verb):
    """Converts the numbers in a verb group to roman numerals so that
    it looks nice on cards.
    
    Arguments: 
    - `verb`: An element that contains a verb group, which
    should be a number between 1 and 3.
    """
    # If the object you get doesn't exist, just return nothing
    if verb == None:
        return None
    else:
        # Convert the integer inside the element (which exists) into
        # an actual int so we can play with it.
        num = int(verb.text)
        rom_grp = ''
        for val in range(num):
            rom_grp += 'I'
        return rom_grp
    
def process_adj(adj):
    """Tacks on some horizontal spacing tex code in front of the
    adjective definition so it looks nice.
    
    Arguments:
    - `adj`: Adjective to add to.
    """
    # If the object you get doesn't exist, just return nothing
    if adj == None:
        return None
    else:
        adj_ = adj.text
        return '\hspace{3.1in} ' + adj_

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
