import enum
from random import random


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
        '''чей ход: cpu/player'''
    def game_start(self):
        self.gamestatus = True
        self.heap = 50

    def action_player(self, count_items):
        """
        ход игрока
        возвращает результат:
            -1 - неверное количество спичек
             0 - игрок сделал ход, игра продолжается
             1 - игрок выиграл

        Args:
            count_items (_type_): _description_

        Returns:
            _type_: _description_
        """

        ''' 

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

