from tkinter import *
from tkinter import messagebox
import copy
import random



def draw_fig():  # загружаем изображения пешек
    global peshki
    i1 = PhotoImage(file="peshmod\\white.jpg")
    i2 = PhotoImage(file="peshmod\\black.jpg")
    peshki = [0, i1, 0, i2, 0]


def new_game():  # новая игра
    global f_hi
    f_hi = True  # право хода
    global field
    field = [[3, 1, 3, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 3, 1, 3]]


def draw(x_poz_1, y_poz_1, x_poz_2, y_poz_2):  # рисуем игровое поле
    global peshki
    global field
    global red_line, green_line
    k = 100
    x = 0
    desk.delete('all')
    red_line = desk.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    green_line = desk.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x < 4 * k:  # рисуем доску
        y = 1 * k
        while y < 4 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 4 * k:  # рисуем доску
        y = 0
        while y < 4 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(4):  # рисуем стоячие пешки
        for x in range(4):
            z = field[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):  # стоячие пешки
                    desk.create_image(x * k, y * k, anchor=NW, image=peshki[z])
    # рисуем активную пешку
    z = field[y_poz_1][x_poz_1]
    if z:
        desk.create_image(x_poz_2 * k, y_poz_2 * k, anchor=NW, image=peshki[z])

def pozici_1(event):  # выбор клетки для хода 1
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    desk.coords(green_line, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке


def pozici_2(event):  # выбор клетки для хода 2
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    if field[y][x] == 1 or field[y][x] == 3:  # проверяем пешку игрока в выбранной клетке
        desk.coords(red_line, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:  # клетка выбрана
            poz2_x, poz2_y = x, y
            if f_hi:  # ход игрока1
                hod_igroka()
                if check_if_win():
                    return
            if not (f_hi):  # ход игрока2
                if enemy == 1:
                    hod_ii()  # передаём ход
                if enemy == 2:
                    hod_igroka2()
                check_if_win()

            poz1_x = -1  # клетка не выбрана
            desk.coords(red_line, -5, -5, -5, -5)  # рамка вне поля


def hod_ii():             #случайный ход бота
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    f_hi = not f_hi
    y = random.randint(0, 3)
    x = random.randint(0, 3)
    while True:
        flag = False
        while field[y][x] != 3:  # ищем клетку с пешкой бота
            y = random.randint(0, 3)
            x = random.randint(0, 3)
        for ix, iy in (0, -1), (1, 0), (0, 1), (-1, 0):
            if 0 <= y + iy <= 3 and 0 <= x + ix <= 3:
                if field[y + iy][x + ix] == 0:
                    flag = True
                    break
        if flag:
            break
        else:
            y = random.randint(0,3)
            x = random.randint(0,3)
    ix = random.randint(-1, 1)  # генерация случайного хода
    iy = random.randint(-1, 1)
    if iy != 0:          #исключаем ходы по диагонали
        ix = 0
    if ix != 0:
        iy = 0
    while not (0 <= y + iy <= 3 and 0 <= x + ix <= 3) or field[y + iy][x + ix] != 0:   #проверяем ход на правила игры
        ix = random.randint(-1, 1)
        iy = random.randint(-1, 1)
        if iy != 0:
            ix = 0
        if ix != 0:
            iy = 0
    poz2_x, poz2_y = x+ix, y+iy
    poz1_x, poz1_y = x, y
    hod(1, poz1_x, poz1_y, poz2_x, poz2_y)  # делаем ход
    desk.update()  # обновление

def hod_igroka():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    f_hi = not f_hi
    spisok = prosmotr_hodov_i()
    if spisok:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:  # проверяем ход на соответствие правилам игры
            hod(1, poz1_x, poz1_y, poz2_x, poz2_y)  # делаем ход
        else:
            f_hi = not f_hi  # считаем ход игрока невыполненным
    desk.update()  # обновление


def hod_igroka2():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    f_hi = not f_hi
    spisok = prosmotr_hodov_i2()
    if spisok:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:  # проверяем ход на соответствие правилам игры
            hod(1, poz1_x, poz1_y, poz2_x, poz2_y)  # делаем ход
        else:
            f_hi = not f_hi  # считаем ход игрока невыполненным
    desk.update()  # обновление

def hod(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global field
    if f:
        draw(poz1_x, poz1_y, poz2_x, poz2_y)  # рисуем игровое поле
    field[poz2_y][poz2_x] = field[poz1_y][poz1_x]
    field[poz1_y][poz1_x] = 0

def check_if_win():
    winner = 0
    for y in range(4):
        for x in range(4):
            if (y == 0 and (x == 1 or x == 2)) or (
                    y == 3 and (x == 1 or x == 2)):  # верхние и нижние(справа и слева смотрит)
                if field[y][x] == 1:
                    if field[y][x + 1] == field[y][x - 1] == 1:
                        winner = 1
                elif field[y][x] == 3:
                    if field[y][x + 1] == field[y][x - 1] == 3:
                        winner = 3
            elif ((y == 1 or y == 2) and (x == 0)) or (
                    (y == 1 or y == 2) and (x == 3)):  # правые и левые(сверху и снизу смотрит)
                if field[y][x] == 1:
                    if field[y + 1][x] == field[y - 1][x] == 1:
                        winner = 1
                elif field[y][x] == 3:
                    if field[y + 1][x] == field[y - 1][x] == 3:
                        winner = 3
            elif (y == x == 1) or (y == x == 2) or (y == 1 and x == 2) or (
                    y == 2 and x == 1):  # центральные(смотрит сверху и снизу, слева и справа, по диагоналям)
                if field[y][x] == 1:
                    if field[y][x - 1] == field[y][x + 1] == 1:
                        winner = 1
                    elif field[y - 1][x] == field[y + 1][x] == 1:
                        winner = 1
                    elif field[y - 1][x - 1] == field[y + 1][x + 1] == 1:
                        winner = 1
                    elif field[y - 1][x + 1] == field[y + 1][x - 1] == 1:
                        winner = 1
                elif field[y][x] == 3:
                    if field[y][x - 1] == field[y][x + 1] == 3:
                        winner = 3
                    elif field[y - 1][x] == field[y + 1][x] == 3:
                        winner = 3
                    elif field[y - 1][x - 1] == field[y + 1][x + 1] == 3:
                        winner = 3
                    elif field[y - 1][x + 1] == field[y + 1][x - 1] == 3:
                        winner = 3
    if winner == 1:
        messagebox.showinfo("Winner", "white winner!")
        new_game()
        draw(-1, -1, -1, -1)  # рисуем игровое поле
        return True
    elif winner == 3:
        messagebox.showinfo("Winner", "black winner!")
        new_game()
        draw(-1, -1, -1, -1)  # рисуем игровое поле
        return True
    return False

def prosmotr_hodov_i():  # проверка наличия ходов игрока 1
    spisok = []
    for y in range(4):  # сканируем всё поле
        for x in range(4):
            if field[y][x] == 1:  # пешка 1
                for ix, iy in (0, -1), (1, 0), (0, 1), (-1, 0):
                    if 0 <= y + iy <= 3 and 0 <= x + ix <= 3:
                        if field[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
    return spisok

def prosmotr_hodov_i2():  # проверка наличия ходов игрока 2
    spisok = []
    for y in range(4):  # сканируем всё поле
        for x in range(4):
            if field[y][x] == 3:  # пешка2
                for ix, iy in (0, -1), (1, 0), (0, 1), (-1, 0):
                    if 0 <= y + iy <= 3 and 0 <= x + ix <= 3:
                        if field[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка

    return spisok

def start(gamemode):
    global main_win
    global desk
    global enemy
    global poz1_x
    main_win = Tk()  # создаём окно
    main_win.title('Так Тиль')  # заголовок окна
    desk = Canvas(main_win, width=400, height=400, bg='#FFFFFF')
    desk.pack()
    enemy = gamemode  # выбор противника, если значение 1,то бот, если 2-игрок
    poz1_x = -1  # клетка не задана
    draw_fig()  # загружаем изображения пешек
    new_game()  # начинаем новую игру
    draw(-1, -1, -1, -1)  # рисуем игровое поле
    desk.bind("<Motion>", pozici_1)  # движение мышки по полю
    desk.bind("<Button-1>", pozici_2)  # нажатие левой кнопки

    mainloop()

if __name__ == "__main__":
    start(2)