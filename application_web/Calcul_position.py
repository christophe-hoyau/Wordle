# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def get_where(cible):
    cible = cible.lower()
    lettre = []
    lettre_indice = []
    for k in range(len(cible)):
        if cible[k] in lettre:
            for L in lettre_indice:
                if L[0] == cible[k]:
                    L[1].append(k)
        else:
            lettre.append(cible[k])
            lettre_indice.append([cible[k], [k]])
    return lettre, lettre_indice


def valid_where(cible, essai):
    if len(essai) == len(cible):
        essai = essai.lower()
        lettre, lettre_indice = get_where(cible)
        valid = [0 for i in range(len(cible))]
        compteur = []
        for s in lettre:
            compteur.append([s, 0])

            #Diviser en deux boucles, la premiere vérifie si il y a des lettres bien placer
        for k in range(len(essai)):
            if essai[k] in lettre:
                for L in lettre_indice:
                    if L[0] == essai[k]:
                        if k in L[1]:
                            valid[k] = 2
                            for C in compteur:
                                if C[0] == essai[k]:
                                    C[1] += 1
        for i in range(len(essai)):
            if valid[i] == 0:
                if essai[i] in lettre:
                    for L in lettre_indice:
                        if L[0] == essai[i]:
                            for C in compteur:
                                if C[0] == essai[i]:
                                    if C[1] != len(L[1]):
                                        valid[i] = 1
                                        C[1] += 1
        return valid
    else:
        return("Le mot n'est pas de la bonne longueur")
