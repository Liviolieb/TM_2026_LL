import joueurs
import cartes
import hand
import table
import random
class partie :
    pack = cartes.Cartes.creer_pack()
    def __init__(self,L_joueurs):
        self.L_joueurs = L_joueurs
        for joueur in L_joueurs:
            cartes_x= random.sample(partie.pack, 2)
            for carte in cartes_x:
                partie.pack.remove(carte)
            joueur.cartes = cartes_x
        self.flop_partie= random.sample(partie.pack, 3)
        for carte in self.flop_partie:
                partie.pack.remove(carte)
        self.turn_partie= random.sample(partie.pack, 1)
        for carte in self.turn_partie:
                partie.pack.remove(carte)
        self.river_partie= random.sample(partie.pack, 1)
        for carte in self.river_partie:
                partie.pack.remove(carte)
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
    def afficher_cartes_table(self):
        for i in range (self.table_partie.etape):
            for j in range (len(self.table_partie.liste[i])):
                print (self.table_partie.liste[i][j])
    def afficher_cartes(self):
        self.afficher_cartes_table(self.table_partie.etape)
        for i in range (len(self.L_joueurs)):
            for j in range (2) :
                print (self.L_joueurs[i].cartes[j])
