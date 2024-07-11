#импорт бибилотек, необходимых для задания
import pygame as pg
from math import pi, sin, cos
from sympy import fourier_series



# параметры цвета
white = (255, 255, 255)
gray = (100, 100, 100)
canvas = (0, 0, 51)

#radius_scale - радиус гравной окружности
radius_scale = 100



#Парметры окна
def main():
    time = 0
    path = []

    pg.init()
    pg.font.init()
    font = pg.font.SysFont('Times New Roman', 24)
    pg.display.set_caption("Ряд Фурье, Каширина Мария ПИ22-4")

    # параметры окна
    width = 3500
    height = 3500

    #старовая точка
    start_x = 500
    start_y = 500

    wave_x = 700

    #настройки по умолчанию
    #terms - кол-во членов, step - шаг анимации
    terms = 1
    step = 0.05
    max_points = 2000



    #инициализация экрана
    screen = pg.display.set_mode((width, height))



    #Управление увеличением членов ряда и скорости
    running = True
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    running = False
                if keys[pg.K_UP]:
                    terms += 1
                if keys[pg.K_DOWN] and terms > 1:
                    terms -= 1
                if keys[pg.K_LEFT] and step > 0.001:
                    step = step - 0.005
                if keys[pg.K_RIGHT]:
                    step = step + 0.005

        #начальные точки для создания анимации
        x = start_x
        y = start_y

        # координаты центра точки
        pg.draw.circle(screen, (255, 255, 255), (round(x), round(y)), 3)

        #создание списков для создания визуализации
        circles = []
        lines = [(start_x, start_y)]

        #нахождение линий и кругов
        for i in range(0, terms):
            prev_x = x
            prev_y = y
            n = 2 * i + 1
            radius = radius_scale * (4 / (n * pi))



            if abs(radius) < 1:
                terms -= 1
                break


            x += radius * cos(n * time)
            y += radius * sin(n * time)

            circles.append(((round(prev_x), round(prev_y)), round(abs(radius))))
            lines.append((x, y))


        #отрисовка кругов с учетом вычислений
        for circle in circles:
            pg.draw.circle(screen, gray, circle[0], circle[1], 2)

        #отрисовка линий с учетом вычислений
        for i in range(0, len(lines) - 1):
            pg.draw.line(screen, white, lines[i], lines[i + 1], 2)


        pg.draw.line(screen, gray, (x, y), (wave_x, y), 2)
        path = add_point(path, [wave_x, y], step * 50, max_points)
        draw_path(screen, path)

        #Ряд Фурье
        from sympy.abc import x
        f = fourier_series(-x, (x, -1, 1))
        te = f.truncate(terms)
        text2 = font.render(str(te), True, 'white')

        #Добавление текста с количеством членов ряда
        text_ab = font.render("Кол-во членов ряда Фурье: ", True, 'red')
        screen.blit(text_ab, [200, 700])
        text_speed = font.render(str(terms), True, 'red')
        screen.blit(text_speed, [650, 700])

        #Добавление текста со скоростью анимации
        text_ab1 = font.render("Скорость анимации: ", True, 'red')
        screen.blit(text_ab1, [700, 700])
        text_step = font.render(str(step), True, 'red')
        screen.blit(text_step, [1000, 700])

        #Добавление названия проекта и суммы ряда Фурье
        text = font.render("Визуализация ряда Фурье", True, 'pink')
        text_1 = font.render("Cумма ряда Фурье:  ", True, 'red')
        screen.blit(text, [500, 50])

        screen.blit(text_1, [100, 100])
        screen.blit(text2, [100, 150])





        #Обновление информации на экране
        pg.display.update()
        screen.fill(canvas)
        time += step





def add_point(new, point, x_increment, max_points):
    new = [[point[0] + x_increment, point[1]] for point in new]
    new.insert(0, point)
    return new[:max_points]

def draw_path(screen, new):
    if len(new) > 1:
        pg.draw.lines(screen, white, False, new, 2)

def message_box(root, font, text):
    pos = 10
    for x in range(len(text)):
        rendered = font.render(text[x], 0, white)
        root.blit(rendered, (10, pos))
        pos += 30


#Проверка запущен скрипт напрямую или нет
if __name__ == "__main__":
    main()