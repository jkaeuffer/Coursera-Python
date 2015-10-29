import simplegui
# template for "Stopwatch: The Game"

# define global variables
tenth_of_seconds = 0
win_score = 0
game_rounds = 0
result = str(win_score) +"/"+str(game_rounds)

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(n):
    ''' converts n into A:BB.C where A = minutes
    BB = seconds and C = tenth of seconds'''
    # initialize the variables we'll need
    minutes = "0"
    seconds = "00"
    tenth_seconds = "0"
    # write the if / elif / else statement to convert
    # check if below 10. If below 10, then only tenth of sec
    if n < 10:
        minutes = "0"
        seconds = "00"
        tenth_seconds = str(n)
    
    # check if below 600. If below 600, then no minute
    elif n < 600:
        # mod 10 gives resulting tenth of sec
        # int div of 10 gives seconds
        minutes = "0"
        if (n // 10) <10:
            seconds = "0"+str(n // 10)
        else:
            seconds = str(n//10)
        tenth_seconds = str(n % 10)
    
    else:
        # int div of 600 gives minutes
        # removing number of minutes in ms from n to 
        # calculate seconds and then tenth of seconds
        minutes = str(n // 600)
        if ((n - int(minutes) * 600) // 10) < 10:
            seconds = "0"+str((n - int(minutes) * 600) // 10)
        else:
            seconds = str((n - int(minutes) * 600) // 10)
        tenth_seconds = str((n - int(minutes) * 600 - 
                             int(seconds) * 10) % 10)
    return "%s:%s.%s" % (minutes, seconds, tenth_seconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    timer.start()
    global tenth_of_seconds
    tenth_of_seconds +=1
    
def stop_timer():
    if timer.is_running():
        reflex()
    timer.stop()
    
def reset_timer():
    global tenth_of_seconds, win_score, game_rounds, result
    if timer.is_running():
        timer.stop()
    tenth_of_seconds = 0
    win_score = 0
    game_rounds = 0
    result = "%s/%s" % (str(win_score), str(game_rounds))
    

# define the reflex test
def reflex():
    ''' should win if the second is whole
    which means mod of 10 should have no remainder'''
    global win_score, game_rounds, result
    if tenth_of_seconds % 10 == 0:
        win_score +=1
        game_rounds +=1
    elif tenth_of_seconds % 10 != 0:
        game_rounds +=1
    result = str(win_score) +"/"+str(game_rounds)
        
    
# define event handler for timer with 0.1 sec interval
timer = simplegui.create_timer(100, start_timer)

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tenth_of_seconds),(175,150),46, "Blue")
    canvas.draw_text(result,(275, 50), 34, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch The Game", 400,300)
frame.set_canvas_background('White')
# register event handlers
start_button = frame.add_button("Start", start_timer, 100)
stop_button = frame.add_button("Stop", stop_timer, 100)
reset_button = frame.add_button("Reset", reset_timer, 100)
drawing = frame.set_draw_handler(draw_handler)


# start frame
frame.start()

