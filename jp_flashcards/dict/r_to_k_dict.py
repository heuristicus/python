#!/usr/bin/python

import sys
import pickle

kana_dict = {}
    

def add_to_dict():
    to_add = add_dialogue()
    for triple in to_add:
        key = triple[0]
        val = (triple[1], triple[2])
        kana_dict[key] = val
    print kana_dict

def add_dialogue():
    pairs = []
    
    while 1:
        key = raw_input('Enter the syllable in roman characters.\n')
        h = raw_input('Enter the syllable in hiragana.\n').decode('utf-8')
        k = raw_input('Enter the syllable in katakana.\n').decode('utf-8')
        cont = raw_input('Another? (y/n)\n')
        pairs.append((key, h, k))
        if cont == 'n':
            break
   
    return pairs

def update_dict():
    to_update = update_dialogue()
    print '%s %s'%('ss', kana_dict['ss'])
    kana_dict.update(to_update)
    print '%s %s'%('ss', kana_dict['ss'])
    print kana_dict

def update_dialogue():
    updates = {}
    while 1:
        key = raw_input('Enter the key to update.\n')
        print 'The current value of %s is (%s, %s).'%(key, kana_dict[key][0], kana_dict[key][1])

        h = raw_input('Enter updated hiragana, or leave blank to keep the current value.\n').decode('utf-8')
        if h == '':
            h = kana_dict[key][0]

        k = raw_input('Enter updated katakana, or leave blank to keep the current value.\n').decode('utf-8')
        if k == '':
            k = kana_dict[key][1]

        updates[key] = (h, k)
        print 'Key %s is now %s'%(key, updates[key])
        cont = raw_input('Another? (y/n)\n')
        if cont == 'n':
            break

    return updates

def display_dict():
    global kana_dict
    com = raw_input('Enter command.  \'all\' shows all keys in the dictionary and exits, \'keys\' allows you to browse keys.\n')
    
    if com == 'all':
        for key in sorted(kana_dict):
            print 'Key %s maps to %s and %s'%(key, kana_dict[key][0], kana_dict[key][1])
        sys.exit(1)
    elif com == 'keys':
        key_dialogue()
    else:
        print 'Sorry, I don\'t understand.  Please try again.'
        display_dict()

def key_dialogue():
    global kana_dict
    try:
        key = raw_input('Enter a key to view, or type \'exit\' to exit.\n')
        if key == 'exit':
            sys.exit(1)
        else:
            print 'Key %s maps to %s and %s'%(key, kana_dict[key][0], kana_dict[key][1])
            key_dialogue()
    except KeyError:
        print 'The key doesn\'t seem to exist.'
        key_dialogue()
    

def read_dict(filename):
    try: 
        dict_file = open(filename, 'rb')
        global kana_dict
        kana_dict = pickle.load(dict_file)
        dict_file.close()
    except IOError:
        c = raw_input('It seems the file %s does not exist.  Do you want to create it? (y/n)\n'%(filename))
        if c == 'y':
            f = open(filename, 'w')
            f.close()
        else:
            print 'Okay, exiting.'
            sys.exit(1)


def write_dict(filename):
    out_file = open(filename, 'wb')
    pickle.dump(kana_dict, out_file)
    out_file.close()
    print 'Wrote dictionary to %s'%(filename)

def main():
    args = sys.argv[1:]
    if not len(args) == 2:
        print 'Usage: [--update | --add | --display] dict_file'
        sys.exit(1)
    else:
        update = False
        add = False
        display = False
        if args[0] == '--update':
            update = True
            del args[0]
        elif args[0] == '--add':
            add = True
            del args[0]
        elif args[0] == '--display':
            display = True
            del args[0]
        dict_file = args[0]

    read_dict(dict_file)
    if add:
        add_to_dict()
    elif update:
        update_dict()
    elif display:
        display_dict()
    
    if not display:
       write_dict(dict_file)

    

if __name__ == '__main__':
    main()
