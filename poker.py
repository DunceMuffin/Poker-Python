# pylint: disable=C0103
# IMPORTS
'''module used to shuffle deck and control RI actions'''
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

def rank_hand(hand):
    '''figure out the rank of their hand, returns a word'''
    count_ref = [get_value(card) for card in hand]
    count_bank = [count_ref.count(value) for value in count_ref]
    same_suit = True if [get_suit(card) for card in hand] == [get_suit(hand[0]) for _ in range(5)] else False
    is_straight = True if [get_rank(hand[0]) for _ in range(5)] == [get_rank(card) for card in hand] else False

    if ['A', 'K', 'Q', 'J', '1'] == [get_value(card) for card in hand] and same_suit:
        return 'Royal Flush!'
    elif is_straight and same_suit:
        return 'Straight Flush: ' + max(hand, key=get_rank).name
    elif max(count_bank) == 4:
        return 'Four of a Kind: ' + hand[count_bank.index(4)].name
    elif 3 in count_bank and 2 in count_bank:
        return 'Full House: ' + hand[count_bank.index(3)].name
    elif same_suit:
        return 'Flush: ' + max(hand, key=get_rank).name
    elif is_straight:
        return 'Striaght: ' + max(hand, key=get_rank).name
    elif 3 in count_bank:
        return 'Three of a Kind: ' + hand[count_bank.index(3)].name
    elif count_bank.count(2) == 4:
        return 'Two Pair: ' + find_high(hand, count_bank).name
    elif 2 in count_bank:
        return 'Pair: ' + hand[count_bank.index(2)].name
    else:
        return 'High Card: ' + max(hand,key=get_rank).name

def find_high(hand, bank):
    '''Used on two pairs to find the higher pair, returns card'''
    hand_bank = hand
    hand_bank.pop(bank.index(1))
    return max(hand, key=get_rank)

def remove_all_cards():
    '''removes cards from all player hands and returns them to the deck'''
    print('Returning cards...\n')
    for player in players:
        remove_cards(player)

def remove_cards(player):
    '''removes cards from a player's hand and returns them to the deck'''
    for i in range(len(player.hand) - 1, -1, -1):
        deck.append(player.hand.pop(i))

def distribute_cards():
    '''distributes cards to all player hands from the deck'''
    print('Distributing cards...')
    for player in players:
        for i in range(5):
            player.hand.append(deck.pop(i))
    organize_hands()

# Use these to reform rank_hands()
def get_value(card):
    '''used for retreiving value, returns value of the card'''
    return card.identifier[0]

def get_rank(card):
    '''used for retreiving rank, returns rank of the card'''
    return card.rank

def get_suit(card):
    '''used for retreiving suit, returns suit of the card'''
    return card.identifier[1]

def organize_hands():
    '''organizes all players hands by card rank'''
    for player in players:
        player.hand.sort(reverse=True, key=get_rank)

def handle_betting():
    '''starts the loops to resolve bets'''

    post_choices = ['fold', 'raise', 'call', 'allin']
    pre_choices = ['check', 'open', 'allin']

    while True:
        if bet.state:
            action = input("What's your selection?\nFold, raise, call, or allin?\n").lower()
        else:
            action = input("What's your selection?\nCheck, open, or allin?\n").lower()
        if action not in (post_choices if bet.state else pre_choices):
            print('Invalid Action')
            continue
        actions[action](players[0])
        break

    for player in players:
        if player == players[0]:
            continue
        if bet.state:
            action = random.choices(population=post_choices, weights=[0.2, 0.37, 0.38, 0.05])[0]
        else:
            action = random.choices(population=pre_choices, weights=[0.25, 0.7, 0.05])[0]
        actions[action](player)

def exchange_cards():
    '''switch out cards the player selects'''
    print('\nRound ' + str(round_num))
    print('Coins: ' + str(players[0].coins))
    print('Which cards do you want to switch out?')
    print_hand(0)
    switch_string = input('Use value and kingdom, ie. AS for Ace of Spades or 1c for Ten of Clubs\n').upper()
    for i in range(len(players[0].hand) - 1, -1, -1):
        if players[0].hand[i].identifier in switch_string:
            pile.append(players[0].hand.pop(i))

    for player in players:
        if player != players[0]:
            for i in range(0, random.randint(0, 4), -1):
                pile.append(player.pop(i))
        while len(player.hand) < 5:
            player.hand.append(deck.pop(random.randint(0, len(deck))))
    organize_hands()
    print_hand(0)
def dump_pile():
    '''remove all cards from the pile and place them back in the deck'''
    for i in range(len(pile) - 1, -1, -1):
        deck.append(pile.pop(i))

def showdown():
    '''flip the cards and declare winner(learn more on poker first)'''
    for player in players:
        if player.state < 1:
            continue
        print(player.name + ' has a ' + rank_hand(player.hand))
    _ = input('') + 'n'

def reset_player_states():
    '''turn all player states to 1'''
    for player in players:
        player.state = 1

def fill_pot():
    '''fill the pot, takeout players who bet too much'''
    for i in range(len(bets) - 1, -1, -1):
        if players[i].state < 1:
            continue
        if bets[i] > players[i].coins:
            bank = bank + bets.pop(i)
    return bank

def check_win():
    '''checks if a player has won during the end of each round, quits upon sucess'''
    for player in players:
        if player.coins == 400:
            raise SystemExit(player.name + 'has Won!')

# PLAYER FUNCTIONS

def bet(player):
    '''should be called on both open and raise, 
    for opening the game with a bet or raising the current highest bet'''
    if player == players[0]:
        inp = ''
        while True:
            if bet.state:
                inp = input('Raise amount? (highest bet is ' + str(max(bets)) + ')\n')
            else:
                inp = input('Open amount?\n')
            try:
                int(inp)
            except ValueError:
                print('Invalid ammount')
                continue
            else:
                break
    else:
        if max(bets) == 0:
            bets[player.identifier] += random.randint(5, 10)
            print(player.name + ' has opened with ' + str(bets[player.identifier]))
        else:
            bets[player.identifier] += max(bets) + random.randint(5, 10)
            print(player.name + ' has raised with ' + str(bets[player.identifier]))
    bet.state = True

def check(player):
    '''do nothing, just move to next player'''
    print(player.name + ' has checked')

def fold(player):
    '''drop bet, out of the round'''
    bets[player.identifier] = 0
    player.state = 0
    print(player.name + ' has folded.')
    print_hand(player.identifier)
    remove_cards(player)

def call(player):
    '''match highest bet so far'''
    bets[player.identifier] = max(bets)
    print(player.name + ' has called')

def allin(player):
    '''make a bet out of all of the player's coins'''
    bets[player.identifier] = player.coins
    print(player.name + ' has gone allin!')

# PRINTERS

def print_hands():  # Remove from debug functions
    '''debug function, shows all player hands'''
    for i in range(players):
        print(players[i].name + "'s hand:")
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

def print_coins():
    '''print all player coins'''
    for player in players:
        print(player.name + ': ' + str(player.coins))

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
    'JC': ['Jack of Clubs', 10],
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
    'JD': ['Jack of Diamonds', 10],
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
    'JH': ['Jack of Hearts', 10],
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
    'JS': ['Jack of Spades', 10],
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
print('Generating...')

players = [Player('player' + str(i), i) for i in range(PLAYER_COUNT)]
deck = [Card(list(cards.keys())[i], list(cards.values())[i][0],
list(cards.values())[i][1]) for i in range(len(list(cards.keys())))]

# Game Loop
round_num = 1
while True:
    # Reminder to consolodate a few of these into higher order funcitons
    bets = [0 for _ in players]
    pile = []
    pot = 0
    bet.state = False

    print('Shuffling...')
    random.shuffle(deck)
    distribute_cards()
    # Reminder to implement some kind of UI

    print('\nRound ' + str(round_num))
    print('Coins: ' + str(players[0].coins))
    print_hand(0)
    handle_betting()
    exchange_cards()
    
    print('\nRound ' + str(round_num))
    print('Coins: ' + str(players[0].coins))
    print_hand(0)
    handle_betting()
    showdown()
    check_win()

    remove_all_cards()
    reset_player_states()
    dump_pile()
    round_num += 1
# To-Do: fix bugs with actions, implement pot and reward upon round completion
