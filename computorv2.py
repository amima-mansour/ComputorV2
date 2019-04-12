# coding: utf-8

import sys
from parse import *
from fonctionPolynomiale import *
from parsingOutils import *

if __name__ == "__main__":
    vars = {}
    fonctions = {}
    matrices = {}
    chaine = input()
    while (chaine != 'exit'):
        parse_objet = Parsing(chaine)
        test = 0
        if parse_objet.tmp_inconnus:
            test = parse_objet.remplacer(vars, fonctions) # remplacement est fait, reste la partie calculatoire
        print('la liste apres remplacement = {}'.format(parse_objet.liste))
        if test == 0:
            nom = parse_objet.var
            liste = parse_objet.liste
            print('le nom de la fonction : {}, la liste : {}'.format(nom, liste))
            if nom != '?':
                # 2 cas possibles : fonction ou variable
                if len(nom) == 2:
                    # fonction
                    fonctions[nom[0]] = [nom[1], liste]
                    print(affiche_polynome(liste))
                else:
                    # variable
                    reel, imaginaire, mat = traitement_partie_calculatoire(liste)
                    print('reel = {}\nimaginaire = {}\nmatrice = {}\n'.format(reel, imaginaire, mat))
                    if mat != 'null':
                        matrices[nom[0]] = mat
                    elif imaginaire != 'null':
                        vars[nom[0]] = reel + ' + ' + imaginaire + ' * i'
                    else:
                        vars[nom[0]] = reel
                    print(vars[nom[0]])
            else:
                pass
                # afficher le calcul sur la sortie standard
        print(vars)
        chaine = input()