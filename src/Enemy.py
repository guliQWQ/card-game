from card import *

enemy_types = {(1, 2): [card('01'), card('01'), card('01'), card('03'), card('02'), card('02'), card('112')],
               (1, 4): [card('01'), card('03'), card('02'), card('01'), card('02'), card('112'), card('116'),
                        card('114')],
               (2, 2): [card('01'), card('02'), card('01'), card('21'), card('21'), card('225')],
               (2, 4): [card('01'), card('02'), card('01'), card('21'), card('21'), card('225'), card('2135')],
               (3, 2): [card('01'), card('51'), card('02'), card('03'), card('51'), card('52')],
               (3, 4): [card('01'), card('02'), card('03'), card('112'), card('225'), card('5123'), card('52')]}

enemy_names = {(1, 2): 'Solider in Qian',
               (1, 4): 'Wen',
               (2, 2): 'Golem',
               (2, 4): 'Xia',
               (3, 2): 'Soldier in Li',
               (3, 4): 'Ka'}


class enemy:
    def __init__(self, num, e_type):
        self.total_HP = num * 10 + 30
        self.card_deck = enemy_types[(num, e_type)].copy()
        self.icon = '../monster/'+str(num)+'.png' if e_type == 2 else f'../monster/boss'+str(num)+'.png'
        self.hand_card = []
        self.drop_card = []
        self.buffs = []
        self.name = enemy_names[(num, e_type)]
        self.ori_atk = 10 + 3 * num
        self.ori_defe = 2 * num
        self.atk = self.ori_atk
        self.defe = self.ori_defe
        self.current_HP = self.total_HP
        self.active = True

    def draw(self):
        random.shuffle(self.card_deck)
        while len(self.hand_card) < 5:
            if not self.card_deck:
                self.card_deck, self.drop_card = self.drop_card, self.card_deck
            self.hand_card.append(self.card_deck.pop())

    def select(self):
        card_num = input('please press 1~5 to select your card\n')
        card_num = int(card_num)
        assert card_num in range(1, 6)
        return self.hand_card.pop(card_num - 1)
