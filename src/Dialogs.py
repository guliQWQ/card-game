import sys
import pygame.image
from docx import Document

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768


class Dialog:

    def __init__(self, stage, dialog_num):
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(f'../background/stage{stage}.jpg').convert()
        self.texts = Document(f'../dialogs/{stage}_{dialog_num}.docx').paragraphs
        self.textbg = pygame.image.load('../icons/text.png').convert()
        self.textbg.set_colorkey((0, 0, 0))
        self.button = pygame.image.load('../icons/option.png').convert()
        self.talkers = self.texts[0].text.split(' ')
        self.characters = dict()
        self.font = pygame.font.Font('../icons/CaslonAntique.ttf', 30)
        self.textbg.blit(self.font.render('press mouse to next', True, 'White'), (1000, 220))
        for talker in self.talkers:
            self.characters[talker] = pygame.image.load(f'../character/{talker}.png').convert()
            self.characters[talker] = pygame.transform.rotozoom(self.characters[talker], 0,
                                                                500 / self.characters[talker].get_width())
            self.characters[talker].set_colorkey((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        self.infects = self.talk(dialog_num)

    def talk(self, dia_num):
        key = set()
        end = len(self.texts)
        i = 1
        which_side = 0
        while i < end:
            text = self.texts[i]
            self.window.blit(self.background, (0, 0))
            to_next = False
            talker, content = text.text.split(': ')
            iskey = False
            for b in text.runs:
                if b.bold:
                    iskey = True
                    key.add(talker.split('_')[0] + ":" + content)
                    break
            if talker == 'Options':
                opts = content.split('&')
                blame = int(opts[0][-1])  # 第一个选项文本的长度
                opts[0] = opts[0][:-1]
                opt = self.options(opts)
                to_next = True
                if opt == 1:
                    end = i + blame + 1
                    which_side -= 1
                elif opt == 2:
                    i += blame
                    which_side += 1
            else:
                if talker in self.talkers:
                    self.window.blit(self.characters[talker], (50, 0))
                self.gradual_typing(text, 30, 540, iskey)
            i += 1

            while not to_next:
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        to_next = True
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()

            pygame.display.flip()
        if dia_num == 5:
            which_side = 0
        return key, which_side

    def __getitem__(self, item):
        return self.infects

    def __del__(self):
        self.talkers = None
        self.background = None
        self.texts = None

    def gradual_typing(self, content, x, y, iskey):  # txt,字体内容。xy坐标，字体大小（默认30）
        name, txt = content.text.split(': ')
        rendering = ''
        textbox_rect = self.textbg.get_rect(topleft=(0, 485))
        self.window.blit(self.textbg, textbox_rect)
        pygame.display.update()
        texts = []
        row_now = 0
        color = 'Red' if iskey else "Brown"

        for char in txt:
            pygame.time.delay(5)
            pygame.event.clear()
            if self.font.render(rendering + char, True, color).get_width() < self.textbg.get_width() - 50:
                rendering += char
            else:
                row_now += 1
                rendering = '-' + char if rendering[-1].isalpha() and char.isalpha() else char
            rendered_text = self.font.render(rendering, True, color)
            if len(texts) == row_now + 1:
                texts[row_now] = rendered_text
            else:
                texts.append(rendered_text)
            self.window.blit(self.textbg, textbox_rect)
            # name of speaker
            self.window.blit((self.font.render(name.split("_")[0], True, 'Brown')),
                             (textbox_rect.x + 60, textbox_rect.y + 10))
            for i in range(len(texts)):
                self.window.blit(texts[i], (x, y + i * self.font.get_height()))  # textbox_rect

            pygame.display.update()

    def options(self, opts):

        button1 = self.button.copy()
        button2 = self.button.copy()
        opt1 = self.font.render(opts[0], True, 'Black')
        opt2 = self.font.render(opts[1], True, 'Black')
        button1.blit(opt1, opt1.get_rect(center=(button1.get_width() / 2, button1.get_height() / 2)))
        button2.blit(opt2, opt2.get_rect(center=(button1.get_width() / 2, button1.get_height() / 2)))
        not_select = True
        rect1 = self.button.get_rect(center=(SCREEN_WIDTH / 2, 250))
        rect2 = self.button.get_rect(center=(SCREEN_WIDTH / 2, 500))

        while not_select:
            self.window.blit(button1, rect1)
            self.window.blit(button2, rect2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect1.topleft[0] < event.pos[0] < rect1.bottomright[0] and rect1.topleft[1] < event.pos[1] < \
                            rect1.bottomright[1]:
                        return 1
                    elif rect2.topleft[0] < event.pos[0] < rect2.bottomright[0] and rect2.topleft[1] < event.pos[1] < \
                            rect2.bottomright[1]:
                        return 2
                if event.type == pygame.QUIT:
                    sys.exit()
