import random
class Cartes :
    Couleurs = ["pique","trefle","carreau","coeur"]
    Valeurs = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    def __init__ (self,couleur=None,valeur=None):
        self.couleur = couleur
        self.valeur = valeur
    def __str__(self):
        return f"{self.valeur} de {self.couleur}"
    def creer_pack ():
        L=[]
        for i in range (13):
            for j in range (4):
                x = Cartes(x)
                x.couleur = Cartes.Couleurs[j]
                x.valeur = Cartes.Valeurs[i]
                L.append(x)
        return L