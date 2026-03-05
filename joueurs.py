class Joueurs :
    Vote =["aug","suivre","coucher","tapis"]
    def __init__ (self, nom, solde, cartes=None, vote=None, role=None, mise=None, cartes_jouables=None):
        self.nom = nom
        self.sold=solde
        self.cartes = cartes
        self.vote =vote
        self.role = role
        self.mise= mise
        self.cartes_jouables = cartes_jouables
    def __str__ (self):
        return self.nom
    def afficher_cartes(self):
        print (self.nom,"a :")
        for carte in self.cartes:
            print (carte)