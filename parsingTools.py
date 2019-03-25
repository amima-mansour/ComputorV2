# coding: utf-8

import re

# verifier l'existence d'un seul = dans la chaine
def equal_number(chaine):

    msg = ''
    liste = chaine.split('=')
    if len(liste) != 2 or liste[1] == '':
        liste = []
        msg = 'Error : we must have one ='
    return liste, msg

# transfomer une chaine de caractere en une liste 
def premier_test(chaine):

    liste_finale = []
    liste = chaine.split()
    for element in liste:
        m = re.search(r"(\*|-|%|/|\+)", element)
        if element in '+*-/%':
            liste_finale.append(element)
        elif m:
            char = m.group(0)
            liste_intermediaire = element.split(char)
            liste_finale.append(liste_intermediaire[0])
            liste_finale.append(char)
            liste_finale.append(liste_intermediaire[1])
        else:
            liste_finale.append(element)
    return liste_finale

# tester tous les elements d'une liste
def second_test(chaine):

    nbr = -1
    msg = ''
    for element in chaine:
        if re.match(r"^((([0-9]*(\.[0-9]+)?)(i)?)|/|%|\+|-|\*|([0-9]*(\.[0-9]+)?)[a-zA-Z]+)$", element):
            nbr = 1
        else:
            msg = 'Error invalid expression'
            nbr = -1
            break
    return nbr, msg