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
        index_vote=0
        index_side=-1
        joueur_aug=0
        tapis=False
        mise_tapis=0
        while True:
            joueur = self.L_joueurs[index_vote]
            if len(self.L_joueurs)>1 :
                if index_vote ==0:
                    nouveau_vote =False
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
                        if index_vote != 0:
                            nouveau_vote =True
                            joueur_aug = index_vote
                        while True:
                            x = afficher.afficher_vote(1,joueur,self.table_partie.mise)
                            if x < joueur.solde :
                                joueur.solde -= (self.table_partie.mise - joueur.mise)+x
                                self.table_partie.main_pot += (self.table_partie.mise - joueur.mise)+x
                                joueur.mise =x + self.table_partie.mise
                                self.table_partie.mise+=x
                                break
                            if joueur.mise < self.table_partie.mise:
                                    afficher.afficher_vote(2,joueur,self.table_partie.mise)
                            else : 
                                afficher.afficher_vote(3,joueur,self.table_partie.mise)
                                break
                    if vote == joueurs.Joueurs.Vote[3]:
                        if index_vote != 0:
                            nouveau_vote =True
                            joueur_aug = index_vote
                        self.table_partie.main_pot += (self.table_partie.mise - joueur.mise)+joueur.solde
                        joueur.mise = joueur.solde + self.table_partie.mise
                        self.table_partie.mise+=joueur.solde
                        joueur.solde =0

                    if vote == joueurs.Joueurs.Vote[1]:
                        if joueur.solde - self.table_partie.mise-joueur.mise >= 0:
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            if tapis is False:
                                self.table_partie.main_pot += self.table_partie.mise-joueur.mise
                            else:
                                self.table_partie.main_pot += mise_tapis-joueur.mise
                                self.table_partie.side_pot[index_side] += self.table_partie.mise-mise_tapis
                            joueur.mise = self.table_partie.mise
                        else:
                            self.table_partie.main_pot += (self.table_partie.mise - joueur.mise)+joueur.solde
                            joueur.mise = joueur.solde + self.table_partie.mise
                            self.table_partie.mise+=joueur.solde
                            joueur.solde =0
                    if vote == joueurs.Joueurs.Vote[2]:
                        joueur.joue =False
                        self.L_joueurs.remove(joueur)
                        index_vote-=1
                else :
                    afficher.afficher_vote(4,joueur,self.table_partie.mise)
                if joueur.solde == 0:
                    tapis=True
                    index_side+=1
                    mise_tapis=joueur.mise
                    joueur.joue=False
                if index_vote == len(self.L_joueurs):
                    if nouveau_vote is True:
                        index_vote=0
                        nouveau_vote = False
                    else:
                        break
                if nouveau_vote is False and joueur_aug-1 == index_vote :
                    break
            else:
                index_vote += 1
                if index_vote == len(self.L_joueurs):
                    break
        
    def def_gagnant (self) :
        joueur_gagnant = None
        if len(self.L_joueurs)==1:
            joueur_gagnant=self.L_joueurs[0]
            return(joueur_gagnant)
        for i in range(len(self.L_joueurs)) :
            for j in range(len(self.L_joueurs)) :
                if self.L_joueurs[i].combo >= self.L_joueurs[j].combo :
                    temp = self.L_joueurs[i]
                    self.L_joueurs[i]=self.L_joueurs[j]
                    self.L_joueurs[j]= temp
        index=1
        while self.L_joueurs[index-1].combo == self.L_joueurs[index].combo :
            index+=1
            if index==len(self.L_joueurs):
                 break
        if index ==1:
            joueur_gagnant = self.L_joueurs[0]
        else :
            points_gagnant=0
            L_joueurs_gagnants = []
            for i in range (index) :
                 L_joueurs_gagnants.append(self.L_joueurs[i])
            for joueur in L_joueurs_gagnants:
                for carte in joueur.cartes_jouee:
                    joueur.points+=carte.valeur
                if joueur.points>points_gagnant:
                    points_gagnant=joueur.points
                    joueur_gagnant= joueur
        return (joueur_gagnant)
    def atribution_pots(self,joueur_gagnant):
        joueur_gagnant.solde += self.table_partie.main_pot
        if self.table_partie.side_pot > 0:
            pass
            
