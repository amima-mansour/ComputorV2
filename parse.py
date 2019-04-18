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
            print("la liste droite = {}\nla liste gauche = {}".format(liste_droite, liste_gauche))
            if re.match(r'( )?\?( )?', liste_droite):
                liste_droite = liste_gauche
                liste_gauche = '?'
            # traiter la partie gauche
            self.var = outils.traitement_nom_de_variable(liste_gauche)
            # traiter la partie droite
            self.liste, self.tmp_inconnus = outils.test_partie_calculatoire(liste_droite, self.var)
            print('variables inconnues transmises = {}'.format(self.tmp_inconnus))

    def remplacer(self, tmp_var, tmp_fonction):
    # chercher les variables inconnues et les remplacer par leur valeurs

        inconnu = '0'
        if len(self.var) == 2:
            inconnu = self.var[1]
        for key, element in self.tmp_inconnus.items():
            if isinstance(element, list):
                valeur = element[1]
                fonction = element[0]
                if ((element[1] not in tmp_var.keys() and not re.match(r'^[0-9]+(\.[0-9]+)?$', element[1])) \
                    or (element[0] not in tmp_fonction.keys())):
                    print("Error : variable not defined")
                    return -1
                self.tmp_inconnus[key] = polynome.calcul(tmp_fonction[fonction], valeur)
            elif element in tmp_var.keys():
                liste = self.liste[:key]
                liste += tmp_var[element].split()
                liste += self.liste[key + 1:]
                self.liste = liste
            elif element == inconnu:
                pass
            else:
                print("Error : variable not defined 1")
                return -1
        return 0