#!/usr/bin/python

import sys
import pickle

def read_def_file(filename):
    f = open(filename, 'rU')
    s = f.read()
    sp = s.split('\n')
    del sp[-1]
    return sp

def read_dict(filename):
    dic = open(filename, 'rb')
    kana_dic = pickle.load(dic)
    dic.close()
    return kana_dic

def save_dict(filename, dic):
    out_file = open(filename, 'wb')
    pickle.dump(dic, out_file)
    out_file.close()
    print 'Wrote updated dictionary to %s'%(filename)

def mk_dict(roman, hiragana, katakana):
    dic = {}
    for i in range(len(roman)):
        dic[roman[i]] = (hiragana[i], katakana[i])
        
    return dic

def main():
    args = sys.argv[1:]
    if not len(args) == 4:
        print 'Usage: dict_file roman_file hiragana_file katakana_file'
        sys.exit(1)
    
    dict_file = args[0]
    r = args[1]
    h = args[2]
    k = args[3]
    del args[:4]

    ro = read_def_file(r)
    hi = read_def_file(h)
    ka = read_def_file(k)

    dic = read_dict(dict_file)
    updated_dic = mk_dict(ro, hi, ka)
    dic.update(updated_dic)
    save_dict(dict_file, dic)

if __name__ == '__main__':
    main()
