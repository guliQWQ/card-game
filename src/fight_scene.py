# python3
from mimetypes import suffix_map
import pygame
import Character
import Enemy
import math
from fight_main import *
from card import *
from Character import *
from Enemy import *

font = pygame.font.Font(r'../icons/CaslonAntique.ttf', 28)


class FightStaus:
    def __init__(self):
        self.background = pygame.image.load('../icons/fight_sit.png').convert()
        self.surface = pygame.Surface((self.background.get_width(), 400))
        self.rectp = self.background.get_rect(topleft=(0, 300))
        self.recte = self.background.get_rect(topleft=(0, 0))
        self.surface.set_colorkey((0, 0, 0))

    def show(self, player, enemy0):
        self.surface.blit(self.background, self.rectp)
        self.surface.blit(self.background, self.recte)
        self.surface.blit(font.render(player.name, True, 'White'), (self.rectp.left + 15, self.rectp.top + 15))
        self.surface.blit(font.render(str(math.ceil(player.current_HP)), True, 'White'),
                          (self.rectp.left + 60, self.rectp.top + 50))
        self.surface.blit(font.render(str(math.ceil(player.atk)), True, 'White'),
                          (self.rectp.left + 120, self.rectp.top + 50))
        self.surface.blit(font.render(str(math.ceil(player.defe)), True, 'White'),
                          (self.rectp.left + 180, self.rectp.top + 50))
        self.surface.blit(font.render(enemy0.name, True, 'White'), (self.recte.left + 15, self.recte.top + 15))
        self.surface.blit(font.render(str(math.ceil(enemy0.current_HP)), True, 'White'),
                          (self.recte.left + 60, self.recte.top + 50))
        self.surface.blit(font.render(str(math.ceil(enemy0.atk)), True, 'White'),
                          (self.recte.left + 120, self.recte.top + 50))
        self.surface.blit(font.render(str(math.ceil(enemy0.defe)), True, 'White'),
                          (self.recte.left + 180, self.recte.top + 50))
        return self.surface


class Pile:
    cards = None

    def __init__(self):
        self.cards = []

    def add(self, Card):
        self.cards.append(Card)

    def peek(self):
        if len(self.cards) > 0:
            return self.cards[-1]
        else:
            return None

    def popAll(self):
        return self.cards

    def clear(self):
        self.cards = []

    def isSnap(self):
        if len(self.cards) > 1:
            return self.cards[-1].value == self.cards[-2].value
        return False


class FightingScene:

    def __init__(self, Player, Monster: Enemy.enemy):
        self.Player = Player
        self.Monster = Monster
        self.discard_pile = Pile()
        self.status = pygame.image.load('../icons/fight_sit.png').convert()
        self.surface = pygame.Surface((self.status.get_width(), 400))
        self.rectp = self.status.get_rect(topleft=(0, 450))
        self.recte = self.status.get_rect(topleft=(800, 150))
        self.status.set_colorkey((0, 0, 0))

    def show_status(self, surface):
        surface.blit(self.status, self.rectp)
        surface.blit(self.status, self.recte)
        surface.blit(font.render(self.Player.name, True, 'White'), (self.rectp.left + 15, self.rectp.top + 15))
        surface.blit(font.render(str(math.ceil(self.Player.current_HP)), True, 'White'),
                     (self.rectp.left + 60, self.rectp.top + 50))
        surface.blit(font.render(str(math.ceil(self.Player.atk)), True, 'White'),
                     (self.rectp.left + 120, self.rectp.top + 50))
        surface.blit(font.render(str(math.ceil(self.Player.defe)), True, 'White'),
                     (self.rectp.left + 180, self.rectp.top + 50))
        surface.blit(font.render(self.Monster.name, True, 'White'), (self.recte.left + 15, self.recte.top + 15))
        surface.blit(font.render(str(math.ceil(self.Monster.current_HP)), True, 'White'),
                     (self.recte.left + 60, self.recte.top + 50))
        surface.blit(font.render(str(math.ceil(self.Monster.atk)), True, 'White'),
                     (self.recte.left + 120, self.recte.top + 50))
        surface.blit(font.render(str(math.ceil(self.Monster.defe)), True, 'White'),
                     (self.recte.left + 180, self.recte.top + 50))

    def draw_text(self, surface, text, size, x, y, color):
        font0 = pygame.font.Font(pygame.font.match_font('arial'), size)
        text_surface = font0.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def discard(self, Card):
        self.discard_pile.add(Card)
        Card.move_to_discard_pile()

    def use_card_from_Player(self, card):
        self.Player, self.Monster = card.work(self.Player, self.Monster)

    def use_card_from_Monster(self, card):
        self.Monster, self.Player = card.work(self.Monster, self.Player)

    def load_background(self, surface):
        background = pygame.image.load(r'../background/stage_fight.jpg').convert()
        surface.blit(background, (0, 0))

        enemySurf = pygame.transform.scale(pygame.image.load(self.Monster.icon).convert(), (300, 300))
        enemySurf.set_colorkey(enemySurf.get_at((0, 0)))

        playerRect = enemySurf.get_rect(topleft=(960, 0))
        surface.blit(enemySurf, playerRect)

        playerSurf = pygame.transform.scale(pygame.image.load(r'../character/Player.png').convert(), (300, 300))
        playerSurf.set_colorkey((0, 0, 0))
        playerRect = playerSurf.get_rect(topleft=(960, 450))
        surface.blit(playerSurf, playerRect)

        HPofMonster = pygame.Surface((80, 15))
        HPofMonster.fill((128, 138, 135))
        HPofMonsterRect = HPofMonster.get_rect(topleft=(930, 30))
        surface.blit(HPofMonster, HPofMonsterRect)
        HPofMonster = pygame.Surface((80, 15))
        HPofMonster.fill((0, 0, 0))
        HPofMonsterRect = HPofMonster.get_rect(topleft=(930, 30))
        surface.blit(HPofMonster, HPofMonsterRect)

        HPofMonster = pygame.Surface((80 * (max(self.Monster.current_HP, 0) / self.Monster.total_HP), 15))
        HPofMonster.fill((255, 0, 0))
        HPofMonsterRect = HPofMonster.get_rect(topleft=(930, 30))
        surface.blit(HPofMonster, HPofMonsterRect)

        HPofPlayer = pygame.Surface((80, 15))
        HPofPlayer.fill((128, 138, 135))
        HPofPlayerRect = HPofPlayer.get_rect(topleft=(930, 420))
        surface.blit(HPofPlayer, HPofPlayerRect)
        HPofPlayer = pygame.Surface((80, 15))
        HPofPlayer.fill((0, 0, 0))
        HPofPlayerRect = HPofPlayer.get_rect(topleft=(930, 420))
        surface.blit(HPofPlayer, HPofPlayerRect)

        HPofPlayer = pygame.Surface((80 * (max(self.Player.current_HP, 0) / self.Player.total_HP), 15))
        HPofPlayer.fill((255, 0, 0))
        HPofPlayerRect = HPofPlayer.get_rect(topleft=(930, 420))
        surface.blit(HPofPlayer, HPofPlayerRect)

        DeckImage = pygame.image.load(r'../cards/back.png').convert()
        DeckImage = pygame.transform.rotozoom(DeckImage, 0, 2 / 3)
        Deckplayerimage = pygame.Surface((DeckImage.get_width(), DeckImage.get_height()))
        Deckplayerimage.blit(DeckImage, (0, 0))
        Deckplayerimage.set_colorkey((255, 255, 255))
        DeckplayerRect = Deckplayerimage.get_rect(center=(100, 100))
        surface.blit(Deckplayerimage, DeckplayerRect)

        DeckplayerRect = Deckplayerimage.get_rect(center=(100, 550))
        surface.blit(Deckplayerimage, DeckplayerRect)

        endTurnButton = EndTurnButton(920, 330)
        endTurnButton.draw(surface)

        if len(self.discard_pile.cards) != 0:
            card_showed = self.discard_pile.cards[-1]
            card_showed.draw(surface)


def loadImage(path, newSize=None):
    image = pygame.image.load(path).convert()
    if newSize:
        image = pygame.transform.scale(image, newSize)
    return image


class EndTurnButton:

    def __init__(self, posX, posY):
        self.image = pygame.image.load(r'../icons/button.png').convert()
        self.function = font.render('End Turn', True, 'Red')
        self.rect = self.image.get_rect()
        self.image.blit(self.function, self.function.get_rect(center=self.rect.center))
        self.rect.x = posX
        self.rect.y = posY

    def draw(self, screen):
        screen.blit(self.image, self.rect)
