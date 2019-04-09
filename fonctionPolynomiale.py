# coding: utf-8

from operations import *

def calcul(liste, inconnu):
    # Cette fonction de tester et réorganiser un polynome.

    for element in liste:
        if inconnu in liste:
            index = liste.index(element)
            p = element.split('^')[1]
            liste[index] = puissance(inconnu, p)

# afficher le polynome sur la sortie standard
def affiche_polynome(liste):
    # pas de simplification au niveau du polynome
    # renvoyer le polynome tel qu'il est

    chaine = ''
    for element in liste:
        if isinstance(element, list):
            chaine += '(' + affiche_polynome(element) + ') '
        else:
            chaine += element
            if liste.index(element) != len(liste) - 1:
                chaine += ' '
    return chaine