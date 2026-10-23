import joueurs
import cartes
import table
import afficher
import random
import asyncio
class partie :
    Grosse_blind= 20 # valeur de mise de la grosse blinde
    Petite_blind=10 # valeur de mise de la petite blinde
    def __init__(self,L_joueurs):
        self.pack = cartes.Cartes.creer_pack()
        self.L_joueurs = L_joueurs
        self.L_gagnants= []
        self.index=0
        self.lancee=None
        self.vues_tables=[]
        self.revel_c=False
                
        for joueur in L_joueurs:
            joueur.mise=0 # pour éventuellement faire des partie à plusieurs mains (plusieurs tours)
            if joueur.solde <=0: # si un joueur avait perdu tout ses sous automatiquement couché et sans cartes
                joueur.couche = True 
                joueur.cartes=[]
                continue
            joueur.couche=False
            joueur.allin=False
            cartes_x= random.sample(self.pack, 2) # on prend 2 cartes aléatoires dans le paquet qu'on attribue au joueur et ensuite on les retire du paquet
            for carte in cartes_x:
                self.pack.remove(carte)
            joueur.cartes = cartes_x 
            if cartes_x[0].valeur==cartes_x[1].valeur: #si le joueur reçoit une paire
                joueur.combo =1
        self.flop_partie= random.sample(self.pack, 3)  # même logique pour le flop (3 cartes)
        for carte in self.flop_partie:
                self.pack.remove(carte)
        self.turn_partie= random.sample(self.pack, 1) # même logique pour le turn (1 carte)
        for carte in self.turn_partie:
                self.pack.remove(carte)
        self.river_partie= random.sample(self.pack, 1) # même logique pour le river (1 carte)
        for carte in self.river_partie:
                self.pack.remove(carte)
        self.L_actifs =[j for j in self.L_joueurs if not j.couche] # on créer une liste avec tout les joueurs sauf ceux couché
        self.table_partie = table.Table(self.flop_partie,self.turn_partie,self.river_partie) 

        if len(self.L_actifs) >=2: #on veut définir une petite et une grosse blinde seulement si 2 joueurs sont actifs (pas possible de jouer avec moin que deux)
            i_pb = random.randrange(len(self.L_actifs))
            pb = self.L_actifs[i_pb]
            gb = self.L_actifs[(i_pb + 1) % len(self.L_actifs)] # la grosse blinde est la suivante, en revenant au début si besoin
            if pb.solde >self.Petite_blind:# pour eviter des soldes negative
                pb.mise = self.Petite_blind
                pb.solde -= self.Petite_blind 
            else:
                pb.mise = pb.solde 
                pb.solde=0
                pb.allin=True

            if gb.solde >self.Grosse_blind: # pour eviter des soldes negative
                gb.mise = self.Grosse_blind
                gb.solde -= self.Grosse_blind 
            else:
                gb.mise = gb.solde
                gb.solde=0
                gb.allin=True

            if gb.mise >= pb.mise:
                self.table_partie.mise = gb.mise
            else:
                self.table_partie.mise = pb.mise
            self.table_partie.pot_princ += pb.mise + gb.mise

            for index, j in enumerate(L_joueurs): # pour commencer après la grosse blinde on retrouve son index
                if j == gb :
                    self.index=index

    async def vote (self,index_vote =0,joueur_aug=None): # joueur_aug = None au lieu de 0 car 0 peut être un index d'un joueur

        if joueur_aug is None : # au début du vote on veut mettre la condition d'arret au joueur qui a commencé le vote 
            joueur_aug = index_vote
        
        while True:
            L_non_couches = [j for j in self.L_joueurs if not j.couche]
            if len(L_non_couches) <= 1: # si tout le monde est couché pas besoin de continuer à faire voter le seul debout
                return()
            
            L_votants = [j for j in self.L_joueurs if not j.couche and not j.allin]
            if len(L_votants) < 1 : # si tout le monde est couché ou en allin pas besoin de faire voter 
                return()
            joueur = self.L_joueurs[index_vote]

            if joueur.couche is False and joueur.allin is False:
                vote_x = await afficher.afficher_vote(0,joueur,self.table_partie.mise-joueur.mise)
                        
                if vote_x: #si l'utilisateur appuie sur valider sans rien mettre dans le toggle
                    joueur.vote = vote_x
                    if joueur.vote == joueurs.Joueurs.Vote[1]: # suivre
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0: # suivre la mise si possible
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.pot_princ += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise
                        else:
                            self.table_partie.pot_princ += joueur.solde # si pas les fonds, mises au tapis
                            joueur.mise += joueur.solde
                            joueur.solde =0
                        index_vote+=1
                        afficher.rafraichir(joueur.zone_jeu,5) # remise en attente
                    if joueur.vote == joueurs.Joueurs.Vote[0]: # Relancer
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0 : # suivre la mise si possible
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.pot_princ += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise

                            while True:                                     # pour s'assurer que le joueur aie une mise valide 
                                x = await afficher.afficher_vote(1,joueur) 
                                if x<0:
                                    await afficher.afficher_vote(7,joueur)  #  gestion de la mise négative
                                elif x <= joueur.solde:                     
                                    if  x>0:      # si la mise est 0 ce n'est pas une "relance" donc pas de raison de refaire un tour de vote
                                        joueur_aug = index_vote
                                    joueur.solde -= x
                                    self.table_partie.mise += x
                                    joueur.mise +=x
                                    self.table_partie.pot_princ += x
                                    break
                                else:
                                    await afficher.afficher_vote(2,joueur) # pas le solde necesssaire pour miser x
                        else:
                            self.table_partie.pot_princ += joueur.solde # si pas les fonds necessaire mise au tapis
                            joueur.mise += joueur.solde
                            joueur.solde =0
                            await afficher.afficher_vote(4,joueur) # pas miser plus car désormais en tapis
                        index_vote+=1
                        afficher.rafraichir(joueur.zone_jeu,5) # remise en attente

                    if joueur.vote == joueurs.Joueurs.Vote[3]: #tapis
                        if joueur.solde - (self.table_partie.mise-joueur.mise) >= 0:  # suivre la mise si possible
                            joueur.solde -= self.table_partie.mise-joueur.mise
                            self.table_partie.pot_princ += self.table_partie.mise-joueur.mise
                            joueur.mise = self.table_partie.mise
                            if joueur.solde != 0: # si après avoir suivi le joueur n'as plus d'argent, il n'augmente pas la mise de la table, il ne "relance" rien
                                joueur_aug = index_vote
                            self.table_partie.pot_princ += joueur.solde # mise au tapis (si solde est déjà 0 ça ne change rien)
                            joueur.mise += joueur.solde
                            self.table_partie.mise= joueur.mise
                            joueur.solde =0
                            index_vote+=1
                            afficher.rafraichir(joueur.zone_jeu,5) # remise en attente
                        else:                                               # direct mettre au tapis
                            self.table_partie.pot_princ += joueur.solde
                            joueur.mise += joueur.solde
                            joueur.solde =0
                            index_vote+=1
                            afficher.rafraichir(joueur.zone_jeu,5)  # remise en attente
    
                        
                    if joueur.vote == joueurs.Joueurs.Vote[2]: # coucher
                        joueur.couche =True
                        index_vote+=1
                        afficher.rafraichir(joueur.zone_jeu,5) # remise en attente
                else :
                    await afficher.afficher_vote(3,joueur) # valider sans toggle ("pas un vote autorisé")
                if joueur.solde == 0: 
                    joueur.allin=True
                
            else:
                index_vote +=1 # cas ou joueur couché ou allin
                afficher.rafraichir(joueur.zone_jeu,5) # remise en attente

            for j in self.L_joueurs:
                if j.zone_entete:  # sécurité au cas où un joueur quitte sa page
                    afficher.rafraichir(j.zone_entete) #pour afficher le changement dans la mise/solde
            

            if index_vote == len(self.L_joueurs): # l'index est donc en dehors de la liste ce qui veut dire qu'ont doit recommencer à 0
                index_vote =0

            if joueur_aug == index_vote : # on est retourné au joueur aug on peut sortir du vote 
                    index_vote=0
                    joueur_aug=0
                    break
        
    def def_gagnant (self,joueurs=None) : 
        self.L_actifs =joueurs if joueurs is not None else [j for j in self.L_joueurs if not j.couche and j.mise>0] # si il ne reçoit pas de joueurs spécifique comme dans pots execos, on prend juste les joueurs qui ne sont pas couché et qui on misé qqch
        if not self.L_actifs:                                                                                      # une personne déjà comptée voit sa mise réduire à 0 
            return[]  # utile pour pots execos, cas de figure normaux pas atteignable
        joueur_gagnant = None
        if len(self.L_actifs)==1: # s'il n'y a qu'un seul joueur actif, alors c'est le gagnant
            joueur_gagnant=self.L_actifs[0] 
            return([joueur_gagnant])
        self.L_actifs.sort(key=lambda j: j.combo, reverse=True) # on trie les joueurs actif du plus haut combo au plus bas

        if self.L_actifs[0].combo != self.L_actifs[1].combo: # si le premier combo n'est pas égal au deuxième, (le plus grand est unique), alors le gagnant est le premier
            joueur_gagnant = self.L_actifs[0]
            return([joueur_gagnant])
        
        else :                          # il y a donc au minimum deux personnes qui ont le même combo
            L_joueurs_gagnants = []
            joueurs_gagnants=[]
            combo_p=[]
            index=0
            while self.L_actifs[index].combo == self.L_actifs[0].combo: # on va maintenant regarder tout le joueurs actif qui ont le même combo que le premier
                joueur =self.L_actifs[index]
                joueur.cle_gagnant = []
                L_joueurs_gagnants.append(joueur)
                for i in range(len(joueur.cartes_combo)): # pour comparer les combo on va regarder la valeur des cartes
                    carte = joueur.cartes_combo[i]
                    if (joueur.combo == 4 or joueur.combo == 8) and (i ==0) and (carte.valeur==13) : # dans le cas de la "roue" l'as est la carte la plus basse (0)
                        joueur.cle_gagnant.append(0)
                    else:
                        joueur.cle_gagnant.append(carte.valeur)
                if joueur.cle_gagnant > combo_p: # comparaison de liste (lexicographique)(la question de la longueur de la liste joue un rôle mais il est inutile ici puisque les combo sont les même donc il y a le même nombre de carte dans combo_carte)
                    joueurs_gagnants=[joueur]
                    combo_p=joueur.cle_gagnant
                elif joueur.cle_gagnant == combo_p:
                    joueurs_gagnants.append(joueur)
                index+=1
                if index == len(self.L_actifs): # dans le cas ou les joueurs actifs ont le même combo avec les même valeurs
                    break
            

            index= len(joueurs_gagnants)
            if index>1: # si après la comparaison des combo il y a encore plusieurs gagnant on regarde les kickers(cartes qui complètent la main)
                combo_p=[]
                joueurs_gagnants_apres_kick=[]
                for joueur in joueurs_gagnants:
                    for carte in joueur.cartes_kicker:
                        joueur.cle_gagnant.append(carte.valeur)
                    if joueur.cle_gagnant > combo_p: #même logique que juste avec les combo mais avec les kickers en plus
                        joueurs_gagnants_apres_kick=[joueur] 
                        combo_p=joueur.cle_gagnant
                    elif joueur.cle_gagnant == combo_p:
                        joueurs_gagnants_apres_kick.append(joueur)
                if joueurs_gagnants_apres_kick:
                    joueurs_gagnants=joueurs_gagnants_apres_kick
            
        return (joueurs_gagnants) #retourne dans tout les cas une liste avec 1 ou plusieurs gagnant
    


    def atribution_pots(self):
        paliers = sorted(set(j.mise for j in self.L_joueurs if j.mise>0))  #chaque palier est défini selon les mises diférentes des joueurs
        palier_p=0
        palier=0

        for palier in paliers:
            contributeurs=[j for j in self.L_joueurs if j.mise >= palier] # tout les joueurs qui ont contribué au palier (ceux dont la mise est supérieur ou égal au palier)
            joueurs_p=[j for j in contributeurs if j.couche is False] # tout les joueurs qui peuvent potentiellement le palier ne doivent pas être couché
            pot=(palier - palier_p)*len(contributeurs) # le pot est tout l'argent qui va être distribué, à un palier donné, le palier_p (précédent) a dejà été distribué
            if not joueurs_p: # si les joueurs qui ont contribués sont couché on leur rembourse leur argent
                part_remb = pot //len(contributeurs)
                for c in contributeurs:
                        c.solde += part_remb
            elif len(joueurs_p)==1: # si le joueur éligible au palier est seul il reçoit tout le pot de ce palier
                joueurs_p[0].solde+= pot
            else: # si il y a plusieurs joueurs éligibles au pot du palier
                gagnants_p = self.def_gagnant(joueurs_p) # on détermine le ou les gagnants
                part,reste= divmod(pot,len(gagnants_p)) # et on réparti le pot chez ces gagnants (divmod car on a pas envie de "bout de jetons")
                for gp in gagnants_p:
                    if reste>0:
                        gp.solde += part +1
                    else:
                        gp.solde += part
                    reste-=1
            palier_p=palier
        for j in self.L_joueurs:
            j.mise =0
        return()
        




        
