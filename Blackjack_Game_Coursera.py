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
deck_in_play = list()
player_hand = list()
dealer_hand = list()
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card():
    ''' Card class creates a card and allows to get its suit and rank'''
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
class Hand():
    def __init__(self):
        self.hand_list = list()

    def __str__(self):
        s = ""
        for card in self.hand_list:
            s += "%s " % (str(card))
        return "Hand contains %s" % s

    def add_card(self, card):
        self.hand_list.append(card)

    def get_value(self):
        '''computes the value of a hand, if the hand contains and ace, count ace as 1 point
        if the hand value is lesser than 12, then add 10 to count one of the aces as 11'''
        card_ranks = []
        self.hand_value = 0
        for card in self.hand_list:
            card_ranks.append(card.get_rank()) 
        for rank in card_ranks:
            self.hand_value += VALUES[rank]
        ''' check if there are aces'''	            
        if "A" in card_ranks and self.hand_value < 12:
            self.hand_value += 10
        return self.hand_value	
   
    def draw(self, canvas, pos):
        '''draw the card, for each card move it laterally by a factor of its center (i) so
        that they are aligned'''
        i = 1
        for card in self.hand_list:
            card.draw(canvas, [pos[0] + i * CARD_CENTER[0], pos[1] + CARD_CENTER[1]])
            i += 3        
 
        
# define deck class 
class Deck():
    def __init__(self):
        self.cards_deck = list()
        for rank in range(len(RANKS)):
            for suit in range(len(SUITS)):
                self.cards_deck.append(Card(SUITS[suit],RANKS[rank]))
            # create a Deck object

    def shuffle(self):
        return random.shuffle(self.cards_deck)     # use random.shuffle()

    def deal_card(self): 
        self.card_dealt = self.cards_deck.pop()
        return self.card_dealt 	# deal a card object from the deck
    
    def __str__(self):
        s = "Deck contains: "
        for card in self.cards_deck:
            s += "%s " % (str(card))
        return s	# return a string representing the deck

#define event handlers for buttons
def deal():
    ''' create the deck, shuffle it, and deal two cards to each player.
    if user hits "deal" while in play, they forfeit their turn and lose a point'''
    global outcome, in_play, deck_in_play, player_hand, dealer_hand, score
    if in_play:
        score -=1
        outcome = "Player loses"
    deck_in_play = Deck()
    deck_in_play.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck_in_play.deal_card())
    dealer_hand.add_card(deck_in_play.deal_card())
    player_hand.add_card(deck_in_play.deal_card())
    dealer_hand.add_card(deck_in_play.deal_card())
    in_play = True
    outcome = "Hit or Stand?"

def hit():
    ''' hit the player with a card if they are in play and then check if that makes him bust.
    if they are not in play, tell them they can't do that'''
    global in_play, player_hand, dealer_hand, score, outcome
    if in_play:
        player_hand.add_card(deck_in_play.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You Busted! New deal?"
            score -= 1
            in_play = False
    else:
        outcome = "You Busted already"

def stand():
    ''' once the player decides to stand, it's the turn of the dealer.
    keep dealing cards to the dealer until they hit 17 or above.'''
    global in_play, dealer_hand, score, outcome
    if player_hand.get_value() > 21:
        outcome = "Can't do, you busted already. Click Deal"
    else:
        if dealer_hand.get_value() >= 17:
            in_play = False
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck_in_play.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted. Deal?"
            in_play = False
            score += 1
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "Player wins. New deal?"
            in_play = False
            score += 1
        else:
            outcome = "Dealer wins. New deal?"
            in_play = False
            score -= 1	# replace with your code below

# draw handler    
def draw(canvas):
    '''draw dealer and player's cards.
    also drawing the score, and the outcome (i.e instructions). Added functionality
    that tells the user the value of his hand. We hide the first card of the dealer until the
    player is no longer in play'''
    player_hand.draw(canvas, [50, 300])
    dealer_hand.draw(canvas, [50, 100])
    canvas.draw_text(str(outcome), (100, 100), 25, "Black")
    canvas.draw_text("Blackjack", (250, 40), 30, "Black")
    canvas.draw_text("Player: %s" % player_hand.get_value(), (100, 500), 25, "Black")
    if not in_play:
        canvas.draw_text("Dealer: %s" % dealer_hand.get_value(), (100, 125), 25, "Black")    
    else:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                      [50 + CARD_BACK_SIZE[0], 100 + CARD_BACK_SIZE[1]], CARD_BACK_SIZE)
    canvas.draw_text("Score= %s" % score, (400, 300), 20, "Black")


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