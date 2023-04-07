# IMPORTS
'''randomizes order of a list, used to shuffle the deck'''
import random

# CLASSES


class Player:
    '''class used to generate players, holds name and hand value'''

    def __init__(self, name, identifier):
        self.name = name
        self.hand = []
        self.coins = 100
        self.state = 1
        self.identifier = identifier


class Card:
    '''class used to generate cards, holds name and identifier value'''

    def __init__(self, identifier, name, rank=0):
        self.name = name
        self.identifier = identifier
        self.rank = rank

# GAME FUNCTIONS


def remove_all_cards():
    '''removes cards from all player hands and returns them to the deck'''
    print('Returning cards...\n')
    for player in players:
        remove_cards(player)

def remove_cards(player):
    '''removes cards from a player's hand and returns them to the deck'''
    for i in reversed(range(len(player.hand))):
        deck.append(player.hand.pop(i))

def distribute_cards():
    '''distributes cards to all player hands from the deck'''
    print('Distributing cards...')
    for player in players:
        for i in range(5):
            player.hand.append(deck.pop(i))


def get_rank(card):
    '''used in organize_hands, returns rank of each card'''
    return card.rank


def organize_hands():
    '''organizes all players hands by card rank'''
    for player in players:
        player.hand.sort(reverse=True, key=get_rank)


def start_betting():
    '''starts the loops to resolve bets'''
    choices = ['check', 'open', 'allin']
    while True:
        action = input(
            'Whats your selection?\ncheck, open, or allin?\n').lower()
        if action not in choices:
            print('Invalid Action')
            continue
        actions[action](players[0])
        break
    for player in players:
        action = random.choice(choices)
        if player == players[0]:
            continue
        actions[action](player)


def continue_betting():
    '''pickup from starting bets'''


def exchange_cards():
    '''switch out cards the player selects'''

def reset_states():
    '''turn all player states to 1'''
    for player in players:
        player.state = 1

# PLAYER FUNCTIONS


def bet(player):
    '''should be called on both open and raise, 
    for opening the game with a bet or raising the current highest bet'''
    if player == players[0]:
        inp = ''
        while True:
            if max(bets) == 0:
                inp = input('Raise amount? (highest bet is ' + max(bets) + ')')
            else:
                inp = input('Open amount?')
            try:
                int(inp)
            except ValueError:
                print('Invalid ammount')
                continue
            else:
                pass
    else:
        if max(bets) == 0:
            bets[player.identifier] = random.randint(5, 25)
            print(player.name + ' has opened with ' + str(bets[player.identifier]))
        else:
            bets[player.identifier] = max(bets) + random.randint(5, 25)
            print(player.name + ' has raised with ' + str(bets[player.identifier]))

def check(player):
    '''do nothing, just move to next player'''
    print(player.name + ' has checked')

def fold(player):
    '''drop bet, out of the round'''
    bets[player.identifier] = 0
    remove_cards(player)
    player.state = 0
    print(player.name + ' has folded')

def call(player):
    '''match highest bet so far'''
    bets[player.identifier] = max(bets)
    print(player.name + ' has called')


def allin(player):
    '''make a bet out of all of the player's coins'''
    bets[player.identifier] = player.coins
    print(player.name + ' has gone allin!')


# DEBUG FUNCTIONS

def print_hands():
    '''debug function, shows all player hands'''
    for i in range(players):
        print_hand(i)


def print_hand(player_num):
    '''debug function, prints all cards in a certain player's hand'''
    for card in players[player_num].hand:
        print(card.name)

def print_deck():
    '''debug function, prints full deck and deck count'''
    for card in deck:
        print(card.name)
    print('Deck count: ', len(deck))

def print_nums():
    '''debug function, print all player ids'''
    for player in players:
        print(player.identifier)

# DATA


actions = {
    'open': bet,
    'raise': bet,
    'fold': fold,
    'call': call,
    'check': check,
    'allin': allin
}

cards = {
    'AC': ['Ace of Clubs', 13],
    '2C': ['Two of Clubs', 1],
    '3C': ['Three of Clubs', 2],
    '4C': ['Four of Clubs', 3],
    '5C': ['Five of Clubs', 4],
    '6C': ['Six of Clubs', 5],
    '7C': ['Seven of Clubs', 6],
    '8C': ['Eight of Clubs', 7],
    '9C': ['Nine of Clubs', 8],
    '1C': ['Ten of Clubs', 9],
    'JC': ['Joker of Clubs', 10],
    'QC': ['Queen of Clubs', 11],
    'KC': ['King of Clubs', 12],
    'AD': ['Ace of Diamonds', 13],
    '2D': ['Two of Diamonds', 1],
    '3D': ['Three of Diamonds', 2],
    '4D': ['Four of Diamonds', 3],
    '5D': ['Five of Diamonds', 4],
    '6D': ['Six of Diamonds', 5],
    '7D': ['Seven of Diamonds', 6],
    '8D': ['Eight of Diamonds', 7],
    '9D': ['Nine of Diamonds', 8],
    '1D': ['Ten of Diamonds', 9],
    'JD': ['Joker of Diamonds', 10],
    'QD': ['Queen of Diamonds', 11],
    'KD': ['King of Diamonds', 12],
    'AH': ['Ace of Hearts', 13],
    '2H': ['Two of Hearts', 1],
    '3H': ['Three of Hearts', 2],
    '4H': ['Four of Hearts', 3],
    '5H': ['Five of Hearts', 4],
    '6H': ['Six of Hearts', 5],
    '7H': ['Seven of Hearts', 6],
    '8H': ['Eight of Hearts', 7],
    '9H': ['Nine of Hearts', 8],
    '1H': ['Ten of Hearts', 9],
    'JH': ['Joker of Hearts', 10],
    'QH': ['Queen of Hearts', 11],
    'KH': ['King of Hearts', 12],
    'AS': ['Ace of Spades', 13],
    '2S': ['Two of Spades', 1],
    '3S': ['Three of Spades', 2],
    '4S': ['Four of Spades', 3],
    '5S': ['Five of Spades', 4],
    '6S': ['Six of Spades', 5],
    '7S': ['Seven of Spades', 6],
    '8S': ['Eight of Spades', 7],
    '9S': ['Nine of Spades', 8],
    '1S': ['Ten of Spades', 9],
    'JS': ['Joker of Spades', 10],
    'QS': ['Queen of Spades', 11],
    'KS': ['King of Spades', 12]
}

# Input('Type of poker?(Currently only Five Draw)\n Five Draw: FD')
# ai = input('type of ai?')

# Get number of players (reminder to shorten this later)
PLAYER_COUNT = 5  # change to 1
'''while int(PLAYER_COUNT) > 8 or int(PLAYER_COUNT) < 2:
    PLAYER_COUNT = input('Number of players?\n')
    try:
        int(PLAYER_COUNT)
    except ValueError:
        print('Input must be an integer!')
        PLAYER_COUNT = 1
        continue
    if int(PLAYER_COUNT) > 8 or int(PLAYER_COUNT) < 2:
        print('Invalid input \nThis game has a max of 8 and a minimum of 2!')
        continue
    PLAYER_COUNT = int(PLAYER_COUNT)
'''
print('Generating...\n')

players = [Player('player' + str(i), i) for i in range(PLAYER_COUNT)]
deck = [Card(list(cards.keys())[i], list(cards.values())[i][0],
             list(cards.values())[i][1]) for i in range(len(list(cards.keys())))]

# Game Loop
round_num = 1
while round_num < 2:
    bets = [0 for _ in players]
    print('Round ' + str(round_num))
    print('Shuffling...')
    random.shuffle(deck)
    distribute_cards()
    organize_hands()
    print('Coins: ' + str(players[0].coins))
    start_betting()

    print_hand(0)
    remove_all_cards()
    round_num += 1

print_nums()