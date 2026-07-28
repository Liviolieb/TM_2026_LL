class Joueurs :
    Vote =["aug","suivre","coucher","tapis"]
    def __init__ (self, nom, solde, cartes=None, vote=None, role=None, mise=0, cartes_jouables=None, cartes_jouee=None, combo =None,couche=False,allin=False, points=0):
        self.nom = nom
        self.solde=solde
        self.cartes = cartes
        self.vote =vote
        self.role = role
        self.mise= mise
        self.cartes_jouables = cartes_jouables
        self.combo = combo
        self.couche = couche
        self.cartes_jouee = cartes_jouee
        self.allin = allin
        self.points= points
    def __str__ (self):
        return self.nom