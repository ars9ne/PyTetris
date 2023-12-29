import random
import sys
import time
import os
# Размеры поля
import keyboard
import socket
import pickle

sleep_interval = 2
online_game = False
server_state = False
print("Добро пожаловать в игру Тетрис, выберите режим игры:\n1) Одиночная игра\n2) Сетевая игра")
choice = int(input())
if choice == 1:
    pass
elif choice == 2:
    online_game = True
    print("1) Создать сервер\n2) Подключиться к игроку")
    choice = int(input())
    if choice == 1:
        server_state = True
        print("Введите ваш ip адрес: ")
        ip = input()
        print("Введите порт: ")
        port = int(input())
        # Создаем сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Привязываем сокет к адресу и порту
        server_socket.bind((ip, port))
        # Переводим сокет в режим прослушивания
        server_socket.listen()
        print("Ожидание подключения клиента...")
        # Принимаем подключение
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент с адреса: {addr}")
    elif choice == 2:
        server_state = True
        print("Введите ip сервера: ")  #
        ip = input()
        print("Введите порт: ")
        port = int(input())
        # Создаем сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Подключаемся к серверу
        client_socket.connect((ip, port))

pause_state = False

h = 20
w = 10
score = 0
opponent_score = 0
playing_field = [[0 for col in range(w)] for row in range(h)]

def set_opponent_score(op_score):
    global opponent_score
    opponent_score = op_score

def print_field(response=None):
    if not online_game:
        state_info = pause_state
        if state_info is True:
            state_info = "PAUSE"
        else:
            state_info = ""
        for i in range(0, len(playing_field)):
            # print(str(playing_field[i]) + str(i))
            print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))
        print(f"\n YOUR SCORE: {score} {state_info}")
        # print(str(playing_field[i]).replace('0', ' ').replace(',', ' '))
    elif online_game:
        state_info = pause_state
        if state_info is True:
            state_info = "PAUSE"
        else:
            state_info = ""

        # Определяем максимальную длину строк для правильного форматирования
        max_len = max(len(str(playing_field[i])) for i in range(len(playing_field)))

        for i in range(len(playing_field)):
            # Форматируем строку из основного поля
            playing_field_str = str(playing_field[i]).replace('0', ' ').replace(',', ' ')

            # Если response предоставлен, добавляем его в вывод
            if response and i < len(response):
                response_str = str(response[i]).replace('0', ' ').replace(',', ' ')
                print(f"{playing_field_str:<{max_len}}    {response_str}")
            else:
                print(playing_field_str)

        print(f"\n YOUR SCORE: {score} {state_info}                  OPPONENT SCORE: {opponent_score}")


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
                    if online_game:
                        # Закрываем соединение
                        client_socket.close()
                        server_socket.close()
                    sys.exit()

        for i in range(len(playing_field)):
            if i == self.position[0]:
                for j in range(len(self.shape)):
                    for k in range(len(self.shape[0])):
                        playing_field[j][k + self.position[1]] = 1

    def check_boundary(self, direction):
        if direction == "down":
            for i in range(len(self.shape[0])):
                # (playing_field[self.position[0]][len(self.shape) + 1] == 2) or
                if self.position[0] + len(self.shape) >= 20:  # проверяем не достигла ли фигура последней линии
                    self.set_static()
                    return False
                else:
                    # проверка на коллизию со статичными блоками:
                    for ti in range(len(self.shape[0])):
                        for tj in range(len(self.shape)):
                            if (playing_field[self.position[0] + tj + 1][self.position[1] + ti] == 2 and self.shape[tj][
                                ti] != 0):  # or (playing_field[self.position[0] + len(self.shape)][self.position[1] + ti] == 2 and self.shape[tj][ti] != 0)
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
                        if self.position[1] + j - 1 < 0 or playing_field[self.position[0] + i][
                            self.position[1] + j - 1] == 2:
                            return False
            return True

        elif direction == "right":
            if self.position[1] + len(self.shape[0]) >= w:
                return False
            for i in range(len(self.shape)):
                for j in range(len(self.shape[i])):
                    if self.shape[i][j] != 0:
                        if self.position[1] + j + 1 >= w or playing_field[self.position[0] + i][
                            self.position[1] + j + 1] == 2:
                            return False
            return True

        elif direction == "rotate":
            new_shape = list(zip(*self.shape[::-1]))
            for i in range(len(new_shape)):
                for j in range(len(new_shape[i])):
                    if new_shape[i][j] != 0:
                        new_x = self.position[0] + i
                        new_y = self.position[1] + j
                        if new_y < 0 or new_y >= w or new_x < 0 or new_x >= h or playing_field[new_x][new_y] == 2:
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
            if self.check_boundary(direction):
                clear_ones()
                self.shape = list(zip(*self.shape[::-1]))
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


r1 = None
def set_r1(response):
    global r1
    r1 = response
    pass


def on_key_press(event):
    global pause_state
    if pause_state:
        if event.name == "p":
            pause_state = False
    elif Figure1.is_active and not pause_state:
        if event.name == "a":
            Figure1.move("left")
        elif event.name == "d":
            Figure1.move("right")
        elif event.name == "s":
            Figure1.move("down")
        elif event.name == "r":
            Figure1.move("rotate")
        os.system('cls||clear')
        if not online_game:
            print_field()
        elif online_game:
            os.system('cls||clear')
            print_field(r1)

        if event.name == "p" and not online_game:
            pause_state = True


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


def send_data():
    if server_state:
        data_to_send = {
            "field": playing_field,
            "score": score
        }
        # Кодируем данные для отправки
        encoded_data = pickle.dumps(data_to_send)
        # Отправляем данные
        client_socket.send(encoded_data)
        #time.sleep(0.1)
    else:
        pass
    pass





Figure1 = Figure(shapes[3])
# print(len(Figure1.get_shape()))
Figure1.spawn()
print_field()
Figure1.move("down")
print_field()
os.system('cls||clear')
if online_game:
    sleep_interval = sleep_interval / 2


def start_game():
    global Figure1
    while True:
        if not pause_state:
            if Figure1.is_active:
                Figure1.move("down")
            else:
                Figure1 = Figure(shapes[random.randint(0, 6)])
                Figure1.position = [0, 4]
                Figure1.is_active = True
                Figure1.spawn()
        # online
        if not server_state and online_game:
            received_data = client_socket.recv(2048)
            # Декодирование данных
            response = pickle.loads(received_data)
            pl1 = response['field']
            o_score = response['score']
            set_opponent_score(o_score)
            print_field(pl1)
        if not online_game:
            print_field()
        if online_game and server_state:
            send_data()
        check_full_lines()
        if not server_state and online_game:
            user_data = playing_field
            # Сериализация данных клиента
            serialized_data = pickle.dumps(user_data)
            # Отправка данных серверу
            client_socket.sendall(serialized_data)
        if online_game:
            time.sleep(0.1)
            received_data = client_socket.recv(2048)
            response = pickle.loads(received_data)
            pl1 = response['field']
            o_score = response['score']
            set_opponent_score(o_score)
            set_r1(pl1)
        os.system('cls||clear')
        print_field(r1)
        time.sleep(sleep_interval)


if __name__ == "__main__":
    start_game()
