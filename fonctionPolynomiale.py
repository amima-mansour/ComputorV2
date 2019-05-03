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

# nettoyer le polynome avant l'affichage sur la sortie standard
def nettoyer_polynome(liste, inconnu):

    liste_finale = []
    i = 0
    while liste:
        element = liste[i]
        if isinstance(element, list):
            nettoyer_polynome(element)
        else:
            if element == inconnu:
                index = liste.index(element)
                if liste[index - 2] == '0':
                    pass
                elif liste[index + 2] == '0':
                    liste_finale.extend(liste[index - 2:index - 1])
                elif liste[index + 2] == '1':
                    liste_finale.extend(liste[index - 2:index + 1])
                elif liste[index - 2] == '1':
                    liste_finale.extend(liste[index:index + 3])
                else:
                    liste_finale.extend(liste[index - 2:index + 3])
                if index + 3 < len(liste) and liste_finale[len(liste_finale) - 1] not in '-+':
                        liste_finale.append(liste[index + 3])
                del liste[index - 2:index + 3]
                i -= 2
                if liste and liste[i] == '+':
                    del liste[i]
                
            else:
                i += 1
    return liste_finale

# afficher le polynome sur la sortie standard
def affiche_polynome(liste, inconnu):
    # pas de simplification au niveau du polynome
    # renvoyer le polynome tel qu'il est

    liste = nettoyer_polynome(liste, inconnu)
    print("la liste apres nettoyage {}".format(liste))
    chaine = ''
    for element in liste:
        if isinstance(element, list):
            chaine += '(' + affiche_polynome(element) + ') '
        else:
            chaine += element
            if liste.index(element) != len(liste) - 1:
                chaine += ' '
    return chaine

# calculer les coefficients du degree 0
def degree_null(liste, inconnu):

    nbr = 0
    for element in liste:
        if re.match(r'(-)?[0-9]+(\.[0-9]+)?', element):
            coeff = 1
            index = liste.index(element)
            if index == 0:
                nbr += calculs.nombre(element) 
            if index - 1 >= 0 and liste[index - 1] in '+-':
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
                nbr += coeff * calculs.nombre(element)
    return nbr
   
# simplifier le polynome :  par exemple 2 * x^2 + 1 + 2 * x + 5 - 2 * x^2 = 2 * x + 6
def simplifier_polynome(liste, inconnu):

    dic = {}
    liste_finale = []
    for element in liste:
        coeff, degree = 1, 1
        # traiter d'abord ce qui est entre les prentheses par exemple f(x) = 5 + (x + 2 - 5 * 3)^2 
        if isinstance(element, list):
            liste_finale.append(simplifier_polynome(element, inconnu))
            continue
        if inconnu == element:
            # index
            index = liste.index(element)
            # degree
            if index + 2 < len(liste) and liste[index + 1] == '^':
                degree = calculs.nombre(liste[index + 2])
                del liste[index + 1]
                del liste[index + 1]
            else:
                degree = 1
            # nbr
            if index - 2 >= 0 and liste[index - 1] == '*':
                nbr = calculs.nombre(liste[index - 2])
                if index - 3 >= 0 and liste[index - 3] == '-':
                    coeff = -1
            elif index + 2 < len(liste) and liste[index + 1] == '*':
                nbr = calculs.nombre(liste[index + 2])
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
            else:
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
                nbr = 1
            if degree in dic.keys():
                dic[degree] += coeff * nbr
            else:
                dic[degree] = coeff * nbr
    dic[0] = degree_null(liste, inconnu)
    i = 0
    while len(dic) != 0 :
        if i in dic.keys():
            if i != 0:
                if dic[i] < 0:
                    liste_finale.append('-')
                else:
                    liste_finale.append('+')
            liste_finale.append(str(dic[i]))
            del dic[i]
        else:
            if i != 0:
                liste_finale.append('+')
            liste_finale.append('0')
        liste_finale.extend(['*', inconnu, '^', str(i)])
        i += 1
    return liste_finale