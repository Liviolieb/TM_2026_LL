import joueurs
import cartes
import table
import afficher
import random
class partie :
    
    def __init__(self,L_joueurs):
        self.pack = cartes.Cartes.creer_pack()
        self.L_joueurs = L_joueurs
        self.L_gagnants= []
        for joueur in L_joueurs:
            joueur.mise=0
            if joueur.solde <=0:
                joueur.couche = True
                joueur.cartes=[]
                continue
            joueur.couche=False
            joueur.allin=False
            cartes_x= random.sample(self.pack, 2)
            for carte in cartes_x:
                self.pack.remove(carte)
            joueur.cartes = cartes_x
        self.flop_partie= random.sample(self.pack, 3)
        for carte in self.flop_partie:
                self.pack.remove(carte)
        self.turn_partie= random.sample(self.pack, 1)
        for carte in self.turn_partie:
                self.pack.remove(carte)
        self.river_partie= random.sample(self.pack, 1)
        for carte in self.river_partie:
                self.pack.remove(carte)
        self.L_actifs =[j for j in self.L_joueurs if not j.couche]
        self.table_partie = table.Table(self.flop_partie,self.turn_partie,self.river_partie)
    async def vote (self):
        index_vote =0
        nouveau_vote = False
        joueur_aug=0
        
        while True:
            L_votants = [j for j in self.L_joueurs if not j.couche and not j.allin]
            if len(L_votants) < 1 :
                return()
            joueur = self.L_joueurs[index_vote]

            vote_juste = False
            if joueur.couche is False and joueur.allin is False:
                vote_x = await afficher.afficher_vote(0,joueur)
                for vote in joueurs.Joueurs.Vote :
                    if vote_x == vote :
                        joueur.vote = vote_x
                        vote_juste = True
                        break
                if vote_juste == True:
                    if vote == joueurs.Joueurs.Vote[1]:
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0:
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.main_pot += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise
                        else:
                            self.table_partie.main_pot += joueur.solde
                            joueur.mise += joueur.solde
                            joueur.solde =0
                        index_vote+=1
                        joueur.zone_jeu.refresh(5)
                    if vote == joueurs.Joueurs.Vote[0]:
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0:
                            if index_vote != 0:
                                nouveau_vote =True
                                joueur_aug = index_vote
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.main_pot += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise

                            while True:
                                x = await afficher.afficher_vote(1,joueur)
                                if x <= joueur.solde :
                                    joueur.solde -= x
                                    self.table_partie.mise += x
                                    joueur.mise +=x
                                    self.table_partie.main_pot += x
                                    break
                                else:
                                    await afficher.afficher_vote(2,joueur)
                        else:
                            self.table_partie.main_pot += joueur.solde
                            joueur.mise += joueur.solde
                            joueur.solde =0
                            await afficher.afficher_vote(4,joueur)
                        index_vote+=1
                        joueur.zone_jeu.refresh(5)

                    if vote == joueurs.Joueurs.Vote[3]:
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0:
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.main_pot += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise
                            if index_vote != 0:
                                nouveau_vote =True
                                joueur_aug = index_vote
                            self.table_partie.main_pot += joueur.solde
                            joueur.mise += joueur.solde
                            self.table_partie.mise= joueur.mise
                            joueur.solde =0
                            index_vote+=1
                            joueur.zone_jeu.refresh(5)
                        else:
                            self.table_partie.main_pot += joueur.solde
                            joueur.mise += joueur.solde
                            joueur.solde =0
                            index_vote+=1
                            joueur.zone_jeu.refresh(5)
    
                        
                    if vote == joueurs.Joueurs.Vote[2]:
                        joueur.couche =True
                        index_vote+=1
                        joueur.zone_jeu.refresh(5)
                else :
                    await afficher.afficher_vote(3,joueur)
                if joueur.solde == 0: 
                    joueur.allin=True
                
            else:
                index_vote +=1
                joueur.zone_jeu.refresh(5)

            for joueurr in self.L_joueurs:
                joueurr.zone_entete.refresh()
            
            if nouveau_vote is True and joueur_aug == index_vote :
                    index_vote=0
                    nouveau_vote = False
                    joueur_aug=0
                    break
            if index_vote == len(self.L_joueurs):
                if nouveau_vote is True:
                    index_vote =0
                else:
                    index_vote=0
                    nouveau_vote = False
                    joueur_aug=0
                    break
        
    def def_gagnant (self,joueurs=None) :
        self.L_actifs =joueurs if joueurs is not None else [j for j in self.L_joueurs if not j.couche]
        joueur_gagnant = None
        if len(self.L_actifs)==1:
            joueur_gagnant=self.L_actifs[0]
            return([joueur_gagnant])
        for i in range(len(self.L_actifs)) :
            for j in range(len(self.L_actifs)) :
                if self.L_actifs[i].combo >= self.L_actifs[j].combo :
                    temp = self.L_actifs[i]
                    self.L_actifs[i]=self.L_actifs[j]
                    self.L_actifs[j]= temp
        index=1
        while self.L_actifs[index-1].combo == self.L_actifs[index].combo :
            index+=1
            if index==len(self.L_actifs):
                 break
        if index ==1:
            joueur_gagnant = self.L_actifs[0]
            return([joueur_gagnant])
        else :
            L_joueurs_gagnants = []
            joueurs_gagnants=[]
            combo_p=[]
            for i in range (index) :
                joueur =self.L_actifs[i]
                joueur.cle_gagnant = []
                L_joueurs_gagnants.append(joueur)
                for i in range(len(joueur.cartes_combo)):
                    carte = joueur.cartes_combo[i]
                    if (joueur.combo == 4 or joueur.combo == 8) and (i ==0) and (carte.valeur==13) :
                        joueur.cle_gagnant.append(0)
                    else:
                        joueur.cle_gagnant.append(carte.valeur)
                if joueur.cle_gagnant > combo_p:
                    joueurs_gagnants=[joueur]
                    combo_p=joueur.cle_gagnant
                elif joueur.cle_gagnant == combo_p:
                    joueurs_gagnants.append(joueur)
            

            index= len(joueurs_gagnants)
            if index>1:
                combo_p=[]
                joueurs_gagnants_apres_kick=[]
                for joueur in joueurs_gagnants:
                    for carte in joueur.cartes_kicker:
                        joueur.cle_gagnant.append(carte.valeur)
                    if joueur.cle_gagnant > combo_p:
                        joueurs_gagnants_apres_kick=[joueur]
                        combo_p=joueur.cle_gagnant
                    elif joueur.cle_gagnant == combo_p:
                        joueurs_gagnants_apres_kick.append(joueur)
                if joueurs_gagnants_apres_kick:
                    joueurs_gagnants=joueurs_gagnants_apres_kick
            
        return (joueurs_gagnants)
    
    def atribution_pots(self,joueur):
        if joueur.allin is False:
            joueur.solde += self.table_partie.main_pot
            return(self.table_partie.main_pot)
        else :
            pot_j=0
            for j in self.L_joueurs :
                if joueur.mise >= j.mise:
                    pot_j+= j.mise
                    if j != joueur:
                        j.mise=0
                else:
                    j.mise -= joueur.mise
                    pot_j += joueur.mise
            joueur.mise=0
            joueur.solde += pot_j
            return(pot_j)


    def atribution_pots_execos_1(self):
        paliers = sorted(set(j.mise for j in self.L_joueurs if j.mise>0))
        gain=0
        palier_p=0
        palier=0
        gagnants=[]

        for palier in paliers:
            contributeurs=[j for j in self.L_joueurs if j.mise >= palier]
            joueurs_p=[j for j in contributeurs if j.couche is False]
            pot=(palier - palier_p)*len(contributeurs)
            if not joueurs_p:
                part_remb = pot / len(contributeurs)
                for c in contributeurs:
                    c.solde += part_remb
                gain += pot
                palier_p=palier
                continue
            gagnants_p = self.def_gagnant(joueurs_p)
            if gagnants_p:
                part = pot/len(gagnants_p)
                for gp in gagnants_p:
                    gp.solde += part
                gain+=pot
                for g in gagnants_p :
                    if g not in gagnants:
                        gagnants.append(g)
            elif len(joueurs_p)==1:
                joueurs_p[0].solde+= pot
                gain+= pot
            else:
                part_remb = pot / len(joueurs_p)
                for jp in joueurs_p:
                    jp.solde += part_remb
                gain += pot
            palier_p=palier
        for j in self.L_joueurs:
            j.mise =0
        for g in gagnants:
            g.couche=True
        return(gain)
        




        
