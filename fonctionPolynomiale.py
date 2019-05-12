# coding: utf-8

from operations import *
import calculs
import re
import resolutions

def calcul(liste, inconnu):
    # Cette fonction permet de tester et réorganiser un polynome.

    for element in liste:
        if inconnu in liste:
            index = liste.index(element)
            p = element.split('^')[1]
            liste[index] = puissance(inconnu, p)

def verifier(liste, inconnu):
    # Cette fonction verifie si la liste ne contient pas des inconnus.

    for element in liste:
        if isinstance(element, list):
            if verifier(element, inconnu):
                return True
        elif element == inconnu:
            return True
        else:
            continue
    return False

def premier_caractere(liste):
    index_1, index_2 = len(liste), len(liste)
    if '+' in liste:
        index_1 = liste.index('+')
    if '-' in liste:
        index_2 = liste.index('-')
    if index_1 < index_2:
        index_final = index_1
    else:
        index_final = index_2
    return index_final

def diviser_en_deux_parties(liste, inconnu):

    index = liste.index(inconnu)
    i = 0
    if index + 2 < len(liste) and liste[index + 1] == '^':
        i += 2
    if index == 0:
        if '*' in liste:
            index_3 = liste.index('*')
            liste_inconnu = ['*']
            liste_inconnu.extend(liste[:index_3])
            liste = liste[index_3:]
        else:
            liste_inconnu = liste
            liste = []
    elif index + i == len(liste) - 1:
        index -= 1
        liste_inconnu = liste[index:]
        liste = liste[:index]
    else:
        liste_inconnu = liste[index - 1:index + i + 1]
        del liste[index - 1:index + i + 1]
    return liste, liste_inconnu

def ajouter_a_liste(liste_finale, liste_a_calculer, liste_inconnu, inconnu):

    if len(liste_a_calculer) > 0 and not verifier(liste_a_calculer, inconnu):
        liste_finale.append(calculs.calcul_global(liste_a_calculer))
    else:
        liste_finale.extend(liste_a_calculer)
    if len(liste_inconnu) > 0:
        liste_finale.extend(liste_inconnu)
    return liste_finale

def calcul_fragmente(liste, inconnu):
    # Cette fonction permet de fragmenter les calculs avant les x^n. exemple 5 * 9 / 9 * x^n => 5 * x^n

    liste_finale = []
    while '+' in liste or '-' in liste:
        index = premier_caractere(liste)
        liste_a_calculer = liste[:index]
        liste_inconnu = []
        if inconnu in liste_a_calculer:
            liste_a_calculer, liste_inconnu = diviser_en_deux_parties(liste_a_calculer, inconnu)
        liste_finale = ajouter_a_liste(liste_finale, liste_a_calculer, liste_inconnu, inconnu)
        liste_finale.append(liste[index])
        liste = liste[index + 1:]
    liste_inconnu = []
    if inconnu in liste:
        liste, liste_inconnu = diviser_en_deux_parties(liste, inconnu)
    liste_finale = ajouter_a_liste(liste_finale, liste, liste_inconnu, inconnu)
    print("la liste apres la fragementation = {}".format(liste_finale))
    return liste_finale

# nettoyer la partie entre parenthese
def nettoyer_polynome_parentheses(liste, liste_finale, index, inconnu):

    if index - 2 >= 0 and liste[index - 1] == '*':
        liste_finale.extend(liste[index-2:index])
    liste_finale.append(nettoyer_polynome(liste[index], inconnu))
    index += 1
    if index < len(liste) and liste[index] in '*/^':
        liste_finale.extend(liste[index:index + 2])
        index += 2
    if index < len(liste) and liste[index] in '+-':
        liste_finale.append(liste[index])
        index += 1
    index += 1
    return liste_finale, index

# nettoyer le polynome avant l'affichage sur la sortie standard
def nettoyer_polynome(liste, inconnu):

    index = 0
    liste_finale = []
    while index < len(liste):
        if isinstance(liste[index], list):
            liste_finale, index = nettoyer_polynome_parentheses(liste, liste_finale, index, inconnu)
            continue
        if liste[index] == inconnu:
            if index - 2 >= 0 and liste[index - 2] == '0':
                index += 3
                continue
            elif index + 2 < len(liste) and liste[index + 2] == '0':
                liste_finale.extend(liste[index - 2:index - 1])
            elif index + 2 < len(liste) and liste[index + 2] == '1':
                if liste[index - 2] == '1':
                    liste_finale.extend(liste[index:index + 1])
                else:
                    liste_finale.extend(liste[index - 2:index + 1])
            elif index - 2 >= 0 and liste[index - 2] == '1':
                liste_finale.extend(liste[index:index + 3])
            else:
                liste_finale.extend(liste[index - 2:index + 3])
            if index + 3 < len(liste) and liste[index + 3] in '-+':
                liste_finale.append(liste[index + 3])
                index += 1
            index += 3
        else:
            index += 1
    return liste_finale

# afficher le polynome sur la sortie standard
def affiche_polynome(liste, inconnu):

    chaine = ''
    index = 0
    while index < len(liste):
        if isinstance(liste[index], list):
            chaine_inter = affiche_polynome(liste[index], inconnu)
            if inconnu not in chaine_inter:
                chaine += chaine_inter + ' '
            else:
                chaine += '(' + chaine_inter + ')'
        else:
            chaine += liste[index]
        if index != len(liste) - 1:
            if liste[index + 1] == '^' or liste[index] == '^':
                pass
            else:
                chaine += ' '
        index += 1
    return chaine

# calculer les coefficients du degree 0
def degree_null(liste, inconnu):

    nbr = 0
    index = 0
    while index < len(liste):
        if type(liste[index]) is not list and re.match(r'(-)?[0-9]+(\.[0-9]+)?', liste[index]):
            coeff = 1
            if index == 0:
                nbr += calculs.nombre(liste[index])
                index += 1
                continue
            if index - 1 >= 0 and liste[index - 1] in '+-':
                if index - 1 >= 0 and liste[index - 1] == '-':
                    coeff = -1
                nbr += coeff * calculs.nombre(liste[index])
        index += 1
    return nbr

# trouver le degree, le coeff correspondant
def elements_polynome(liste, index):

    coeff, degree = 1, 1
    # degree
    if index + 2 < len(liste) and liste[index + 1] == '^':
        print("rentrer")
        degree = calculs.nombre(liste[index + 2])
        del liste[index + 1: index + 3]
    # nbr
    if index - 2 >= 0 and liste[index - 1] == '*':
        nbr = calculs.nombre(liste[index - 2])
        del liste[index - 2: index + 1]
        index -= 2
        if index - 1 >= 0 and liste[index - 1] == '-':
            coeff = -1
    elif index + 2 < len(liste) and liste[index + 1] == '*':
        nbr = calculs.nombre(liste[index + 2])
        del liste[index: index + 3]
        index -= 1
        if index >= 0 and liste[index] == '-':
            coeff = -1
    else:
        if index - 1 >= 0 and liste[index - 1] == '-':
            coeff = -1
        del liste[index]
        index -= 1
        nbr = 1
    return degree, nbr, liste, coeff, index

# reconstruire le polynome final a partir des elements de dictionnaire dic
def trouver_polynome_final(dic, inconnu, liste_finale):

    i = 0
    while len(dic) != 0 :
        if i in dic.keys():
            if i == 0 and len(liste_finale) != 0:
                liste_finale = [str(dic[i]), '*', inconnu, '^', str(i) , '+'] + list(liste_finale)
                del dic[i]
                continue
            if len(liste_finale) != 0:
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

# simplifier le polynome :  par exemple 2 * x^2 + 1 + 2 * x + 5 - 2 * x^2 = 2 * x + 6
def simplifier_polynome(liste, inconnu):

    dic, liste_finale = {}, []
    index, dic[0] = 0, 0
    while index < len(liste):
        # traiter d'abord ce qui est entre les prentheses par exemple f(x) = 5 + (x + 2 - 5 * 3)^2
        if isinstance(liste[index], list):
            print("rentrer")
            if index - 2 >= 0 and liste[index - 1] == '*':
                liste_finale.extend(liste[index-2:index])
                del liste[index -2:index]
                index -= 2
            liste_finale.append(simplifier_polynome(liste[index], inconnu))
            del liste[index]
            if index < len(liste) and (liste[index] == '^' or liste[index] == '/' or liste[index] == '*'):
                liste_finale.extend(liste[index:index + 2])
                del liste[index:index + 2]
            if index - 2 >= 0 and liste[index - 1] == '*':
                liste_finale.extend[index-2:index]
            continue
        if inconnu == liste[index]:
            degree, nbr, liste, coeff, index = elements_polynome(liste, index)
            if degree in dic.keys():
                dic[degree] += coeff * nbr
            else:
                dic[degree] = coeff * nbr
        else:
            index += 1
    dic[0] += degree_null(liste, inconnu)
    return trouver_polynome_final(dic, inconnu, liste_finale)

def integrer_2_polynomes(liste1, liste2):

    liste_finale = list(liste1)
    if calculs.nombre(liste1[0]) > 0:
        liste_finale.append('-')
    for element in liste2:
        if element == '+':
            liste_finale.append('-')
        elif element == '-':
            liste_finale.append('+')
        else:
            liste_finale.append(element)
    return liste_finale

def developper_puissance(liste, inconnu, puissance, nbr):

    carc = '+'
    coeff = 1
    if nbr < 0:
        carc, coeff = '-', -1
    index, liste_finale = 0, []
    while index < len(liste):
        if liste[index] == inconnu:
            liste_finale.extend([liste[index], '^'])
            liste_finale.append(str(calculs.nombre(liste[index + 2])*2))
            index += 2
        elif liste[index] in '+-':
            if carc == liste[index]:
                liste_finale.append('+')
            else:
                liste_finale.append('-')
        elif liste[index] == '*':
           liste_finale.append('*')
        else:
            liste_finale.append(str(calculs.nombre(liste[index])**puissance * coeff * nbr))
        index += 1
    tmp, index = 2, 0
    if puissance == 2:
        while index < len(liste):
            if liste[index] == '-':
                if carc == liste[index]:
                    carc = '+'
                else:
                    carc = '-'
            elif liste[index] == inconnu:
                index += 2
            elif liste[index] in '*+':
                pass
            else:
                tmp *= calculs.nombre(liste[index])
            index += 1
        if tmp < 0 and carc == '-':
            coeff, carac = -1, '+'
        liste_finale.extend([carc, str(coeff * tmp), inconnu, '^', '1'])
        if calculs.nombre(liste_finale[0]) < 0:
            liste_finale = ['-'] + liste_finale
        else:
            liste_finale = ['+'] + liste_finale
    return liste_finale