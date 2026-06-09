class Table :
    etape=0
    type_etape=["stage0","flop","turn","river"]
    def __init__(self, flop, turn, river,mise=0, main_pot = 0 , side_pot=[]):
        self.flop = flop
        self.turn = turn
        self.river = river
        self.liste= [flop,turn, river]
        self.mise = mise
        self.main_pot = main_pot
        self.side_pot = side_pot