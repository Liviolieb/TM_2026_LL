import table
import cartes
class hand :
    liste_main_s = ["carte haute","pair","two_pair","three_oak","full_house","flush","four_oak","straight","straight_flush","royal_flush"]
    def __init__(self,cartes_joueur, table):
        cartes_jouables = []
        self.L_valeur = []
        for i in range (len(cartes_joueur)):
            cartes_jouables.append(cartes_joueur[i])
            self.L_valeur.append(cartes_joueur[i].valeur)
        for i in range (table.etape):
            for j in range(len(table.liste[i])):
                cartes_jouables.append(table.liste[i][j])
                self.L_valeur.append(table.liste[i][j].valeur)
        self.cartes_jouables = cartes_jouables
        
        
    def analyse_main (self):
        main_special= 0
        cartes_jouee=[]
        L_pique=[]
        L_trefle=[]
        L_carreau=[]
        L_coeur=[]
        nb_pair =0
        pair =False
        three_oak =False
        four_oak = False
        flush = False
        straight = False
        straight_flush = False
        position = []
        temp=[]

        for i in range (1,14):
            occurence_valeur =self.L_valeur.count(i)
            if occurence_valeur == 2:
                main_special = 1

                pair = True
                nb_pair += 1
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    cartes_jouee.append(self.cartes_jouables[position[j]])
                if nb_pair >= 2:
                    main_special= 2
            if occurence_valeur == 3:
                main_special= 3
                if pair is False :
                    cartes_jouee =[]
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    cartes_jouee.append(self.cartes_jouables[position[j]])
                three_oak = True
            if three_oak and pair is True :
                main_special = 4
            if occurence_valeur == 4:
                four_oak = True
                cartes_jouee=[]
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for i in range (len(position)) :
                    cartes_jouee.append(self.cartes_jouables[position[i]])
        for j in range (len(self.cartes_jouables))  :
            if self.cartes_jouables[j].couleur == "pique" :
                L_pique.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "trefle" :
                L_trefle.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "carreau" :
                L_carreau.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "coeur" :
                L_coeur.append(self.cartes_jouables[j])
        if len(L_carreau) >= 5:
            main_special=5
            flush = True
            if four_oak is False :
                cartes_jouee=L_carreau
        if len(L_coeur) >= 5:
            main_special=5
            flush = True
            if four_oak is False :
                cartes_jouee=L_coeur
        if len(L_trefle) >= 5:
            main_special=5
            flush = True
            if four_oak is False :
                cartes_jouee=L_trefle
        if len(L_pique) >= 5:
            main_special=5
            flush = True
            if four_oak is False :
                cartes_jouee = L_pique
        if four_oak is True :
            main_special = 6
        L_sorted= sorted(self.L_valeur)
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
                    cartes_jouee= suite
                    break
            else :
                n_suite = 0
        if straight is True and flush is True:
            main_special=8
            straight_flush = True
            cartes_jouee = L_sorted[2:]
        if L_sorted[-1]==13 and straight_flush is True :
            main_special= 9
            cartes_jouee = L_sorted[2:]
        return (main_special,cartes_jouee)