import random
import sys

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

###########  Card tempalte      ##########
###########                     ##########
class Card:
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

# test_card = Card("Two","Hears")
# print(test_card)
# print(test_card.value)

###########  Deck tempalte      ##########
###########                     ##########
class Deck:
    
    def __init__(self):
        self.all_cards = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(rank,suit))
    
    def __str__(self):
        visible_list = ""
        for card in self.all_cards:
            visible_list += "\n" + card.__str__()
        return "the list has : " + visible_list

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one_card(self):
        return self.all_cards.pop()

# abc = Deck()
# len(abc.all_cards)

# print("====== created player deck example =====")
# game_deck = Deck()
# for card in game_deck.all_cards[-3:-1]:
#     print(card)
# print(len(game_deck.all_cards))
# print("====== shuffled example =====")
# game_deck.shuffle()
# for card in game_deck.all_cards[-3:-1]:
#     print(card)
# print(len(game_deck.all_cards))

# print("=====deal one card trial=====")
# dealed_card = game_deck.all_cards.pop()
# print(dealed_card)
# print("=====remaining cards=====")
# print(len(game_deck.all_cards))

###########     hand tempalte   ##########
###########                     ##########
class Hand:
    def __init__(self):
        self.cards_on_hand = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self, card):
        self.cards_on_hand.append(card)
        self.value += card.value
    
    def adjust_for_ace(self,card):
        if card.rank == "Ace" and self.value > 11:
            self.value -= 10

player_hand = Hand()
dealer_hand = Hand()

# print("=====add a player card=====")
# player_hand.add_card(dealed_card)
# print(dealed_card)
# print("=====cards on player hand=====")
# print(player_hand.cards_on_hand[0])
# print("number of cards: ",len(player_hand.cards_on_hand))
# print("value of player",player_hand.value)
# for card in player_hand.cards_on_hand:
#     print(card)
# print(f"player value = {player_hand.value}")
# print("=====adjust for ace value for player =====")
# player_hand.adjust_for_ace(dealed_card)
# print(f"adjusted player value = {player_hand.value}")

# print("=====add a dealer card=====")
# dealer_hand.add_card(dealed_card)
# print(dealed_card)
# print("=====cards on dealer hand=====")
# print(dealer_hand.cards_on_hand[0])
# print("number of cards: ",len(dealer_hand.cards_on_hand))
# print("value of dealer",player_hand.value)
# for card in dealer_hand.cards_on_hand:
#     print(card)
# print(f"player value = {dealer_hand.value}")
# print("=====adjust for ace value for dealer =====")
# dealer_hand.adjust_for_ace(dealed_card)
# print(f"adjusted player value = {dealer_hand.value}")

###########     Chip tempalte   ##########
###########                     ##########
class Chips:
    
    def __init__(self, amount):
        self.total = amount  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

###########      Functions      ##########
###########                     ##########
def take_bet(total_chips):
    while True:
        try:
            bet = int(input("Please input your bet: "))
            if int(bet) <= total_chips:
                return int(bet)
            else:
                print("Your bet exceeds your available chips. Please input a smaller bet.")
        except ValueError:
            print("Please input a valid integer for your bet.")

def hit_or_stand(deck,hand):
    player_choice = ""
    try:
        player_choice = input("hit or stand?: ").lower()
        if player_choice == "hit":
            dealed_card = deck.deal_one_card()
            hand.add_card(dealed_card)
            print(f"{dealed_card} is added")
        elif player_choice == "stand":
            return "stand"
    except ValueError:
        print("please input 'hit' or 'stand'")
        pass

def show_some(player,dealer):
    print(f"Dealer cards value: {dealer.value}. Cards:")
    print(" ","***hidden card***")
    for card in dealer.cards_on_hand[1:]:
        print(" ",card)
    print(f"Player cards value: {player.value}. Cards:")    
    for card in player.cards_on_hand:
        print(" ",card)
    
def show_all(player,dealer):
    print(f"Dealer cards value: {dealer.value}. Cards:")
    for card in dealer.cards_on_hand:
        print(" ",card)
    print(f"Player cards value: {player.value}. Cards:")    
    for card in player.cards_on_hand:
        print(" ",card)

def player_busts(player):
    if player.value > 21:
        print("Player busts")
        return True
    else:
        return False

def player_wins(player,dealer):
    if player.value > dealer.value and player.value <= 21:
        print(">>Player Wins")
        return True
    else:
        return False

def dealer_busts(dealer):
    if dealer.value > 21:
        print(">>Dealer busts")
        return True
    else:
        return False
    
def dealer_wins(player,dealer):
    if player.value < dealer.value and dealer.value <= 21:
        print(">>Dealer Wins")
        return True
    else:
        return False
    
def push(player,dealer):
    if player.value == dealer.value == 21:
        print(">>Tie")
        return True
    else:
        return False

###########    combined game    ##########
###########                     ##########
round = 1
playing = True
player_chips = Chips(1000)

while playing:
    # Print an opening statement
    print("Welcome to the game - Blackjack")
    # Create & shuffle the deck, deal two cards to each player
    print("====== Created a new game  =====")
    print(f"Round: {round}")
    game_deck = Deck()
    game_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for _ in range(2):
        dealed_card = game_deck.all_cards.pop()
        player_hand.add_card(dealed_card)
        dealer_hand.add_card(dealed_card)
    # Set up the Player's chips
    print("Player chips =", player_chips.total)
    
    # Prompt the Player for their bet
    taken_bet = take_bet(player_chips.total)
    player_chips.bet = taken_bet
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
#    while playing:  # recall this variable from our hit_or_stand function
    while True:
        # Prompt for Player to Hit or Stand
        if hit_or_stand(game_deck,player_hand) == "stand":
            break
        print("\n")
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand) 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            print("\n")
            break
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while player_busts(player_hand) == False and dealer_hand.value < 17:
        dealed_card = game_deck.all_cards.pop()
        dealer_hand.add_card(dealed_card)
        
        # Show all cards
    print ("\n","====Showing all cards====")
    show_all(player_hand,dealer_hand) 
        # Run different winning scenarios
    if player_busts(player_hand) == True:
        player_chips.lose_bet()
    
    elif dealer_busts(dealer_hand) == True:
        player_chips.win_bet()
    
    elif player_wins(player_hand,dealer_hand) == True:
        player_chips.win_bet()
        
    elif dealer_wins(player_hand,dealer_hand) == True:
        player_chips.lose_bet()
        
    elif push(player_hand,dealer_hand) == True:
        pass
    
    # Inform Player of their chips total 
    print("Player chips =", player_chips.total)
    
    # Ask to play again
    round += 1
    while True:
        if player_chips.total == 0:
            print("Game Over")
            playing = False
            break
        try:
            again_choice = input("Play again? Y or N").upper()
            if again_choice == "Y":
                print(f"Round: {round}")
                break
            elif again_choice == "N":
                playing = False
                break
        except ValueError:
            print("Please input Y or N")
    if not playing:
        break