import pygame
import random

import hwatwo_solitaire
from pico2d import *

display_width = 1200
display_height = 700

# ----------------------
BLACK = (93, 93, 93)
GRAY = (140, 140, 140)
# -----------------------


back_img = pygame.image.load("poker_cards\\back.png")

main_img = pygame.image.load("main.png")
clock = pygame.time.Clock()

screen = pygame.display.set_mode([display_width, display_height])
pygame.display.set_caption("Solitaire")

class Moved_card(object):

    moved = False
    moved_card = []
    card_d = ()
    cards = None

    def click_up(self, deck_list):

        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, Suggest_Deck):
                    if item.check_pos() and item.check_card(self.moved_card):
                        item.add_card(self.moved_card)
                        self.moved = False
                        self.moved_card = []
                        if isinstance(self.cards, Hidden_Deck):
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


class Hidden_Deck(Deck):    # 엎어져 있는 카드

    def __init__(self, x, y):
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
                if "heart" in self.cards[-1] or "diamond" in self.cards[-1]:
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
            elif "spade" in card or "club" in card:
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

        return result


class Suggest_Deck(Deck):
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


class Collect_Deck(Deck):

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
    dictionary = ["ace_club", "2_club", "3_club", "4_club", "5_club", "6_club",
           "7_club", "8_club", "9_club", "10_club", "jack_club", "queen_club",
           "king_club", "ace_spade", "2_spade", "3_spade", "4_spade",
           "5_spade", "6_spade", "7_spade", "8_spade", "9_spade", "10_spade",
           "jack_spade", "queen_spade", "king_spade", "ace_heart", "2_heart",
           "3_heart", "4_heart", "5_heart", "6_heart", "7_heart", "8_heart",
           "9_heart", "10_heart", "jack_heart", "queen_heart", "king_heart",
           "ace_diamond", "2_diamond", "3_diamond", "4_diamond", "5_diamond",
           "6_diamond", "7_diamond", "8_diamond", "9_diamond", "10_diamond",
           "jack_diamond", "queen_diamond", "king_diamond"]

    length = len(dictionary)
    for i in range(length):
        if len(dictionary) > 1:
            c = random.choice(dictionary)
            r.append(c)
            dictionary.remove(c)
        else:
            c = dictionary.pop()
            r.append(c)

    return r

# ==========================================================================================



# ============================================intro=========================================
def game_intro():
    intro = True
    pygame.init()

    while intro:
        screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False



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
    deck_list = [Suggest_Deck(250, 50), Hidden_Deck(240, 230), Hidden_Deck(350, 230), Hidden_Deck(470, 230),
                 Hidden_Deck(590, 230), Hidden_Deck(710, 230), Hidden_Deck(830, 230), Hidden_Deck(950, 230),
                 Collect_Deck(590, 50), Collect_Deck(710, 50), Collect_Deck(830, 50), Collect_Deck(950, 50)]
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
            if isinstance(item, Collect_Deck):
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
