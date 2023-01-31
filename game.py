import enum
from random import randint


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
    help = ('Игра 50 спичек.\n'
            'Правила: на столе лежат 50 спичек. Каждый по очереди берет из кучки от одной до восьми спичек\n'
            'Выигрывает тот, кто заберет последние спички из кучки')

    heap: int  # куча спичек
    gamestatus: bool  # состояние игры

    def __init__(self):
        self.gamestatus = False
        '''состояние игрв (продолжается)'''
        self.heap = 50
        '''число спичек в куче'''
        self.act = Order.player
        '''чей ход: cpu/player'''

    def start(self):
        """старт игры
        """
        self.gamestatus = True
        self.heap = 50

    def stop(self):
        """остановка игры
        """
        self.gamestatus = False

    def action_player(self, count_items):
        """ход игрока
        Args:
            count_items (_type_): число спичек, которые взял игрок

        Returns:
            _type_: возвращает результат:
                -1 - неверное количество спичек
                 0 - игрок сделал ход, игра продолжается
                 1 - игрок выиграл
        """
        if self.gamestatus:
            # игрок сделал ход
            self.heap -= count_items
            return
        else:
            pass

    def action_cpu(self):
        """ход компьютера
        Returns:
            _type_: _description_
        """
        if self.gamestatus:
            if self.heap <= 8:
                # компьютер выиграл
                count = self.heap
                self.heap = 0
                return count
            elif 9 < self.heap < 18:
                # предвыигрышный ход
                count = self.heap-9
                self.heap -= count
                return count
            else:
                # обычный ход
                count = randint(1, 8)
                self.heap -= count
                return count
        else:
            pass

    def check_game_state(self):
        """проверка на конец игры (0 спичек)
        Returns:
            _type_: _description_
        """
        return self.heap == 0
