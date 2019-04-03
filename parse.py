# coding: utf-8

import re
import parsingOutils as outils
import fonctionPolynomiale as polynome

class Parsing:
    """ Parser la chaine.
    1- verifier l'existence d'un seul = dans la chaine
    2- spliter la chaine en deux parties : droite et gauche
    3- Si la partie droite est '?', il s'agit d'evaluer la partie gauche
    4- Sinon la partie gauche est le nom de variable à stocker dans un dictionnaire avec la valeur."""

    def __init__(self, chaine):
        
        liste_gauche, liste_droite = outils.equal_number(chaine)
        # permutation des parties gauche et droite dans le cas ou la partie droite = '?'
        if liste_droite and liste_gauche:
            liste_droite = liste_droite.strip()
            liste_gauche = liste_gauche.strip()
            if re.match(r'( )?\?( )?', liste_droite):
                liste_droite = liste_gauche
                liste_gauche = ['?']
            # traiter la partie gauche
            self.var = outils.traitement_nom_de_variable(liste_gauche)
            print(self.var)
            # traiter la partie droite
            self.liste, self.tmp = outils.test_partie_calculatoire(liste_droite)

    @property
	def var(self):
		return self.var
    
    def remplacer(self, tmp_var, tmp_fonction):

        for key, element in enumerate(self.tmp):
            if isinstance(element, list):
                valeur = element[1]
                fonction = element[0]
                if valeur not in tmp_var.keys() and not re.match(r'^[0-9]+(\.[0-9]+)?$'):
                   print("Error : variable not defined")
                    return -1
                if fonction not in tmp_fonction.keys():
                   print("Error : variable not defined")
                    return -1
                tmp = polynome.calcul(tmp_fonction[fonction], valeur)
                self.tmp[key] = tmp
            elif element not in tmp.values():
                print("Error : variable not defined")
                return -1
            else:
                self.tmp[key] = tmp[element]
        return 0
    
    # afficher le polynome sur la sortie standard
    def affiche_polynome(self, inconnu, variable, liste):

        degree = inconnu + '^0'
        i = 0
        chaine = variable + '(' + inconnu + ') = '
        while len(liste) > 0:
            # on suppose ici que les puissances sont sous la forme de X^n
            while degree not in liste:
                i += 1
                chaine += '0 * ' + degree
                degree = inconnu + '^' + str(i)
            while degree in liste:
                i += 1
                index = liste.index(degree)
                # * se trouve avant le degree
                # * se trouve apres le degree
                # * absente regarder le signe de l'index precedent : - ou + ou rien : debut d'expression
        print(chaine)

    # afficher la matrice sur la sortie standard
    def affiche_matrice(self, liste):

    