import random
class cartes :
    Couleurs = ["pique","trefle","carreau","coeur"]
    Valeurs = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    def __init__ (self):
        couleur = self.couleur
        valeur = self.valeur
    def creer_pack ():
        L=[]
        for i in range (13):
            for j in range (4):
                x = cartes(x)
                x.couleur = cartes.Couleurs[j]
                x.valeur = cartes.Valeurs[i]
                L.append(x)
