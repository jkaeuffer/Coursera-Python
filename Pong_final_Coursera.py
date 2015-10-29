# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [1,0]
score1 = 0
score2 = 0
paddle1_pos = [4, (HEIGHT/2 - HALF_PAD_HEIGHT)]
paddle2_pos = [596, (HEIGHT/2 - HALF_PAD_HEIGHT)]

paddle1_vel = 0
paddle2_vel = 0

# check if ball bounces with the wall
def check_bounce_wall():
    if ball_pos[1] - BALL_RADIUS == 0: # 1 is the line width for the ball
        return True
    elif ball_pos[1] + BALL_RADIUS == HEIGHT:
        return True
    else:
        return False

# check if it bounces with a paddle    
def check_bounce_paddle():
    if (ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH): # hits the right side
        return ball_pos[1] + ball_vel[1] + BALL_RADIUS >= paddle2_pos[1] and ball_pos[1] + ball_vel[1] - BALL_RADIUS <= paddle2_pos[1] + PAD_HEIGHT
    elif (ball_pos[0] + ball_vel[0] - BALL_RADIUS) <= (PAD_WIDTH):
        return ball_pos[1] + BALL_RADIUS >= paddle1_pos[1] and ball_pos[1] - BALL_RADIUS<= paddle1_pos[1] + PAD_HEIGHT 
    return False
            
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction is False:
        ball_vel[0] = random.randrange(-239,-121)/60
        ball_vel[1] = random.randrange(-179,-61)/60
    elif direction is True:
        ball_vel[0] = random.randrange(120,240)/60
        ball_vel[1] = random.randrange(-179,-61)/60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    if int(random.randrange(0,2)) == 1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS,1,'White', 'White')
    # make it bounce
    if check_bounce_wall():
        ball_vel[1] = - ball_vel[1]
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel >= 0 and paddle1_pos[1] + PAD_HEIGHT + paddle1_vel <= HEIGHT:
        paddle1_pos[1] += paddle1_vel
    if paddle2_pos[1] + paddle2_vel >= 0 and paddle2_pos[1] + PAD_HEIGHT + paddle2_vel <= HEIGHT:
        paddle2_pos[1] += paddle2_vel
    # draw paddles
    canvas.draw_line(paddle1_pos, (paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT),PAD_WIDTH,'White')
    canvas.draw_line(paddle2_pos, (paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT), PAD_WIDTH, 'White')
    # determine whether paddle and ball collide    
    if check_bounce_paddle():
        ball_vel[0] = (- ball_vel[0])*1.1
    #if check_hits_gutter():
    if (ball_pos[0] + BALL_RADIUS) >= (WIDTH - HALF_PAD_WIDTH): # hits right gutter
        if ball_pos[1] + BALL_RADIUS < paddle2_pos[1] or ball_pos[1] - BALL_RADIUS > paddle2_pos[1] + PAD_HEIGHT:
            score1 += 1
            spawn_ball(LEFT)
    elif (ball_pos[0] - BALL_RADIUS) <= (HALF_PAD_WIDTH): # hits left gutter
        if ball_pos[1] + BALL_RADIUS < paddle1_pos[1] or ball_pos[1] - BALL_RADIUS > paddle1_pos[1] + PAD_HEIGHT:
            score2 +=1
            spawn_ball(RIGHT)
            
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/2 - 70, 100), 70,'White')
    canvas.draw_text(str(score2), (WIDTH/2 + 40, 100), 70,'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 5
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += 5
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
