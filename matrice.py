# coding: utf-8

# fonction qui permet de verifier retourner une matrice sous forme de liste
def matrice_parsing(chaine):

    matrice = []
    liste = chaine.split(';')
    for element in liste:
        liste_temp = []
        element_tmp = element.split(',')
        liste_temp.append(int(element_tmp[0]))
        liste_temp.append(int(element_tmp[1]))
        matrice.append = liste_temp
    return matrice

# fonction qui permet de verifier que les dimensions de deux matrices sont egales
def compare_dimensions(M1, M2):

    n = len(M1) # recuperer le nombre des lignes de la matrice M1
    m = len(M1[0]) # recuperer le nombre des colonnes de la matrice M1
    try:
        assert n == len(M2)
        assert m == len(M2[0])
    except:
        print("Erreur : Matrice dimensions")
    else:
        return n, m

# fonction qui permet de verifier que les dimensions de deux matrices sont inversees
def dimensions_multiplication(M1, M2):

    m = len(M1[0]) # recuperer le nombre des colonnes de la matrice M1
    try:
        assert m == len(M2)
    except:
        print("Erreur Matrice dimensions : Multiplication of the 2 Matrices is impossible")
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
def somme_matrice(M1, M2):

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

    n = len(M) # nombre de lignes de la matrice
    m = len(M[0]) # le nombre de colonnes de la matrice
    for i in range(n):
        for j in range(m):
            M[i][j] *= reel
    return M

# fonction qui permet de extraire d'une matrice d'une autre
def extraire_matrice(M, ligne, colonne):

    n = len(M) - 1
    M1 =[[0 for j in range(n)] for i in range(n)]#creer une matrice nxn pleine de zéro
    for i in range(n):
        k = i
        if i == ligne:
            k = i + 1
        for j in range(n):
            e = j
            if i == colonne:
                e = j + 1
            M1[i][j] = M[k][e]
    return M1


# fonction qui permet de determiner le determinant de la matrice
def determinant_matrice_2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

# fonction qui permet de determiner le determinant de la matrice
def determinant_matrice(M):

    n = matrice_carree(M)
    if n == 2:
        return determinant_matrice_2(M)
    det = 0
    coeff = 1
    for i in range(n):
        M1 = extraire_matrice(M, i)
        det += coeff * M[0][i] * determinant_matrice(extraire_matrice(M1, i, 0))
        coeff *= -1
    return det

# fonction qui permet de determiner la comatrice
def comatrice(M):
    n = len(M)
    m = len(M[0])
    comM =[[0 for j in range(n)] for i in range(m)]#creer une matrice nxn pleine de zéro
    for i in range(n):
        for j in range(m):
            comM[i][j] = -1 ** (i + j) * determinant_matrice(extraire_matrice(M, i, j))
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
    try:
        det = determinant_matrice(M)
        M = multiplication_matrice_reel(transpose(comatrice(M)), 1 / det)
    except:
        print("Error : Matrix non inversible")
    else:
        return M

# afficher la matrice sur la sortie standard
def affiche_matrice(self, liste):
    chaine = ''
    for element in liste:
        chaine = '[ '
        for key, e in enumerate(element):
            chaine += e + ' '
            if key != len(element) - 1:
                chaine += ', '
        chaine += ']\n'
        print(chaine)

def traiter_matrice(liste):
    # effectuer les calculs sur les matrices

    return '0'