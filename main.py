#!/usr/bin/env python3.8

#six                0     suit - масть
#seven              1     rank - ранг
#eight              2     trump - козырь
#nine               3
#ten                4
#eleven - jack      5     diamonds - бубны
#twelve - queen     6     hearts - черви
#thirteen - king    7     spades - пики
#fourteen - ace     8     clubs - крести



from functools import total_ordering    #модуль включает функции высшего порядка, декоратор сравнения
from functools import reduce            #модуль включает функции высшего порядка, встроенная функция
from enum import IntEnum    #модуль перечисления, класс для создания перечисляемых констант
import random               #модуль предлагает набор инструментов для генерирования псевдослучайных чисел
import time

class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Suit(IntEnum):
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    CLUBS = 4

@total_ordering
class DeckCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __int__(self):
        return int(self.rank)

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __repr__(self):
        suit = dict()
        suit[1] = 'diamonds'
        suit[2] = 'hearts'
        suit[3] = 'spades'
        suit[4] = 'clubs'

        rank = dict()
        rank[2] = 'two'
        rank[3] = 'three'
        rank[4] = 'four'
        rank[5] = 'five'
        rank[6] = 'six'
        rank[7] = 'seven'
        rank[8] = 'eight'
        rank[9] = 'nine'
        rank[10] = 'ten'
        rank[11] = 'jack'
        rank[12] = 'queen'
        rank[13] = 'king'
        rank[14] = 'ace'

        return '{} {}'.format(suit[int(self.suit)], rank[int(self)])

    def isMinor(self):
        return int(self.rank) <= 10


def timing(method_to_decorate):
    def measure_time():
        start_time = time.time()
        method_to_decorate()
        end_time = time.time()

        period = (end_time - start_time)
        method_name = method_to_decorate.__name__

        print('Функция {} вычислена за {} секунд'.format(method_name, period))

    return measure_time

def random_card_factory():
    rank = random.choice(list(Rank))
    suit = random.choice(list(Suit))

    return DeckCard(rank, suit)

def yes_no(result):
    if result:
        return "бьёт"
    return "не бьёт"

def sameSuit(card1, card2):
    return card1.suit == card2.suit

def beats(card1, card2):
    if (card1 > card2) and (card1.suit == card2.suit):
        return True
    return False

def beats2(card1, card2, trump):
    if_beats = beats(card1, card2)

    if (card1.suit == trump) and (if_beats == True):
        return True
    elif (card1.suit == trump) and (card1.suit != card2.suit):
        return True
    elif (if_beats == True):
        return True
    return False

def beatsList(beatlist, card2, trump):
    mapping_result = list(map(lambda x: x if beats2(x, card2, trump) else False, beatlist))
    winning_card_list = list(filter(lambda x: x, mapping_result))

    #winning_card_list = list(filter(lambda x: beats2(x, card2, trump), beatlist))

    return winning_card_list

#def beatsList(beatlist, card2, trump):
    #winning_card_list = list()

    #for card in beatlist:
        #if beats2(card, card2, trump):
            #winning_card_list.append(card)

    #return winning_card_list

def random_player_name():
    name_letters = ['Петя', 'Вася', 'Миша']
    return random.choice(name_letters)

def score(points, cards):

    if len(cards) == 0:
        # no cards left
        return points
    leftCards = cards[1:]
    if cards[0] < 10:
        # cards[0] != Ace
        points = list(map(lambda x: x+cards[0], points)) # add point to all variants
        return score(points, leftCards)
    elif cards[0] > 9 and cards[0] != 14:
        points = list(map(lambda x: x+10, points)) # add point to all variants
        return score(points, leftCards)
    else:
        # cards[0] == Ace
        p1 = list(map(lambda x: x+1, points)) # add 1 to all variants
        ans1 = score(p1, leftCards)

        p2 = list(map(lambda x: x+11, points)) # add 11 to all variants
        ans2 = score(p2, leftCards)

        return ans1 + ans2 # 1 + 11


class Play:
    def __init__(self):
        self.card1 = random_card_factory()
        self.card2 = random_card_factory()

    def run(self):
        print(self.card1)
        print(self.card2)

        random_card_list = [random_card_factory() for x in range(0,10)]
        print(random_card_list)

        random_card_list1 = [random_card_factory() for x in range(0,3)]
        print(random_card_list1)

        print('Младшая карта {}'.format(self.card1.isMinor()))

        same_suit_result = sameSuit(self.card1, self.card2)
        print('Карты одной масти {}'.format(same_suit_result))

        beats_result = yes_no(beats(self.card1, self.card2))
        print('Карта {} {} карту {}'.format(self.card1, beats_result, self.card2))

        beats2_result = yes_no(beats2(self.card1, self.card2, Suit.SPADES))
        print('Карта {} {} карту {}'.format(self.card1, beats2_result, self.card2))

        print(beatsList(random_card_list, self.card2, Suit.SPADES))

        random_score = list(map(lambda rank: int(rank), random_card_list1))
        result_score = sorted(list(set(score([0], random_score))))
        print('Игрок {} набрал {} очков при картах {}'.format(random_player_name(), result_score, random_card_list1))

@timing
def func():
    game = Play()
    game.run()

def higher_order_function(func_param):
    func_param()

@timing
def main():
    higher_order_function(func)


if __name__ == '__main__':
    main()

print("__name__ имеет значение " + __name__)
