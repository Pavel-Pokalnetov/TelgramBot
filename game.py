import enum


class Order(enum.Enum):
    '''кто ходит'''
    player = 0
    cpu = 1


class Game:
    '''
    игра спички
    на столе 50 спичек
    за ход можно забрать не более 8 спичек
    выигрывает то, забрал последние спички со стола
    '''

    heap: int  # куча спичек
    gamestatus: bool  # состояние игры

    def __init__(self):
        self.gamestatus = False
        '''состояние игрв (продолжается)'''
        self.heap = 50
        '''число спичек в куче'''
        self.act = Order.player
        '''чей ход
        cpu
        player'''

    def action_player(self, count_items):
        ''' ход игрока
        возвращает результат:
            -1 - неверное количество спичек
             0 - игрок сделал ход, игра продолжается
             1 - игрок выиграл
        '''
        if self.gamestatus:
            if count_items < 0 or count_items > 8:
                # игрок взял неверное число спичек
                return [-1]
            elif self.heap-count_items == 0:
                # игрок выиграл
                self.heap = 0
                return [1]
            elif self.heap-count_items < 0:
                # игрок выбрал больше чем есть
                pass
                return [-1]
            else:
                # игрок сделал ход
                self.heap -= count_items
                return [0]
        else:
            pass

    def action_cpu(self):
        '''ход компьютера'''
        if self.gamestatus:
            if self.heap <= 8:
                # компьютер выиграл
                count = self.heap
                self.heap = 0
                return [1, count]
            elif self.heap-9 <= 8:
                # предвыигрышный ход
                count = self.heap-9
                self.heap -= count
                return [0, count]
            else:
                # обычный ход
                count = random.randint(1, 8)
                self.heap -= count
                return [0, count]
        else:
            pass

    def check_game_state():
        '''проверка на конец игры (0 спичек)'''
        return self.heap == 0

    def tik(self, count_matches_player):
        '''циклический ход игры'''
        def matches(number):
            '''
            1 - спичка
            2,3,4 - спички
            5,6,7,8 - спичек
            '''
            result = str(number) + ' спич'
            if number == 1:
                result += 'ка'
            elif 1 < number < 5:
                result += 'ки'
            else:
                result += 'ек'
            return result

        if (self.gamestatus()):
            if act == Order.cpu:
                # ход компьютера
                state = self.action_cpu()
                if state[0] == 1:
                    # компьютер выиграл
                    self.gamestatus = False
                    return ('Ход компьютера - {},\n'
                            'осталось 0 спичек,\n'
                            'Вы проиграли'.format(matches(state[1])))
                else:
                    return ('Ход компьютера - {},\n'
                            'осталось {} спичек,\n'
                            'Ваш ход'.format(matches(state[1]), self.heap))
                act = Order.player
            else:
                # ход игрока
                state = self.action_player(count_matches_player)
                if state[0] == '1':
                    # игрок выиграл
                    self.gamestatus == False
                    return ("Вы выиграли")
                elif state[0] == '0':
                    pass
