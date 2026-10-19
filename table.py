class Table :
    type_etape=["stage0","flop","turn","river"]
    etape_libelles={"stage0":"Pré-Flop","flop":"Flop","turn":"Turn","river":"River"} #en joli pour le label
    def __init__(self, flop, turn, river): # seuls eux sont définis et modifiés à l'aide du constructeur
        self.etape=0
        self.flop = flop
        self.turn = turn
        self.river = river
        self.liste= [flop,turn, river]
        self.mise = 0
        self.pot_princ = 0