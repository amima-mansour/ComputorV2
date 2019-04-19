# coding: utf-8

import re
import matrice
import operations

def nombre(chaine):
    # Cette fonction permet de tester si une chaine est un nombre et si oui le retourner.

        if isinstance(chaine, (int, float)):
            return chaine
        if '.' in chaine:
            return  float(chaine)
        return int(chaine)

def calcul_elementaire(liste, char):
    # Cette fonction permet de faire un calcul elementaire.

    while char in liste:
        index = liste.index(char)
        if index != 0 and index + 1 < len(liste) and re.match(r'(-)?[0-9]+(\.[0-9]+)?',liste[index - 1]) \
            and re.match(r'(-)?[0-9]+(\.[0-9]+)?',liste[index + 1]):
            n_1 = nombre(liste[index - 1])
            n_2 = nombre(liste[index + 1])
            if char == '^':
                tmp = n_1 ** n_2
            elif char == '*':
                tmp = n_1 * n_2
            elif char == '/':
                try:
                    tmp = n_1 / n_2
                except ZeroDivisionError:
                    print ("Error : Zero Division")
                    return []
            elif char == '%':
                tmp = n_1 % n_2
            elif char == '+':
                tmp = n_1 + n_2
            else:
                tmp = n_1 - n_2
        liste[index] = str(tmp)
        del liste[index - 1]
        del liste[index]
    return liste

def variables_inconnues(liste):
    # Cette fonction recuperer les variables inconnues et leurs indices

    variables = {}
    for element in liste:
        if element == 'i':
            continue
        index = liste.index(element)
        if isinstance(element, list):
            variables_inter = variables_inconnues(element)
            if variables_inter != {}:
                variables[index] = variables_inter
        elif re.match(r'^[A-Za-z]+$', element):
            if index + 1 < len(liste) and isinstance(liste[index + 1], list):
                # une variable de type f(2)
                variables[index] = [element.lower() , liste[index + 1]]
            else:
                # une variable de type var
                variables[index] = element.lower()
        else:
            continue
    return variables

def calcul(liste):
    # Cette fonction permet d'effectuer tous les calculs elementaires.

    liste = calcul_elementaire(liste, '^')
    liste = calcul_elementaire(liste, '/')
    liste = calcul_elementaire(liste, '%')
    liste = calcul_elementaire(liste, '*')
    liste = calcul_elementaire(liste, '+')
    liste = calcul_elementaire(liste, '-')
    if not liste:
        return 'null'
    return liste[0]


def calcul_global(liste):
    # Cette fonction permet d'effectuer des calculs avec des parentheses.

    if len(liste) == 1:
        return liste[0]
    liste_finale = []
    # l'objectif est de calculer ce qui a dans les parentheses
    for i, element in enumerate(liste):
        if isinstance(element, list):
            liste_finale.append(calcul_parenthese(element))
        elif re.match('^[a-zA-Z]+$', element) and i  + 1 != len(liste) and isinstance(liste[i + 1], list):
            liste_finale.append(element)
            liste_finale.append(calcul_parenthese(liste[i + 1]))
        elif re.match(r'^(\*|\+|\^|-|\/|%)$', element) or re.match('^[a-zA-Z]+$', element):
            liste_finale.append(element)
        elif re.match(r'(-)?[0-9]+(\.[0-9]+)?', element):
            liste_finale.append(element)
        elif '[' in element:
            liste_finale.append(matrice.matrice_parsing(element))
        else:
            print("Error : something is wrong")
    return calcul(liste_finale)

def verifier_structure(liste):
    # verifier si la liste contient le nombre complexe i, dans ce cas retourne 1
    # si la liste contient une matice, elle retourne 2
    # sinon retourne 0

    print('la liste dans le structure {}'.format(liste))
    for element in liste:
        if element == 'i':
            return 1
        elif isinstance(element, list) or re.match(r'(^(\+|\^|\*|-|%|\/|[0-9]+(\.[0-9]+)?)$)', element):
            continue
        else:
            return 2
    return 0