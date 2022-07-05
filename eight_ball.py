import main as main
from main import *
from constants import *
import pygame
import pymunk
import pymunk.pygame_util
import math
import table as table


global message
message = "Player 1 - Shoot!"

global solid_txt
solid_txt = ""
global stripe_txt
stripe_txt = ""

global ball_in_pocket
ball_in_pocket = False
global pocketed_balls
pocketed_balls = []


global feed
feed = ""

global turn
turn = 0  # EVEN --> P1 TURN;  ODD --> P2 TURN

global stripes_player
global solids_player
stripes_player = ""
solids_player = ""
#global ball_in_pocket
#ball_in_pocket = False

#global solids_remaining
#global stripes_remaining

# HANDLE COLLISIONS


def handle_pocket(space):
    
    # pocket hit box
    pocket_segments = [
        # POSITION       #ANGLE        #START POINT    #END POINT
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
        pocket_segment_moment = pymunk.moment_for_segment(
            1, start_point, end_point, 2)
        pocket_segment_body = pymunk.Body(
            1, pocket_segment_moment, body_type=pymunk.Body.STATIC)
        pocket_segment_body.position = position
        pocket_segment_body.angle = angle
        pocket_segment_shape = pymunk.Segment(
            pocket_segment_body, start_point, end_point, 4)
        pocket_segment_shape.id = 2
        pocket_segment_shape.color = pygame.Color(BLACK)
        space.add(pocket_segment_body, pocket_segment_shape)

    def collision_detected(arbiter, space, data):
        global ball_in_pocket
        global solid_txt
        global stripe_txt
        global feed
        global solids_player
        global stripes_player

        #global decided
        #decided = False

        ball = arbiter.shapes[0]

        if arbiter.shapes[1].id <= 151515:  # (1 or ball.id <= 151515):
            #message = "BALL CONTACT"
            main.POOL_BALL_CONTACT.play()

        # if arbiter.shapes[1].id == 3331397:
            #message = "RAIL CONTACT"
            # pass

        # COLLISION DETECTED / BALL POCKETED
        # OUTISDE ID NO. IS THE COLLISION DETECTOR    AND: IGNORE CUE BALL POCKET TEMP
        if arbiter.shapes[1].id == 2 and not (ball.id == 1):
            space.remove(ball)  # ball.body,
            ball_in_pocket = True
            pocketed_balls.append(ball)
            main.POOL_POCKET.play()
            if ball.id == 111:
                print('1ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 1-Ball!"
                else:
                    feed = "Player 2, you made the 1-Ball!"
                table.solids_remaining.remove(ball)
                #space.remove(table.one_ball_img)
                space.remove(table.one_display_body, table.one_display_shape)
            elif ball.id == 222:
                print('2ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 2-Ball!"
                else:
                    feed = "Player 2, you made the 2-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.two_display_body, table.two_display_shape)
            elif ball.id == 333:
                print('3ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 3-Ball!"
                else:
                    feed = "Player 2, you made the 3-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.three_display_body, table.three_display_shape)
            elif ball.id == 444:
                print('4ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 4-Ball!"
                else:
                    feed = "Player 2, you made the 4-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.four_display_body, table.four_display_shape)
            elif ball.id == 555:
                print('5ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 5-Ball!"
                else:
                    feed = "Player 2, you made the 5-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.five_display_body, table.five_display_shape)
            elif ball.id == 666:
                print('6ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 6-Ball!"
                else:
                    feed = "Player 2, you made the 6-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.six_display_body, table.six_display_shape)
            elif ball.id == 777:
                print('7ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 7-Ball!"
                else:
                    feed = "Player 2, you made the 7-Ball!"
                table.solids_remaining.remove(ball)
                space.remove(table.seven_display_body, table.seven_display_shape)
            elif ball.id == 888:
                print('8ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 8-Ball!"
                else:
                    feed = "Player 2, you made the 8-Ball!"
            if ball.id == 999:
                print('9ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 9-Ball!"
                else:
                    feed = "Player 2, you made the 9-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.nine_display_body, table.nine_display_shape)
            elif ball.id == 101010:
                print('10ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 10-Ball!"
                else:
                    feed = "Player 2, you made the 10-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.ten_display_body, table.ten_display_shape)
            elif ball.id == 111111:
                print('11ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 11-Ball!"
                else:
                    feed = "Player 2, you made the 11-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.eleven_display_body, table.eleven_display_shape)
            elif ball.id == 121212:
                print('12ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 12-Ball!"
                else:
                    feed = "Player 2, you made the 12-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.twelve_display_body, table.twelve_display_shape)
            elif ball.id == 131313:
                print('13ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 13-Ball!"
                else:
                    feed = "Player 2, you made the 13-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.thirteen_display_body, table.thirteen_display_shape)
            elif ball.id == 141414:
                if turn % 2 == 0:
                    feed = "Player 1, you made the 14-Ball!"
                else:
                    feed = "Player 2, you made the 14-Ball!"
                print('14ball')
                table.stripes_remaining.remove(ball)
                space.remove(table.fourteen_display_body, table.fourteen_display_shape)
            elif ball.id == 151515:
                print('15ball')
                if turn % 2 == 0:
                    feed = "Player 1, you made the 15-Ball!"
                else:
                    feed = "Player 2, you made the 15-Ball!"
                table.stripes_remaining.remove(ball)
                space.remove(table.fifteen_display_body, table.fifteen_display_shape)
            handle_rules()

        return True

    handler = space.add_default_collision_handler()
    handler.begin = collision_detected


# RULES-SEQUENCE
def handle_rules():
    global solids_player
    global stripes_player
    global turn
    global solid_txt
    global stripe_txt

    #BREAK, IF GROUPS ARE NOT SET
    if solids_player == "" or stripes_player == "":  
        # PLAYER ONE TURN
        if turn % 2 == 0:
            # IF MULTIPLE BALLS ARE MADE OFF THE BREAK
            if len(pocketed_balls) > 1:
                # IF MADE MORE SOLIDS THAN STRIPES
                if len(table.stripes_remaining) > len(table.solids_remaining):
                    solids_player = "Player 1"
                    solid_txt = "Player 1 (SOLIDS)"
                    stripes_player = "Player 2"
                    stripe_txt = "Player 2 (STRIPES)"
                    print("1Solids = " + solids_player +
                          "\nStripes = " + stripes_player)
                # IF MADE MORE STRIPES THAN SOLIDS
                elif len(table.solids_remaining) > len(table.stripes_remaining):
                    solids_player = "Player 2"
                    solid_txt = "Player 2 (SOLIDS)"
                    stripes_player = "Player 1"
                    stripe_txt = "Player 1 (STRIPES)"
                    print("2Solids = " + solids_player +
                          "\nStripes = " + stripes_player)
            # IF ONLY ONE BALL IS MADE
            else:
                for ball_pkt in pocketed_balls:
                    # SOLID MADE
                    if ball_pkt.id <= 777:
                        solids_player = "Player 1"
                        solid_txt = "Player 1 (SOLIDS)"
                        stripes_player = "Player 2"
                        stripe_txt = "Player 2 (STRIPES)"
                        print("3Solids = " + solids_player +
                              "\nStripes = " + stripes_player)
                    # STRIPE MADE
                    elif ball_pkt.id >= 999:
                        solids_player = "Player 2"
                        solid_txt = "Player 2 (SOLIDS)"
                        stripes_player = "Player 1"
                        stripe_txt = "Player 1 (STRIPES)"
                        print("4Solids = " + solids_player +
                              "\nStripes = " + stripes_player)
        # PLAYER TWO TURN
        elif turn % 2 == 1:
            if len(pocketed_balls) > 1:
                # IF MADE MORE SOLIDS THAN STRIPES
                if len(table.stripes_remaining) > len(table.solids_remaining):
                    solids_player = "Player 2"
                    solid_txt = "Player 2 (SOLIDS)"
                    stripes_player = "Player 1"
                    stripe_txt = "Player 1 (STRIPES)"
                    print("3Solids = " + solids_player +
                          "\nStripes = " + stripes_player)
                # IF MADE MORE STRIPES THAN SOLIDS
                elif len(table.solids_remaining) > len(table.stripes_remaining):
                    solids_player = "Player 1"
                    solid_txt = "Player 1 (SOLIDS)"
                    stripes_player = "Player 2"
                    stripe_txt = "Player 2 (STRIPES)"
                    print("4Solids = " + solids_player +
                          "\nStripes = " + stripes_player)
            else:
                for ball_pkt in pocketed_balls:
                    #SOLID MADE
                    if ball_pkt.id <= 777:
                        solids_player = "Player 2"
                        solid_txt = "Player 2 (SOLIDS)"
                        stripes_player = "Player 1"
                        stripe_txt = "Player 1 (STRIPES)"
                        print("3Solids = " + solids_player +
                              "\nStripes = " + stripes_player)
                    # STRIPE MADE
                    elif ball_pkt.id >= 999:
                        solids_player = "Player 1"
                        solid_txt = "Player 1 (SOLIDS)"
                        stripes_player = "Player 2"
                        stripe_txt = "Player 2 (STRIPES)"
                        print("4Solids = " + solids_player +
                              "\nStripes = " + stripes_player)

    #AFTER THE BREAK
    else:
        #IF PLAYER ONE TURN
        if is_even(turn):
            for ball_pkt in pocketed_balls:
                #IF PLAYER ONE IS SOLIDS
                if solids_player == "Player 1":
                    if ball_pkt.id <= 777 and not (ball_pkt.id == 1):  #BALL POCKETED IS SOLID
                        pass
                    elif ball_pkt.id == 888 and (len(table.solids_remaining) == 0) and not(ball_pkt.id == 1):
                        print("PLAYER 1, YOU WIN!")
                    elif ball_pkt.id == 888 and ((len(table.solids_remaining) > 0) or ball_pkt.id == 1):
                        print("PLAYER 1, YOU LOSE!")
                    elif ball_pkt.id >= 999:
                        turn+=1
                #IF PLAYER ONE IS STRIPES
                if stripes_player == "Player 1":
                    if ball_pkt.id >= 999 and not (ball_pkt.id == 1):   #BALL POCKETED IS STRIPED
                        pass
                    elif ball_pkt.id == 888 and (len(table.stripes_remaining) == 0) and not (ball_pkt.id == 1):
                        print("PLAYER 1 YOU WIN!")
                    elif ball_pkt.id == 888 and ((len(table.stripes_remaining) > 0) or ball_pkt.id == 1):
                        print("PLAYER 1, YOU LOSE!")
                    elif ball_pkt.id <= 777:
                        turn+=1
        #PLAYER TWO TURN
        elif turn % 2 == 1:
            for ball_pkt in pocketed_balls:
                #IF PLAYER TWO IS SOLIDS
                if solids_player == "Player 2":
                    if ball_pkt.id <= 777 and not (ball_pkt.id == 1):  #BALL POCKETED IS SOLID
                        pass
                    elif ball_pkt.id == 888 and (len(table.solids_remaining) == 0) and not(ball_pkt.id == 1):
                        print("PLAYER 2, YOU WIN!")
                    elif ball_pkt.id == 888 and ((len(table.solids_remaining) > 0) or ball_pkt.id == 1):
                        print("PLAYER 2, YOU LOSE!")
                    elif ball_pkt.id >= 999:
                        turn+=1
                #IF PLAYER TWO IS STRIPES
                if stripes_player == "Player 2":
                    if ball_pkt.id >= 999 and not (ball_pkt.id == 1):   #BALL POCKETED IS STRIPED
                        pass
                    elif ball_pkt.id == 888 and (len(table.stripes_remaining) == 0) and not (ball_pkt.id == 1):
                        print("PLAYER 2 YOU WIN!")
                    elif ball_pkt.id == 888 and ((len(table.stripes_remaining) > 0) or ball_pkt.id == 1):
                        print("PLAYER 2, YOU LOSE!")
                    elif ball_pkt.id <= 777:
                        turn+=1

            


def is_even(input):
    if input % 2 == 0:
        return True
    else:
        return False


def reset_feed():
    global feed
    feed = ""


def update_ball_pocketed():
    global ball_in_pocket
    ball_in_pocket = False

def check_ball_pocketed():
    global turn
    #global message
    #global stripe_txt, solid_txt
    if ball_in_pocket == False: #NO BALL POCKETED, UPDATE TURN
        turn+=1


    """
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
    """


def check_turn():
    global message

    if turn % 2 == 0:  # IF PLAYER ONE TURN
        print("Player 1 - Shoot!")
        message = ("Player 1 - Shoot!")
    else:  # IF PLAYER TWO TURN
        print("Player 2 - Shoot!")
        message = ("Player 2 - Shoot!")

