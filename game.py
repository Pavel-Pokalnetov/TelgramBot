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
        self.heap = 50
        self.act = Order.player
        
    def action_player(self, count_items):
        '''
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
        
        if self.gamestatus:
            if self.heap <= 8:
                # компьютер выиграл
                count = self.heap
                self.heap = 0
                return [1, count]
            elif self.heap == 9:
                # компьютер проиграл
                count = random.randint(1, 8)
                self.heap -= count
                return [0, count]
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

    def check_game_state(self):
        return self.heap
    
    def tik(self):
        '''циклический ход игры'''
        if act==Order.cpu:
            # ход компьютера
            pass
        else:
            # ход игрока
            pass
        
        