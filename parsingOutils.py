# coding: utf-8

import re
import matrice
from test_nom_de_variable import *
import fonctionPolynomiale as polynome
import calculs
import complexe

def remplacer(objet, tmp_var, tmp_fonction, tmp_matrices, tmp_inconnus):
# chercher les variables inconnues et les remplacer par leur valeurs

    inconnu = '0'
    if len(objet.var) == 2:
        inconnu = objet.var[1]
    for key, element in tmp_inconnus.items():
        if isinstance(element, dict):
            test = remplacer(objet, tmp_var, tmp_fonction, element)
            if test == 0:
                continue
            return test
        if isinstance(element, list):
            print("element = {}".format(element))
            valeur = element[1][0]
            fonction = element[0]
            if ((len(tmp_var.keys()) > 0 and valeur not in tmp_var.keys() and not re.match(r'^[0-9]+(\.[0-9]+)?$', valeur)) \
                or (tmp_fonction and fonction not in tmp_fonction.keys())):
                print("Error : variable or function not defined")
                return -1
            objet.liste[key] = polynome.calcul(tmp_fonction[fonction], valeur)
        elif tmp_var and element in tmp_var.keys():
            liste = objet.liste[:key]
            liste += tmp_var[element].split()
            liste += objet.liste[key + 1:]
            objet.liste = liste
        elif tmp_matrices and element in tmp_matrices.keys():
            liste = objet.liste[:key]
            liste += [tmp_matrices[element]]
            liste += objet.liste[key + 1:]
            objet.liste = liste
        elif element == inconnu:
            continue
        else:
            print("Error : variable not defined")
            return -1
    objet.liste = nettoyer_post_remplacement(objet.liste)
    return 0

# nettoyer la liste apres leremplacement
def nettoyer_post_remplacement(liste):

    index = 0
    while index < len(liste):
        if isinstance(liste[index], list) and len(liste[index]) == 1 and not isinstance(liste[index][0], list):
            del liste[index]
            index -= 1
        index += 1
    return liste

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
        return -1
    except AssertionError:
        print('Error : brackets\' problem')
        return -1

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
        indice_2 = indice_caractere(nouvelle_chaine, '(', ')')
        if indice_2 > 0:
            liste_finale.append(premier_test(nouvelle_chaine[:indice_2].strip()))
            indice_2 += 1
            if indice_2 < len(nouvelle_chaine):
                liste_finale = liste_finale + premier_test(nouvelle_chaine[indice_2:].strip())
        else:
            liste_finale.append([])
    return liste_finale

# traiter le nom de la variable ou de fonction
def traitement_nom_de_variable(chaine):

    if chaine == '?':
        return [chaine]
    # test de la variable avec 'i'
    if not test_complexe(chaine):
        return []
    if '(' in chaine or ')' in chaine:
        # recuperer dans ce cas le nom de la fonction, de la composition s'il y en a et le nom de l'inconu
        fonction, inconnu = test_fonction(chaine)
        return [fonction.lower(), inconnu.lower()]
    else:
        # tester le nom de la variable
        if test_variable(chaine) == 1:
            return [chaine.lower()]
        return []

#  organiser la chaine : chaque element est dans un bloc
def organiser_chaine(chaine):

    if re.match(r'^[0-9]+(\.[0-9]+)?$', chaine):
        return [chaine]
    liste_finale = []
    m = re.search(r'(\*|\^|\/|%|\+|-|i|[a-zA-Z]+)', chaine)
    if not m:
        return []
    char = m.group(0)
    liste_inter = chaine.split(char)
    for element_inter in liste_inter:
        if element_inter == '':
            continue
        if re.match(r'^([0-9]+|[a-zA-Z]+|i)$', element_inter):
            liste_finale.append(element_inter)
        else:
            liste_finale.extend(organiser_chaine(element_inter))
        if char == 'i' or re.match('[a-zA-Z]+', char):
            liste_finale.append('*')
            liste_finale.append(char)
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
        elif re.match(r'^(((-)?[0-9]+(\.[0-9]+)?)|\*|\^|\/|%|\+|-|i|[a-zA-Z]+)$', element):
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
                        liste_inter = organiser_chaine(element)
                        if not liste_inter:
                            print("Error : Syntax")
                            return []
                        liste_finale.extend(liste_inter)
                    else:
                        liste_finale.append('i')
                    element = ''
    return liste_finale

# tester la partie calculatoire
def test_partie_calculatoire(chaine, nom_var):

    inconnu = ''
    if len(nom_var) == 2:
        inconnu = nom_var[1]
    # parsing pour mettre cette expression dans une liste
    liste = premier_test(chaine)
    # eliminer les elements vides
    for element in liste:
        if not element:
            liste.remove(element)
    # chaque nombre et operateur constitue un element tout seul de la liste
    liste = organiser_liste(liste)
    if not liste:
        return liste, {}
    # chercher les variables inconnues et se trouvant dans l'expression
    variables = calculs.variables_inconnues(liste)
    return liste, variables

# traiter la partie calculatoire
def traitement_partie_calculatoire(liste):
    # traiter la partie calculatoire

    reel, img, mat = '0', '0', 'null'
    # aucune trace de matrice, pas de complexe
    # complexe
    struct = calculs.verifier_structure(liste)
    if struct == 1:
        img, reel, liste = complexe.calcul_imaginaire(liste)
        if len(liste) > 0:
            reel = calculs.nombre(calculs.calcul_global(liste)) + calculs.nombre(reel)
        reel = str(reel)
    elif struct == 2:
        mat = matrice.traiter(liste)
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
        fin = indice_caractere(chaine[index + 1:].strip(), '[', ']') + index
        if fin < 0:
            return []
        if index != 0:
            liste.extend(chaine[:index].strip().split())
        matrice_element = matrice.matrice_parsing(chaine[index + 1:fin + 1].strip())
        if not matrice_element:
            return []
        liste.append(matrice_element)
        if fin < len(chaine) - 1:
            chaine = chaine[fin + 2:].strip()
    if chaine != '' and chaine != ' ':
        liste.extend(chaine.split())
    return liste