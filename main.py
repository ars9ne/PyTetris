# Размеры поля
h = 20
w = 10

playing_field = [[0 for col in range(w)] for row in range(h)]
def print_field():
    for i in range(0, len(playing_field)):
        print(str(playing_field[i]) + str(i))
        # print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))

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
        for i in range(len(playing_field)):
            if i == self.position[0]:
                # Вставка фигуры на игровое поле
                for j in range(len(self.shape)):
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
print((Figure1.get_shape()))
Figure1.spawn()
print_field()


