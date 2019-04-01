# coding: utf-8
import re

# tester si le nom de la variable est different de i 
def test_complexe(chaine):

    try:
        assert chaine != 'i'
    except:
        print("Error : i can not be the name of a variable")

# tester si le nom de la fonction est correcte 
def test_fonction(chaine):

    motif = r'[a-zA-Z]+\(([a-zA-Z]+\([a-zA-Z]\)|[a-zA-Z])\)'
    try:
        assert re.match(motif, chaine)
        index = chaine.index('(')
        nom_fonction = ''.join(chaine[:index])
        nom_composition = []
        nouvelle_chaine = chaine[index + 1:]
        if '(' in nouvelle_chaine:
            index = nouvelle_chaine.index('(')
            nom_composition = nouvelle_chaine[:index]
            index += 1
            inconnu = nouvelle_chaine[index:index + 1]
        else:
            inconnu = nouvelle_chaine[0:1]
        if not(nom_composition):
            nom_composition = ''
        else:
            nom_composition = ''.join(nom_composition)
        return nom_fonction, nom_composition, inconnu
    except:
        print("Error : it should be like 'f(x)' or 'f(g(x))'")
        return "", "", ""

# tester si le nom de la variable est correcte 
def test_variable(chaine):

    motif = r'[a-zA-Z]+'
    try:
        assert re.match(motif, chaine)
    except:
        print("Error : variable name is wrong it must be like asd or asD or ASD")