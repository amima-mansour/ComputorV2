# coding: utf-8

import calculs
import re

# fonction qui permet de verifier retourner une matrice sous forme de liste
def matrice_parsing(chaine):

    matrice = []
    liste = chaine.split(';')
    if len(liste) >= 2 and not liste[1]:
        print("Error Matrix")
        return matrice
    for element in liste:
        element = element[1:len(element) - 1]
        liste_tmp = []
        element_tmp = element.split(',')
        for el in element_tmp:
            if re.match(r'^[0-9]+([0-9]+\.)?$', el):
                liste_tmp.append(calculs.nombre(el))
            else:
                print("Error Matrix")
                return []
        matrice.append(liste_tmp)
    return matrice

# fonction qui permet de verifier que les dimensions de deux matrices sont egales
def compare_dimensions(M1, M2):

    n = len(M1) # recuperer le nombre des lignes de la matrice M1
    m = len(M1[0]) # recuperer le nombre des colonnes de la matrice M1
    try:
        assert n == len(M2)
        assert m == len(M2[0])
    except:
        print("Erreur : Matrix dimensions")
    else:
        return n, m

# fonction qui permet de verifier que les dimensions de deux matrices sont inversees
def dimensions_multiplication(M1, M2):

    m = len(M1[0]) # recuperer le nombre des colonnes de la matrice M1
    try:
        assert m == len(M2)
    except:
        print("Erreur Matrice dimensions : Multiplication des 2 Matrices impossible")
    else:
        return m

# fonction qui permet de verifier que si une matrice est carree
def matrice_carree(M):

    m = len(M) # recuperer le nombre de lignes de la matrice
    try:
        assert m == len(M[0])
    except:
        print("Erreur Matrice dimensions : Matrice non carree")
    else:
        return m


# fonction qui permet de faire la somme de deux matrices
def addition_matrice(M1, M2):

    n, m = compare_dimensions(M1, M2)
    M = [[0 for j in range(m)] for i in range(n)]# creer une matrice nxm pleine de zéro

    for i in range(n):
        for j in range(m):
            M[i][j] = M1[i][j]+M2[i][j]

    return M

# fonction qui permet de faire la soustraction de deux matrices
def soustraction_matrice(M1, M2):

    n, m = compare_dimensions(M1, M2)
    M=[[0 for j in range(m)] for i in range(n)]#creer une matrice nxm pleine de zéro
    for i in range(n):
        for j in range(m):
            M[i][j] = M1[i][j]- M2[i][j]
    return M

# fonction qui permet de faire la multiplication de deux matrices
def multiplication_matrice(M1, M2):

    m = dimensions_multiplication(M1, M2)
    n1 = len(M1) # nombre de lignes de la matrice produit
    m1 = len(M2[0]) # le nombre de colonnes de la matrice produit
    M =[[0 for j in range(m1)] for i in range(n1)]#creer une matrice nxn pleine de zéro
    for i in range(n1):
        for j in range(m1):
            for k in range(m):
                M[i][j] += M1[i][k] * M2[k][j]
    return M

# fonction qui permet de faire la multiplication d'une matrice par un reel
def multiplication_matrice_reel(M, reel):

    print("la matrice M = {} le reel = {}".format(M, reel))
    n = len(M) # nombre de lignes de la matrice
    m = len(M[0]) # le nombre de colonnes de la matrice
    for i in range(n):
        for j in range(m):
            M[i][j] = reel *  M[i][j]
    return M

# fonction qui permet de extraire d'une matrice d'une autre
def extraire_matrice(M, ligne, colonne):

    n = len(M) - 1
    M1 =[[0 for j in range(n)] for i in range(n)]#creer une matrice nxn pleine de zéro
    k = 0
    for i in range(n + 1):
        if i != ligne: 
            l = 0
            for j in range(n + 1):
                if j != colonne:
                    M1[k][l] = M[i][j]
                    l += 1
            k += 1
    return M1


# fonction qui permet de determiner le determinant de la matrice
def determinant_matrice_2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

# fonction qui permet de determiner le determinant de la matrice
def determinant_matrice(M):

    n = matrice_carree(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return determinant_matrice_2(M)
    det = 0
    coeff = 1
    for i in range(n):
        det += coeff * M[i][0] * determinant_matrice(extraire_matrice(M, i, 0))
        coeff *= -1
    return det

# fonction qui permet de determiner la comatrice
def comatrice(M):

    n = len(M)
    m = len(M[0])
    comM =[[0 for j in range(n)] for i in range(m)]#creer une matrice nxn pleine de zéro
    for i in range(n):
        for j in range(m):
            coeff = (-1) ** (i + j)
            comM[i][j] = coeff * determinant_matrice(extraire_matrice(M, i, j))
    return comM

# fonction qui permet de determiner la transpose d'une matrice
def transpose(M):

    n = len(M)
    m = len(M[0])
    transM =[[0 for j in range(n)] for i in range(m)]#creer une matrice nxn pleine de zéro
    for i in range(m):
        for j in range(n):
            transM[i][j] = M[j][i]
    return transM

# fonction qui permet d'inverser une matrice
def inverser_matrice(M):

    det = determinant_matrice(M)
    if det != 0:
        M = multiplication_matrice_reel(transpose(comatrice(M)), 1 / det)
        return M
    else:
        print("Erreur : Matrice non inversibles")

# traiter la liste des matrices suivant les operations
def traiter(liste):

    if liste[0] == 'det(':
        return determinant_matrice(liste[1])
    if liste[0] == 'inv(':
        print("la liste et matrice = {}".format(liste[1]))
        return inverser_matrice(liste[1]) 
    if liste[0] == 'com(':
        return comatrice(liste[1])
    if liste[0] == 'trans(':
        return transpose(liste[1])
    mat = liste[0]
    i = 1
    while i < len(liste):
        if '+' in liste[i]:
            mat = addition_matrice(mat, liste[i + 1])
        elif '-' in liste[i]:
            mat = soustraction_matrice(mat, liste[i + 1])
        elif '*' in liste[i]:
            if isinstance(mat, list) and isinstance(liste[i + 1], list):
                mat = multiplication_matrice(mat, liste[i + 1])
            else:
                if isinstance(mat, list):
                    nbr = liste[i + 1]
                else:
                    nbr = mat
                    mat = liste[i + 1]
                mat = multiplication_matrice_reel(mat, calculs.nombre(nbr))
        else:
            pass
        i += 1
    return mat



# afficher la matrice sur la sortie standard
def affiche_matrice(liste):

    chaine = ''
    i = 1
    for element in liste:
        chaine += '[ '
        for key, e in enumerate(element):
            chaine += str(e) + ' '
            if key != len(element) - 1:
                chaine += ', '
        chaine += ']'
        if i != len(liste):
            chaine += '\n'
        i += 1
    print(chaine)