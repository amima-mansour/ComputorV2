# coding: utf-8

import sys
import parse

if __name__ == "__main__":
    var = {}
    chaine = input()
    while (chaine != 'exit'):
        # 1- parsing de la chaine 
        parse_object = parse.Parsing(chaine)
        nbr = parse_object.second_parsing()
        if nbr == -1:
            parse_object.affiche_erreur()
        print(nbr)
        chaine = input()