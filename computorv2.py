# coding: utf-8

import sys
import parse

if __name__ == "__main__":
    var = {}
    fonction = {}
    chaine = input()
    while (chaine != 'exit'):
        parse_objet = parse.Parsing(chaine)
        if parse_objet.remplacer(var, fonction) == 0: # remplacement est fait, reste la partie calculatoire
            variable = parse_objet.var
            liste = parse_objet.liste
            if variable != '?':
                # 2 cas possibles : fonction ou variable
                if len(variable) == 2:
                    # fonction
                    fonction[variable[0]] = liste
                else:
                    # variable
                    var[variable[0]] = liste
            else:
                parse_objet.
                # afficher le calcul sur la sortie standard

        chaine = input()