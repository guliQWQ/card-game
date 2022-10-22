import pygame
import numpy as np
import random
from main import ROW, COL, BLOCK, BORDER, SCREEN_WIDTH, SCREEN_HEIGHT

font0 = pygame.font.Font('../icons/CaslonAntique.ttf', 32)
hint = ['direction key: move', 'e: interaction', 'b: open bag', 'r: relive']
hint_sur = pygame.surface.Surface((300, 130))
for h in range(4):
    hint_sur.blit(font0.render(hint[h], True, 'White'), (0, h * 32))
hint_sur.set_colorkey('Black')


class DrawMaze(object):
    def __init__(self, stage):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建屏幕对象
        self.num = stage
        self.maze = MakeMaze(ROW, COL)
        self.back = pygame.image.load("../background/stage@.jpg".replace('@', str(stage))).convert()
        self.road = pygame.image.load("../background/block@.png".replace('@', str(stage))).convert()
        self.monster = pygame.image.load("../monster/@.png".replace('@', str(stage)))
        self.monster.set_colorkey(self.monster.get_at((0, 0)))
        self.chest = pygame.image.load(f"../background/chest.png").convert()
        self.chest.set_colorkey(self.chest.get_at((0, 0)))
        self.next_arrow = pygame.image.load(f"../icons/next_level.png")
        self.chest.set_colorkey(self.chest.get_at((0, 0)))
        self.talk = pygame.image.load(f'../icons/talk.png').convert()
        self.talk.set_colorkey(self.talk.get_at((0, 19)))
        self.blocks = pygame.sprite.Group()
        self.preparing_blocks()
        self.blocks.draw(self.back)
        self.back.blit(hint_sur, (980, 300))

    def display(self):
        self.screen.blit(self.back, (0, 0))
        self.draw_block()

    def draw_block(self):
        # 画迷宫，怪和宝箱
        monster_list = (np.where(np.array(self.maze.maze) == 2))
        chest_list = (np.where(np.array(self.maze.maze) == 3))
        talk = np.squeeze(np.where(np.array(self.maze.maze) == 5))

        for i in range(len(monster_list[0])):
            rect = (monster_list[1][i] * BLOCK + BORDER, monster_list[0][i] * BLOCK + BORDER, BLOCK, BLOCK)
            self.screen.blit(self.monster, rect)
        for i in range(len(chest_list[0])):
            rect = (chest_list[1][i] * BLOCK + BORDER, chest_list[0][i] * BLOCK + BORDER, BLOCK, BLOCK)
            self.screen.blit(self.chest, rect)
        rect = ((talk[1] + 0.5) * BLOCK + BORDER, (talk[0] + 0.5) * BLOCK + BORDER, BLOCK, BLOCK)
        self.screen.blit(self.talk, rect)
        rect = (COL * BLOCK + BORDER + 16, (ROW - 1) * BLOCK + BORDER + 16, 32, 32)
        self.screen.blit(self.next_arrow, rect)

    def preparing_blocks(self):
        blocks = list(np.squeeze(np.where(np.array(self.maze.maze) != 0)).T)
        for b in blocks:
            self.blocks.add(Blocks(self.num, b))


class Blocks(pygame.sprite.Sprite):
    def __init__(self, num, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../background/block"+str(num)+".png").convert()
        self.rect = (pos[1] * self.image.get_width() + BORDER, pos[0] * self.image.get_height() + BORDER,
                     self.image.get_width(), self.image.get_height())


class MakeMaze(object):
    def __init__(self, x, y):
        self.maze = None
        self.width = y
        self.height = x
        self.random_map(x, y)
        self.treasures = ['5127']
        self.put_monsters_chest_talk()

    def __getitem__(self, item: list):
        return self.maze[item[0]][item[1]]

    def print(self):
        print(f'maze with {ROW} rows and {COL} columns')
        print(len(self.maze), len(self.maze[0]))

    def chest_left(self):
        return np.where(np.array(self.maze) == 3)[0].shape[0]

    def monster_left(self):
        return np.where(np.array(self.maze) == 2)[0].shape[0]

    def random_map(self, h, w):
        self.maze = []
        for i in range(h):
            self.maze.append([0] * w)

        cell_now = [0, 0]
        end = [h - 1, w - 1]
        self.maze[h - 1][w - 1] = 1
        self.maze[cell_now[0]][cell_now[1]] = 1

        while end not in self.neigh(cell_now):  # create a way to boss
            cell_now = self.grow(cell_now)

        for i in range(h):
            for j in range(w):
                cell_now = [i, j]
                neigh_now = self.neigh(cell_now)
                nv = self.neigh_visited(neigh_now)

                if self.maze[i][j] == 1 and [i, j] != [0, 0] and [i, j] != [self.height - 1, self.width - 1]:
                    if nv <= len(neigh_now) - 2:  # grow more block
                        self.grow(cell_now)
                    else:  # remove unnecessary block
                        self.maze[i][j] = 0
                        dj_res = self.dj()
                        if len(dj_res[0]) != 0 and self.neigh_visited(self.neigh([i, j])) < 2:
                            self.maze[i][j] = 1
                else:
                    if nv < 2:
                        self.maze[i][j] = 1

        while True:
            dj_res = self.dj()
            if len(dj_res[0]) == 0:
                break
            else:
                _ = self.grow([dj_res[0][0], dj_res[1][0]])

        for i in range(h):
            for j in range(w):
                if self.maze[i][j] == 1 and self.neigh_visited(self.neigh([i, j])) > 1 \
                        and [i, j] != [0, 0] and [i, j] != [self.height - 1, self.width - 1]:
                    self.maze[i][j] = 0
                    dj_res = self.dj()
                    if len(dj_res[0]) != 0:
                        self.maze[i][j] = 1

    def neigh(self, cell_now):
        nes = []
        if cell_now[0] != 0:
            nes.append([cell_now[0] - 1, cell_now[1]])
        if cell_now[0] != self.height - 1:
            nes.append([cell_now[0] + 1, cell_now[1]])
        if cell_now[1] != 0:
            nes.append([cell_now[0], cell_now[1] - 1])
        if cell_now[1] != self.width - 1:
            nes.append([cell_now[0], cell_now[1] + 1])
        return nes

    def grow(self, cell_now):
        neigh_now = self.neigh(cell_now)
        random.shuffle(neigh_now)
        while neigh_now:
            cell_now = neigh_now.pop()
            if self.maze[cell_now[0]][cell_now[1]] == 0:
                self.maze[cell_now[0]][cell_now[1]] = 1
                break
        return cell_now

    def dj(self):
        weight = 10000 * np.array(self.maze)
        stack = [[0, 0]]
        weight[0, 0] = 1
        while stack:
            cell_now = stack.pop()
            neigh_now = self.neigh(cell_now)
            for n in neigh_now:
                if weight[n[0], n[1]] == 10000:
                    stack.append(n)
                    weight[n[0], n[1]] = weight[cell_now[0], cell_now[1]] + 1
        not_connected = (np.where(weight == 10000))
        return not_connected

    def dead_and_path(self, dead):
        for neis in self.neigh(dead):
            if self.maze[neis[0]][neis[1]] == 1:
                return neis

    def neigh_visited(self, ns):
        count = 0
        for n in ns:
            count += self.maze[n[0]][n[1]]
        return count

    # @staticmethod
    def validpos(self, block_now, speed):
        # 判断坐标的有效性，如果超出数组边界或是不满足值为1的条件，说明该点无效返回False，否则返回True
        block_next = [int(block_now[0] + speed[0] / BLOCK), int(block_now[1] + speed[1] / BLOCK)]  # 列行
        if block_next[1] in range(self.height) and block_next[0] in range(self.width) \
                and self.maze[block_next[1]][block_next[0]] == 1:
            return True
        else:
            return False

    def put_monsters_chest_talk(self):
        origin = list(np.squeeze(np.where(np.array(self.maze))).T)
        self.maze[-1][-1] = 4
        dead_end = [p for p in origin if (self.neigh_visited(self.neigh(p)) == 1 and
                                          (p[0] != 0 or p[1] != 0) and self.maze[p[0]][p[1]] != 4)]
        random.shuffle(dead_end)
        i = 0
        for d in dead_end:
            path = self.dead_and_path(d)

            if path is not None:
                self.maze[path[0]][path[1]] = 2
                self.maze[d[0]][d[1]] = 3
                i += 1
            if i >= 3:
                break
        self.maze[dead_end[i][0]][dead_end[i][1]] = 5

    def kill(self, n):
        self.maze[n[0]][n[1]] = 1
