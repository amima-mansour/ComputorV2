# coding: utf-8

import re
import matrice
import operations

def nombre(chaine):
    # Cette fonction permet de tester si une chaine est un nombre et si oui le retourner.

    isinstance(chaine, str)
        if '.' in chaine:
            return  float(chaine)
        return int(chaine)
    return chaine

def calcul_elementaire(liste, char):
    # Cette fonction permet de faire un calcul elementaire.

    while char in liste:
        index = liste.index(char)
        if index != 0 and index + 1 < len(liste) and re.match(r'[0-9]+',liste[index - 1]) and re.match(r'[0-9]+',liste[index + 1]):
            if char == '^':
                tmp = puissance(liste[i - 1], liste[i + 1])
            elif char == '*':
                tmp = liste[i - 1] * liste[i + 1]
            elif char == '/':
                try:
                    tmp = liste[i - 1] / liste[i + 1]
                except ZeroDivisionError:
                    print ("Error : Zero Division")
                    return []
            elif char == '%':
                tmp = liste[i - 1] % liste[i + 1]
            elif char == '+':
                tmp = liste[i - 1] + liste[i + 1]
            else:
                tmp = liste[i - 1] - liste[i + 1] 
        liste[index] = tmp
        del liste[index - 1]
        del liste[index + 1]
    return liste

def variables_inconnues(liste):
    # Cette fonction recuperer les variables inconnues et leur indice

    variables = {}
    for element in liste:
        if re.match(r'^[a-zA-z]+$', element):
            index = liste.index(element)
            if index + 1 < len(liste) and isinstance(liste[index + 1], list):
                # une variable de type f(2) 
                variables[index] = [element.lower() , liste[index + 1]]
            else:
                # une variable de type var
                variables[index] = element.lower()
    return variables

def calcul_simplification(liste):
    # Cette fonction permet de tester et réorganiser la liste.

    liste = calcul_elementaire(liste, '^')
    liste = calcul_elementaire(liste, '/')
    liste = calcul_elementaire(liste, '%')
    liste = calcul_elementaire(liste, '*')
    liste = calcul_elementaire(liste, '+')
    liste = calcul_elementaire(liste, '-')


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
    return calcul_simplification(liste_finale)
            
