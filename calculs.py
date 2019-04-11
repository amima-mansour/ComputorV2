# coding: utf-8

import re
import matrice
import operations

def nombre(chaine):
    # Cette fonction permet de tester si une chaine est un nombre et si oui le retourner.

        if '.' in chaine:
            return  float(chaine)
        return int(chaine)

def calcul_elementaire(liste, char):
    # Cette fonction permet de faire un calcul elementaire.

    while char in liste:
        index = liste.index(char)
        if index != 0 and index + 1 < len(liste) and re.match(r'[0-9]+',liste[index - 1]) \
            and re.match(r'[0-9]+',liste[index + 1]):
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
    # Cette fonction recuperer les variables inconnues et leur indice

    variables = {}
    for element in liste:
        if element == 'i':
            continue
        index = liste.index(element)
        if isinstance(element, list):
            variables_inter = variables_inconnues(element)
            if variables_inter != {}:
                variables[index] = variables_inter
        elif re.match(r'^[a-zA-z]+$', element):
            if index + 1 < len(liste) and isinstance(liste[index + 1], list):
                # une variable de type f(2)
                variables[index] = [element.lower() , liste[index + 1]]
            else:
                # une variable de type var
                variables[index] = element.lower()
        else:
            pass
    print('les variables inconnues sont : {}'.format(variables))
    return variables

def calcul(liste):
    # Cette fonction permet de tester et réorganiser la liste.

    liste = calcul_elementaire(liste, '^')
    liste = calcul_elementaire(liste, '/')
    liste = calcul_elementaire(liste, '%')
    liste = calcul_elementaire(liste, '*')
    liste = calcul_elementaire(liste, '+')
    liste = calcul_elementaire(liste, '-')
    if not liste:
        return 'null'
    return liste[0]


def calcul_parenthese(liste):
    # Cette fonction permet de tester et réorganiser un polynome.

    liste_finale = []
    # l'objectif est de calculer ce qui a dans les parentheses
    for i, element in enumerate(liste):
        if re.match('^[a-zA-Z]+$', element) and i  + 1 < len(liste) and isinstance(liste[i + 1], list):
            liste_finale.append(element)
            liste_finale.append(calcul_parenthese(liste[i + 1]))
        elif re.match(r'^(\*|\+|\^|-|\/|%)$', element) or re.match('^[a-zA-Z]+$', element):
            liste_finale.append(element)
        elif re.match(r'[0-9]+(\.[0-9]+)?', element):
            liste_finale.append(nombre(element))
        elif '[' in element:
            liste_finale.append(matrice.matrice_parsing(element))
        elif isinstance(element, list):
            liste_finale.append(calcul_parenthese(element))
        else:
            print("Error : something is wrong")
    return calcul(liste_finale)

def calcul_complexe_elementaire(operateur, nombre):
    # effectuer des calculs elementaires

    if operateur == '*':
        return nombre
    if operator == '/':
        return 
    if operator == '^':
        if nombre % 2 == 0:
            return '1'
        else:
            return -1
# A modifier ici
def calcul_complexe(liste):
    # calculer les nombres complexes

    liste_reel = liste.copy()
    liste_img = []
    index_i = []
    for element in liste:
        if element = 'i':
            index_i.append(liste.index(element))
    for element in index:
        coeff = 1
        if index < len(liste) - 1:

            

    reel = '0'
    img = '0'
    return reel, img

def verifier_structure(liste):
    # verifier si la liste contient le nombre complexe i, dans ce cas retourne 1
    # si la liste contient une matice, elle retourne 2
    # sinon retourne 0

    for element in liste:
        if 'i' in element or element == 'i':
            return 1
        elif re.match(r'(^(/+|\^|\*|-|%|\/|[0-9]+)$)', element):
            pass
        else:
            return 2
    return 0