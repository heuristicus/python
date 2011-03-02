#!/bin/usr/python

import sys
import lxml
from lxml.etree import ElementTree, Element, SubElement, parse, tostring

def check_file_for_xml(filename):
    """Checks whether a file contains xml or not, and returns a
    boolean value to say whether this is the case or not.
    
    Arguments:
    - `filename`: Name of file to check.
    """
    # See if the file exists.
    try:
        open(filename)
    except IOError:
        # create file if it doesn't exist.
        print 'File %s does not exist, creating...' %(filename),
        open(filename, 'w')
        print 'Done'
        return False
    # Try and parse the file and see if we get an error, basic xml
    # content check.
    try:
        tree = parse(filename)
    # Error when the parse method does not find xml, or finds malformed XML.
    except lxml.etree.XMLSyntaxError:
        print 'File is not XML.'
        return False
    # Return true, because no error was thrown
    print 'File is XML.'
    return True

def get_tree(filename):
    tree = parse(filename)
    return tree

def make_root(root_name):
    root = Element(root_name)
    return root
    
def add_to_root(root, subelement):
    try:
        root.append(subelement)
    except AssertionError:
        print 'The subelement %s was invalid.' %(subelement)

def save_file(root, filename):
#    tree = ElementTree()
#    tree._setroot(root)
#    tree.write(filename, pretty_print=True)
    f = open(filename, 'w')
    s = tostring(root, pretty_print=True)
    print s
    f.write(s)
    print 'XML tree saved to %s.' %(filename)

# testing method for some possible operations
#def do_operations(filename, root_name):
#    is_xml = check_file_for_xml(filename)
#    if is_xml:
#        tree = get_tree(filename)
#        root = tree.getroot()
#        te = Element('woah')
#        te.text = 'yes'
#        add_to_root(root, te)
#        save_file(root, filename)
#    else:
#        root = make_root(root_name)
#        te = Element('woah')
#        te.text = 'yes'
#        add_to_root(root, te)
#        save_file(root, filename)

class xmlHandler():
    """Intended as a way of accessing methods in this class with some
    variables which don't change. It will also get details of the xml
    contents of a file, and if it doesn't contain xml, it will create
    a root for it to use. It should also create the file if it doesn't
    exist.
    """
    
    def __init__(self, filename, root_name='default_root'):
        """Initialises this class with the filename that you want to
        write xml to or read from.
        
        Arguments: - `filename`: The filename of the file that you
        have stored xml in or the file in which you would like to
        store the xml once it is created.  

        - `root_name`: The name of the root to be created, should the
        file not have xml inside it.
        """
        self._filename = filename
        self.rname = root_name
        self.get_file_data(self._filename)
        
    def get_file_data(self, filename):
        """Initialises the object with the tree, and tree's root which
        are contained in the file which is assumed to be xml. If it is
        not, the tree root will be created and returned.
        
        Arguments:
        - `self`: 
        - `filename`: Filename to get details from.
        """
        # See if the file contains xml
        isXML = check_file_for_xml(filename)
        if isXML:
            # get data out of the file, if it contains xml, so we can
            # use it later
            self.tree = get_tree(filename)
            self.root = self.tree.getroot()
        else:
            # No root in the file, so create one. Set the tree to the
            # none type so that we can use the fact that it's empty
            # later if necessary
            self.root = make_root(self.rname)
            self.tree = None

    def save_file(self):
        """Saves the data in this object to the file contained within
        it. The add_element method uses this method each time it is
        called, to ensure that definitions added are not lost
        """
        save_file(self.root, self._filename)

    def add_element(self, element):
        """Adds an element to the root of the file.

        Arguments: 
        - `element`: The element to add to the root
        object. This can have any depth you like.
        """
        add_to_root(self.root, element)
        save_file(self.root, self._filename)
    
            
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print 'You need to have a filename to check.'
        sys.exit(0)
    _file = args[0]
    test = xmlHandler(_file)

if __name__ == '__main__':
    main()
    
