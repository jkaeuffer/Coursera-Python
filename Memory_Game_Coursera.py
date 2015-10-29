# implementation of card game - Memory

import simplegui
import random

exposed = [False] * 16
cards_state = 0
turns = 0

# helper function to initialize globals
def new_game():
    global numbers, exposed, cards_state, turns
    numbers = range(8) + range(8)
    random.shuffle(numbers)
    exposed = [False] * 16
    cards_state = 0
    turns = 0
    label.set_text("Turns = %s" % turns)
     
# define event handlers
def mouseclick(pos):
    global card_index, exposed, cards_state, choice1, choice2, turns
    # add game state logic here
    card_index = pos[0] // 50
    if cards_state == 0:
        if not exposed[card_index]:
            choice1 = card_index
            cards_state = 1
            exposed[card_index] = True            
    elif cards_state == 1:
        if not exposed[card_index]:
            choice2 = card_index
            cards_state = 2
            exposed[card_index] = True
            turns +=1
    elif cards_state == 2:
        if not exposed[card_index]:
            if not numbers[choice1] == numbers[choice2]:
                exposed[choice1] = exposed[choice2] = False
            cards_state = 0
            choice1 = card_index
            cards_state = 1
            exposed[card_index] = True
    label.set_text("Turns = %s" % turns)
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards_pos, exposed
    first_pos = [10,65]
    line_pos = [0,0]
    canvas.draw_line(line_pos, [line_pos[0], line_pos[1]+100], 1, "Grey")
    cards_pos = list()
    i = 0
    for n in numbers:
        cards_pos.append((line_pos[0], line_pos[0]+50))
        if not exposed[i]:
            canvas.draw_text("", first_pos, 50, "White")            
        else:
            canvas.draw_line([line_pos[0]+25, line_pos[1]], [line_pos[0]+25, line_pos[1]+100], 48, "Black")
            canvas.draw_text(str(n), first_pos, 50, "White")
        line_pos[0] += 50
        canvas.draw_line(line_pos, [line_pos[0], line_pos[1]+100], 1, "Grey")
        first_pos[0] += 50
        i += 1
    if False not in exposed:
        canvas.draw_polygon([(0,0), (800,0), (800,100), (0,100)], 1, "Black", "Black")
        canvas.draw_text("Congrats you won after %s turns!" % turns, (200, 55), 30, "White")
    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
frame.set_canvas_background("Green")
label = frame.add_label("Turns = 0")



# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

