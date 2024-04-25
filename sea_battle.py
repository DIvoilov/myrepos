import random
import numpy as np


class BoardOutException(Exception):
    def __str__(self):
        return "выход за границу карты, сделайте другой ход"


class LengthOutException(Exception):

    def __str__(self):
        return "попытка создать корабли недопустимой длины "


class DirectionException(Exception):
    def __str__(self):
        return "направление должно быть 'g' или 'v' "


class ShipLocalException(Exception):

    def __str__(self):
        return "здесь не может быть установлен корабль"

class ShotOutBoardException(Exception):
    def __str__(self):
        return "вы выстрелили за пределы карты"

class ShotAgainDotException(Exception):
    def __str__(self):
        return "вы уже стреляли в эту точку"
class ShotException(Exception):

    def __str__(self):
        return "неверный формат выстрела"
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False

    def getDot(self):
        return [int(self.x), int(self.y)]
    def getx(self):
        return self.x
    def gety(self):
        return self.y


class Ship:
    def __init__(self, length, first, direction):
        self.length=length
        self.first=first
        self.direction=direction
        self.life = length
    def hit(self):
        self.life -= 1
        if self.life == 0:
            print("корабль уничтожен")
            return 1
        return 0

    def dots(self):
        dots = list()
        dots.append(self.first)
        if self.direction  == 'g':
            for i in range(1,self.length):
                dots.append(Dot(self.first.getx(), self.first.gety() - i))
        elif self.direction  == 'v':
            for i in range(1, self.length):
                dots.append(Dot(self.first.getx()+i, self.first.gety()))
        return dots


class Board:
    def __init__(self, hid=True):
        self.cells = np.zeros((6, 6))
        self.ships = list()
        self.hid = hid
        self.life = 0

    def add_ship(self,length, first, direction):
        if length >= 4 or length < 0:
            raise LengthOutException
        if direction != 'g' and direction != 'v':
            raise DirectionException
        if direction == 'g':
            for i in range(length):
                if not Board.out(dot=Dot(first.getx(), first.gety() - i)):
                    raise BoardOutException
                if self.cells[first.getx(), first.gety() - i] == 1 or self.cells[first.getx(), first.gety() - i] == -1:
                    raise ShipLocalException
        elif direction == 'v':
            for i in range(length):
                if not Board.out(dot=Dot(first.getx() + i, first.gety())):
                    raise BoardOutException
                if self.cells[first.getx() + i, first.gety()] == 1 or self.cells[first.getx() + i,first.gety()] == -1:
                    raise ShipLocalException

        self.ships.append(Ship(length, first, direction))
        for i in range(length):
            if direction == 'g':
                self.cells[first.getx(), first.gety() - i] = 1
            else:
                self.cells[first.getx() + i, first.gety()] = 1
        self.counter(Ship(length, first, direction))

        self.life += 1


    def counter(self, ship):
        dots = ship.dots()
        for dot in dots:
            x = dot.getx()
            y = dot.gety()
            for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if Board.out(dot=Dot(x+i,y+j)):
                        if  self.cells[x + i , y + j] == 0:
                            self.cells[x + i , y + j] = -1


    def display(self):

        if self.hid:
            for i in range(6):
                print('|', end=' ')
                for j in range(6):
                    if self.cells[i, j] == 0 or self.cells[i,j] == -1:
                        print("0 |", end=' ')
                    elif self.cells[i, j] == 2:
                        print("X |",end=' ')
                    elif self.cells[i, j] == 3:
                        print("T |", end=' ')
                    else:
                        print("K |", end=' ')
                print()
        else:
            for i in range(6):
                print('|', end=' ')
                for j in range(6):
                    if self.cells[i, j] == 2:
                        print("X |", end=' ')
                    elif self.cells[i, j] == 3:
                        print("T |", end=' ')
                    else:
                        print("0 |", end=' ')
                print()
    @staticmethod
    def out(dot):
        return True if 0 <= dot.getx() <= 5 and 0 <= dot.gety() <= 5 else False

    def shot(self, dot):
        x = dot.getx()
        y = dot.gety()
        if not Board.out(dot):
            raise ShotOutBoardException
        elif self.cells[x, y] == 2 or self.cells[x,y] == 3:
            raise ShotAgainDotException
        elif self.cells[x,y] == 1:
            self.cells[x, y] = 2
            for ship in self.ships:
                for dots in ship.dots():
                    if dots == dot:
                        f = ship.hit()
                        if f:
                            self.life -= 1
                        break
            return 0
        else:
            self.cells[x, y] = 3
            return 1


    def getlife(self):
        return self.life


class Player:
    def __init__(self):
        self.selfBoard = Board()
        self.hostileBoard = Board()

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                print("Вражеское поле")
                self.hostile_display()
                dot = self.ask()
                f = self.hostileBoard.shot(dot)
                if f:
                    break
            except Exception as e:
                Player.message(e)

    def set_self_board(self, board):
        self.selfBoard = board

    def set_hostil_board(self,board):
        self.hostileBoard = board

    def get_life(self):
        return self.hostileBoard.getlife()

    def self_display(self):
        self.selfBoard.display()

    def hostile_display(self):
        self.hostileBoard.display()
    @staticmethod
    def message(e):
        print(e)
class User(Player):
    def ask(self):
        step = input("Ваш ход")
        step = step.split()
        if len(step) != 2:
            raise ShotException
        return Dot(int(step[0])-1, int(step[1])-1)
    @staticmethod
    def message():
        print("Повторите ход")


class AI(Player):
    def ask(self):
        dot=np.random.randint(0,5,2)
        return Dot(dot[0], dot[1])

class Game:
    def __init__(self):
        self.userboard = Board()
        self.aiboard=Board(False)
        self.user = User()
        self.ai = AI()
    def greet(self):
        print("Добро пожаловать в игру 'Моской бой'. Для начала вам нужно разместить на доску 1 корабль на 3 клетки")
        print("2 корабля на 2 клетки и 4 корабля на 1 клетку, формат ввода: x,y,'k'; где x,y- координаты точки (от 0 до 6)")
        print("а k-это направление корабля горизонтально 'g' или вертикально 'v'. Далее вы будет совершать ходы")
        print("в формате x,y; где x,y - координаты выстрела. Побеждает тот, кто первый собьет все корабли соперника")
    def generate_user_board(self):
        print("Поставь корабль длины 3")
        self.userboard.display()
        while True:
            try:
                s=input()
                s=s.split()
                self.userboard.add_ship(3, Dot(int(s[0])-1, int(s[1])-1), s[2])
                break
            except Exception as e:
                print(e)
                print("Повторите попытку ввода")
        print("Поставь корабль длины 2")
        self.userboard.display()
        while True:
            try:
                s = input()
                s = s.split()
                self.userboard.add_ship(2, Dot(int(s[0])-1, int(s[1])-1), s[2])
                break
            except Exception as e:
                print(e)
                print("Повторите попытку ввода")

        print("Поставь корабль длины 2")
        self.userboard.display()
        while True:
            try:
                s = input()
                s = s.split()
                self.userboard.add_ship(2, Dot(int(s[0])-1, int(s[1])-1), s[2])
                break
            except Exception as e:
                print(e)
                print("Повторите попытку ввода")
        for i in range(4):
            print("Поставь корабль длины 1")
            self.userboard.display()
            while True:
                try:
                    s = input()
                    s = s.split()
                    self.userboard.add_ship(1, Dot(int(s[0])-1, int(s[1])-1), s[2])
                    break
                except Exception as e:
                    print(e)
                    print("Повторите попытку ввода")
        self.user.set_self_board(self.userboard)
        self.ai.set_hostil_board(self.userboard)

    def random_board(self):
        while True:
            s = 10000
            while True:
                try:
                    s -= 1
                    dot=np.random.randint(0, 6, 2)
                    k=random.choice(['g', 'v'])
                    self.aiboard.add_ship(3, Dot(dot[0],dot[1]), k)
                    break
                except Exception as e:
                    if s < 0:
                        break
                    pass
            for i in range(2):
                if s< 0:
                    break
                while True:
                    try:
                        s -= 1
                        dot = np.random.randint(0, 6, 2)
                        k = random.choice(['g', 'v'])
                        self.aiboard.add_ship(2, Dot(dot[0], dot[1]), k)
                        break
                    except Exception as e:
                        if s < 0:
                            break
                        pass
            for i in range(4):
                if s< 0:
                    break
                while True:
                    try:
                        s -= 1
                        dot = np.random.randint(0, 6, 2)
                        self.aiboard.add_ship(1, Dot(dot[0], dot[1]), 'v')
                        break
                    except Exception as e:
                        if s < 0:
                            break
                        pass
            if s > 0:
                self.ai.set_self_board(self.aiboard)
                self.user.set_hostil_board(self.aiboard)
                return
            else:
                self.aiboard=Board()

    def loop(self):
        self.generate_user_board()
        self.random_board()
        k=1
        while True:
            if k:
                self.user.move()
                k-=1
                if self.user.get_life() == 0:
                    print("Вы выиграли")
                    break
            else:
                self.ai.move()
                print("Ваше поле")
                self.user.self_display()
                k+=1
                if self.ai.get_life() == 0:
                    print("Вы проиграли")
                    break
    def start(self):
        self.greet()
        self.loop()

game=Game()
game.start()
