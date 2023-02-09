class GameX0():
    def __init__(self):
        self.gamestatus = False

    def gamestart(self):
        self.pool = {'A': ['1', ' ', '0'],
                     'B': [' ', '2', ' '],
                     'C': ['x', ' ', '3']}
        self.gamestatus = True
    def gamestop(self):
        self.gamestatus = False
            
    def set_chip(self,chip):
        if chip=='x':
            self.chip_player='x'
            self.chip_cpu='o'
        else:
            self.chip_player='o'
            self.chip_cpu='x'
        
    def print_pool(self) -> str:
        str = '  1 2 3\n' +\
            'A|{}|{}|{}|\n'.format(self.pool['A'][0], self.pool['A'][1], self.pool['A'][2],) +\
            'B|{}|{}|{}|\n'.format(self.pool['B'][0], self.pool['B'][1], self.pool['B'][2],) +\
            'C|{}|{}|{}|\n'.format(self.pool['C'][0], self.pool['C'][1], self.pool['C'][2],)
        print(str)
        return str

    def run_player(self, cell:str):
        x = cell[0].upper
        try:
            y = int(cell[1])
        except:
            return 1
        if x not in 'ABC':
            return 1
        if not 0 < y < 4:
            return 1

        if self.pool[x][y-1]!=' ':
            return 2
        else:
            self.pool[x][y]=self.chip_player
        
    def check_game(pool):
        
        "".join(pool['А'])==""

gm = GameX0()
gm.gamestart()
gm.print_pool()
