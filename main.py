import sys
import time
import os
# Размеры поля
import keyboard

h = 20
w = 10

playing_field = [[0 for col in range(w)] for row in range(h)]
def print_field():
    for i in range(0, len(playing_field)):
        print(str(playing_field[i]) + str(i))
    print('\n')
    # print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))


def clear_ones(): #очищает все активные блоки (для перемещения)
    for ki in range(len(playing_field)):
        for kj in range(len(playing_field[0])):
            if playing_field[ki][kj] == 1:
                playing_field[ki][kj] = 0


class Figure(object):
    def __init__(self, shape, is_active=False):
        self.shape = shape
        self.is_active = is_active
        self.position = [0, 4]

    def get_shape(self):
        return self.shape

    def get_position(self):
        return self.position

    def spawn(self):
        for i in range(len(playing_field)):
            if i == self.position[0]:
                # Вставка фигуры на игровое поле
                for j in range(len(self.shape)):
                    for k in range(len(self.shape[0])):
                        playing_field[j][k + self.position[1]] = 1


    def move(self, direction):
        if direction == "down":
            clear_ones()
            self.position[0] = self.position[0] + 1
            for i in range(len(playing_field)):
                if i == self.position[0]:
                    # Вставка фигуры на игровое поле
                    for j in range(self.position[0],len(self.shape)+self.position[0]):
                        for k in range(len(self.shape[0])):
                            playing_field[j][k + self.position[1]] = 1
        elif direction == "left":
            clear_ones()
            self.position[1] = self.position[1] - 1
            for i in range(len(playing_field)):
                if i == self.position[0]:
                    # Вставка фигуры на игровое поле
                    for j in range(self.position[0], len(self.shape) + self.position[0]):
                        for k in range(len(self.shape[0])):
                            playing_field[j][k + self.position[1]] = 1
        elif direction == "right":
            clear_ones()
            self.position[1] = self.position[1] + 1
            for i in range(len(playing_field)):
                if i == self.position[0]:
                    # Вставка фигуры на игровое поле
                    for j in range(self.position[0], len(self.shape) + self.position[0]):
                        for k in range(len(self.shape[0])):
                            playing_field[j][k + self.position[1]] = 1


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

Figure1 = Figure(shapes[3])
#print((Figure1.get_shape()))
Figure1.spawn()
print_field()
Figure1.move("down")
print_field()
while True:
    print_field()
    time.sleep(0.5)
    Figure1.move("down")
    if keyboard.is_pressed("a"):
        Figure1.move("left")
    elif keyboard.is_pressed("d"):
        Figure1.move("right")
    time.sleep(0.5)
    os.system('cls||clear')