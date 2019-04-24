# coding: utf-8

import re
import matrice
from test_nom_de_variable import *
import fonctionPolynomiale as polynome
import calculs
import complexe

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

# trouver l'indice de du caractere fermant char2
def indice_caractere(chaine, char1, char2):

    i = 0
    nbr_caractere_ouvrant = 1
    longueur = len(chaine)
    while i < longueur:
        if chaine[i] == char1:
            nbr_caractere_ouvrant += 1
        if chaine[i] == char2:
            nbr_caractere_ouvrant -= 1
        if nbr_caractere_ouvrant == 0:
            break
        i += 1
    try:
        assert nbr_caractere_ouvrant == 0 or i < longueur and chaine[i] == char2
        if nbr_caractere_ouvrant == 0:
            return i
        while i < longueur:
            if chaine[i] == char2:
                if nbr_caractere_ouvrant == 0:
                    return i
                else:
                    nbr_caractere_ouvrant -= 1
            i += 1
        print('Error : brackets\' problem')
        return 0
    except AssertionError:
        print('Error : brackets\' problem')
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
        indice_2 = indice_caractere(nouvelle_chaine, ')', '(')
        if indice_2 > 0:
            liste_finale.append(premier_test(nouvelle_chaine[:indice_2].strip()))
            indice_2 += 1
            if indice_2 < len(nouvelle_chaine):
                liste_finale = liste_finale + premier_test(nouvelle_chaine[indice_2:].strip())
        else:
            liste_finale = []
    return liste_finale

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

#  organiser la chaine : chaque element est dans un bloc
def organiser_chaine(chaine):

    liste_finale = []
    m = re.search(r'(\*|\^|\/|%|\+|-|i)', chaine)
    char = m.group(0)
    liste_inter = chaine.split(char)
    for element_inter in liste_inter:
        if element_inter == '':
            continue
        if re.match(r'^([0-9]+|[a-zA-Z]+|i)$', element_inter):
            liste_finale.append(element_inter)
        else:
            liste_finale.extend(organiser_chaine(element_inter))
        if char == 'i':
            liste_finale.append('*')
            liste_finale.append('i')
        elif liste_inter.index(element_inter) != len(liste_inter) - 1:
            liste_finale.append(char)
        else:
            pass
    return liste_finale

#  organiser la nouvelle liste pour mieux faire le calcul
def organiser_liste(liste):

    liste_finale = []
    for element in liste:
        if isinstance(element, list):
            liste_finale.append(organiser_liste(element))
        elif re.match(r'^([0-9]+(\.[0-9]+)?|\*|\^|\/|%|\+|-|i|[a-zA-Z]+)$', element):
            liste_finale.append(element)
        else:
            while element:
                m = re.search(r"\*|\/|\+|-|%|\^", element)
                if m:
                    char = m.group(0)
                    index_char = element.index(char)
                    if index_char != 0:
                        liste_finale.append(''.join(element[:index_char]))
                    liste_finale.append(element[index_char])
                    if index_char != len(element) - 1:
                        element = ''.join(element[index_char + 1:])
                else:
                    if element != 'i':
                        liste_finale.extend(organiser_chaine(element))
                    else:
                        liste_finale.append('i')
                    element = ''
    return liste_finale

# tester la partie calculatoire
def test_partie_calculatoire(chaine, nom_var):

    # parsing pour mettre cette expression dans une liste
    liste = premier_test(chaine)
    # eliminer les elements vides
    for element in liste:
        if not element:
            liste.remove(element)
    # chaque nombre et operateur constitue un element tout seul de la liste
    liste = organiser_liste(liste)
    # chercher les variables inconnues et se trouvant dans l'expression
    variables = calculs.variables_inconnues(liste)
    return liste, variables

# traiter la partie calculatoire
def traitement_partie_calculatoire(liste):
    # traiter la partie calculatoire

    reel, img, mat = 0, 0, 'null'
    # aucune trace de matrice, pas de complexe
    # complexe
    struct = calculs.verifier_structure(liste)
    print("la structure est egale a {}".format(struct))
    if struct == 1:
        img, reel, liste = complexe.calcul_imaginaire(liste)
        print("type reel = {} et reel = {}".format(type(reel), reel))
        reel = str(calculs.nombre(calculs.calcul_global(liste)) + calculs.nombre(reel))
    elif struct == 2:
        mat = liste[0]
    else:
        reel = calculs.calcul_global(liste)
    return reel, img, mat

# traiter une chaine de liaison entre deux matrices
def traitement_liaison(chaine):

    liste = []
    for element in chaine:
        m = re.search(r'\*|\+|\/|-|%', chaine)
        char = m.group(0)
        index = chaine.index(char)
        if index != 0:
            liste.append(chaine[:index].strip())
        liste.append(char)
        chaine = chaine[index + 1:].strip()
    if chaine:
        liste.append(chaine)
    return liste

# traiter les matrices possibles
def traitement_matrice(chaine):

    liste = []
    while '[' in chaine:
        index = chaine.index('[')
        fin = indice_caractere(chaine[1:].strip(), '[', ']')
        if index != 0:
            liste.extend(traitement_liaison(chaine[:index].strip()))
        liste.append(matrice.matrice_parsing(chaine[index + 1:fin + 1].strip()))
        if fin < len(chaine) - 1:
            chaine = chaine[fin + 2:].strip()
    if chaine != '':
        liste.append(chaine)
    return liste
