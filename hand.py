import table
import cartes
class hand :
    liste_main_s = ["carte haute","pair","two_pair","three_oak","straight","flush","full_house","four_oak","straight_flush","royal_flush"]
    noms_mains = ["Carte haute", "Paire", "Double paire", "Brelan", "Suite",
              "Couleur", "Full", "Carré", "Quinte flush", "Quinte flush royale"]
    def __init__(self,cartes_joueur, table):
        cartes_jouables = []
        self.L_valeur = [] # liste des valeurs de cartes jouables
        for i in range (len(cartes_joueur)):
            cartes_jouables.append(cartes_joueur[i])
            self.L_valeur.append(cartes_joueur[i].valeur)
        for i in range (table.etape):
            for j in range(len(table.liste[i])):
                cartes_jouables.append(table.liste[i][j])
                self.L_valeur.append(table.liste[i][j].valeur)
        self.cartes_jouables = cartes_jouables # on fait une liste ou on ajoute les 2 cartes du joueurs et selon l'étape les cartes dévoilée sur la table
        
    def kicker(self,cartes_combo): #fonction qui défini les cartes qui complète les cartes combo pour faire une main complète
        cartes_kicker=[]
        if len(cartes_combo)<5:  # toujours vrai sauf pour suite/couleur/quinte flush, qui fournissent déjà 5 cartes
            v_kicker=self.L_valeur.copy() #copie pour ne pas modifier L_valeur ou cartes_jouables
            cartes_kicker=self.cartes_jouables.copy()

            for carte in cartes_kicker[:]: # on parcours carte par carte une copie de cartes_kicker
                for combo in cartes_combo:
                    if carte.valeur ==combo.valeur and carte.couleur == combo.couleur: # on enlève les cartes qu'on à déjà prises dans les cartes_combo
                        cartes_kicker.remove(carte)
                        v_kicker.remove(carte.valeur)
                        break
            v_kicker=sorted(v_kicker)
            nb_kicker = (5-len(cartes_combo)) # on retiens le nombre de cartes qu'il nous faut pour compléter la main
            v_kicker=v_kicker[-nb_kicker:] #on prend uniquement les cartes les plus hautes qui nous intéressent
            for carte in cartes_kicker[:]: 
                    if carte.valeur not in v_kicker: # on passe tout notre liste de carte du kicker et si la valeur n'est pas celle qui nous interesse, on enlève la carte de la liste
                        cartes_kicker.remove(carte)
                    else:
                        v_kicker.remove(carte.valeur)

        cartes_kicker.sort(key=lambda carte: carte.valeur, reverse=True) # on les trie dans l'ordre décroissant pour def_gagnant
        return cartes_kicker

            

    def analyse_main (self):  #fonction d'analyse du combo 
        main_special= 0 # la variable (int) qui va définir le combo selon la liste_main_s
        cartes_combo=[]  # les cartes qui seront associée avec la main spéciale
        cartes_kicker = []  # les cartes qui complètent si nécessaire les cartes combo pour faire une main de 5 cartes
        L_pique=[] # les cartes de couleur pique
        L_trefle=[] # les cartes de couleur trefle
        L_carreau=[] # les cartes de couleur carreau
        L_coeur=[] # les cartes de couleur coeur
        paires =[] # toutes les paires détéctée
        three_oak =[] # tout les brelan détécté
        flush = False # variable qui dit si on est en présence d'une couleur
        straight = False # variable qui dit si on est en présence d'une suite
        position = [] # liste qui va contenir les position des cartes lors de la répétition de leur valeur
        temp=[] # variable temporaire qui va être utiliser comme 1 paire ou 1 brelan à rajouter dans la liste de brelan ou paires
        cartes_couleur=[] # toute les cartes d'une certaine couleur si leurs nombre excede 5
        s_f= False  # variable qui dit si on est en présence d'une quinte flush 

        for i in range (1,14): #boucle sur les 13 différentes cartes pour vérifier combien de fois on les retrouves dans notre main
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
                for k in range (len(position)) :
                    cartes_combo.append(self.cartes_jouables[position[k]])
                cartes_kicker=self.kicker(cartes_combo)
                return(main_special,cartes_combo,cartes_kicker)
        
        if len(three_oak) ==2 : # si on a deux fois une liste de 3 même cartes alors on aura un full composé des deux dernières cartes de la première liste qui ont une valeur plus petite (car on ajoute les cartes de 1 à 13) et de la deuxieme liste
            main_special=6
            cartes_combo= three_oak[1]+three_oak[0][1:]
            cartes_kicker=self.kicker(cartes_combo)
            return (main_special,cartes_combo,cartes_kicker)
        
        elif len(three_oak)==1 and len(paires) >= 1: #si on a une liste de trois même cartes et une ou plusieurs liste avec deux cartes, on aura donc un full avec le three_oak et la dernière pair détécté (avec la valeur la plus élevée)
            main_special=6
            cartes_combo= three_oak[0] + paires[-1]
            cartes_kicker=self.kicker(cartes_combo)
            return(main_special,cartes_combo,cartes_kicker)
        
        L_sorted= sorted(set(self.L_valeur)) #on transforme la liste en set pour enlever les doublons puis on la trie en ordre croissant

        if {13,1,2,3,4}.issubset(set(self.L_valeur)): #on vérifie si la "roue" est dans L_valeur
            L_sorted = [0] + L_sorted # si il y a une roue on utilise 0 pour représenter l'as

        n_suite=0
        suite=[]
        m_suite=[]
        suite_C=[]
        
        for i in range (len(L_sorted)-1):        #on parcourt la liste et on vérifie que l'élément suivant est égal à celui en cours plus 1
            if L_sorted[i]+1== L_sorted[i+1]:
                n_suite += 1
                suite.append(L_sorted[i])  # si c'est le cas on ajoute la carte dans notre liste suite et on rajoute 1 à n_suite
                if n_suite >= 4 : #si le nombre d'élément dans la liste suite (=n_suite) est égal a 4 alors on rajoute l'élément suivant pour faire une main de 5 cartes
                    straight=True
                    m_suite =suite[-4:]+[L_sorted[i+1]] # on réécrit chaque fois m_suite comme les 5 cartes les plus hautes consécutives

            else :
                n_suite = 0
                suite=[]

        suite = m_suite

        for i in range (len(suite)): # suite ne contient que des valeurs on la parcourt et on cherche dans cartes jouables les cartes qui ont cette valeurs
            for j in range (len(self.cartes_jouables)):
                if (suite[i]== 0) and (self.cartes_jouables[j].valeur == 13): # si la carte a la valeur 0 alors on sait que c'est un as (13)
                    suite_C.append(self.cartes_jouables[j])
                    break
                if suite[i] == self.cartes_jouables[j].valeur:# en règle général on ajoute seulement si l'élément de suite est égal à la valeur de la carte
                    suite_C.append(self.cartes_jouables[j])
                    break

        for j in range (len(self.cartes_jouables))  : # pour chaque carte on regarde sa couleur et on la trie selon cette dernière
            if self.cartes_jouables[j].couleur == "pique" :
                L_pique.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "trefle" :
                L_trefle.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "carreau" :
                L_carreau.append(self.cartes_jouables[j])
            if self.cartes_jouables[j].couleur == "coeur" :
                L_coeur.append(self.cartes_jouables[j])
        if len(L_carreau) >= 5:  # si l'occurence d'une couleur est égale ou supérieur à 5 on peut constituer une main d'une certaine couleur
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
            temp_c_suite=[]
            c_suite=[]
            c_valeur=[]
            nc_suite=0
            for i in range (len(cartes_couleur)):  # on applique le même fonctionnement que en haut pour detecter une suite 
                c_valeur.append(cartes_couleur[i].valeur)

            c_sorted= sorted(set(c_valeur)) #on transforme la liste en set pour enlever les doublons puis on la trie en ordre croissant

            if {13,1,2,3,4}.issubset(set(c_valeur)): #on vérifie si la "roue" est dans L_valeur
                c_sorted = [0] + c_sorted

            for i in range (len(c_sorted)-1): #on parcourt la liste et on vérifie que l'élément suivant est égal à celui en cours plus 1
                if c_sorted[i]+1== c_sorted[i+1]:
                    nc_suite += 1
                    c_suite.append(c_sorted[i]) # si c'est le cas on ajoute la carte dans notre liste suite et on rajoute 1 à n_suite
                    if nc_suite >= 4 : #si le nombre d'élément dans la liste suite (=n_suite) est égal a 4 alors on rajoute l'élément suivant pour faire une main de 5 cartes
                        temp_c_suite= c_suite[-4:]+ [c_sorted [i+1]] # on réécrit chaque fois temp_c_suite comme les 5 cartes les plus hautes consécutives
                        s_f=True # on a fait la vérification de suite sur des cartes déjà toute de la même couleur alors on peut affirmer que c'est une quinte flush
                else :
                    nc_suite = 0
                    c_suite=[]
            c_suite= temp_c_suite

            if s_f: 
                for i in range (len(c_suite)): # c_suite ne contient que des valeurs on la parcourt et on cherche dans cartes couleur la carte qui a cette valeur
                    for j in range (len(cartes_couleur)):
                        if (c_suite[i] == 0) and (cartes_couleur[j].valeur == 13):  # si la cartes a la valeur 0 alors on sait que c'est un as (13)
                            c_suite_C.append(cartes_couleur[j])
                            break
                        if c_suite[i] == cartes_couleur[j].valeur:  # en règle général on ajoute seulement si l'élément de suite est égal à la valeur de la carte
                            c_suite_C.append(cartes_couleur[j])
                            break

        # l'ordre des conditions suit le classement des mains, du plus fort au plus faible : une main plus faible ne doit jamais être testée avant une main plus forte compatible
        
        if s_f is True:
            main_special=8 
            cartes_combo = c_suite_C
            if c_suite[-1]==13 : # si la valeur la plus haute (dernière car ordre croissant) est 13 (as) on à une quinte flush royale
                main_special= 9
                cartes_combo = c_suite_C


        elif flush is True: # dans ce cas on à uniquement un combo couleur et détecté
            main_special=5
            v_couleur= []
            for i in range (len(cartes_couleur)): # on fait une liste avec la valeur des cartes de la couleur en question
                v_couleur.append(cartes_couleur[i].valeur)
            v_couleur = sorted(v_couleur, reverse=True) #on la trie dans l'ordre décroissant (utile pour prendre les plus haute, et surtout pour la comparaison de liste dans def_gagnant)
            v_couleur = v_couleur[:5] #on garde seulement les 5 plus haute (5 prmière)
            cartes_combo=[]
            for i in range (5): # v_couleur contient les valeurs on on la parcourt et on cherche dans cartes couleur la carte qui a cette valeur
                for j in range (len(cartes_couleur)):
                    if cartes_couleur[j].valeur == v_couleur[i]: # si l'élément de v_couleur est égal à la valeur de la carte on l'ajoute au combo
                        cartes_combo.append(cartes_couleur[j])
                        break



        elif straight is True : # si c'est une suite on a déjà la liste toute prête qui contient la suite la plus haute
                main_special =4
                cartes_combo= suite_C
        elif len(three_oak) ==1: #si il n'y a qu'une seule liste avec 3 cartes alors three_oak
            main_special=3
            cartes_combo=three_oak[0]
        elif len(paires) >=2: #si il y a deux ou plus listes avec deux cartes alors on a une double paire avec les dernières paires détéctée (avec la valeur la plus élevée)
            main_special=2
            cartes_combo= paires[-1] + paires[-2]
        elif len(paires) ==1 : # si il n'y a qu'une seule liste avec 2 cartes alors paire
            main_special=1
            cartes_combo=paires[0]

        cartes_kicker=self.kicker(cartes_combo)



        

        return (main_special,cartes_combo,cartes_kicker)