import table
import cartes
class hand :
    liste_main_s = ["carte haute","pair","two_pair","three_oak","straight","flush","full_house","four_oak","straight_flush","royal_flush"]
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
        paires =[]
        three_oak =[]
        flush = False
        straight = False
        position = []
        temp=[]
        cartes_couleur=[]
        s_f= False 

        for i in range (1,14):
            occurence_valeur =self.L_valeur.count(i)
            if occurence_valeur == 2:
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    temp.append(self.cartes_jouables[position[j]])
                paires.append(temp)
                temp=[]
 
            if occurence_valeur == 3:

                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    temp.append(self.cartes_jouables[position[j]])
                three_oak.append(temp)
                temp=[]

            if occurence_valeur == 4:
                main_special=7
                cartes_jouee=[]
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for i in range (len(position)) :
                    cartes_jouee.append(self.cartes_jouables[position[i]])
                return(main_special,cartes_jouee)
        
        if len(three_oak) ==2 :
            main_special=6
            cartes_jouee= three_oak[0][1:]+three_oak[1]
            return(main_special,cartes_jouee)
        elif len(three_oak)==1 and len(paires) >= 1:
            main_special=6
            cartes_jouee= three_oak[0] + paires[-1]
            return(main_special,cartes_jouee)
        elif len(three_oak) ==1:
            main_special=3
            cartes_jouee=three_oak[0]
        elif len(paires) >=2:
            main_special=2
            cartes_jouee= paires[-1] + paires[-2]
        elif len(paires) ==1 :
            main_special=1
            cartes_jouee=paires[0]
        
        L_sorted= sorted(set(self.L_valeur))
        

        n_suite=0
        suite=[]
        suite_C=[]
        
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
                suite=[]
        if n_suite ==4:
            for i in range (len(suite)):
                for j in range (len(self.cartes_jouables)):
                    if suite[i] == self.cartes_jouables[j].valeur:
                        suite_C.append(self.cartes_jouables[j])
                        break

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
            flush = True
            cartes_couleur=L_carreau
        elif len(L_coeur) >= 5:
            flush = True
            cartes_couleur=L_coeur
        elif len(L_trefle) >= 5:
            flush = True
            cartes_couleur=L_trefle
        elif len(L_pique) >= 5:
            flush = True
            cartes_couleur = L_pique

        if flush is True :
            c_suite_C=[]
            c_suite=[]
            c_valeur=[]
            nc_suite=0
            for i in range (len(cartes_couleur)):
                c_valeur.append(cartes_couleur[i].valeur)
            c_sorted= sorted(set(c_valeur))
            for i in range (len(c_sorted)-1):
                if c_sorted[i]+1== c_sorted[i+1]:
                    nc_suite += 1
                    c_suite.append(c_sorted[i])
                    if nc_suite == 4 :
                        c_suite.append(c_sorted[i+1])
                        s_f=True
                        break
                else :
                    nc_suite = 0
                    c_suite=[]
            if nc_suite ==4:
                for i in range (len(c_suite)):
                    for j in range (len(cartes_couleur)):
                        if c_suite[i] == cartes_couleur[j].valeur:
                            c_suite_C.append(cartes_couleur[j])
                            break

                    
        if s_f is True :   
            main_special=8
            cartes_jouee = c_suite_C
            if c_suite[-1]==13 :
                main_special= 9
                cartes_jouee = c_suite_C
        elif len(three_oak) ==2 :
            main_special=6
            cartes_jouee= three_oak[0][1:]+three_oak[1]
        elif len(three_oak)==1 and len(paires) >= 1:
            main_special=6
            cartes_jouee= three_oak[0] + paires[-1]
        elif flush is True:
            main_special=5
            v_couleur= []
            for i in range (len(cartes_couleur)):
                v_couleur.append(cartes_couleur[i].valeur)
            v_couleur = sorted(v_couleur)
            v_couleur = v_couleur[-5:]
            cartes_jouee=[]
            for i in range (5):
                for j in range (len(cartes_couleur)):
                    if cartes_couleur[j].valeur == v_couleur[i]:
                        cartes_jouee.append(cartes_couleur[j])
                        break



        elif straight is True :
                main_special =4
                cartes_jouee= suite_C
        elif len(three_oak) ==1:
            main_special=3
            cartes_jouee=three_oak[0]
        elif len(paires) >=2:
            main_special=2
            cartes_jouee= paires[-1] + paires[-2]
        elif len(paires) ==1 :
            main_special=1
            cartes_jouee=paires[0]

        return (main_special,cartes_jouee)