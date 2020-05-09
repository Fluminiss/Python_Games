# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
WIDTH = 800
HEIGHT = 100
cardnumber = 16
cardwidth = WIDTH // cardnumber
selected_cards = []
turns = 0

def new_game():
    global cards, exposed, state, turns
    cards = range(0,8)
    cards.extend(range(0,8))
    random.shuffle(cards)
    exposed = []
    for i in range(16):
        exposed.append(False)
    state = 0
    turns = 0

        
# define event handlers
def mouseclick(pos):
    global state, selected_cards, turns

    
    x, y = pos
    cardnr = x // cardwidth
    #print cardnr
    if exposed[cardnr] == True:
        return


    print selected_cards
    print state
    if state == 2:
        if cards[selected_cards[0]] == cards[selected_cards[1]]:
            exposed[selected_cards[0]] = True
            exposed[selected_cards[1]] = True
            selected_cards=[]
            state = 0
            
        else:
            exposed[selected_cards[0]] = False
            exposed[selected_cards[1]] = False
            selected_cards=[]
            state = 0
    #print cardnr
    selected_cards.append(cardnr)
    exposed[cardnr] = True
    # add game state logic here
    print turns
    if state == 0:
        state = 1
        turns+=1
    elif state == 1:
        state = 2
    else:
        state = 1
    label.set_text("Turns = " + str(turns))
    #print state
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(cards)):
        if exposed[i] == True:
            canvas.draw_text(str(cards[i]),[50*(i+0.3),50],40,'white')
        else:
            canvas.draw_polygon([[cardwidth*i,0],
                                 [cardwidth*i,HEIGHT],
                                 [cardwidth*(1+i),HEIGHT],
                                 [cardwidth*(1+i),0]],
                                 2,'green','green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric