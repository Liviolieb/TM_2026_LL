import table
import cartes
class hand :
    liste_main_s = ["carte haute","pair","two_pair","three_oak","full_house","flush","four_oak","straight","straight_flush","royal_flush"]
    def __init__(self,cartes_joueur, table):
        cartes_jouables = []
        cartes_jouables.append(cartes_joueur)
        for i in range (table.etape):
            cartes_jouables.append(table.liste[i])
        self.cartes_jouables = cartes_jouables
        
    def analyse_main (self):
        main_special= 0
        nb_pique=0
        nb_trefle=0
        nb_carreau=0
        nb_coeur=0
        L_valeur=[]
        nb_pair =0
        pair =False
        three_oak =False
        four_oak = False
        flush = False
        straight = False
        straight_flush = False

        for i in range (len(self.cartes_jouables)) :
            x=cartes.Cartes(self.cartes_jouables[i]).valeur
            L_valeur.append(x)
        for i in range (1,14):
            occurence_valeur =L_valeur.count(i)
            if occurence_valeur == 2:
                main_special = 1
                
                pair = True
                nb_pair += 1
                if nb_pair >= 2:
                    main_special= 2
            if occurence_valeur == 3:
                main_special= 3
                three_oak = True
            if three_oak and pair is True :
                main_special = 4
            if occurence_valeur == 4:
                four_oak = True
            if cartes.Cartes(self.cartes_jouables[i]).couleur == "pique" :
                nb_pique+=1
            if cartes.Cartes(self.cartes_jouables[i]).couleur == "trefle" :
                nb_trefle+=1
            if cartes.Cartes(self.cartes_jouables[i]).couleur == "carreau" :
                nb_carreau+=1
            if cartes.Cartes(self.cartes_jouables[i]).couleur == "coeur" :
                nb_coeur+=1
        if nb_carreau or nb_coeur or nb_trefle or nb_pique >= 5:
            main_special=5
            flush = True
        if four_oak is True :
            main_special = 6
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
                    main_special= 7
                    break
            else :
                n_suite = 0
        if straight is True and flush is True:
            main_special=8
            straight_flush = True
        if L_sorted[-1]==13 and straight_flush is True :
            main_special= 9
        return (main_special)