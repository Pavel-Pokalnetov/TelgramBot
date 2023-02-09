class GameX0():
    def __init__(self):
        self.gamestatus = False

    def gamestart(self):
        self.pool = [['1', ' ', '0'],
                     [' ', '2', ' '],
                     ['x', ' ', '3']]
        self.gamestatus = True

    def gamestop(self):
        self.gamestatus = False

    def set_chip(self, chip):
        if chip == 'x':
            self.chip_player = 'x'
            self.chip_cpu = 'o'
        else:
            self.chip_player = 'o'
            self.chip_cpu = 'x'

    def print_pool(self) -> str:
        str = '  1 2 3\n' +\
            'A|{}|{}|{}|\n'.format(self.pool[0][0], self.pool[0][1], self.pool[0][2],) +\
            'B|{}|{}|{}|\n'.format(self.pool[1][0], self.pool[1][1], self.pool[1][2],) +\
            'C|{}|{}|{}|\n'.format(
                self.pool[2][0], self.pool[2][1], self.pool[2][2],)
        print(str,end='')
        return str

    def run_player(self, cell: str):
        x = cell[0].upper()
        try:
            y = int(cell[1])-1
        except:
            return 1
        if not x in 'ABC':
            return 1
        else:
            x = 'ABC'.index(x)

        if not 0 <= y < 3:
            return 1

        if self.pool[x][y] != ' ':
            return 1
        else:
            self.pool[x][y] = self.chip_player
            return 0

    def check_game_final(self, pool):
        # проверка горизонталей
        for i in (0, 1, 2):
            if (''.join(pool[i]) == 'xxx' or
               ''.join(pool[i]) == 'ooo'):
                return True
        # проверка вертикалей
        for i in (0, 1, 2):
            temp = ''
            for j in (0, 1, 2):
                temp += pool[j][i]
            if temp == 'xxx' or temp == 'ooo':
                return True
        # проверка диагоналей
        diag = pool[0][0]+pool[1][1]+pool[2][2]
        if diag == 'xxx' or diag == 'ooo':
            return True
        diag = pool[0][2]+pool[1][1]+pool[2][0]
        if diag == 'xxx' or diag == 'ooo':
            return True
        return False


def test():
    gm = GameX0()
    gm.gamestart()
    # gm.print_pool()
    # gm.run_player('A1')
    # gm.run_player('A2')
    # gm.run_player('A3')
    # gm.run_player('B1')
    # gm.run_player('b2')
    # gm.run_player('B3')
    # gm.run_player('C1')
    # gm.run_player('c2')
    # gm.run_player('c3')

    gm.pool = [['o', 'x', 'o'],
               [' ', 'o', 'o'],
               ['x', 'o', 'x']]
    gm.print_pool()
    print(gm.check_game_final(gm.pool))


test()
