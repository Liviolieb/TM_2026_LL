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
        
    def kicker(self,cartes_combo):
        cartes_kicker=[]
        if len(cartes_combo)<5:
            v_kicker=self.L_valeur.copy()
            cartes_kicker=self.cartes_jouables.copy()

            for carte in cartes_kicker[:]:
                for combo in cartes_combo:
                    if carte.valeur ==combo.valeur:
                        cartes_kicker.remove(carte)
                        v_kicker.remove(carte.valeur)
                        break
            v_kicker=sorted(v_kicker)
            nb_kicker = (5-len(cartes_combo))
            v_kicker=v_kicker[-nb_kicker:]
            for carte in cartes_kicker[:]:
                    if carte.valeur not in v_kicker:
                        cartes_kicker.remove(carte)
                    else:
                        v_kicker.remove(carte.valeur)

        cartes_kicker.sort(key=lambda carte: carte.valeur, reverse=True)
        return cartes_kicker

            

    def analyse_main (self):  #fonction d'analyse du combo 
        main_special= 0
        cartes_combo=[]
        cartes_kicker = []
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

        for i in range (1,14): #boucle sur les 14 différentes cartes pour vérifier combien de fois on les retrouves dans notre main
            occurence_valeur =self.L_valeur.count(i)

            if occurence_valeur == 2: # si deux fois dans notre main on rajoute les deux cartes dans une liste (temp) qui est ensuite elle même ajoutée dans une liste (paires)
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    temp.append(self.cartes_jouables[position[j]])
                paires.append(temp)
                temp=[]
 
            if occurence_valeur == 3:# si trois fois dans notre main on rajoute les trois cartes dans une liste (temp) qui est ensuite elle même ajoutée dans une liste (three_oak)
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for j in range (len(position)) :
                    temp.append(self.cartes_jouables[position[j]])
                three_oak.append(temp)
                temp=[]

            if occurence_valeur == 4: # si quatres fois dans notre main on ajoutes ces cartes dans une liste et on peut sortir de la fonction car aucun autre combo plus fort n'est possible
                main_special=7
                cartes_combo=[]
                position = [j for j, x in enumerate(self.L_valeur) if x == i]
                for i in range (len(position)) :
                    cartes_combo.append(self.cartes_jouables[position[i]])
                cartes_kicker=self.kicker(cartes_combo)
                return(main_special,cartes_combo,cartes_kicker)
        
        if len(three_oak) ==2 : # si on a deux fois une liste de 3 même cartes alors on aura un full composé des deux première cartes de la première liste qui ont une valeur plus petite (car on ajoute les cartes de 1 à 14) et de la deuxieme liste
            main_special=6
            cartes_combo= three_oak[1]+three_oak[0][1:]
            cartes_kicker=self.kicker(cartes_combo)
            return (main_special,cartes_combo,cartes_kicker)
        
        elif len(three_oak)==1 and len(paires) >= 1: #si on a une liste de trois même cartes et une ou plusieurs liste avec deux cartes, on aura donc un full avec le three_oak et la dernière pair détécté (avec la valeur la plus élevée)
            main_special=6
            cartes_combo= three_oak[0] + paires[-1]
            cartes_kicker=self.kicker(cartes_combo)
            return(main_special,cartes_combo,cartes_kicker)
        elif len(three_oak) ==1: #si il n'y a qu'une seule liste avec 3 cartes alors three_oak
            main_special=3
            cartes_combo=three_oak[0]
        elif len(paires) >=2: #si il y a deux ou plus listes avec deux cartes alors on a une double paire avec les dernières paires détéctée (avec la valeur la plus élevée)
            main_special=2
            cartes_combo= paires[-1] + paires[-2]
        elif len(paires) ==1 : # si il n'y a qu'une seule liste avec 2 cartes alors paire
            main_special=1
            cartes_combo=paires[0]
        
        L_sorted= sorted(set(self.L_valeur)) #on transforme la liste en set pour enlever les doublons puis on la trie en ordre croissant

        if {13,1,2,3,4}.issubset(set(self.L_valeur)): #on vérifie si la "roue" est dans L_valeur
            L_sorted = [0] + L_sorted

        n_suite=0
        suite=[]
        m_suite=[]
        suite_C=[]
        
        for i in range (len(L_sorted)-1):        #on parcourt la liste et on vérifie que l'élément suivant est égal à celui en court plus 1
            if L_sorted[i]+1== L_sorted[i+1]:
                n_suite += 1
                suite.append(L_sorted[i])  # si c'est le cas on ajoute la carte dans notre liste suite et on rajoute 1 a n_suite
                if n_suite >= 4 : #si le nombre d'élément dans la liste suite (=n_suite) est égal a 4 alors on rajoute l'élément suivant pour faire une main de 5 cartes
                    straight=True
                    m_suite =suite[-4:]+[L_sorted[i+1]]

            else :
                n_suite = 0
                suite=[]

        suite = m_suite

        for i in range (len(suite)):
            for j in range (len(self.cartes_jouables)):
                if (suite[i]== 0) and (self.cartes_jouables[j].valeur == 13):
                    suite_C.append(self.cartes_jouables[j])
                    break
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
            if {13,1,2,3,4}.issubset(set(c_valeur)):
                c_sorted = [0] + c_sorted

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
                        if (c_suite[i] == 0) and (cartes_couleur[j].valeur == 13):
                            c_suite_C.append(cartes_couleur[j])
                            break
                        if c_suite[i] == cartes_couleur[j].valeur:
                            c_suite_C.append(cartes_couleur[j])
                            break

                    
        if s_f is True :   
            main_special=8
            cartes_combo = c_suite_C
            if c_suite[-1]==13 :
                main_special= 9
                cartes_combo = c_suite_C
        elif flush is True:
            main_special=5
            v_couleur= []
            for i in range (len(cartes_couleur)):
                v_couleur.append(cartes_couleur[i].valeur)
            v_couleur = sorted(v_couleur, reverse=True)
            v_couleur = v_couleur[:5]
            cartes_combo=[]
            for i in range (5):
                for j in range (len(cartes_couleur)):
                    if cartes_couleur[j].valeur == v_couleur[i]:
                        cartes_combo.append(cartes_couleur[j])
                        break



        elif straight is True :
                main_special =4
                cartes_combo= suite_C
        elif len(three_oak) ==1:
            main_special=3
            cartes_combo=three_oak[0]
        elif len(paires) >=2:
            main_special=2
            cartes_combo= paires[-1] + paires[-2]
        elif len(paires) ==1 :
            main_special=1
            cartes_combo=paires[0]

        cartes_kicker=self.kicker(cartes_combo)



        

        return (main_special,cartes_combo,cartes_kicker)