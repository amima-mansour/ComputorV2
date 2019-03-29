# coding: utf-8

def polynome_test(chaine):
    # Cette fonction de tester si la chaine est un polynome.

    motif_1 = r"^( )?(-)?([0-9]*)(\.[0-9]+)?( \* )?(X\^([0-9])([0-9]*)|X|)(( - | \+ )([0-9]*)(\.[0-9]+)?( \* )?(X\^([0-9])([0-9]*)|X|))*( )?$"
    for element in chaine:
        if re.match(motif_1, element):
            continue
        else:
            print("Please enter a valid equation !")
            exit()