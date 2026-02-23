class hand :
    def __init__(self,cartes_joueur, flop, turn, river,):
        cartes_jouables = []
        cartes_jouables.append(cartes_joueur,flop,turn, river)
        self.cartes_jouables = cartes_jouables
        
    def analyse_main (self):
        nb_pique=0
        nb_trefle=0
        nb_carreau=0
        nb_coeur=0
        L_valeur=[]
        pair = False
        two_pair = False
        three_oak= False
        straight= False
        flush = False
        full_house = False
        four_oak=False
        straight_flush=False
        royal_flush=False

        for i in range (len(self.cartes_jouables)) :
            x=self.cartes_jouables[i].valeur
            L_valeur.append(x)
            if self.cartes_jouables[i].couleur == "pique" :
                nb_pique+=1
            if self.cartes_jouables[i].couleur == "trefle" :
                nb_trefle+=1
            if self.cartes_jouables[i].couleur == "carreau" :
                nb_carreau+=1
            if self.cartes_jouables[i].couleur == "coeur" :
                nb_coeur+=1
        if nb_carreau or nb_coeur or nb_trefle or nb_pique >= 5:
            flush = True
        for i in range (1,14):
            occurence_valeur =L_valeur.count(i)
            if occurence_valeur == 2:
                pair == True
                nb_pair += 1
            if occurence_valeur == 3:
                three_oak = True
            if occurence_valeur == 4:
                four_oak =True
        if nb_pair >= 2:
            two_pair =True
        L_sorted= sorted(L_valeur)
        n_suite=0
        suite=[]
        for i in range (len(L_sorted)-1):
            if L_sorted[i]+1== L_sorted[i+1]:
                n_suite += 1
                suite.append(L_sorted[i])
                if n_suite == 4 :
                    suite.append(L_sorted[i+1])
                    straight=True
                    break
            else :
                n_suite = 0
        if straight is True and flush is True:
            straight_flush = True
        if n_suite[-1]==13 and straight_flush is True :
            royal_flush = True