import joueurs
import cartes
import hand
import table
import afficher
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
        self.table_partie.mise =0
        index_vote=0
        while True:
            joueur = self.L_joueurs[index_vote]
            vote_x = afficher.afficher_vote(0,joueur,self.table_partie.mise)
            vote_juste = False
            for vote in joueurs.Joueurs.Vote :
                if vote_x == vote :
                    joueur.vote = vote_x
                    vote_juste = True
                    index_vote += 1
                    break
            if vote_juste == True:
                if vote == joueurs.Joueurs.Vote[0]:
                     while True:
                        x = afficher.afficher_vote(1,joueur,self.table_partie.mise)
                        if x < joueur.solde :
                             joueur.mise =x
                        if joueur.mise >= self.table_partie.mise:
                            self.table_partie.mise=joueur.mise
                            break
                        if joueur.mise < self.table_partie.mise:
                                afficher.afficher_vote(2,joueur,self.table_partie.mise)
                        else : 
                            afficher.afficher_vote(3,joueur,self.table_partie.mise)
                            break
                if vote == joueurs.Joueurs.Vote[3]:
                     joueur.mise = joueur.solde
                if vote == joueurs.Joueurs.Vote[1]:
                     joueur.mise = self.table_partie.mise
                if vote == joueurs.Joueurs.Vote[2]:
                     self.L_joueurs.remove(joueur)
                     index_vote-=1
            else :
                afficher.afficher_vote(4,joueur,self.table_partie.mise)
            if index_vote == len(self.L_joueurs):
                 break
        
    def def_gagnant (self) :
        for i in range(len(self.L_joueurs)) :
            for j in range(len(self.L_joueurs)) :
                if self.L_joueurs[i].combo >= self.L_joueurs[j].combo :
                    temp = self.L_joueurs[i]
                    self.L_joueurs[i]=self.L_joueurs[j]
                    self.L_joueurs[j]= temp
        index=0
        while self.L_joueurs[index].combo == self.L_joueurs[index+1].combo :
             index+=1
        if index ==0:
             return (self.L_joueurs[0])
        else :
            L_joueurs_gagnants = []
            for i in range (index) :
                 L_joueurs_gagnants.append(self.L_joueurs[i])
            