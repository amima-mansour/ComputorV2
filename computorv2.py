# coding: utf-8

import sys
import parse

if __name__ == "__main__":
    var = {}
    chaine = input()
    while (chaine != 'exit'):
        parse_object = parse.Parsing(chaine)
        chaine = input()