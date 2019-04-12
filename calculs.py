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

    print("la longueur de la liste avant calcul = {}".format(len(liste)))
    if len(liste) == 1:
        return liste[0]
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

def trouver_indice_fin(liste, start, pas):
    # renvoie l'indice de la partie a traiter

    fin = start
    if pas > 0:
        while fin < len(liste) and liste[fin] != '-' and liste[fin] != '+':
            fin += pas
        return fin
    while fin > -1 and liste[fin] != '-' and liste[fin] != '+':
        fin += pas
    return fin + 1

def calcul_complexe_elementaire_droite(liste, start):
    # effectuer des calculs elementaires en respectant la priorite

    fin = trouver_indice_fin(liste, start, 1)
    liste_a_traiter = liste[start + 1:fin]
    print("la fin = {}".format(fin))
    print("La liste prise = {}".format(liste_a_traiter))
    liste = liste[:start] + liste[fin:]
    img = calcul_parenthese(liste_a_traiter)
    return img, liste

def calcul_complexe_elementaire_gauche(liste, start):
    # effectuer des calculs elementaires en respectant la priorite

    fin = trouver_indice_fin(liste, start, -1)
    liste_a_traiter = liste[fin:start]
    liste = liste[:fin] + liste[start + 1:]
    img = calcul_parenthese(liste_a_traiter)
    return img, liste

def calcul_imaginaire(liste):
    # retourner la partie imaginaire dans l'expression

    img_total = 0
    while 'i' in liste:
        index = liste.index('i')
        img_droite, img_gauche = 1, 1
        if index != len(liste) - 1 and liste[index + 1] == '*':
            img_droite, liste = calcul_complexe_elementaire_droite(liste, index + 1)
        print("La liste droite = {}".format(liste))
        index = liste.index('i')
        if index != 0 and liste[index - 1] == '*':
            img_gauche, liste = calcul_complexe_elementaire_gauche(liste, index - 1)
        img = nombre(img_droite * img_gauche)
        index = liste.index('i')
        if index != 0 and liste[index - 1] in '-+':
            print("le nombre img = {}".format(img))
            if liste[index - 1]  == '-':
                img *= -1
            del liste[index]
            del liste[index - 1]
        img_total += img
    return str(img_total)

def verifier_structure(liste):
    # verifier si la liste contient le nombre complexe i, dans ce cas retourne 1
    # si la liste contient une matice, elle retourne 2
    # sinon retourne 0

    for element in liste:
        if element == 'i':
            return 1
        elif re.match(r'(^(\+|\^|\*|-|%|\/|[0-9]+)$)', element):
            pass
        else:
            return 2
    return 0