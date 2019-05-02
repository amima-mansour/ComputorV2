# coding: utf-8

import sys
from parse import *
from fonctionPolynomiale import *
from parsingOutils import *

if __name__ == "__main__":
    variables = {}
    fonctions = {}
    matrices = {}
    chaine = input()
    while (chaine != 'exit'):
        parse_objet = Parsing(chaine)
        test = 0
        if parse_objet.tmp_inconnus:
            test = remplacer(parse_objet, variables, fonctions, parse_objet.tmp_inconnus) # remplacement est fait, reste la partie calculatoire
        if test == 0:
            nom = parse_objet.var
            liste = parse_objet.liste
            print('le nom de la fonction : {}, la liste : {}'.format(nom, liste))
            if nom != '?' and len(nom) == 2:
                fonctions[nom[0]] = [nom[1], liste]
                liste = simplifier_polynome(liste, nom[1])
                print(affiche_polynome(liste))
            else:
                reel, imaginaire, mat = traitement_partie_calculatoire(liste)
                if nom != '?':
                    if mat != 'null':
                        matrices[nom[0]] = mat
                    elif imaginaire != 0:
                        variables[nom[0]] = reel + ' + ' + imaginaire + ' * i'
                    else:
                        variables[nom[0]] = reel
                if mat != 'null' and isinstance(mat, list):
                    matrice.affiche_matrice(mat)
                elif imaginaire != 0:
                    print('{} + {} * i'.format(reel, imaginaire))
                elif reel != 0:
                    print(reel)
                else:
                    print(mat)
        print("les variables a printer sont {}".format(variables))
        chaine = input()