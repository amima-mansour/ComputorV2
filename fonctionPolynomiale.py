# coding: utf-8

from operations import *
import calculs
import re

def calcul(liste, inconnu):
    # Cette fonction permet de tester et réorganiser un polynome.

    for element in liste:
        if inconnu in liste:
            index = liste.index(element)
            p = element.split('^')[1]
            liste[index] = puissance(inconnu, p)

def calcul_fragmente(liste, inconnu):
    # Cette fonction permet de fragmenter les calculs avant les x^n. exemple 5 * 9 / 9 * x^n => 5 * x^n

    liste_finale = []
    while '+' in liste or '-' in liste:
        index_1, index_2 = len(liste), len(liste)
        if '+' in liste:
            index_1 = liste.index('+')
        if '-' in liste:
            index_2 = liste.index('-')
        if index_1 < index_2:
            index_min = index_1
        else:
            index_min = index_2
        liste_a_calculer = liste[:index_min]
        liste_inconnu = []
        if inconnu in liste_a_calculer:
            # partie redondante
            # a fusionner plz
            index = liste_a_calculer.index(inconnu)
            if index > 0:
                index -= 1
            liste_inconnu = liste_a_calculer[index:]
            liste_a_calculer = liste_a_calculer[:index]
        if liste_a_calculer:
            liste_finale.append(calculs.calcul(liste_a_calculer))
        if len(liste_inconnu) > 0:
            liste_finale.extend(liste_inconnu)
        liste_finale.append(liste[index_min])
        liste = liste[index_min + 1:]
    liste_inconnu = []
    if inconnu in liste:
        index = liste.index(inconnu)
        if index > 0:
            index -= 1
        liste_inconnu = liste[index:]
        liste = liste[:index]
    if liste:
        liste_finale.append(calculs.calcul(liste))
    if len(liste_inconnu) > 0:
        liste_finale.extend(liste_inconnu)
    print("la liste apres la fragementation = {}".format(liste_finale))
    return liste_finale


    liste_finale.append(calculs.calcul(liste))



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
                if index + 3 < len(liste_finale) and liste_finale[len(liste_finale) - 1] not in '-+':
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
    index = 0
    while inconnu in liste:
        element = liste[index]
        coeff, degree = 1, 1
        # traiter d'abord ce qui est entre les prentheses par exemple f(x) = 5 + (x + 2 - 5 * 3)^2
        if isinstance(element, list):
            liste_finale.append(simplifier_polynome(element, inconnu))
            continue
        if inconnu == element:
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
                del liste[index - 2: index + 1]
                if index - 3 >= 0 and liste[index - 3] == '-':
                    coeff = -1
                index -= 2
            elif index + 2 < len(liste) and liste[index + 1] == '*':
                nbr = calculs.nombre(liste[index + 2])
                del liste[index: index + 3]
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
            else:
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
                del liste[index]
                index -= 1
                nbr = 1
            if degree in dic.keys():
                dic[degree] += coeff * nbr
            else:
                dic[degree] = coeff * nbr
        else:
            index += 1
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
    print("liste apres simplification {}".format(liste_finale))
    return liste_finale

####RESOLUTION#####

# trouver le degree
def degree(liste, inconnu):

    degree = 0
    for element in liste:
        if element == '^':
            index = liste.index(element)
            nbr = calculs.nombre(liste[index + 2])
            if degree < nbr:
                degree = nbr
    return degree

# calcul discriminant

# resolution
def resoudre(liste, inconnu):

    liste_finale = []
    a, b, c = 'null'
    degree = degree(liste, inconnu)
    if (degree > 2):
        print("Degree is greater than 2")
    else:
        for element in liste:
            if isinstance(element, list):
                liste_finale.extend(developper(element))
            else:
                liste_finale.append(element)
        liste = simplifier(liste_finale)
        for element in liste:
            if element == inconnu:
                index = liste.index(element)
                if liste[index + 2] == '0':
                    c = liste[index - 2]
                elif liste[index + 2] == '1':
                    b = liste[index - 2]
                else:
                    a = liste[index - 2]
    return a, b, c, a**2 - 4 * b * c


