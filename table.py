class Table :
    type_etape=["stage0","flop","turn","river"]
    def __init__(self, flop, turn, river,mise=0, pot_princ = 0, etape =0, jape=None):
        self.etape=etape
        self.flop = flop
        self.turn = turn
        self.river = river
        self.liste= [flop,turn, river]
        self.mise = mise
        self.pot_princ = pot_princ
        self.jape= jape