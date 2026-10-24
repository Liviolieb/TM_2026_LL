import asyncio
class Joueurs :
    Vote =["aug","suivre","coucher","tapis"]
    Vote_libelles ={"aug":"Relancer","suivre":"Suivre","coucher":"Coucher","tapis":"Tapis"} # en joli pour le toggle
    couleurs_vote = {"aug": "red","suivre": "blue","coucher": "grey-7","tapis": "deep-purple",}
    def __init__ (self, nom, solde): # ce sont les deux seules variables qui sont définies et modifiées depuis le constructeur
        self.nom = nom
        self.solde=solde
        self.cartes = None
        self.vote =None
        self.role = None
        self.mise= 0
        self.hand = None
        self.combo = 0
        self.couche = False
        self.cartes_combo = []
        self.cartes_kicker = []
        self.cartes_jouee=self.cartes_kicker+self.cartes_combo
        self.allin = False
        self.points= 0
        self.pret = asyncio.Event()
        self.zone_table=None
        self.zone_infos = None
        self.zone_jeu = None
        self.reponse_vote = None
        self.a_vote = asyncio.Event()
        self.mise_v=None
        self.cle_gagnant=[]
        self.temps=0
        self.en_vote =False
    def __str__ (self): # surcharge pour d'anciens tests (version textuelle)
        return self.nom