# coding: utf-8

def reduced_form(chaine):
    # Cette fonction determine la forme reduite de l'equation.
    
    equality = chaine.split('=')
    left = equality[0].split()
    right = equality[1].split()
    coeff_gauche = identifier_coefficients(left)
    coeff_droite = identifier_coefficients(right)
    coeff_final = {}
    for element in coeff_gauche:
        if element in coeff_droite.keys():
            coeff_final[element] = coeff_gauche[element] - coeff_droite[element]
            coeff_droite[element] = 0
        else:
            coeff_final[element] = coeff_gauche[element]
    for element in coeff_droite:
        if coeff_droite[element]:
            coeff_final[element] = -1 * coeff_droite[element]
    coeff_final_copy = coeff_final.copy()
    degree, chaine = reduced_string(coeff_final_copy)
    if degree > 0:
        chaine = chaine[3:]
    return chaine, degree, coeff_final

def racine_carre(nombre):
    # Cette fonction calcule la racine carree d'un nombre 

    i = 0.000001
    while i * i < nombre:
        resultat = i 
        i += 0.000001
    return resultat

def solutions(a, b, c):
    # Cette fonction trouve les solutions d'une equation de second degree.

    discriminant = b * b - 4 * a * c
    if discriminant == 0:
        solution = -1 * b / (2 * a)
        if type(solution) == float:
            solution = round(solution, 6)
        print ("Discriminant is null, the solution is:\n{}".format(solution))
    elif discriminant > 0:
        racine = racine_carre(discriminant)
        solution_1 = (-1 * b + racine) / (2  * a)
        solution_2 = (-1 * b - racine) / (2  * a)
        if type(solution_1) == float:
            solution_1 = round(solution_1, 6)
        if type(solution_2) == float:
            solution_2 = round(solution_2, 6)
        print("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(solution_2, solution_1))
    else:
        racine = racine_carre(-1 * discriminant)
        premiere_partie = -1 * b / (2 * a)
        seconde_partie =  racine / (2  * a)
        if type(premiere_partie) == float:
            premiere_partie = round(premiere_partie, 6)
        if type(seconde_partie) == float:
            seconde_partie = round(seconde_partie, 6)
        print("Discriminant is strictly negative, the two solutions are:\n{} - i * {}\n{} + i * {}".format(premiere_partie,
            seconde_partie, premiere_partie, seconde_partie))
