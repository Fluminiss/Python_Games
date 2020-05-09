# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):
        cardstring = ""
        for card in self.cards:
            cardstring += card.get_suit()
            cardstring += card.get_rank()
            cardstring += " " 
        return "Your hand contains " + cardstring# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        has_ace = False
        value = 0
        for card in self.cards:
            value += VALUES[(card.get_rank())]# compute the value of the hand, see Blackjack video
            if card.get_rank() == 'A':
                has_ace = True
        if has_ace and value + 10 <= 21:
            value += 10
        return value

    def draw(self, canvas, pos):
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas, [pos[0] + i * CARD_SIZE[0],pos[1]])# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        return self.cards.pop()	# deal a card object from the deck
    
    def __str__(self):
        cardstring = ""
        for card in self.cards:
            cardstring += card.get_suit()
            cardstring += card.get_rank()
            cardstring += " " 
        return "The deck contains " + cardstring
            # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    if in_play == True:
        outcome = "You lose...!"
        score -= 1
    # your code goes here
    in_play = True
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

def hit():
    global score, in_play, outcome
    # replace with your code below
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21 and in_play:
        outcome = "You have busted"
        score -= 1
        in_play = False

def stand():
    # replace with your code below
    global score, in_play, outcome
    if in_play:
        if player_hand.get_value() > 21:
            score -= 1
            in_play = False
            outcome = "You have busted"
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:    
        if dealer_hand.get_value() > 21:
            score += 1
            in_play = False
            outcome = "The dealer busted"
        elif dealer_hand.get_value() < player_hand.get_value():
            score += 1
            in_play = False
            outcome = "You won!"
        else:
            score -= 1
            in_play = False
            outcome = "The dealer wins!"    
        
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global score, in_play, outcome
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas,[50,50])
    dealer_hand.draw(canvas,[50,200])
    canvas.draw_text("Blackjack", (250, 30), 40, 'black')
    canvas.draw_text("Score = "+str(score), (200, 500), 40, 'Black')
    card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
    if in_play:
        canvas.draw_text("Hit or Stand?", (200, 400), 40, 'Black')
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [50 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
    else:
        canvas.draw_text(outcome, (200, 550), 40, 'black')
        canvas.draw_text("New Deal?", (200, 450), 40, 'Black')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric