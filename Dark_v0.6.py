import pygame
import math


pygame.font.init()

text_win = "You win"
text_info = ""

# TypeGenerater = 0
DebagMod = False

MX = MY = 128

scale = 5  # Масштаб

SX = MX * scale  # Размер экрана исходя из размера плазмы и ее масштаба
SY = MX * scale

line = [0] * MX  # Создаем список из нулей длиной MX


pygame.init()
screen = pygame.display.set_mode((SX, SY))
clock = pygame.time.Clock()
Text1 = pygame.font.Font(None, 36)
Text2 = pygame.font.Font(None, 26)
running = True

Units_coords1 = []  # Координаты частей сущности
Units_coords2 = []  # Координаты частей сущности

MouseArea1 = []
MouseArea2 = []

Areas = []  # Массивы с координатами областей победы, переходов или чего-то еще

Global_coords = []  # Координаты статичных объектов
Effects = []  # Кооррдинаты визуальных эффектов
Objects = []  # Массив с объектами

MAP, MAP_ID = [], [] #карта
MAP_X, MAP_Y = 4, 4
SPAWN = "start"

def choiser_map():  #подключить генератор
    Objects.clear()
    global Global_coords, Areas
    Areas, Global_coords = [], []
    from Dark_maps import maps
    if MAP[MAP_X][MAP_Y]==1:
        for i in maps:
            if i[0][0]["id"] == MAP_ID[MAP_X][MAP_Y]:
                map = i
    else:
        print(">>> Вне карты!")
        for i in maps:
            if i[0][0]["id"] == -1:
                map = i

    for imp_obj in map:
        init_obj(imp_obj)


def init_obj(cell):
    n=0
    if type(cell[0]) is dict:
        """
        if DebagMod:
            print("Name:", cell[0]["MapName"], "\nid:", cell[0]["id"], "\ntype:", cell[0]["type"])
        """
    elif cell[0] == "circle":
        circle(cell[1], cell[2], cell[3])
    elif cell[0] == "player":
        for i in Objects:
            if i.type == "Player":
                n+=1
        if n<1:
            Objects.append(Player(cell[1][SPAWN][0], cell[1][SPAWN][1], cell[1][SPAWN][2]))
    elif cell[0] == "area":
        area(cell[1], cell[2], cell[3], cell[4], cell[5])
    elif cell[0] == "box":
        box(cell[1], cell[2], cell[3], cell[4])
    elif cell[0] == "point":
        point(cell[1], cell[2])
    else:
        print("В сейве хуйня какая-то")


def drawBox(x, y, color):  # отрисовывает пиксель в увеличенном маштабе по сетке 1/5
    pygame.draw.rect(screen, color, (int(x) * 5, int(y) * 5, 5, 5))


def circle(x, y, r):
    posR = []
    for r in range(r - 6, r):
        for i in range(1, 361):
            cord1 = [int(r * math.cos(i)) + x, int(r * math.sin(i)) + y]
            if not (cord1 in posR):
                posR.append(cord1)

    for i in posR:
        if not (i in Global_coords):
            Global_coords.append(i)


def box(x1, y1, x2, y2):
    posR = []
    for i in range(y1, y2 + 1):
        for j in range(x1, x2 + 1):
            posR.append([j, i])

    for i in posR:
        if not (i in Global_coords):
            Global_coords.append(i)


def point(x, y):
    if not ([x, y] in Global_coords):
        Global_coords.append([x, y])


class Player:
    def __init__(self, x, y, r):
        self.type = "Player"
        self.posR1 = []  # координаты точек внешнего круга
        self.posR2 = []  # координаты точек внутреннего круга
        self._posR1 = []
        self.x = x  # x центра
        self.y = y  # y центра
        self.r = r
        self.v_x = 0
        self.v_y = 0

        posR3 = []

        r = self.r // 3 * 2
        for i in range(1, 360):  # внутренний круг
            cord1 = [int(r * math.cos(i)) + self.x, int(r * math.sin(i)) + self.y]
            if not (cord1 in self.posR2):
                self.posR2.append(cord1)

        for i in range(-2, 3):
            for j in range(-2, 3):
                self.posR1.append([self.x + i, self.y + j])

        for i in range(self.r - 2):
            r = self.r + 1 - i
            for i in range(1, 360):
                cord1 = [int(r * math.cos(i)) + self.x, int(r * math.sin(i)) + self.y]
                if not (cord1 in self.posR1):
                    self.posR1.append(cord1)

        for i in self.posR1:
            posR3.append(i)
        self.posR1 = posR3

        self.writecoordsinGList()

    def beta_uppdate(self):
        posR3 = []
        _posR3 = []
        for i in self._posR1:
            self.posR1.append(i)
        for i in range(len(self.posR1)):
            self.posR1[i][0] += self.v_x
            self.posR1[i][1] += self.v_y
        for i in range(len(self.posR2)):
            self.posR2[i][0] += self.v_x
            self.posR2[i][1] += self.v_y

        for i in self.posR1:  # проверка на добавление из глобальных
            if not (i in Global_coords):
                posR3.append(i)
            else:
                _posR3.append(i)
        self.posR1 = posR3
        self._posR1 = _posR3

        self.v_x = 0
        self.v_y = 0

        self.writecoordsinGList()

    def writecoordsinGList(self):
        for i in self.posR1:
            if not (i in Units_coords1):
                Units_coords1.append(i)
        for i in self.posR2:
            if not (i in Units_coords2):
                Units_coords2.append(i)


def area(x1, y1, x2, y2, flag=None): #дописать области
    for i in range(y1, y2 + 1):
        for j in range(x1, x2 + 1):
            Areas.append([j, i, flag])


def restart(seed=-1):
    print()
    global WIN, MAP, MAP_ID, MAP_X, MAP_Y, SPAWN
    WIN = False
    MAP_X, MAP_Y = 4, 4
    SPAWN = "start"

    from Dark_maps import map_generator3
    MAP, MAP_ID = map_generator3(seed)
    choiser_map()

    screen.fill((255, 255, 255))
    pygame.display.flip()




restart(-1)
color = 2
motion = "n"
WIN = False
editing = False
text1 = Text1.render(text_win, True, (180, 0, 0))
text2 = Text2.render(text_info, True, (180, 0, 0))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # смена отображения
            if event.button == 1 and DebagMod:
                print(event.pos[0] // 5, event.pos[1] // 5)
                if editing:
                    MouseArea1 = [event.pos[0] // 5, event.pos[1] // 5]
            if event.button == 2 and DebagMod:
                if color == 0:
                    color = 2
                else:
                    color = 0
            if event.button == 3 and DebagMod:
                print(event.pos[0] // 5, event.pos[1] // 5)
                if editing:
                    MouseArea2 = [event.pos[0] // 5, event.pos[1] // 5]
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and DebagMod:
                print(event.pos[0] // 5, event.pos[1] // 5)
                if editing and len(MouseArea1) == 2:
                    x1, y1, x2, y2 = MouseArea1[0], MouseArea1[1], event.pos[0] // 5, event.pos[1] // 5
                    x1, x2, y1, y2 = sorted([x1, x2])[0], sorted([x1, x2])[1], sorted([y1, y2])[0], sorted([y1, y2])[1]
                    box(x1, y1, x2, y2)
                    MouseArea1 = []
            if event.button == 3 and DebagMod:
                print(event.pos[0] // 5, event.pos[1] // 5)
                if editing and len(MouseArea2) == 2:
                    x1, y1, x2, y2 = MouseArea2[0], MouseArea2[1], event.pos[0] // 5, event.pos[1] // 5
                    x1, x2, y1, y2 = sorted([x1, x2])[0], sorted([x1, x2])[1], sorted([y1, y2])[0], sorted([y1, y2])[1]
                    posR = []
                    for i in range(y1, y2 + 1):
                        for j in range(x1, x2 + 1):
                            posR.append([j, i])
                    for i in posR:
                        if i in Global_coords:
                            Global_coords.remove(i)
                    MouseArea2 = []

        if event.type == pygame.KEYDOWN:  # перезапуск по r и автовин
            if event.key == pygame.K_h and DebagMod:
                WIN = True
            if event.key == pygame.K_1:
                if not (DebagMod):
                    DebagMod = True
                    text_info += "DebagModON "
                    text2 = Text2.render(text_info, True, (180, 0, 0))
            if event.key == pygame.K_2 and DebagMod:
                if not (editing):
                    editing = True
                    text_info += "Edit "
                    text2 = Text2.render(text_info, True, (180, 0, 0))
            if event.key == pygame.K_RETURN and DebagMod and editing:
                save = []
                for i in Global_coords:
                    save.append(["point", i[0], i[1]])
                print(save)
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s:
                Units_coords1.clear()
                Units_coords2.clear()
                for pl in Objects:
                    if pl.type == "Player":
                        if event.key == pygame.K_w:
                            motion = "w"
                        if event.key == pygame.K_s:
                            motion = "s"
                        if event.key == pygame.K_a:
                            motion = "a"
                        if event.key == pygame.K_d:
                            motion = "d"
        if event.type == pygame.KEYUP:
            motion = "n"

    if WIN:
        screen.fill((255, 255, 255))
        screen.blit(text1, (270, 280))
        screen.blit(text2, (3, 3))
        pygame.display.flip()
        # pygame.time.delay(10)
        continue

    screen.fill((0, 0, 0))

    if color != 2:
        for i in Global_coords:  # отрисовка статики
            drawBox(i[0], i[1], [205, 205, 205])
        for i in Areas:  # отрисовка статики
            if i[-1] != "win":
                drawBox(i[0], i[1], [0, 0, 255])

    for pl in Objects:
        if pl.type == "Player":
            Units_coords1.clear()
            Units_coords2.clear()
            n = 0
            for i in pl.posR2:
                if [i[0], i[1], "win"] in Areas:
                    WIN = True
            if motion == "w":
                for i in pl.posR2:
                    if i[1] < 0:
                        MAP_X-=1
                        SPAWN = "down"
                        choiser_map()
                        break
                    if [i[0], i[1] - 1] in Global_coords or i[1] < 0:
                        n += 1

                if n == 0:
                    pl.v_y = -1
                else:
                    pl.v_y = 1
            if motion == "s":
                for i in pl.posR2:
                    if i[1] > 128:
                        MAP_X+=1
                        SPAWN = "up"
                        choiser_map()
                        break
                    if [i[0], i[1] + 1] in Global_coords or i[1] > 128:
                        n += 1
                if n == 0:
                    pl.v_y = 1
                else:
                    pl.v_y = -1
            if motion == "a":
                for i in pl.posR2:
                    if i[0] < 0:
                        MAP_Y-=1
                        SPAWN = "right"
                        choiser_map()
                        break
                    if [i[0] - 1, i[1]] in Global_coords or i[0] < 0:
                        n += 1
                if n == 0:
                    pl.v_x = -1
                else:
                    pl.v_x = 1
            if motion == "d":
                for i in pl.posR2:
                    if i[0] > 128:
                        MAP_Y+=1
                        SPAWN = "left"
                        choiser_map()
                        break
                    if [i[0] + 1, i[1]] in Global_coords or i[0] > 128:
                        n += 1
                if n == 0:
                    pl.v_x = 1
                else:
                    pl.v_x = -1
            pl.beta_uppdate()

    for i in Units_coords1:
        drawBox(i[0], i[1], [255, 255, 255])
    for i in Units_coords2:
        drawBox(i[0], i[1], [200, 200, 200])
    for i in Areas:
        if i[-1] == "win":
            drawBox(i[0], i[1], [0, 255, 0])
    screen.blit(text2, (3, 3))
    clock.tick(45)
    pygame.display.flip()

pygame.quit()
