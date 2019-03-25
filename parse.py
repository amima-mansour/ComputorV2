# coding: utf-8

import re
import parsingTools as tools

class Parsing:
    """ Parser la chaine.
    1- verifier l'existence d'un seul = dans la chaine
    2- spliter la chaine en deux parties : droite et gauche
    3- Si la partie droite est '?', il s'agit d'evaluer la partie gauche
    4- Sinon la partie gauche est le nom de variable à stocker dans un dictionnaire avec la valeur."""

    def __init__(self, chaine):
        
        self.liste, self.msg_erreur = tools.equal_number(chaine)
        self.liste_finale = []
        self.var = ''
        # resolution
        if self.liste and re.match(r'( )?\?( )?', self.liste[1]):
            self.liste_finale = tools.premier_test(self.liste[0])
        # assignation
        elif self.liste and '?' not in self.liste[1]:
            self.liste_finale = tools.premier_test(self.liste[1])
            if not self.liste_finale:
                self.msg_erreur = "Error: ? is missing"
            else:
                self.var = self.liste[0].lower() 
        else:
            if self.msg_erreur == '':
                self.msg_erreur = "Error: ? is missing"
    
    def second_parsing(self):

        self.nbr = -1
        msg = ''
        if self.liste_finale:
            self.nbr, msg = tools.second_test(self.liste_finale)
        if self.var != '':
            m = re.match(r'^[a-z]+$', self.var)
            if not m:
                self.nbr = -1
                msg = self.msg_erreur = "Error: Not a valid variable name"
        if self.msg_erreur == '':
            self.msg_erreur = msg
        return self.nbr
    
    def affiche_erreur(self):

        print(self.msg_erreur)