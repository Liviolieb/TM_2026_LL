import joueurs
import cartes
import hand
import table
import random
class partie :
    pack = cartes.creer_pack()
    def __init__(self,L_joueurs):
        self.L_joueurs = L_joueurs
        for joueur in L_joueurs:
            cartes_x= random.choice(partie.pack, k=2)
            partie.pack -= cartes_x
            joueur.cartes = cartes_x
        self.flop_partie= random.choice(partie.pack, k=3)
        partie.pack -= self.flop_partie
        self.turn_partie= random.choice(partie.pack, k=1)
        partie.pack -= self.turn_partie
        self.river_partie= random.choice(partie.pack, k=1)
        partie.pack -= self.river_partie
        self.table_partie = table.Table(self.flop_partie,self.turn_partie,self.river_partie)
    def vote(self):
        index_vote=0
        while True:
            joueur = self.L_joueurs[index_vote]
            print(f"{joueur}, que voulez vous faire")
            print(joueurs.Joueurs.Vote)
            vote_x = input(":")
            vote_juste = False
            for vote in joueurs.Joueurs.Vote :
                if vote_x == vote :
                    joueur.vote = vote_x
                    vote_juste = True
                    index_vote += 1
                    break
            if vote_juste == True:
                break
            else :
                print("pas un vote autorisé")
    def afficher_carte_table(self):
        for i in range (self.table_partie.etape):
            for j in range (len(self.table_partie.liste[i])):
                print (self.table_partie.Liste[i][j])
    def afficher_cartes(self):
        self.afficher_carte_table(self.table_partie.etape)
        for i in range (len(self.L_joueurs)):
            for j in range (2) :
                print (self.L_joueurs[i].cartes[j])
    