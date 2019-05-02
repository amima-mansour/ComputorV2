# coding: utf-8

from operations import *
import calculs
import re

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

# simplifier le polynome :  par exemple 2 * x^2 + 1 + 2 * x + 5 - 2 * x^2 = 2 * x + 6
def simplifier_polynome(liste, inconnu):

    dic = {}
    liste_finale = []
    # traiter d'abord ce qui a entre les prentheses par exemple f(x) = 5 + (x + 2 - 5 * 3)^2 
    for element in liste:
        coeff = 1
        if isinstance(element, list):
            liste_finale.append(simplifier_polynome(element, inconnu))
            continue
        if re.match(r'[0-9]+(\.[0-9])?', element):
            nbr = calculs.nombre(element)
            index = liste.index(element)
            if index - 4 >= 0 and liste[index - 1] == '*' and liste[index - 3] == '^' and liste[index - 4] == inconnu:
                degree = calculs.nombre(liste[index - 2])
                if index - 5 >= 0 and liste[index - 5] == '-':
                    coeff = -1
            elif index + 4 < len(liste) and liste[index + 1] == '*' and liste[index + 2] == inconnu and liste[index + 3] == '^':
                degree = calculs.nombre(liste[index + 4])
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
            elif (index - 2 >= 0 and liste[index - 1] == '*' and liste[index - 2] == inconnu) or \
                (index + 2 < len(liste) and liste[index + 1] == '*' and liste[index + 2] == inconnu):
                degree = 1
                if (index - 1 >= 0 and liste[index - 1] == '-') or (index - 3 >= 0):
                    coeff = -1
            else:
                degree = 0
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
            if degree in dic.keys():
                dic[degree] += coeff * nbr
            else:
                dic[degree] = coeff * nbr
    print("le dic final est {}".format(dic))
    i = 0
    while len(dic) != 0 :
        if i in dic.keys():
            if i != 0:
                if dic[i] < 0:
                    liste_finale.append('-')
                else:
                    liste_finale.append('+')
            liste_finale.append(str(dic[i]))
        else:
            if i != 0:
                liste_finale.append('+')
            liste_finale.append('0')
        liste_finale.extend(['*', inconnu, '^', str(i)])
        del dic[i]
        i += 1
    print("la liste finale est {}".format(liste_finale))
    return liste_finale