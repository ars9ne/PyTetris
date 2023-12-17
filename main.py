import random
import sys
import time
import os
# Размеры поля
import keyboard

h = 20
w = 10
score = 0
playing_field = [[0 for col in range(w)] for row in range(h)]


def print_field():
    for i in range(0, len(playing_field)):
        #print(str(playing_field[i]) + str(i))
        print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))
    print(f"\n YOUR SCORE: {score}")
    # print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))


def clear_ones():  # очищает все активные блоки (для перемещения)
    for ki in range(len(playing_field)):
        for kj in range(len(playing_field[0])):
            if playing_field[ki][kj] == 1:
                playing_field[ki][kj] = 0


class Figure(object):
    def __init__(self, shape, is_active=True):
        self.shape = shape
        self.is_active = is_active
        self.position = [0, 4]  # позиция верхнего левого кубика фигуры

    def get_shape(self):
        return self.shape

    def set_static(self):
        # Превращение активной фигуры в статичную
        for ki in range(len(playing_field)):
            for kj in range(len(playing_field[0])):
                if playing_field[ki][kj] == 1:
                    playing_field[ki][kj] = 2
        self.is_active = False

    def get_position(self):
        return self.position

    def spawn(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] != 0 and playing_field[i][self.position[1] + j] == 2:
                    print("GAME OVER")
                    print(f"FINAL SCORE: {score}")
                    time.sleep(10)
                    sys.exit()

        for i in range(len(playing_field)):
            if i == self.position[0]:
                for j in range(len(self.shape)):
                    for k in range(len(self.shape[0])):
                        playing_field[j][k + self.position[1]] = 1

    def check_boundary(self, direction):
        if direction == "down":
            for i in range(len(self.shape[0])):
                #(playing_field[self.position[0]][len(self.shape) + 1] == 2) or
                if self.position[0] + len(self.shape) >= 20: #проверяем не достигла ли фигура последней линии
                    self.set_static()
                    return False
                else:
                    # проверка на коллизию со статичными блоками:
                    for ti in range(len(self.shape[0])):
                        for tj in range(len(self.shape)):
                            if (playing_field[self.position[0] + tj + 1][self.position[1] + ti] == 2 and self.shape[tj][ti] != 0): # or (playing_field[self.position[0] + len(self.shape)][self.position[1] + ti] == 2 and self.shape[tj][ti] != 0)
                                self.set_static()
                                return False
            if (playing_field[self.position[0]][len(self.shape) + 1] != 2) or (len(self.shape) + 1 < 20):
                return True
        elif direction == "left":
            if self.position[1] <= 0:
                return False
            for i in range(len(self.shape)):
                for j in range(len(self.shape[i])):
                    if self.shape[i][j] != 0:
                        if self.position[1] + j - 1 < 0 or playing_field[self.position[0] + i][self.position[1] + j - 1] == 2:
                            return False
            return True

        elif direction == "right":
            if self.position[1] + len(self.shape[0]) >= w:
                return False
            for i in range(len(self.shape)):
                for j in range(len(self.shape[i])):
                    if self.shape[i][j] != 0:
                        if self.position[1] + j + 1 >= w or playing_field[self.position[0] + i][self.position[1] + j + 1] == 2:
                            return False
            return True

    def insert_figure(self):
        # Вставка фигуры на игровое поле
        for j in range(self.position[0], len(self.shape) + self.position[0]):
            for k in range(len(self.shape[0])):
                if self.shape[j - self.position[0]][k] != 0:
                    playing_field[j][k + self.position[1]] = 1

    def move(self, direction):
        if direction == "down":
            if self.check_boundary(direction):
                clear_ones()
                self.position[0] = self.position[0] + 1
                for i in range(len(playing_field)):
                    if i == self.position[0]:
                        # Вставка фигуры на игровое поле
                        self.insert_figure()
        elif direction == "left":
            if self.check_boundary(direction):
                clear_ones()
                self.position[1] = self.position[1] - 1
                self.insert_figure()
        elif direction == "right":
            if self.check_boundary(direction):
                clear_ones()
                self.position[1] = self.position[1] + 1
                self.insert_figure()
        elif direction == "rotate":
            self.shape = list(zip(*self.shape))[::-1]
            clear_ones()
            self.insert_figure()


shapes = [
    [
        [1],
        [1],
        [1],
        [1]  # I shape
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]  # J shape
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]  # L shape
    ],
    [
        [1, 1],
        [1, 1]  # O shape
    ],
    [
        [1, 1, 0],
        [0, 1, 1]  # Z shape
    ],
    [
        [1, 1, 1],
        [0, 1, 0]  # T shape
    ],
    [
        [0, 1, 1],
        [1, 1, 0]  # S shape
    ]
]


def on_key_press(event):
    if Figure1.is_active:
        if event.name == "a":
            Figure1.move("left")
        elif event.name == "d":
            Figure1.move("right")
        elif event.name == "s":
            Figure1.move("down")
        elif event.name == "r":
            Figure1.move("rotate")
        os.system('cls||clear')
        print_field()


def check_full_lines():
    global score
    global playing_field
    for i in range(len(playing_field)):
        if all(cell == 2 for cell in playing_field[i]):
            for j in range(len(playing_field[i])):
                playing_field[i][j] = 0
            for k in range(i, 0, -1):
                playing_field[k] = playing_field[k - 1]
            playing_field[0] = [0 for _ in range(w)]
            score += 50


keyboard.on_press(on_key_press)

Figure1 = Figure(shapes[3])
# print(len(Figure1.get_shape()))
Figure1.spawn()
print_field()
Figure1.move("down")
print_field()
os.system('cls||clear')
while True:
    print_field()
    if Figure1.is_active:
        Figure1.move("down")
    else:
        Figure1 = Figure(shapes[random.randint(0, 6)])
        Figure1.position = [0, 4]
        Figure1.is_active = True
        Figure1.spawn()
    time.sleep(2)
    check_full_lines()
    os.system('cls||clear')
