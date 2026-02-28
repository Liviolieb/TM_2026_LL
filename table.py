class Table :
    etape=0
    def __init__(self, flop, turn, river, main_pot , side_pot):
        self.flop = flop
        self.turn = turn
        self.river = river
        self.liste= [flop,turn, river]
        self.main_pot = main_pot
        self.side_pot = side_pot