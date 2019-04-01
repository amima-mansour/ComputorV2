# coding: utf-8

def puissance(a, b):
    
    if a == 0:
        return 0
    if b == 0:
        return 1
    return a * puissance(a, b - 1)