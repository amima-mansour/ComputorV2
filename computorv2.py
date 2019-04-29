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
        if test == 0:
            nom = parse_objet.var
            liste = parse_objet.liste
            print('le nom de la fonction : {}, la liste : {}'.format(nom, liste))
            if nom != '?' and len(nom) == 2:
                fonctions[nom[0]] = [nom[1], liste]
                print(affiche_polynome(liste))
            else:
                reel, imaginaire, mat = traitement_partie_calculatoire(liste)
                if nom != '?':
                    if mat != 'null':
                        matrices[nom[0]] = mat
                    elif imaginaire != 0:
                        vars[nom[0]] = reel + ' + ' + imaginaire + ' * i'
                    else:
                        vars[nom[0]] = reel
                if mat != 'null' and isinstance(mat, list):
                    matrice.affiche_matrice(mat)
                elif imaginaire != 0:
                    print('{} + {} * i'.format(reel, imaginaire))
                elif reel != 0:
                    print(reel)
                else:
                    print(mat)
        print("les vars a printer sont {}".format(vars))
        chaine = input()