# python3
from fight_scene import *
from main import SCREEN_WIDTH, SCREEN_HEIGHT
from Enemy import *
import sys


class Cards(pygame.sprite.Sprite):

    def __init__(self, name, effect, image, scale, x, y):
        super().__init__()
        self.name = name
        self.effect = effect
        self.scale = scale
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect(x=x, y=y)
        self.original_rect = self.image.get_rect(x=x, y=y)

    def update(self, rel):
        self.rect.move_ip(rel)

    def originalRec(self):
        self.rect.x = self.original_rect.x
        self.rect.y = self.original_rect.y

    def getRect(self):
        return self.rect

    def move_to_discard_pile(self):
        self.rect.update(60, 400, self.rect.width, self.rect.height)

    def Monster_card_discard_pile(self, image, scale):
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect(x=60, y=200)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def fight(player, num, monster_type):
    caption = 'The Road to Villain'
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(caption)
    monster = enemy(num, monster_type)
    fightS = FightingScene(player, monster)
    fightS.load_background(surface)

    monster_discard_item = None
    fightS.Player.draw()
    start_x = 200
    start_y = 550
    gap = 10
    width = fightS.Player.hand_card[0].picture.get_width() * (2 / 3)

    items = []
    for i in range(5):
        items.append(pygame.sprite.GroupSingle(
            Cards(fightS.Player.hand_card[i].name, fightS.Player.hand_card[i].usages,
                  fightS.Player.hand_card[i].picture, 2 / 3, start_x + (width + gap) * i, start_y)))

    test_if_play = pygame.Rect(start_x, start_y, 720, 200)
    drag = False
    clock = pygame.time.Clock()
    ifquit = False
    etb = EndTurnButton(920, 330)
    discard = 0
    select_card = -1
    played_one_card_this_turn = False
    fs = FightStaus()
    while not ifquit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    click = event.pos
                    if not played_one_card_this_turn:
                        for its in range(5):
                            if items[its].sprite is not None and items[its].sprite.rect.collidepoint(click):
                                drag = True
                                select_card = its

                    else:
                        if etb.rect.collidepoint(click):
                            fightS.Monster.draw()
                            enemy_card = fightS.Monster.hand_card.pop(0)

                            fightS.use_card_from_Monster(enemy_card)
                            monster_discard_item = pygame.sprite.GroupSingle(
                                Cards(enemy_card.name, enemy_card.usages, enemy_card.picture, 2 / 3, 60, 200))

                            fightS.Monster.drop_card.append(enemy_card)

                            select_card = -1
                            played_one_card_this_turn = False
                            player.shuffle()
                            player.draw()
                            items = []
                            for i in range(5):
                                items.append(pygame.sprite.GroupSingle(
                                    Cards(fightS.Player.hand_card[i].name, fightS.Player.hand_card[i].usages,
                                          fightS.Player.hand_card[i].picture, 2 / 3, start_x + (width + gap) * i,
                                          start_y)))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = event.pos

                    if test_if_play.collidepoint(click) and drag:
                        items[select_card].sprite.originalRect()

                    else:
                        if drag:
                            played_one_card_this_turn = True
                            fightS.discard(items[select_card].sprite)
                            items[select_card].empty()

                            card_use = fightS.Player.hand_card.pop(select_card)
                            fightS.use_card_from_Player(card_use)
                            fightS.Player.drop_card.append(card_use)

                    drag = False

            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    items[select_card].update(event.rel)

        fightS.load_background(surface)
        for each in items:
            each.draw(surface)
        if monster_discard_item is not None:
            monster_discard_item.draw(surface)
        surface.blit(fs.show(player, monster), (800, 150))
        pygame.display.update()
        clock.tick(30)

        if fightS.Monster.current_HP <= 0 or player.current_HP <= 0:
            player.battle_end()
            if fightS.Monster.current_HP <= 0:
                return True
            else:
                return False
