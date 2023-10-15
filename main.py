import numpy as np


def tic_tac(a):
    if(a == 1):
        return "x"
    elif (a ==- 1):
        return "o"
    else:
        return " "


def display(field):
    m = np.shape(field)
    for i in range(m[0]):
        print('\n')
        for j in range(m[1]):
            if j!=2:
                print(tic_tac(field[i,j]), "| ",end=" ")
            else:
                print(tic_tac(field[i,j]),  end=" ")
    print("\n")


def step(field, state, N):
    player = 0
    if(N % 2 == 0):
        player = 1
    if(player):
        print('Ход крестиков')
    else:
        print('Ход ноликов')
    while True:
        move = input("Введите ячейку (2 числа через пробел)\n")
        move = list(map(int, move.split()))
        if((1 <= move[0]<= 3) and (1 <= move[1]<= 3)):
            if(field[move[0]-1, move[1]-1] == 0):
                if(player):
                    field[move[0]-1, move[1]-1] = 1
                    break
                else:
                    field[move[0]-1, move[1]-1]=-1
                    break
            else:
                print("Эта ячейка занята")
        else:
            print("Недопустимые значения")
    display(field)
    if(player):
        if(state[move[0]*10]==2):
            print("Крестики победили")
            return 1
        state[move[0] * 10] += 1
        if (state[move[1]] == 2):
            print("Крестики победили")
            return 1
        state[move[1]] += 1
        if(move[0]==move[1]):
            if (state[11] == 2):
                print("Крестики победили")
                return 1
            state[11] += 1
            if(move[0]==2):
                if (state[13] == 2):
                    print("Крестики победили")
                    return 1
                state[13]+=1
        if((move[0]==1 and move[1]==3) or (move[0]==3 and move[1]==1)):
            if (state[13] == 2):
                print("Крестики победили")
                return 1
            state[13] += 1
    else:
        if (state[move[0] * 10] == -2):
            print("Нолики победили")
            return 1
        state[move[0] * 10] -= 1
        if (state[move[1]] == -2):
            print("Нолики победили")
            return 1
        state[move[1]] -= 1
        if (move[0] == move[1]):
            if (state[11] == -2):
                print("Нолики победили")
                return 1
            state[11] -= 1
            if (move[0] == 2):
                if (state[13] == -2):
                    print("Нолики победили")
                    return 1
                state[13] -= 1
        if ((move[0] == 1 and move[1] == 3) or (move[0] == 3 and move[1] == 1)):
            if (state[13] == -2):
                print("Крестики победили")
                return 1
            state[13] -= 1
    return 0

state = {10: 0,
         20: 0,
         30: 0,
         1: 0,
         2: 0,
         3: 0,
         11: 0,
         13: 0,
         }
field = np.zeros((3,3))
N = 0
s=0
while N < 9:
    N += 1
    s = step(field, state, N)
    if(s):
        break
if(N==9 and s!=1):
    print('ничья')