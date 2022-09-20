import pygame
import random
import math
import numpy as np

elements = {0: 'none', 1: 'metal', 2: 'wood', 3: 'earth', 4: 'aqua', 5: 'flame', 6: 'metal'}
usage = {1: 'attack', 2: 'defend', 3: 'cure', 4: 'self_atk_up', 5: 'enemy_atk_down', 6: 'enemy_defe_down',
         7: 'enemy_control', 8: 'watch_enemy_card', 9: 'self_cost_up'}
Buffs = {1: 'atk_up', 2: 'defe_up', 3: 'atk_down', 4: 'defe_down', 5: 'bleeded', 6: 'recover', 7: 'burnt', 8: 'drown',
         9: 'cost_up', 10: 'under_control'}
Names = {'01': 'Attack', '02': 'Defend', '03': 'Cure', '08': 'Aerial Eye', '112': 'Nameless Fan',
         '116': 'Roaming Cloud', '114': 'Unlimited Blade Works', '21': 'Insertion', '225': 'Stand',
         '2135': 'The Advert of Tree Kingdom',
         '51': 'Fire Ball', '52': "Fire Wall", '5123': 'Phoenix'}


class card:
    def __init__(self, code):  # 最多四位的字符串，用数字编码功能
        self.element = int(code[0])
        self.usages = list(map(int, list(code[1:])))
        self.name = Names[code]
        self.imagePath = f'../cards/{code}.png'
        self.picture = pygame.image.load(self.imagePath)
        self.user = None
        self.object = None
        self.intro = (self.name+': ')+' '.join(usage[u] for u in self.usages)

    def __str__(self):
        effs = ''.join([usage[u] + ' ' for u in self.usages])
        s = f'element:{elements[self.element]},effect={effs}'
        return s

    def get_image_path(self):
        return self.imagePath

    def work(self, player, enemy):
        self.user = player
        self.object = enemy
        for u in self.usages:
            if u == 1:
                self.attack(u)
            elif u == 3:
                self.user.current_HP = min(self.user.total_HP, self.user.current_HP + 8)
            self.buffon(self.element, u)
        self.buff_cont()
        return self.user, self.object

    def attack(self, u):
        if self.user.current_HP > 0 and self.object.current_HP > 0 and u == 1:
            dmg = self.user.atk - self.object.defe
            self.object.current_HP -= dmg

    def watch(self):
        print('enemy\'s hand_card:\n')
        for card1 in self.object.hand_card:
            print(card(card1))

    def remove_debuff(self, ele):
        self.user.buffs.sort()
        for buff in self.user.buffs:
            if buff[0] == ele + 1 and (buff[1] in [3, 4, 5, 7, 8, 10]):
                buff[2] = 0  # 可以这么用吗？

    def remove_buff(self, ele):
        self.object.buffs.sort()
        for buff in self.object.buffs:
            if buff[0] == ele + 1 and buff[1] in [1, 2, 6]:
                buff[2] = 0

    def buffon(self, ele, u):
        buff_turns = 2
        if self.user.current_HP > 0 and self.object.current_HP > 0:
            # 功能debuff
            if u == 5:
                self.object.buffs.append([ele, 3, buff_turns])  # 元素，buff类型，buff持续回合

            if u == 6:
                self.object.buffs.append([ele, 4, buff_turns])

            if u == 7:
                self.object.buffs.append([ele, 10, buff_turns])
                p = random.random()
                if p <= 0.7:
                    self.object.active = False  # 控

            if u == 4:
                self.user.buffs.append([ele, 1, buff_turns])

            elif u == 2:
                self.user.buffs.append([ele, 2, buff_turns])

            elif u == 9:
                self.user.buffs.append([ele, 9, buff_turns])
                self.user.cost += 2

            # 属性buff
            if elements[ele] == 'flame':
                if u == 1:
                    self.remove_buff(ele)
                    self.object.buffs.append([ele, 7, buff_turns])
                elif u == 2 or u == 3:
                    self.remove_debuff(ele)

            elif elements[ele] == 'aqua':
                if u == 1 or u == 7:
                    self.remove_buff(ele)
                    self.object.buffs.append([ele, 8, buff_turns])
                elif u == 2 or u == 3:
                    self.remove_debuff(ele)

            elif elements[ele] == 'wood':

                self.user.buffs.append([ele, 6, buff_turns])
                if u == 1:
                    self.remove_buff(ele)
                    self.object.buffs.append([ele, 5, buff_turns])
                elif u == 2 or u == 3:
                    self.remove_debuff(ele)

            elif elements[ele] == 'metal':  # 因为1和6都是金，所以给自己加buff的时候是6，破别人buff的时候是1

                self.user.buffs.append([6, 1, buff_turns])
                if u == 1:
                    self.remove_buff(1)
                if u == 2:
                    self.remove_debuff(1)

            elif elements[ele] == 'earth':
                self.remove_buff(ele)
                self.user.buffs.append([ele, 2, buff_turns])
                if u == 2 or u == 3:
                    self.remove_debuff(ele)

    def buff_cont(self):
        atk_para = 1
        defe_para = 1
        self.user.buffs.sort()

        atk_buff = 0
        defe_buff = 0
        HP_buff = 0
        for buff in self.user.buffs:
            atk_buff = atk_buff + 1 if Buffs[buff[1]] == 'atk_up' else atk_buff - 1 if Buffs[buff[
                1]] == 'atk_down' else atk_buff
            defe_buff = defe_buff + 1 if Buffs[buff[1]] == 'defe_up' else defe_buff - 1 if Buffs[buff[
                1]] == 'defe_down' else defe_buff
            HP_buff = HP_buff + 1 if (Buffs[buff[1]] == 'recover') else HP_buff - 1 if (
                    Buffs[buff[1]] == 'burnt' or Buffs[buff[1]] == 'bleeded') else HP_buff
            if buff[1] == 8:
                p = random.random()
                if p <= 0.3:
                    self.user.active = False
            if buff[1] == 10:
                self.user.active = False

            buff[2] -= 1
        self.user.atk = self.user.ori_atk + atk_buff * atk_para
        self.user.defe = self.user.ori_defe + defe_buff * defe_para
        self.user.current_HP = min(self.user.current_HP + HP_buff * 5, self.user.total_HP)
        self.user.buffs = [buff for buff in self.user.buffs if buff[2] > 0]


# class people:
#     def __init__(self, ele, name):
#         if ele == 0:
#             self.card_deck = ['51', '41', '4126', '22', '5127', '3127', '08', '2146']
#         self.level = 1
#         self.name = name
#         self.hand_card = []
#         self.drop_card = []
#         self.cost = self.level if self.level <= 5 else 5
#         self.cost_now = self.cost
#         self.buffs = []
#         self.ori_atk = 15 * self.level
#         self.atk = self.ori_atk
#         self.max_HP = 50
#         self.HP = self.max_HP
#         self.ori_defe = 5 * self.level
#         self.defe = self.ori_defe
#         self.active = True
#
#     def draw(self):
#         random.shuffle(self.card_deck)
#         while len(self.hand_card) < 5:
#             if not self.card_deck:
#                 self.card_deck, self.drop_card = self.drop_card, self.card_deck
#             self.hand_card.append(self.card_deck.pop())
#
#     def select(self):
#         card_num = input('please press 1~5 to select your card\n')
#         card_num = int(card_num)
#         assert card_num in range(1, 6)
#         return self.hand_card.pop(card_num - 1)
#
#
# def main():
#     p1 = people(0, 'me')
#     p2 = people(0, 'sb')
#
#     while p1.HP > 0 and p2.HP > 0:
#
#         p1.draw()  # 每回合将卡抽到5张
#         p2.draw()
#
#         print('your hand_card:\n')
#
#         for c in p1.hand_card:
#             c1 = card(c)
#             print(c1)
#
#         if p1.active:
#             out_code = p1.select()
#             card_out = card(out_code)
#             p1.drop_card.append(out_code)
#
#             print('chosen card:')
#             print(card_out)
#             p1, p2 = card_out.work(p1, p2)
#             card_out.buff_cont()
#         else:
#             print('you have been controled')
#             p1.active = True
#         print('your buff')
#         for buff in p1.buffs:
#             print(f'{elements[buff[0]]} {Buffs[buff[1]]} {buff[2]}')
#
#         if p2.active:
#             ecard = p2.hand_card.pop(random.randrange(0, 5))  # 抽卡
#             enemy_card = card(ecard)  # 印卡
#             print(enemy_card)
#             p1.drop_card.append(ecard)  # 卡放入弃牌堆
#             p2, p1 = enemy_card.work(p2, p1)  # 卡打出效果
#             enemy_card.buff_cont()  # 结算自己的buff
#         else:
#             print('enemy has been controled')
#             p2.active = True
#         print('enemy\'s buff')
#         for buff in p2.buffs:
#             print(f'{elements[buff[0]]} {Buffs[buff[1]]} {buff[2]}')
#
#
# if __name__ == '__main__':
#     main()
