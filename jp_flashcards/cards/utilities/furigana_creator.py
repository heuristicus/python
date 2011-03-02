#!/usr/bin/python
# -*- coding: utf-8 -*-
import alph_checker
import sys

HELP = 'This script reads two strings: a kanji definition, with spaces separating each par of text which contains a kanji (e.g この本は面白いでしょう would be input as この本は 面 白いでしょう), and a hiragana definition separated in the same way (このほは おも しろいでしょう), and attempts to give leading hiragana, kanji, furigana and okurigana in a list in that order, for each separate part.'


def get_list():
    """Gets a series of lists containing leading hiragana, furigana and okurigana
    from user input of two strings, one containing kanji, the other
    just hiragana. If kanji input is skipped, returns a list of two
    items: -1 followed by the hiragana string entered."""
    in_ = read_k_h()
    if in_[0] == -1:
        return in_
    else:
        out = []
        for i in range(len(in_[0])):
            out.append(make_comp(in_[0][i], in_[1][i]))
        return out

def read_k_h():
    """Reads a kanji and hiragana definition, and makes sure that they
    contain the same number of parts. Each part should start with a
    kanji, but this is not necessary. The string should be split such
    that each part only contains a single kanji, so that it is
    possible to determine the furigana."""
    jp_def = []
    k_skip = False
    kanji = raw_input('Enter the Japanese word, with kanji present. When the next character is a kanji, please enter a space and then continue. If you just want to enter hiragana, just press return.\n')
    if kanji == '':
        jp_def.append(-1)
        k_skip = True
    hiragana = raw_input('Please enter the hiragana equivalent of the last entry (if there was one), separated in the same way.\n')
    if hiragana == '':
        print 'You need to enter a hiragana definition.'
        read_k_h()
    # Replace japanese spaces with standard encoding spaces, and then
    # split the strings on spaces. This should give strings where the
    # first character is a kanji
    s_kanji = kanji.replace("\xe3\x80\x80", " ").split(" ")
    s_hiragana = hiragana.replace("\xe3\x80\x80", " ").split(" ") 
    # Performs some basic validation on the entered strings, if the
    # kanji definition has not been skipped. Otherwise, it appends the
    # hiragana definition to the return list and returns it.
    if not k_skip:
        if len(s_kanji) != len(s_hiragana):
            print 'The number of parts of the kanji and hiragana definitions differ. Try again.'
            return read_k_h()
        # Probably useless now, since have catch for this above.
        if len(s_hiragana) == 0:
            print 'You need to enter a hiragana definition.'
            return read_k_h()
    else:
        jp_def.append(hiragana)
        return jp_def
    
    jp_def.append(s_kanji)
    jp_def.append(s_hiragana)
    return jp_def 

def make_comp(kanji, hiragana):
    """Takes a kanji definition, with spaces before each kanji, and a
    hiragana definition separated in the same way, and attempts to
    give leading hiragana, kanji, furigana and okurigana in a list in that order.

    !!! THERE IS A QUIRK: IF YOU ENTER TWO HIRAGANA STRINGS, YOU STILL
        GET A LIST OF 4, BUT THE LAST 3 WILL BE EMPTY !!!"""
    # List where each index contains a character of the kanji string.
    k_char = j_list(kanji)
    # List where each index contains a character of the hiragana string.
    h_char = j_list(hiragana)
    # Lists where each index contains a reference to what type of
    # character it is. h is hiragana, k is katakana, j is kanji, and x
    # means a non-japanese character.
    k_str = list(alph_checker.which_alph(kanji))
    h_str = list(alph_checker.which_alph(hiragana))
    # Used to store the number of leading hiragana characters.
    num_lead_h = 0
    
    for i in range(len(h_str)):
        if k_str[i] == 'j':
            break
        if h_str[i] == k_str [i]:
            num_lead_h += 1

    lead_h = ""
    if num_lead_h != 0:
        lead_h = "".join(h_char[:num_lead_h])
        # Delete the leading hiragana from the lists
        del(k_char[:num_lead_h])
        del(h_char[:num_lead_h])
        del(k_str[:num_lead_h])
        del(h_str[:num_lead_h])
    
    # Goes through the list backwards and finds the number of
    # okurigana after the kanji
    num_okurigana = 0
    for i in range(len(h_str)):
        i += 1
        if k_str[-i] == 'j':
            break
        if h_str[-i] == k_str [-i]:
            num_okurigana += 1

    okurigana = ""
    if num_okurigana != 0:
        okurigana = "".join(h_char[-num_okurigana:])
        del(k_char[-num_okurigana:])
        del(h_char[-num_okurigana:])
        del(k_str[-num_okurigana:])
        del(h_str[-num_okurigana:])
    
    kanji = "".join(k_char)
    furigana = "".join(h_char)
    group = [lead_h, kanji, furigana, okurigana]
    return group


def j_list(jap_str):
    """Takes a string of japanese characters and puts them into a list
    so that the individual characters are in one list index, rather
    than each hex code, since the default list split splits to hex
    codes, and each character is made up of 3 codes."""
    # makes a list of chars from the japanese string. Each japanese
    # character is made up of three hex codes, so the list length is
    # three times the number of characters in the string
    std_list = list(jap_str)
    # list to store output
    o_list = []  
    # store for the last place we took a hex code from (end of one
    # character)
    lastind = 0 
    # Go through a range which is the number of characters in the string
    for ind in range(len(std_list)/3):
        # Add 1 to the index so we can multiply to get the end of one char
        ind += 1
        # append three hex codes joined into a string by taking groups
        # of three characters from the standard list
        o_list.append("".join(std_list[lastind:ind*3]))
        # Multiply the last index by three so that we start from the
        # first hex code from the next character
        lastind = ind*3
    return o_list

if __name__ == '__main__':
    print 'Not intended to run like this.'
