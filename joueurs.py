class Joueurs :
    Vote =["aug","suvre","coucher","tapis"]
    def __init__ (self, nom, solde, cartes=None, vote=None, role=None, mise=None):
        self.Nom = Nom
        self.sold=solde
        self.cartes = cartes
        self.vote =vote
        self.role = role
        self.mise= mise
    def __str__ (self):
        return f"le joueur {self.Nom}"
    