import os
import pygame.display
from Dialogs import Dialog
from fight_main import fight
from fight_scene import *
from main import ROW, COL, BLOCK, BORDER
from card import card

SPEED = 8
pygame.display.init()

card_will_get = [['5123', '51', '52'], ['112', '116', '114'], ['21', '225', '2135']]


class Character:
    def __init__(self, name, code):

        if code == 0:
            self.block = [0, 0]
            self.chara = 'player'
            file_path = '../character/hero/'
            self.chi = 0
        else:
            self.block = [ROW - 1, COL - 1]
            self.chara = 'boss'
            file_path = '../character/boss'+str(code)+'/'

        self.rect = pygame.Rect(self.block[1] * BLOCK + BORDER, self.block[0] * BLOCK + BORDER, 64, 64)
        self.card_deck = [card('01'), card('01'), card('01'), card('02'), card('02'), card('03'), card('03')]
        self.level = 1
        self.name = name
        self.keys = set()
        self.hand_card = []
        self.drop_card = []
        self.attack_se = pygame.mixer.Sound('../bgm/attack.mp3')
        self.cost = self.level if self.level <= 5 else 5
        self.cost_now = self.cost
        self.buffs = []
        self.ori_atk = 15
        self.atk = self.ori_atk
        self.total_HP = 50
        self.current_HP = self.total_HP
        self.ori_defe = 5
        self.defe = self.ori_defe
        self.active = True
        self.dead = False

        dead_pics_file = os.listdir(file_path+'dead')
        static_pics_file = os.listdir(file_path+'stay')
        run_pics_file = os.listdir(file_path+'run')
        self.static_pics = []
        self.run_pics = []
        self.atk_pics = []
        self.dead_pics = []
        self.speed = [0, 0]
        self.time_now = pygame.time.get_ticks()
        for file in static_pics_file:
            img = pygame.image.load(f'{file_path}stay/{file}')
            img.set_colorkey((0, 0, 0))
            self.static_pics.append(img)
        for file in dead_pics_file:
            img = pygame.image.load(f'{file_path}dead/{file}')
            img.set_colorkey((0, 0, 0))
            self.dead_pics.append(img)

        if code == 0:
            for file in run_pics_file:
                img = pygame.image.load(f'{file_path}run/{file}')
                img.set_colorkey((0, 0, 0))
                self.run_pics.append(img)
            atk_pics_file = os.listdir(f'{file_path}attack')
            for file in atk_pics_file:
                img = pygame.image.load(f'{file_path}attack/{file}')
                img.set_colorkey((0, 0, 0))
                self.atk_pics.append(img)

    def shuffle(self):
        random.shuffle(self.card_deck)

    def draw(self):
        random.shuffle(self.card_deck)
        while len(self.hand_card) < 5:
            if not self.card_deck:
                self.card_deck, self.drop_card = self.drop_card, self.card_deck
            self.hand_card.append(self.card_deck.pop())

    def draw_self(self, screen, frame_num, is_moving, is_atk, dead_time):

        if is_moving:
            pic_now = self.run_pics[(frame_num // 3) % (len(self.run_pics))]
            if self.speed[0] < 0:
                pic_now = pygame.transform.flip(pic_now, True, False)

        elif is_atk:
            pic_now = self.atk_pics[(frame_num // 6) % (len(self.atk_pics))]

        elif dead_time > 0 or self.dead:
            self.dead = True
            time_now = pygame.time.get_ticks()
            if time_now - dead_time < 100 * len(self.dead_pics):
                pic_now = self.dead_pics[((time_now - dead_time) // 100) % len(self.dead_pics)]
            else:
                pic_now = self.dead_pics[-1]

        else:
            pic_now = self.static_pics[(frame_num // 10) % (len(self.static_pics))]

        screen.blit(pic_now, (self.rect.left, self.rect.top))

    def move(self, p):
        if p not in range(1, BLOCK // SPEED + 1):
            self.speed = [0, 0]
            return False, 0
        if self.rect.topleft[0] != self.block[0] + BLOCK + BORDER or \
                self.rect.topleft[1] != self.block[1] + BLOCK + BORDER:
            self.rect.move_ip(self.speed[0] * SPEED / BLOCK, self.speed[1] * SPEED / BLOCK)
            return True, p + 1

    def attack(self, maze0):
        dt = 0
        bossdt = 0
        self.attack_se.play()
        for n in maze0.maze.neigh([self.block[1], self.block[0]]):  # 列行转为行列
            if maze0.maze[n] == 2:
                talk = True if maze0.maze.monster_left() == 2 else False
                if talk:
                    d = Dialog(maze0.num, 6)
                    self.infected(d[0])
                res = fight(self, maze0.num, 2)
                if res:
                    if talk:
                        d = Dialog(maze0.num, 7)
                        self.infected(d[0])
                    maze0.maze.kill(n)
                    break
                else:
                    self.dead = True
                    dt = pygame.time.get_ticks()
            elif maze0.maze[n] == 3:
                self.card_deck.append(card(card_will_get[maze0.num - 1][3 - maze0.maze.chest_left()]))
                self.current_HP = self.total_HP
                maze0.maze.kill(n)

            elif maze0.maze[n] == 4:
                kn = Dialog(maze0.num, 2)
                self.infected(kn[0])
                res = fight(self, maze0.num, 4)
                if res:
                    kn = Dialog(maze0.num, 3)
                    self.infected(kn[0])

                    bossdt = pygame.time.get_ticks()
                    maze0.maze.kill(n)
                    break
                else:
                    self.dead = True
                    dt = pygame.time.get_ticks()
            elif maze0.maze[n] == 5:
                kn = Dialog(maze0.num, 5)
                self.infected(kn[0])
        return dt, bossdt

    def battle_end(self):
        self.atk = self.ori_atk
        self.defe = self.ori_defe
        self.current_HP = self.total_HP
        while self.drop_card:
            self.card_deck.append(self.drop_card.pop())
        while self.hand_card:
            self.card_deck.append(self.hand_card.pop())

    def reset(self):
        self.block = [0, 0]
        self.rect = pygame.Rect(self.block[1] * BLOCK + BORDER, self.block[0] * BLOCK + BORDER, 64, 64)

    def check_dire(self, maze, up, left, right, down, moving, p):
        if moving:
            return moving, p
        elif (up or left or right or down) and self.speed == [0, 0] and p == 0:
            if left:
                self.speed = [-BLOCK, 0]
            if right:
                self.speed = [BLOCK, 0]
            if up:
                self.speed = [0, -BLOCK]
            if down:
                self.speed = [0, BLOCK]
            if maze.validpos(self.block, self.speed):  # 合法性判断,x对应数组的列，y坐标对应数组行，注意别弄反了
                self.block[0] += self.speed[0] // BLOCK
                self.block[1] += self.speed[1] // BLOCK
                return True, 1
            else:
                return False, 0
        else:
            return False, 0

    def infected(self, keys):
        if keys[0] is not None:
            for k in keys[0]:
                self.keys.add(k)
        self.chi += keys[1]
