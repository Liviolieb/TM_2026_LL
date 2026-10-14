import asyncio
class Joueurs :
    Vote =["aug","suivre","coucher","tapis"]
    def __init__ (self, nom, solde, cartes=None, vote=None, role=None, mise=0, cartes_jouables=None, combo =0,couche=False,allin=False, points=0, jape=None,zone_entete = None,zone_jeu = None,reponse_vote = None,mise_v=None):
        self.nom = nom
        self.solde=solde
        self.cartes = cartes
        self.vote =vote
        self.role = role
        self.mise= mise
        self.cartes_jouables = cartes_jouables
        self.combo = combo
        self.couche = couche
        self.compte = False
        self.cartes_combo = []
        self.cartes_kicker = []
        self.cartes_jouee=self.cartes_kicker+self.cartes_combo
        self.allin = allin
        self.points= points
        self.jape= jape
        self.pret = asyncio.Event()
        self.zone_entete = zone_entete
        self.zone_jeu = zone_jeu
        self.reponse_vote = reponse_vote
        self.a_vote = asyncio.Event()
        self.mise_v=mise_v
        self.cle_gagnant=[]
        self.temps=0
        self.label_temps=""
    def __str__ (self):
        return self.nom