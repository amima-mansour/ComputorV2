# coding: utf-8

import sys
import parse

if __name__ == "__main__":
    var = {}
    fonction = {}
    chaine = input()
    while (chaine != 'exit'):
        parse_object = parse.Parsing(chaine)
        if parse_object.remplacer(var, fonction) == 0:
            if parse_object.var != '?':
                variable = parse_object.var
                # 2 cas possibles : fonction ou variable
                if len(variable) == 2:
                    # fonction
                    fonction[variable[0]] = liste
                else:
                    # variable
                    var[variable[0]] = liste
            else:
                parse_object.
                # afficher le calcul sur la sortie standard

        chaine = input()