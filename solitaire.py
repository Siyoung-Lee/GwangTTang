import pygame
import random
import time
import game_framework

import hwatwo_solitaire

from pico2d import *

display_width = 1200
display_height = 700

# ----------------------
BLACK = (93, 93, 93)
GRAY = (140, 140, 140)
# -----------------------
hwatwo = False

back_img = pygame.image.load("poker_cards\\back.png")
if hwatwo:
    back_img = pygame.image.load("hwatwo_cards\\back.png")

main_img = pygame.image.load("main1.png")
clock = pygame.time.Clock()

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption("Solitaire")

class Moved_card(object):

    moved = False
    # the screen.
    moved_card = []
    card_d = ()
    cards = None

    def click_up(self, deck_list):

        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, Deck_2):
                    if item.check_pos() and item.check_card(self.moved_card):
                        item.add_card(self.moved_card)
                        self.moved = False
                        self.moved_card = []
                        if isinstance(self.cards, Deck_1):
                            self.cards.show_card()
                        self.cards = None
                        break
            else:
                self.cards.add_card(self.moved_card)
                self.moved = False
                self.moved_card = []
                self.cards = None

    def draw(self, screen, card_dict):
        # 옮겨지는 카드 그리기
        if self.moved:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0]
            y = pos[1] - self.card_d[1]
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 30


class Deck(object):

    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 100, 150)

    def check_pos(self):
        # 커서가 카드 위에 있는지 check
        pos = pygame.mouse.get_pos()
        if pos[0] >= self.rect.left and pos[0] <= self.rect.right:
            if pos[1] >= self.rect.top and pos[1] <= self.rect.bottom:
                return True
            else:
                return False
        else:
            return False


class Deck_1(Deck):

    def __init__(self, x, y):
        # call parent's constructor:
        Deck.__init__(self, x, y)
        self.y = y
        self.hidden = []

    def extend_list(self, lst):
        self.hidden.extend(lst)
        self.cards.append(self.hidden.pop())
        if len(self.hidden) > 0:
            for i in range(len(self.hidden)):
                self.rect.top += 30

    def draw_card(self, screen, card_dict):
        # 카드 외곽선
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 100, 150], 2)
        i = self.y
        if len(self.hidden) > 0:
            for item in self.hidden:
                screen.blit(back_img, ([self.rect.left, i], [100, 150]))
                i += 30
        if len(self.cards) > 0:
            for item in self.cards:
                screen.blit(card_dict[item], [self.rect.left, i])
                i += 30

    def add_card(self, card):
        if len(self.cards) > 0 or len(self.hidden) > 0:
            for i in range(len(card)):
                self.rect.top += 30
        else:
            for i in range(len(card)):
                if i > 0:
                    self.rect.top += 30
        self.cards.extend(card)

    def click_down(self, card):

        if len(self.cards) > 0:
            top = self.rect.top
            lst = []
            for i in range(len(self.cards)):
                if self.check_pos():
                    pos = pygame.mouse.get_pos()
                    lst.insert(0, self.cards.pop())
                    card.card_d = (pos[0] - self.rect.left, pos[1] -
                                   self.rect.top)
                    card.moved = True
                    card.cards = self
                    card.moved_card.extend(lst)
                    if len(self.cards) > 0 or len(self.hidden) > 0:
                        self.rect.top -= 30
                    break
                else:
                    lst.insert(0, self.cards.pop())
                    self.rect.top -= 30
            else:
                self.rect.top = top
                self.cards.extend(lst)

    def show_card(self):
        if len(self.cards) == 0 and len(self.hidden) > 0:
            self.cards.append(self.hidden.pop())

    def check_card(self, moved_card):
        card = moved_card[0]
        result = False
        if len(self.cards) == 0:
            if "king" in card:
                result = True
        else:
            if "heart" in card or "diamond" in card:
                if "spade" in self.cards[-1] or "club" in self.cards[-1]:
                    next_card = "X"
                    if "king" in self.cards[-1]:
                        next_card = "queen"
                    elif "queen" in self.cards[-1]:
                        next_card = "jack"
                    elif "jack" in self.cards[-1]:
                        next_card = "10_"
                    elif "10_" in self.cards[-1]:
                        next_card = "9_"
                    elif "9_" in self.cards[-1]:
                        next_card = "8_"
                    elif "8_" in self.cards[-1]:
                        next_card = "7_"
                    elif "7_" in self.cards[-1]:
                        next_card = "6_"
                    elif "6_" in self.cards[-1]:
                        next_card = "5_"
                    elif "5_" in self.cards[-1]:
                        next_card = "4_"
                    elif "4_" in self.cards[-1]:
                        next_card = "3_"
                    elif "3_" in self.cards[-1]:
                        next_card = "2_"
                    elif "2_" in self.cards[-1]:
                        next_card = "ace"

                    if next_card in card:
                        result = True
            elif "heart" in self.cards[-1] or "diamond" in self.cards[-1]:
                next_card = "X"
                if "king" in self.cards[-1]:
                    next_card = "queen"
                elif "queen" in self.cards[-1]:
                    next_card = "jack"
                elif "jack" in self.cards[-1]:
                    next_card = "10_"
                elif "10_" in self.cards[-1]:
                    next_card = "9_"
                elif "9_" in self.cards[-1]:
                    next_card = "8_"
                elif "8_" in self.cards[-1]:
                    next_card = "7_"
                elif "7_" in self.cards[-1]:
                    next_card = "6_"
                elif "6_" in self.cards[-1]:
                    next_card = "5_"
                elif "5_" in self.cards[-1]:
                    next_card = "4_"
                elif "4_" in self.cards[-1]:
                    next_card = "3_"
                elif "3_" in self.cards[-1]:
                    next_card = "2_"
                elif "2_" in self.cards[-1]:
                    next_card = "ace"

                if next_card in card:
                    result = True

        if hwatwo:
            card = moved_card[0]
            result = False
            if len(self.cards) == 0:
                if "12_" in card:
                    result = True
            else:
                if "gwang" in card or "tti" in card:
                    if "basic" in self.cards[-1] or "basic2" in self.cards[-1]:
                        next_card = "X"
                        if "12_" in self.cards[-1]:
                            next_card = "11_"
                        elif "11_" in self.cards[-1]:
                            next_card = "10_"
                        elif "10_" in self.cards[-1]:
                            next_card = "9_"
                        elif "9_" in self.cards[-1]:
                            next_card = "8_"
                        elif "8_" in self.cards[-1]:
                            next_card = "7_"
                        elif "7_" in self.cards[-1]:
                            next_card = "6_"
                        elif "6_" in self.cards[-1]:
                            next_card = "5_"
                        elif "5_" in self.cards[-1]:
                            next_card = "4_"
                        elif "4_" in self.cards[-1]:
                            next_card = "3_"
                        elif "3_" in self.cards[-1]:
                            next_card = "2_"
                        elif "2_" in self.cards[-1]:
                            next_card = "1_"

                        if next_card in card:
                            result = True

                elif "gwang" in self.cards[-1] or "tti" in self.cards[-1]:
                    next_card = "X"
                    if "12_" in self.cards[-1]:
                        next_card = "11_"
                    elif "11_" in self.cards[-1]:
                        next_card = "10_"
                    elif "10_" in self.cards[-1]:
                        next_card = "9_"
                    elif "9_" in self.cards[-1]:
                        next_card = "8_"
                    elif "8_" in self.cards[-1]:
                        next_card = "7_"
                    elif "7_" in self.cards[-1]:
                        next_card = "6_"
                    elif "6_" in self.cards[-1]:
                        next_card = "5_"
                    elif "5_" in self.cards[-1]:
                        next_card = "4_"
                    elif "4_" in self.cards[-1]:
                        next_card = "3_"
                    elif "3_" in self.cards[-1]:
                        next_card = "2_"
                    elif "2_" in self.cards[-1]:
                        next_card = "1_"
                        if next_card in card:
                            result = True

        return result


class Deck_2(Deck):
    def __init__(self, x, y):

        Deck.__init__(self, x, y)
        self.hidden_cards = []
        self.cards_list = []
        self.x = x

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            c = self.cards.pop()
            card.moved_card.append(c)
            self.cards_list.remove(c)
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self
            self.rect.left -= 20
        else:
            pos = pygame.mouse.get_pos()
            flag = False
            if pos[0] >= 100 and pos[0] <= 200:
                if pos[1] >= 50 and pos[1] <= 200:
                    flag = True
            if flag:
                self.rect.left = self.x
                if len(self.hidden_cards) > 0:
                    self.cards = []
                    for i in range(3):
                        c = self.hidden_cards.pop()
                        self.cards_list.insert(0, c)
                        self.cards.append(c)
                        if len(self.hidden_cards) == 0 and i < 2:
                            break

                else:
                    self.hidden_cards.extend(self.cards_list)
                    self.cards_list = []
                    self.cards = []

                if len(self.cards) > 1:
                    for i in range(len(self.cards)):
                        if i > 0:
                            self.rect.left += 20

    def draw_card(self, screen, card_dict):

        x = self.x
        if len(self.hidden_cards) > 0:
            screen.blit(back_img, ([100, 50], [100, 150]))

            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
            screen.blit(back_img, ([100, 50], [100, 150]))

    def add_card(self, card):
        self.cards.extend(card)
        self.cards_list.extend(card)
        self.rect.left += 20


class Deck_3(Deck):

    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:3] == 'ace':
                    result = True
            else:
                suit = self.cards[0][4:]
                next_card = ''
                if suit in card:
                    if 'ace' in self.cards[-1]:
                        next_card = '2_' + suit
                    elif '2_' in self.cards[-1]:
                        next_card = '3_' + suit
                    elif '3_' in self.cards[-1]:
                        next_card = '4_' + suit
                    elif '4_' in self.cards[-1]:
                        next_card = '5_' + suit
                    elif '5_' in self.cards[-1]:
                        next_card = '6_' + suit
                    elif '6_' in self.cards[-1]:
                        next_card = '7_' + suit
                    elif '7_' in self.cards[-1]:
                        next_card = '8_' + suit
                    elif '8_' in self.cards[-1]:
                        next_card = '9_' + suit
                    elif '9_' in self.cards[-1]:
                        next_card = '10_' + suit
                    elif '10_' in self.cards[-1]:
                        next_card = 'jack_' + suit
                    elif 'jack_' in self.cards[-1]:
                        next_card = 'queen_' + suit
                    elif 'queen_' in self.cards[-1]:
                        next_card = 'king_' + suit

                    if next_card == card:
                        result = True
        if hwatwo:
            result = False
            if len(moved_card) == 1:
                card = moved_card[0]
                if len(self.cards) == 0:
                    if card[:2] == '1_':
                        result = True
                else:
                    suit = self.cards[0][5:]
                    next_card = ''
                    if suit in card:
                        if '1_' in self.cards[-1]:
                            next_card = '2_' + suit
                        elif '2_' in self.cards[-1]:
                            next_card = '3_' + suit
                        elif '3_' in self.cards[-1]:
                            next_card = '4_' + suit
                        elif '4_' in self.cards[-1]:
                            next_card = '5_' + suit
                        elif '5_' in self.cards[-1]:
                            next_card = '6_' + suit
                        elif '6_' in self.cards[-1]:
                            next_card = '7_' + suit
                        elif '7_' in self.cards[-1]:
                            next_card = '8_' + suit
                        elif '8_' in self.cards[-1]:
                            next_card = '9_' + suit
                        elif '9_' in self.cards[-1]:
                            next_card = '10_' + suit
                        elif '10_' in self.cards[-1]:
                            next_card = '11' + suit
                        elif '11' in self.cards[-1]:
                            next_card = '12' + suit

        return result

    def click_down(self, card):

        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):

        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 100, 150], 2)
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])


def shuffle_cards():
    """This shuffle the cards"""
    r = []
    lst = ["ace_club", "2_club", "3_club", "4_club", "5_club", "6_club",
           "7_club", "8_club", "9_club", "10_club", "jack_club", "queen_club",
           "king_club", "ace_spade", "2_spade", "3_spade", "4_spade",
           "5_spade", "6_spade", "7_spade", "8_spade", "9_spade", "10_spade",
           "jack_spade", "queen_spade", "king_spade", "ace_heart", "2_heart",
           "3_heart", "4_heart", "5_heart", "6_heart", "7_heart", "8_heart",
           "9_heart", "10_heart", "jack_heart", "queen_heart", "king_heart",
           "ace_diamond", "2_diamond", "3_diamond", "4_diamond", "5_diamond",
           "6_diamond", "7_diamond", "8_diamond", "9_diamond", "10_diamond",
           "jack_diamond", "queen_diamond", "king_diamond"]
    if hwatwo:
        r = []
        lst = ["1_basic", "1_basic2", "1_tti", "1_gwang",
               "2_basic", "2_basic2", "2_tti", "2_gwang",
               "3_basic", "3_basic2", "3_tti", "3_gwang",
               "4_basic", "4_basic2", "4_tti", "4_gwang",
               "5_basic", "5_basic2", "5_tti", "5_gwang",
               "6_basic", "6_basic2", "6_tti", "6_gwang",
               "7_basic", "7_basic2", "7_tti", "7_gwang",
               "8_basic", "8_basic2", "8_tti", "8_gwang",
               "9_basic", "9_basic2", "9_tti", "9_gwang",
               "10_basic", "10_basic2", "10_tti", "10_gwang",
               "11_basic", "11_basic2", "11_tti", "11_gwang",
               "12_basic", "12_basic2", "12_tti", "12_gwang",
               ]
    length = len(lst)
    for i in range(length):
        if len(lst) > 1:
            c = random.choice(lst)
            r.append(c)
            lst.remove(c)
        else:
            c = lst.pop()
            r.append(c)

    return r

# ==========================================================================================


def hwatwo_version():
    hwatwo = True

    while hwatwo:
        screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()






# ============================================intro=========================================
def game_intro():
    intro = True
    pygame.init()

    #screen = pygame.display.set_mode([display_width, display_height])

    while intro:
        screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

                if event.key == pygame.K_s:
                    intro = False
                    hwatwo_version()


        screen.blit(main_img, [0, 0])
        pygame.display.flip()

        clock.tick(10)

game_intro()


def main():
    pygame.init()
    intro = False

    # 끄기 버튼 누를 때까지의 loop
    done = False

    # 스크린 업데이트 시 걸리는 시간
    clock = pygame.time.Clock()

    # ============================카드 그리기=================================
    card_dict = {}
    img = pygame.image.load("poker_cards/ace_club.png").convert()
    card_dict["ace_club"] = img
    img = pygame.image.load("poker_cards/2_club.png").convert()
    card_dict["2_club"] = img
    img = pygame.image.load("poker_cards/3_club.png").convert()
    card_dict["3_club"] = img
    img = pygame.image.load("poker_cards/4_club.png").convert()
    card_dict["4_club"] = img
    img = pygame.image.load("poker_cards/5_club.png").convert()
    card_dict["5_club"] = img
    img = pygame.image.load("poker_cards/6_club.png").convert()
    card_dict["6_club"] = img
    img = pygame.image.load("poker_cards/7_club.png").convert()
    card_dict["7_club"] = img
    img = pygame.image.load("poker_cards/8_club.png").convert()
    card_dict["8_club"] = img
    img = pygame.image.load("poker_cards/9_club.png").convert()
    card_dict["9_club"] = img
    img = pygame.image.load("poker_cards/10_club.png").convert()
    card_dict["10_club"] = img
    img = pygame.image.load("poker_cards/jack_club.png").convert()
    card_dict["jack_club"] = img
    img = pygame.image.load("poker_cards/queen_club.png").convert()
    card_dict["queen_club"] = img
    img = pygame.image.load("poker_cards/king_club.png").convert()
    card_dict["king_club"] = img
    img = pygame.image.load("poker_cards/ace_spade.png").convert()
    card_dict["ace_spade"] = img
    img = pygame.image.load("poker_cards/2_spade.png").convert()
    card_dict["2_spade"] = img
    img = pygame.image.load("poker_cards/3_spade.png").convert()
    card_dict["3_spade"] = img
    img = pygame.image.load("poker_cards/4_spade.png").convert()
    card_dict["4_spade"] = img
    img = pygame.image.load("poker_cards/5_spade.png").convert()
    card_dict["5_spade"] = img
    img = pygame.image.load("poker_cards/6_spade.png").convert()
    card_dict["6_spade"] = img
    img = pygame.image.load("poker_cards/7_spade.png").convert()
    card_dict["7_spade"] = img
    img = pygame.image.load("poker_cards/8_spade.png").convert()
    card_dict["8_spade"] = img
    img = pygame.image.load("poker_cards/9_spade.png").convert()
    card_dict["9_spade"] = img
    img = pygame.image.load("poker_cards/10_spade.png").convert()
    card_dict["10_spade"] = img
    img = pygame.image.load("poker_cards/jack_spade.png").convert()
    card_dict["jack_spade"] = img
    img = pygame.image.load("poker_cards/queen_spade.png").convert()
    card_dict["queen_spade"] = img
    img = pygame.image.load("poker_cards/king_spade.png").convert()
    card_dict["king_spade"] = img
    img = pygame.image.load("poker_cards/ace_heart.png").convert()
    card_dict["ace_heart"] = img
    img = pygame.image.load("poker_cards/2_heart.png").convert()
    card_dict["2_heart"] = img
    img = pygame.image.load("poker_cards/3_heart.png").convert()
    card_dict["3_heart"] = img
    img = pygame.image.load("poker_cards/4_heart.png").convert()
    card_dict["4_heart"] = img
    img = pygame.image.load("poker_cards/5_heart.png").convert()
    card_dict["5_heart"] = img
    img = pygame.image.load("poker_cards/6_heart.png").convert()
    card_dict["6_heart"] = img
    img = pygame.image.load("poker_cards/7_heart.png").convert()
    card_dict["7_heart"] = img
    img = pygame.image.load("poker_cards/8_heart.png").convert()
    card_dict["8_heart"] = img
    img = pygame.image.load("poker_cards/9_heart.png").convert()
    card_dict["9_heart"] = img
    img = pygame.image.load("poker_cards/10_heart.png").convert()
    card_dict["10_heart"] = img
    img = pygame.image.load("poker_cards/jack_heart.png").convert()
    card_dict["jack_heart"] = img
    img = pygame.image.load("poker_cards/queen_heart.png").convert()
    card_dict["queen_heart"] = img
    img = pygame.image.load("poker_cards/king_heart.png").convert()
    card_dict["king_heart"] = img
    img = pygame.image.load("poker_cards/ace_diamond.png").convert()
    card_dict["ace_diamond"] = img
    img = pygame.image.load("poker_cards/2_diamond.png").convert()
    card_dict["2_diamond"] = img
    img = pygame.image.load("poker_cards/3_diamond.png").convert()
    card_dict["3_diamond"] = img
    img = pygame.image.load("poker_cards/4_diamond.png").convert()
    card_dict["4_diamond"] = img
    img = pygame.image.load("poker_cards/5_diamond.png").convert()
    card_dict["5_diamond"] = img
    img = pygame.image.load("poker_cards/6_diamond.png").convert()
    card_dict["6_diamond"] = img
    img = pygame.image.load("poker_cards/7_diamond.png").convert()
    card_dict["7_diamond"] = img
    img = pygame.image.load("poker_cards/8_diamond.png").convert()
    card_dict["8_diamond"] = img
    img = pygame.image.load("poker_cards/9_diamond.png").convert()
    card_dict["9_diamond"] = img
    img = pygame.image.load("poker_cards/10_diamond.png").convert()
    card_dict["10_diamond"] = img
    img = pygame.image.load("poker_cards/jack_diamond.png").convert()
    card_dict["jack_diamond"] = img
    img = pygame.image.load("poker_cards/queen_diamond.png").convert()
    card_dict["queen_diamond"] = img
    img = pygame.image.load("poker_cards/king_diamond.png").convert()
    card_dict["king_diamond"] = img
    # ==========================================================================

    card_list = shuffle_cards()
    # 카드 좌표 지정
    deck_list = [Deck_2(250, 50), Deck_1(240, 230), Deck_1(350, 230), Deck_1(470, 230),
                 Deck_1(590, 230), Deck_1(710, 230), Deck_1(830, 230), Deck_1(950, 230),
                 Deck_3(590, 50), Deck_3(710, 50), Deck_3(830, 50), Deck_3(950, 50)]
    m_card = Moved_card()

    deck_list[1].extend_list(card_list[:1])
    del card_list[:1]
    deck_list[2].extend_list(card_list[:2])
    del card_list[:2]
    deck_list[3].extend_list(card_list[:3])
    del card_list[:3]
    deck_list[4].extend_list(card_list[:4])
    del card_list[:4]
    deck_list[5].extend_list(card_list[:5])
    del card_list[:5]
    deck_list[6].extend_list(card_list[:6])
    del card_list[:6]
    deck_list[7].extend_list(card_list[:7])
    del card_list[:7]

    deck_list[0].hidden_cards.extend(card_list)
    game_over = False
    font = pygame.font.Font(None, 25)
    text = font.render("Congratulations, You Won!", True, BLACK)

    if hwatwo:
        card_dict = {}
        hwatwo_img = pygame.image.load("hwatwo_cards/1_basic.png").convert()
        card_dict["1_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/1_basic2.png").convert()
        card_dict["1_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/1_gwang.png").convert()
        card_dict["1_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/1_tti.png").convert()
        card_dict["1_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/2_basic.png").convert()
        card_dict["2_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/2_basic2.png").convert()
        card_dict["2_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/2_gwang.png").convert()
        card_dict["2_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/2_tti.png").convert()
        card_dict["2_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/3_basic.png").convert()
        card_dict["3_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/3_basic2.png").convert()
        card_dict["3_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/3_gwang.png").convert()
        card_dict["3_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/3_tti.png").convert()
        card_dict["3_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/4_basic.png").convert()
        card_dict["4_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/4_basic2.png").convert()
        card_dict["4_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/4_gwang.png").convert()
        card_dict["4_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/4_tti.png").convert()
        card_dict["4_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/5_basic.png").convert()
        card_dict["5_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/5_basic2.png").convert()
        card_dict["5_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/5_gwang.png").convert()
        card_dict["5_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/5_tti.png").convert()
        card_dict["5_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/6_basic.png").convert()
        card_dict["6_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/6_basic2.png").convert()
        card_dict["6_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/6_gwang.png").convert()
        card_dict["6_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/6_tti.png").convert()
        card_dict["6_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/7_basic.png").convert()
        card_dict["7_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/7_basic2.png").convert()
        card_dict["7_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/7_gwang.png").convert()
        card_dict["7_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/7_tti.png").convert()
        card_dict["7_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/8_basic.png").convert()
        card_dict["8_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/8_basic2.png").convert()
        card_dict["8_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/8_gwang.png").convert()
        card_dict["8_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/8_tti.png").convert()
        card_dict["8_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/9_basic.png").convert()
        card_dict["9_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/9_basic2.png").convert()
        card_dict["9_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/9_gwang.png").convert()
        card_dict["9_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/9_tti.png").convert()
        card_dict["9_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/10_basic.png").convert()
        card_dict["10_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/10_basic2.png").convert()
        card_dict["10_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/10_gwang.png").convert()
        card_dict["10_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/10_tti.png").convert()
        card_dict["10_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/11_basic.png").convert()
        card_dict["11_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/11_basic2.png").convert()
        card_dict["11_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/11_gwang.png").convert()
        card_dict["11_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/11_tti.png").convert()
        card_dict["11_tti"] = hwatwo_img

        hwatwo_img = pygame.image.load("hwatwo_cards/12_basic.png").convert()
        card_dict["12_basic"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/12_basic2.png").convert()
        card_dict["12_basic2"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/12_gwang.png").convert()
        card_dict["12_gwang"] = hwatwo_img
        hwatwo_img = pygame.image.load("hwatwo_cards/12_tti.png").convert()
        card_dict["12_tti"] = hwatwo_img
        # ==========================================================================


        card_list = shuffle_cards()
        # 카드 좌표 지정
        deck_list = [Deck_2(250, 50), Deck_1(240, 230), Deck_1(350, 230), Deck_1(470, 230),
                     Deck_1(590, 230), Deck_1(710, 230), Deck_1(830, 230), Deck_1(950, 230),
                     Deck_3(590, 50), Deck_3(710, 50), Deck_3(830, 50), Deck_3(950, 50)]
        m_card = Moved_card()

        deck_list[1].extend_list(card_list[:1])
        del card_list[:1]
        deck_list[2].extend_list(card_list[:2])
        del card_list[:2]
        deck_list[3].extend_list(card_list[:3])
        del card_list[:3]
        deck_list[4].extend_list(card_list[:4])
        del card_list[:4]
        deck_list[5].extend_list(card_list[:5])
        del card_list[:5]
        deck_list[6].extend_list(card_list[:6])
        del card_list[:6]
        deck_list[7].extend_list(card_list[:7])
        del card_list[:7]

        deck_list[0].hidden_cards.extend(card_list)
        game_over = False

    # ------------------------------------------------------- -----------
    while not done:
        screen.fill(0)

        # 메인루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in deck_list:
                    item.click_down(m_card)

            if event.type == pygame.MOUSEBUTTONUP:
                m_card.click_up(deck_list)

        # 게임 로직
        for item in deck_list:
            if isinstance(item, Deck_3):
                if len(item.cards) != 13:
                    break
        else:
            game_over = True

        screen.fill((GRAY))


        # 카드 drawing
        for item in deck_list:
            item.draw_card(screen, card_dict)
        m_card.draw(screen, card_dict)
        if game_over:
            pygame.draw.rect(screen, BLACK, [245, 246, 250, 25])
            screen.blit(text, [250, 250])

        pygame.display.flip()

        clock.tick(20)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
