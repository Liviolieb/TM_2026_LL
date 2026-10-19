class Cartes :
    Couleurs = ["pique","trefle","carreau","coeur"]
    Valeurs = [1,2,3,4,5,6,7,8,9,10,11,12,13] #noter que 1 est la carte “2“ et 13 est l'“as“
    def __init__ (self,couleur=None,valeur=0):
        self.couleur = couleur
        self.valeur = valeur
    def __str__(self): # surcharge concernant des ancien test (version textuelle)
        return f"{self.valeur} de {self.couleur}"
    @staticmethod # la methode ne s'applique pas à un objet Cartes
    def creer_pack (): # un pack a toute les combinaison possible de couleur et valeur (13*4=52)
        L=[]
        for valeur in Cartes.Valeurs: 
            for couleur in  Cartes.Couleurs:
                x = Cartes()
                x.couleur = couleur
                x.valeur = valeur
                L.append(x)
        return (L)