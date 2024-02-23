'''
This is a Black Jack sample game between an user and a machine
'''


import random

# SUIT, RANK, INT VALUE DICT
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#CARD CLASS
class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


#DECK CLASS
class Deck():
    
    def __init__(self):
        
        self.deck = [] # start with an empty list
        
        for suit in suits:
            for rank in ranks:
                #Create the card Object
                created_card = Card(suit,rank)
                self.deck.append(created_card)
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "the deck has" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# HAND
class Hand:
    
    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def remove_one(self):
        return self.cards.pop(0)
    
    # Card passed in from Deck.deal() --> single card (suite, rank)
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        #track ace
        if card.rank == "Ace":
            self.aces += 1


    # As Ace can be 1 or 11:
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value =- 10
            self.aces =- 1

    def __str__(self):
        return f'Player has {len(self.cards)} cards.'


# CHIPS
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total =+ self.bet
    
    def lose_bet(self):
        self.total =- self.bet

############# GAME SETUP ################
        
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("Sorry, You don't have enough chips! You have: {}".format(chips.total))
            else:
                break
            
def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Hit or Stand? Enter h or s ")
        if x[0].lower() == "h":
            hit(deck,hand)
        elif x[0] == "s":
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print("Sorry, I did not understand. Please enter h or s only!")
            continue
        break

def show_some(player,dealer):
    # show only ONE of the dealer's cards

    print("\n Dealer's Hand")
    print("First card hidden")
    print(dealer.cards[1])

    # Show all (2 cards) of the player's hand/cards
    print("\n Player's Hand")
    for card in player.cards:
        print(card)
    
def show_all(player,dealer):
    # show all the dealer's cards
    print("\n Dealer's Hand")
    for card in dealer.cards:
        print(card)

    # calculate and display the value (J+K == 20)
    print(f"Value of Dealer's Hand is: {dealer.value}")

    # show all the player's cards
    print("\n Player's Hand")
    for card in player.cards:
        print(card)
    print(f"Value of Player's Hand is: {player.value}")

def player_busts(player, dealer, chips):
    print("BUST PLAYER!!!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!!!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("PLAYER WINS!!! DEALER BUSTED!!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("DEALER WINS!!!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! PUSH")

## GAME LOGIC ##
while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Set up the Player's chips
    player_chips = Chips()  # remember the default value is 100    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand) 
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break