import main as m
from main import *
from constants import *
import pygame, pymunk, pymunk.pygame_util, math


global message
message = "Player 1 - Shoot!"

global solid_txt
solid_txt = ""
global stripe_txt
stripe_txt = ""

global feed
feed = ""

global turn
turn = 0  #EVEN --> P1 TURN;  ODD --> P2 TURN

global ball_pocketed
ball_pocketed = False

global player_one_is_solids
player_one_is_solids = None
global player_one_is_stripes
player_one_is_stripes = None
global player_two_is_solids
player_two_is_solids = None
global player_two_is_stripes
player_two_is_stripes = None

global pocketed_balls
pocketed_balls = []

def reset_feed():
    global feed
    feed = ""


def update_ball_pocketed():
    global ball_pocketed
    ball_pocketed = False

def check_ball_pocketed():
    global turn
    global message
    global stripe_txt, solid_txt
    if ball_pocketed == False: #NO BALL POCKETED, UPDATE TURN
        turn+=1

    else: #BALL GETS POCKETED
        if turn % 2 == 0:   #PLAYER ONE TURN
            if player_one_is_solids:
                for ball in pocketed_balls:
                    if ball.id <= 777 and not (ball.id == 1): #IF SOLID GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(solids_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 1, YOU LOSE")
                        message = ("PLAYER 1, YOU LOSE")
                    elif ball.id == 888 and (len(solids_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 1, YOU WIN")
                        message = ("PLAYER 1, YOU WIN")
                    elif ball.id >= 999 or ball.id == 1:   #IF STRIPE GETS MADE OR CUE BALL
                        turn+=1
            if player_one_is_stripes:
                for ball in pocketed_balls:
                    if ball.id >= 999 and not (ball.id == 1): #IF STRIPED GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(stripes_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 1, YOU LOSE")
                        message = ("PLAYER 1, YOU LOSE")
                    elif ball.id == 888 and (len(stripes_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 1, YOU WIN")
                        message = ("PLAYER 1, YOU WIN")
                    elif ball.id <= 777 or ball.id == 1:   #IF SOLID GETS MADE
                        turn+=1
        else:   #PLAYER TWO TURN
            if player_two_is_solids:
                for ball in pocketed_balls:
                    if ball.id <= 777 and not (ball.id == 1): #IF SOLID GETS MADE, AND NOT CUE BALL
                        pass
                    elif ball.id == 888 and (len(solids_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 2, YOU LOSE")
                        message = ("PLAYER 2, YOU LOSE")
                    elif ball.id == 888 and (len(solids_remaining) == 0) and not (ball.id == 1): #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 2, YOU WIN")
                        message = ("PLAYER 2, YOU WIN")
                    elif ball.id >= 999 or ball.id == 1: #IF STRIPE GETS MADE OR CUE BALL
                        turn+=1
            if player_two_is_stripes:
                for ball in pocketed_balls:
                    if ball.id >= 999 and not (ball.id == 1):   #IF IF STRIPE GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(stripes_remaining) > 0):    #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 2, YOU LOSE")
                        message = ("PLAYER 2, YOU LOSE")
                    elif ball.id == 888 and (len(stripes_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 2, YOU WIN")
                        message = ("PLAYER 2, YOU WIN")
                    elif ball.id >= 777 or ball.id == 1:   #IF SOLID GETS MADE OR CUE BALL
                        turn+=1

    
def check_turn():
    global message

    if turn % 2 == 0:   #IF PLAYER ONE TURN
        print("Player 1 - Shoot!")
        message = ("Player 1 - Shoot!")
    else:   #IF PLAYER TWO TURN
        print("Player 2 - Shoot!")
        message = ("Player 2 - Shoot!")

#HANDLE COLLISIONS
def handle_pocket_rules(space):
    #pocket hit box
    pocket_segments = [
        #POSITION       #ANGLE        #START POINT    #END POINT
        #((27, 39), degrees2_radians(90), (0, 0), (15, 0)),
        #((40, 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((188, 138), main.degrees2_radians(-45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 10, 120), main.degrees2_radians(0), (0, 0), (25, 0)),  

        #((WIDTH - 51, 27), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 24, 39), degrees2_radians(90), (0, 0), (15, 0)),
        ((WIDTH - 203, 123), main.degrees2_radians(45), (0, 0), (25, 0)), 

        #((25, HEIGHT - 55), degrees2_radians(90), (0, 0), (15, 0)),
        #((37, HEIGHT - 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((190, HEIGHT - 145), main.degrees2_radians(45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 10, HEIGHT - 122), main.degrees2_radians(0), (0, 0), (25, 0)), 

        #((WIDTH - 58, HEIGHT - 25), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 25, HEIGHT - 51), degrees2_radians(90), (0, 0), (15, 0))
        ((WIDTH - 205, HEIGHT - 128), main.degrees2_radians(-45), (0, 0), (25, 0)) 
    ]
    for position, angle, start_point, end_point in pocket_segments:
        pocket_segment_moment = pymunk.moment_for_segment(1, start_point, end_point, 2)
        pocket_segment_body = pymunk.Body(1, pocket_segment_moment, body_type = pymunk.Body.STATIC)
        pocket_segment_body.position = position
        pocket_segment_body.angle = angle
        pocket_segment_shape = pymunk.Segment(pocket_segment_body, start_point, end_point, 4)
        pocket_segment_shape.id = 2
        pocket_segment_shape.color = pygame.Color(BLACK)
        space.add(pocket_segment_body, pocket_segment_shape)

    def collision_detected(arbiter, space, data):
        global pocketed_balls
        global ball_pocketed
        global player_one_is_solids
        global player_one_is_stripes
        global player_two_is_solids
        global player_two_is_stripes
        global solids_remaining
        global stripes_remaining
        #global message
        global solid_txt, stripe_txt
        global feed
        
        
        ball = arbiter.shapes[0]



        if arbiter.shapes[1].id <= 151515: #(1 or ball.id <= 151515):
            #message = "BALL CONTACT"
            main.POOL_BALL_CONTACT.play()

        #if arbiter.shapes[1].id == 3331397:
            #message = "RAIL CONTACT"
            #pass

        
        
        #COLLISION DETECTED / BALL POCKETED
        if arbiter.shapes[1].id == 2 and not (ball.id == 1): #OUTISDE ID NO. IS THE COLLISION DETECTOR    AND: IGNORE CUE BALL POCKET TEMP
            space.remove(ball) #ball.body,
            ball_pocketed = True
            pocketed_balls.append(ball)
            main.POOL_POCKET.play()

            if player_one_is_solids == None or player_one_is_stripes == None or player_two_is_solids == None or player_two_is_stripes == None:
                if turn % 2 == 0: #PLAYER 1 TURN
                    if ball.id <= 777:
                        player_one_is_solids = True
                        player_one_is_stripes = False
                        player_two_is_solids = False
                        player_two_is_stripes = True
                        solid_txt = "Player 1 (Solids)"
                        print("Player 1 (Solids)")
                        stripe_txt = "Player 2 (Stripes)"
                        print("Player 2 (Stripes)")

                        if ball.id == 111:
                            print("Player 1, you made the 1-Ball!")
                            feed = "Player 1, you made the 1-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(one_ball_body, one_ball_shape)
                        elif ball.id == 222:
                            print("Player 1, you made the 2-Ball!")
                            feed = "Player 1, you made the 2-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(two_ball_body, two_ball_shape)
                        elif ball.id == 333:
                            print("Player 1, you made the 3-Ball!")
                            feed = "Player 1, you made the 3-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(three_ball_body, three_ball_shape)
                        elif ball.id == 444:
                            print("Player 1, you made the 4-Ball!")
                            feed = "Player 1, you made the 4-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(four_ball_body, four_ball_shape)
                        elif ball.id == 555:
                            print("Player 1, you made the 5-Ball!")
                            feed = "Player 1, you made the 5-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(five_ball_body, five_ball_shape)
                        elif ball.id == 666:
                            print("Player 1, you made the 6-Ball!")
                            feed = "Player 1, you made the 6-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(six_ball_body, six_ball_shape)
                        elif ball.id == 777:
                            print("Player 1, you made the 7-Ball!")
                            feed = "Player 1, you made the 7-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(seven_ball_body, seven_ball_shape)

                        elif ball.id == 888:
                            print("Player 1, you made the 8-Ball!")
                            feed = "Player 1, you made the 8-Ball!"


                    elif ball.id >= 999: 
                        player_one_is_solids = False
                        player_one_is_stripes = True
                        player_two_is_solids = True
                        player_two_is_stripes = False

                        solid_txt = "Player 2 (Solids)"
                        stripe_txt = "Player 1 (Stripes)"
                        print("Player 2 (Solids)")
                        print("Player 1 (Stripes)")

                        if ball.id == 999:
                            print("Player 1, you made the 9-Ball!")
                            feed = "Player 1, you made the 9-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(nine_ball_body, nine_ball_shape)
                        elif ball.id == 101010:
                            print("Player 1, you made the 10-Ball!")
                            feed = "Player 1, you made the 10-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(ten_ball_body, ten_ball_shape)
                        elif ball.id == 111111:
                            print("Player 1, you made the 11-Ball!")
                            feed = "Player 1, you made the 11-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(eleven_ball_body, eleven_ball_shape)
                        elif ball.id == 121212:
                            print("Player 1, you made the 12-Ball!")
                            feed = "Player 1, you made the 12-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(twelve_ball_body, twelve_ball_shape)
                        elif ball.id == 131313:
                            print("Player 1, you made the 13-Ball!")
                            feed = "Player 1, you made the 13-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(thirteen_ball_body, thirteen_ball_shape)
                        elif ball.id == 141414:
                            print("Player 1, you made the 14-Ball!")
                            feed = "Player 1, you made the 14-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fourteen_ball_body, fourteen_ball_shape)
                        elif ball.id == 151515:
                            print("Player 1, you made the 15-Ball!")
                            feed = "Player 1, you made the 15-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fifteen_ball_body, fifteen_ball_shape)

                else:   #PLAYER 2 TURN
                    if ball.id <= 777:
                        player_two_is_solids = True
                        player_two_is_stripes = False
                        player_one_is_solids = False
                        player_one_is_stripes = True

                        solid_txt = "Player 2 (Solids)"
                        stripe_txt = "Player 1 (Stripes)"
                        print("Player 2 (Solids)")
                        print("Player 1 (Stripes)")

                        if ball.id == 111:
                            print("Player 2, you made the 1-Ball!")
                            feed = "Player 2, you made the 1-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(one_ball_body, one_ball_shape)
                        elif ball.id == 222:
                            print("Player 2, you made the 2-Ball!")
                            feed = "Player 2, you made the 2-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(two_ball_body, two_ball_shape)
                        elif ball.id == 333:
                            print("Player 2, you made the 3-Ball!")
                            feed = "Player 2, you made the 3-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(three_ball_body, three_ball_shape)
                        elif ball.id == 444:
                            print("Player 2, you made the 4-Ball!")
                            feed = "Player 2, you made the 4-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(four_ball_body, four_ball_shape)
                        elif ball.id == 555:
                            print("Player 2, you made the 5-Ball!")
                            feed = "Player 2, you made the 5-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(five_ball_body, five_ball_shape)
                        elif ball.id == 666:
                            print("Player 2, you made the 6-Ball!")
                            feed = "Player 2, you made the 6-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(six_ball_body, six_ball_shape)
                        elif ball.id == 777:
                            print("Player 2, you made the 7-Ball!")
                            feed = "Player 2, you made the 7-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(seven_ball_body, seven_ball_shape)

                        elif ball.id == 888:
                            print("Player 2, you made the 8-Ball!")
                            feed = "Player 2, you made the 8-Ball!"

                    elif ball.id >= 999: 
                        player_two_is_solids = False
                        player_two_is_stripes = True
                        player_one_is_solids = True
                        player_one_is_stripes = False

                        solid_txt = "Player 1 (Solids)"
                        stripe_txt = "Player 2 (Stripes)"
                        print("Player 1 (Solids)")
                        print("Player 2 (Stripes)")

                        if ball.id == 999:
                            print("Player 2, you made the 9-Ball!")
                            feed = "Player 2, you made the 9-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(nine_ball_body, nine_ball_shape)
                        elif ball.id == 101010:
                            print("Player 2, you made the 10-Ball!")
                            feed = "Player 2, you made the 10-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(ten_ball_body, ten_ball_shape)
                        elif ball.id == 111111:
                            print("Player 2, you made the 11-Ball!")
                            feed = "Player 2, you made the 11-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(eleven_ball_body, eleven_ball_shape)
                        elif ball.id == 121212:
                            print("Player 2, you made the 12-Ball!")
                            feed = "Player 2, you made the 12-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(twelve_ball_body, twelve_ball_shape)
                        elif ball.id == 131313:
                            print("Player 2, you made the 13-Ball!")
                            feed = "Player 2, you made the 13-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(thirteen_ball_body, thirteen_ball_shape)
                        elif ball.id == 141414:
                            print("Player 2, you made the 14-Ball!")
                            feed = "Player 2, you made the 14-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fourteen_ball_body, fourteen_ball_shape)
                        elif ball.id == 151515:
                            print("Player 2, you made the 15-Ball!")
                            feed = "Player 2, you made the 15-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fifteen_ball_body, fifteen_ball_shape)

            else:
                if turn % 2 == 0:
                    if ball.id == 111:
                        print("Player 1, you made the 1-Ball!")
                        feed = "Player 1, you made the 1-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(one_ball_body, one_ball_shape)
                    elif ball.id == 222:
                        print("Player 1, you made the 2-Ball!")
                        feed = "Player 1, you made the 2-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(two_ball_body, two_ball_shape)
                    elif ball.id == 333:
                        print("Player 1, you made the 3-Ball!")
                        feed = "Player 1, you made the 3-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(three_ball_body, three_ball_shape)
                    elif ball.id == 444:
                        print("Player 1, you made the 4-Ball!")
                        feed = "Player 1, you made the 4-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(four_ball_body, four_ball_shape)
                    elif ball.id == 555:
                        print("Player 1, you made the 5-Ball!")
                        feed = "Player 1, you made the 5-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(five_ball_body, five_ball_shape)
                    elif ball.id == 666:
                        print("Player 1, you made the 6-Ball!")
                        feed = "Player 1, you made the 6-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(six_ball_body, six_ball_shape)
                    elif ball.id == 777:
                        print("Player 1, you made the 7-Ball!")
                        feed = "Player 1, you made the 7-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(seven_ball_body, seven_ball_shape)
                    elif ball.id == 888:
                        print("Player 1, you made the 8-Ball!")
                        feed = "Player 1, you made the 8-Ball!"
                    elif ball.id == 999:
                        print("Player 1, you made the 9-Ball!")
                        feed = "Player 1, you made the 9-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(nine_ball_body, nine_ball_shape)
                    elif ball.id == 101010:
                        print("Player 1, you made the 10-Ball!")
                        feed = "Player 1, you made the 10-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(ten_ball_body, ten_ball_shape)
                    elif ball.id == 111111:
                        print("Player 1, you made the 11-Ball!")
                        feed = "Player 1, you made the 11-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(eleven_ball_body, eleven_ball_shape)
                    elif ball.id == 121212:
                        print("Player 1, you made the 12-Ball!")
                        feed = "Player 1, you made the 12-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(twelve_ball_body, twelve_ball_shape)
                    elif ball.id == 131313:
                        print("Player 1, you made the 13-Ball!")
                        feed = "Player 1, you made the 13-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(thirteen_ball_body, thirteen_ball_shape)
                    elif ball.id == 141414:
                        print("Player 1, you made the 14-Ball!")
                        feed = "Player 1, you made the 14-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(fourteen_ball_body, fourteen_ball_shape)
                    elif ball.id == 151515:
                        print("Player 1, you made the 15-Ball!")
                        feed = "Player 1, you made the 15-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(fifteen_ball_body, fifteen_ball_shape)
                else:
                    if ball.id == 111:
                        print("Player 2, you made the 1-Ball!")
                        feed = "Player 2, you made the 1-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(one_ball_body, one_ball_shape)
                    elif ball.id == 222:
                        print("Player 2, you made the 2-Ball!")
                        feed = "Player 2, you made the 2-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(two_ball_body, two_ball_shape)
                    elif ball.id == 333:
                        print("Player 2, you made the 3-Ball!")
                        feed = "Player 2, you made the 3-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(three_ball_body, three_ball_shape)
                    elif ball.id == 444:
                        print("Player 2, you made the 4-Ball!")
                        feed = "Player 2, you made the 4-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(four_ball_body, four_ball_shape)
                    elif ball.id == 555:
                        print("Player 2, you made the 5-Ball!")
                        feed = "Player 2, you made the 5-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(five_ball_body, five_ball_shape)
                    elif ball.id == 666:
                        print("Player 2, you made the 6-Ball!")
                        feed = "Player 2, you made the 6-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(six_ball_body, six_ball_shape)
                    elif ball.id == 777:
                        print("Player 2, you made the 7-Ball!")
                        feed = "Player 2, you made the 7-Ball!"
                        solids_remaining.remove(ball)
                        space.remove(seven_ball_body, seven_ball_shape)
                    elif ball.id == 888:
                        print("Player 2, you made the 8-Ball!")
                        feed = "Player 2, you made the 8-Ball!"
                    elif ball.id == 999:
                        print("Player 2, you made the 9-Ball!")
                        feed = "Player 2, you made the 9-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(nine_ball_body, nine_ball_shape)
                    elif ball.id == 101010:
                        print("Player 2, you made the 10-Ball!")
                        feed = "Player 2, you made the 10-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(ten_ball_body, ten_ball_shape)
                    elif ball.id == 111111:
                        print("Player 2, you made the 11-Ball!")
                        feed = "Player 2, you made the 11-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(eleven_ball_body, eleven_ball_shape)
                    elif ball.id == 121212:
                        print("Player 2, you made the 12-Ball!")
                        feed = "Player 2, you made the 12-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(twelve_ball_body, twelve_ball_shape)
                    elif ball.id == 131313:
                        print("Player 2, you made the 13-Ball!")
                        feed = "Player 2, you made the 13-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(thirteen_ball_body, thirteen_ball_shape)
                    elif ball.id == 141414:
                        print("Player 2, you made the 14-Ball!")
                        feed = "Player 2, you made the 14-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(fourteen_ball_body, fourteen_ball_shape)
                    elif ball.id == 151515:
                        print("Player 2, you made the 15-Ball!")
                        feed = "Player 2, you made the 15-Ball!"
                        stripes_remaining.remove(ball)
                        space.remove(fifteen_ball_body, fifteen_ball_shape)
        return True

    handler = space.add_default_collision_handler()
    handler.begin = collision_detected


def create_object_balls(space):
    global solid_balls, striped_balls, solids_remaining, stripes_remaining, object_balls
    solid_balls = []
    striped_balls = []
    object_balls = []
    solids_remaining = []
    stripes_remaining = []
    
    for ball in range (0, 15):
        object_ball_body = pymunk.Body()
        object_ball_shape = pymunk.Circle(object_ball_body, BALL_RADIUS)
        object_ball_shape.mass = BALL_MASS
        object_ball_shape.elasticity = BALL_ELASTICITY
        object_ball_shape.friction = BALL_FRICTION

        #SOLIDS
        if ball == 0:  #1-BALL
            object_ball_shape.color = pygame.Color(YELLOW)
            object_ball_body.position = (WIDTH/2 + 175 , HEIGHT/2)
            object_ball_shape.id = 111
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 1: #2-BALL
            object_ball_shape.color = pygame.Color(BLUE)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 - 18)
            object_ball_shape.id = 222
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 2: #3-BALL
            object_ball_shape.color = pygame.Color(RED)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 72) 
            object_ball_shape.id = 333
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 3: #4-BALL
            object_ball_shape.color = pygame.Color(PURPLE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2) 
            object_ball_shape.id = 444
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 4: #5-BALL
            object_ball_shape.color = pygame.Color(ORANGE)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 + 36)
            object_ball_shape.id = 555
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 5: #6-BALL
            object_ball_shape.color = pygame.Color(GREEN)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 54)
            object_ball_shape.id = 666
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 6: #7-BALL
            object_ball_shape.color = pygame.Color(BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 18)
            object_ball_shape.id = 777
            solid_balls.append(object_ball_shape)
            solids_remaining.append(object_ball_shape)
        elif ball == 7: #8-BALL
            object_ball_shape.color = pygame.Color(BLACK)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2)
            object_ball_shape.id = 888
        
        #STRIPES
        elif ball == 8: #9-BALL
            object_ball_shape.color = pygame.Color(LIGHT_YELLOW)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 18)
            object_ball_shape.id = 999
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        elif ball == 9: #10-BALL
            object_ball_shape.color = pygame.Color(LIGHT_BLUE)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 54)
            object_ball_shape.id = 101010
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        elif ball == 10: #11-BALL
            object_ball_shape.color = pygame.Color(LIGHT_RED)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 + 18)
            object_ball_shape.id = 111111
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        elif ball == 11: #12-BALL
            object_ball_shape.color = pygame.Color(LIGHT_PURPLE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 36)
            object_ball_shape.id = 121212
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        elif ball == 12: #13-BALL
            object_ball_shape.color = pygame.Color(LIGHT_ORANGE) 
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 - 36) 
            object_ball_shape.id = 131313
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        elif ball == 13: #14-BALL
            object_ball_shape.color = pygame.Color(LIGHT_GREEN)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 36)
            object_ball_shape.id = 141414
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)
        else: #15-BALL
            object_ball_shape.color = pygame.Color(LIGHT_BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 72) 
            object_ball_shape.id = 151515
            striped_balls.append(object_ball_shape)
            stripes_remaining.append(object_ball_shape)

        object_balls.append(object_ball_shape)
        space.add(object_ball_shape, object_ball_body)


def display_object_balls(space):
    global one_ball_body, one_ball_shape
    global two_ball_body, two_ball_shape
    global three_ball_body, three_ball_shape
    global four_ball_body, four_ball_shape
    global five_ball_body, five_ball_shape
    global six_ball_body, six_ball_shape
    global seven_ball_body, seven_ball_shape
    global nine_ball_body, nine_ball_shape
    global ten_ball_body, ten_ball_shape
    global eleven_ball_body, eleven_ball_shape
    global twelve_ball_body, twelve_ball_shape
    global thirteen_ball_body, thirteen_ball_shape
    global fourteen_ball_body, fourteen_ball_shape
    global fifteen_ball_body, fifteen_ball_shape

    one_ball_body = pymunk.Body()
    one_ball_body.position = (189, 30)
    one_ball_shape = pymunk.Circle(one_ball_body, BALL_RADIUS)
    one_ball_shape.mass = BALL_MASS
    one_ball_shape.elasticity = BALL_ELASTICITY
    one_ball_shape.friction = BALL_FRICTION
    one_ball_shape.color = pygame.Color(YELLOW)
    one_ball_shape.id = 111
    space.add(one_ball_shape, one_ball_body)

    two_ball_body = pymunk.Body()
    two_ball_body.position = (229, 30)
    two_ball_shape = pymunk.Circle(two_ball_body, BALL_RADIUS)
    two_ball_shape.mass = BALL_MASS
    two_ball_shape.elasticity = BALL_ELASTICITY
    two_ball_shape.friction = BALL_FRICTION
    two_ball_shape.color = pygame.Color(BLUE)
    two_ball_shape.id = 222
    space.add(two_ball_shape, two_ball_body)

    three_ball_body = pymunk.Body()
    three_ball_body.position = (271, 30)
    three_ball_shape = pymunk.Circle(three_ball_body, BALL_RADIUS)
    three_ball_shape.mass = BALL_MASS
    three_ball_shape.elasticity = BALL_ELASTICITY
    three_ball_shape.friction = BALL_FRICTION
    three_ball_shape.color = pygame.Color(RED)
    three_ball_shape.id = 333
    space.add(three_ball_shape, three_ball_body)

    four_ball_body = pymunk.Body()
    four_ball_body.position = (312, 30)
    four_ball_shape = pymunk.Circle(four_ball_body, BALL_RADIUS)
    four_ball_shape.mass = BALL_MASS
    four_ball_shape.elasticity = BALL_ELASTICITY
    four_ball_shape.friction = BALL_FRICTION
    four_ball_shape.color = pygame.Color(PURPLE)
    four_ball_shape.id = 444
    space.add(four_ball_shape, four_ball_body)

    five_ball_body = pymunk.Body()
    five_ball_body.position = (352, 30)
    five_ball_shape = pymunk.Circle(five_ball_body, BALL_RADIUS)
    five_ball_shape.mass = BALL_MASS
    five_ball_shape.elasticity = BALL_ELASTICITY
    five_ball_shape.friction = BALL_FRICTION
    five_ball_shape.color = pygame.Color(ORANGE)
    five_ball_shape.id = 555
    space.add(five_ball_shape, five_ball_body)

    six_ball_body = pymunk.Body()
    six_ball_body.position = (394, 30)
    six_ball_shape = pymunk.Circle(six_ball_body, BALL_RADIUS)
    six_ball_shape.mass = BALL_MASS
    six_ball_shape.elasticity = BALL_ELASTICITY
    six_ball_shape.friction = BALL_FRICTION
    six_ball_shape.color = pygame.Color(GREEN)
    six_ball_shape.id = 666
    space.add(six_ball_shape, six_ball_body)

    seven_ball_body = pymunk.Body()
    seven_ball_body.position = (435, 30)
    seven_ball_shape = pymunk.Circle(seven_ball_body, BALL_RADIUS)
    seven_ball_shape.mass = BALL_MASS
    seven_ball_shape.elasticity = BALL_ELASTICITY
    seven_ball_shape.friction = BALL_FRICTION
    seven_ball_shape.color = pygame.Color(BURGUNDY)
    seven_ball_shape.id = 777
    space.add(seven_ball_shape, seven_ball_body)

    nine_ball_body = pymunk.Body()
    nine_ball_body.position = (848, 30)
    nine_ball_shape = pymunk.Circle(nine_ball_body, BALL_RADIUS)
    nine_ball_shape.mass = BALL_MASS
    nine_ball_shape.elasticity = BALL_ELASTICITY
    nine_ball_shape.friction = BALL_FRICTION
    nine_ball_shape.color = pygame.Color(LIGHT_YELLOW)
    nine_ball_shape.id = 999
    space.add(nine_ball_shape, nine_ball_body)
    
    ten_ball_body = pymunk.Body()
    ten_ball_body.position = (889, 30)
    ten_ball_shape = pymunk.Circle(ten_ball_body, BALL_RADIUS)
    ten_ball_shape.mass = BALL_MASS
    ten_ball_shape.elasticity = BALL_ELASTICITY
    ten_ball_shape.friction = BALL_FRICTION
    ten_ball_shape.color = pygame.Color(LIGHT_BLUE)
    ten_ball_shape.id = 101010
    space.add(ten_ball_shape, ten_ball_body)

    eleven_ball_body = pymunk.Body()
    eleven_ball_body.position = (930, 30)
    eleven_ball_shape = pymunk.Circle(eleven_ball_body, BALL_RADIUS)
    eleven_ball_shape.mass = BALL_MASS
    eleven_ball_shape.elasticity = BALL_ELASTICITY
    eleven_ball_shape.friction = BALL_FRICTION
    eleven_ball_shape.color = pygame.Color(LIGHT_RED)
    eleven_ball_shape.id = 111111
    space.add(eleven_ball_shape, eleven_ball_body)

    twelve_ball_body = pymunk.Body()
    twelve_ball_body.position = (970, 30)
    twelve_ball_shape = pymunk.Circle(twelve_ball_body, BALL_RADIUS)
    twelve_ball_shape.mass = BALL_MASS
    twelve_ball_shape.elasticity = BALL_ELASTICITY
    twelve_ball_shape.friction = BALL_FRICTION
    twelve_ball_shape.color = pygame.Color(LIGHT_PURPLE)
    twelve_ball_shape.id = 121212
    space.add(twelve_ball_shape, twelve_ball_body)

    thirteen_ball_body = pymunk.Body()
    thirteen_ball_body.position = (1011, 30)
    thirteen_ball_shape = pymunk.Circle(thirteen_ball_body, BALL_RADIUS)
    thirteen_ball_shape.mass = BALL_MASS
    thirteen_ball_shape.elasticity = BALL_ELASTICITY
    thirteen_ball_shape.friction = BALL_FRICTION
    thirteen_ball_shape.color = pygame.Color(LIGHT_ORANGE)
    thirteen_ball_shape.id = 131313
    space.add(thirteen_ball_shape, thirteen_ball_body)

    fourteen_ball_body = pymunk.Body()
    fourteen_ball_body.position = (1052, 30)
    fourteen_ball_shape = pymunk.Circle(fourteen_ball_body, BALL_RADIUS)
    fourteen_ball_shape.mass = BALL_MASS
    fourteen_ball_shape.elasticity = BALL_ELASTICITY
    fourteen_ball_shape.friction = BALL_FRICTION
    fourteen_ball_shape.color = pygame.Color(LIGHT_GREEN)
    fourteen_ball_shape.id = 141414
    space.add(fourteen_ball_shape, fourteen_ball_body)

    fifteen_ball_body = pymunk.Body()
    fifteen_ball_body.position = (1093, 30)
    fifteen_ball_shape = pymunk.Circle(fifteen_ball_body, BALL_RADIUS)
    fifteen_ball_shape.mass = BALL_MASS
    fifteen_ball_shape.elasticity = BALL_ELASTICITY
    fifteen_ball_shape.friction = BALL_FRICTION
    fifteen_ball_shape.color = pygame.Color(LIGHT_BURGUNDY)
    fifteen_ball_shape.id = 151515
    space.add(fifteen_ball_shape, fifteen_ball_body)
