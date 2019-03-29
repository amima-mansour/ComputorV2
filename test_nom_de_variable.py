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

    motif = r'[a-zA-Z]+\(([a-zA-Z]+\([a-zA-Z]\)|[a-zA-Z]\)'
    try:
        assert re.match(motif, chaine)
        index = chaine.index('(')
        nom_fonction = chaine[:index - 1]
        nom_compoition = ''
        nouvelle_chaine = chaine[index + 1:]
        if '(' in nouvelle_chaine:
            index = nouvelle_chaine.index('(')
            nom_composition = nouvelle_chaine[:index - 1]
            inconnu = nouvelle_chaine[index + 1]
        else:
            inconnu = nouvelle_chaine[index + 1]
        return ''.join(nom_fonction), ''.join(name_compoition), inconnu
    except:
        print("Error : it should be like 'f(x)' or 'f(g(x))'")

# tester si le nom de la variable est correcte 
def test_variable(chaine):

    motif = r'[a-zA-Z]+'
    try:
        assert re.match(motif, chaine)
    except:
        print("Error : variable name is wrong it must be like asd or asD or ASD")