class Table :
    etape=0
    type_etape=["flop","turn","river"]
    def __init__(self, flop, turn, river,mise=0, main_pot = None , side_pot=None):
        self.flop = flop
        self.turn = turn
        self.river = river
        self.liste= [flop,turn, river]
        self.mise = mise
        self.main_pot = main_pot
        self.side_pot = side_pot