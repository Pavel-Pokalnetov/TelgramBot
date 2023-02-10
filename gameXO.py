from random import randint


class GameX0():
    def __init__(self):
        self.gamestatus = False  # состояние игры
        self.pool = [[' ', ' ', ' '],  # игровое поле
                     [' ', ' ', ' '],
                     [' ', ' ', ' ']]
        self.chip_player: str  # кто чем ходит
        self.player_step: bool  # ход человека/компьютера

    def help(self):
        # правила игры
        msg = 'Игра крестики-нолики класическая\nигровое поле 3х3\n' +\
            self.print_pool() +\
              '\nвыбор ячейки, для хода указывается\nкоординатами, по тупу шахмат: ' +\
              'А1..С3\n'
        return msg

    def gamestart(self):
        # старт игры
        self.pool = [[' ', ' ', ' '],
                     [' ', ' ', ' '],
                     [' ', ' ', ' ']]
        self.gamestatus = True
        msg = self.help()
        if randint(0, 10) > 5:
            self.set_chip('x')
            msg += "\nвы ходите крестиками\n"
        else:
            self.set_chip('o')
            msg += "\nвы ходите ноликами\n"
        return msg

    def gamestop(self):
        # остановка игры
        self.gamestatus = False

    def set_chip(self, chip):
        # установка фигруры игрока: X или O
        if chip == 'x':
            self.chip_player = 'x'
            self.chip_cpu = 'o'
        else:
            self.chip_player = 'o'
            self.chip_cpu = 'x'

    def print_pool(self) -> str:
        # вывод игрового поля
        str = '`  1 2 3\n' +\
            'A|{}|{}|{}|\n'.format(self.pool[0][0], self.pool[0][1], self.pool[0][2],) +\
            'B|{}|{}|{}|\n'.format(self.pool[1][0], self.pool[1][1], self.pool[1][2],) +\
            'C|{}|{}|{}|`'.format(
                self.pool[2][0], self.pool[2][1], self.pool[2][2],)
        # print(str, end='')
        return str

    def run_player(self, cell: str):
        # ход игрока
        # возврат
        #   1 - если ход неверный
        #   0 - если ход выполнен
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

    def run_cpu(self):
        # ход компьютера
        temp_pool = self.pool
        for x, y in ((x, y) for x in (0, 1, 2) for y in (0, 1, 2)):
            if temp_pool[x][y] == ' ':
                temp_pool[x][y] = self.chip_cpu
                if self.check_game_final(temp_pool):
                    # выигрышный ход
                    self.pool[x][y] = self.chip_cpu
                    return 'мой ход: {}{}'.format('ABC'[x], y+1)
                temp_pool[x][y] = self.chip_player
                if self.check_game_final(temp_pool):
                    # защитный ход
                    self.pool[x][y] = self.chip_cpu
                    return 'мой ход: {}{}'.format('ABC'[x], y+1)
                temp_pool[x][y] = ' '
        while (True):
            # если защищать нечего и нет выигрышных ходов
            # то стаивм случайно в свободную клетку
            x, y = randint(0, 2), randint(0, 2)
            if self.pool[x][y] == ' ':
                self.pool[x][y] = self.chip_cpu
                return 'мой ход: {}{}'.format('ABC'[x], y+1)

    def game_step(self, data: str):
        if not self.gamestatus:
            return
        msg = ''
        if self.player_step:
            # ход человека
            if self.run_player(data) == 1:
                # неверный ход
                msg = 'неверный ход\nповторите ввод'
            else:
                if self.check_game_final():
                    # человек выиграл
                    msg = 'вы выиграли'
                    self.gamestop()
                    return msg
                self.player_step = not (self.player_step)
        else:
            # ход компьютера
            msg = self.run_cpu()
            if self.check_game_final():
                # компьютер выиграл
                msg += '\nя выиграл'
                self.gamestop()
            else:
                # компьютер сделал ход
                msg += '\nваш ход'
                self.player_step = not (self.player_step)
        msg += '\n'+self.print_pool
        return msg


def test():
    gm = GameX0()
    print(gm.gamestart())
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

    # gm.pool = [[' ', 'x', 'o'],
    #            [' ', 'o', 'o'],
    #            ['x', 'o', 'x']]
    # gm.print_pool()
    # print(gm.check_game_final(gm.pool))
    # print(gm.help())
    # print(gm.run_cpu())
    # print(gm.print_pool())


if __name__=='__main__':
    test()
