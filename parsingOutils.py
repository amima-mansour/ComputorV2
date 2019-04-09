# coding: utf-8

import re
import matrice
from test_nom_de_variable import *
import fonctionPolynomiale as polynome
import calculs

# verifier l'existence d'un seul = dans la chaine
def equal_number(chaine):

    liste = chaine.split('=')
    try:
        assert len(liste) == 2 and liste[0] != '' and liste[1] != ''
    except:
        print('Error : we must have an expression like a = b + c or b + c = ?')
        return '', ''
    else:
        return liste[0], liste[1]

# trouver l'indice de la parenthese fermante
def indice_parenthese(chaine):

    i = 0
    nbr_parenthese_ouvrante = 0
    longueur = len(chaine)
    while i < longueur and chaine[i] != ')':
        if chaine[i] == '(':
            nbr_parenthese_ouvrante += 1
        i += 1
    try:
        assert i < longueur and chaine[i] == ')'
        if nbr_parenthese_ouvrante == 0:
            return i
        while i < longueur:
            if chaine[i] == ')':
                if nbr_parenthese_ouvrante == 0:
                    return i
                else:
                    nbr_parenthese_ouvrante -= 1
            i += 1
        print('Error : parentheses\' problem')
        return 0
    except AssertionError:
        print('Error : parentheses\' problem')
        return 0

# transfomer une partie de la chaine de caractere principale en une liste
def test_elementaire(chaine):

    liste_finale = []
    liste = chaine.split()
    for i, element in enumerate(liste):
        if element == ')':
            liste_finale
        m = re.search(r"(\*|-|%|/|\+|\^)", element)
        if element in '+*-/%^':
            liste_finale.append(element)
        elif m:
            char = m.group(0)
            liste_intermediaire = element.split(char)
            print(liste_intermediaire)
            if liste_intermediaire[0] == '':
                liste_finale.append(element)
            else:
                liste_finale.append(liste_intermediaire[0])
                liste_finale.append(char)
                liste_finale.append(liste_intermediaire[1])
        else:
            liste_finale.append(element)
    return liste_finale

# transfomer une chaine de caractere en une liste.
def premier_test(chaine):

    liste_finale = []
    if '(' not in chaine:
        return test_elementaire(chaine)
    else:
        indice_1 = chaine.index('(')
        if indice_1 != 0:
            liste_finale = liste_finale + test_elementaire(chaine[:indice_1].strip())
        indice_1 += 1
        nouvelle_chaine = chaine[indice_1:].strip()
        indice_2 = indice_parenthese(nouvelle_chaine)
        if indice_2 > 0:
            liste_finale.append(premier_test(nouvelle_chaine[:indice_2].strip()))
            indice_2 += 2
            if indice_2 < len(nouvelle_chaine):
                liste_finale = liste_finale + premier_test(nouvelle_chaine[indice_2:].strip())
        else:
            liste_finale = []
    return liste_finale

# convertit une chaine de caractere en un nombre
def convertir_en_nombre(chaine):

    if '.' in chaine :
        return float(chaine)
    return int(chaine)

def convertir_en_complexe(chaine):

    reel = 0
    imaginaire = 0
    if 'i' in chaine :
        nbr = '1'
        if chaine != 'i':
            nbr = chaine.split('i')[0];
        imaginaire = convertir_en_nombre(nbr)
    else:
        reel = convertir_en_nombre(chaine)
    return reel, imaginaire

# traiter le nom de la variable ou de fonction
def traitement_nom_de_variable(chaine):

    if chaine == '?':
        return [chaine]
    # test de la variable avec 'i'
    test_complexe(chaine)
    if '(' in chaine:
        # recuperer dans ce cas le nom de la fonction, de la composition s'il y en a et le nom de l'inconu
        fonction, inconnu = test_fonction(chaine)
        return [fonction.lower(), inconnu.lower()]
    else:
        # tester le nom de la variable
        test_variable(chaine)
        return [chaine.lower()]

# tester la partie calculatoire
def test_partie_calculatoire(chaine, nom_var):

    # parsing pour mettre cette expression dans une liste
    liste = premier_test(chaine)
    variables = {}
    print(nom_var)
    if len(nom_var) == 1:
        variables = calculs.variables_inconnues(liste)
    print('variables dans la fonction = {}'.format(variables))
    return liste, variables

# traiter la partie calculatoire
def traitement_partie_calculatoire(liste):
    # traiter la partie calculatoire

    reel, imaginaire, mat = 'null', 'null', 'null'
    # aucune trace de matrice, pas de complexe
    # complexe
    struct = calculs.verifier_structure(liste)
    print('la structure est {}'.format(struct))
    if struct == 1:
        reel, imaginaire = calculs.calcul_complexe(liste)
    # matrice
    elif struct == 2:
        mat = matrice.traiter_matrice(liste)
    else:
        reel = calculs.calcul(liste)
    return reel, imaginaire, mat