from main import *
from properties import *
from properties import *
import pygame, pymunk, pymunk.pygame_util, math#, pyglet
from threading import Timer
import os


def starting_stage():
    pass


def eight_ball_pocket_rules(arbiter, space, data):
    global solid_txt
    global stripe_txt
    global feed
    global ball_pocketed
    
    ball = arbiter.shapes[0]
    # OUTISDE ID NO. IS THE COLLISION DETECTOR    AND: IGNORE CUE BALL POCKET TEMP
    if arbiter.shapes[1].id == 2 and not (ball.id == 1):
            ball_pocketed = True
            pocketed_balls.append(ball)

            if player_one_is_solids == None or player_one_is_stripes == None or player_two_is_solids == None or player_two_is_stripes == None:
                if turn % 2 == 0:  # PLAYER 1 TURN
                    if ball.id <= 777:
                        player_one_is_solids = True
                        player_one_is_stripes = False
                        player_two_is_solids = False
                        player_two_is_stripes = True
                        solid_txt = "Player 1 (Solids)"
                        stripe_txt = "Player 2 (Stripes)"

                        if ball.id == 111:
                            print("You made the 1-Ball!")
                            feed = "You made the 1-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(one_ball_body, one_ball_shape)
                        elif ball.id == 222:
                            print("You made the 2-Ball!")
                            feed = "You made the 2-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(two_ball_body, two_ball_shape)
                        elif ball.id == 333:
                            print("You made the 3-Ball!")
                            feed = "You made the 3-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(three_ball_body, three_ball_shape)
                        elif ball.id == 444:
                            print("You made the 4-Ball!")
                            feed = "You made the 4-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(four_ball_body, four_ball_shape)
                        elif ball.id == 555:
                            print("You made the 5-Ball!")
                            feed = "You made the 5-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(five_ball_body, five_ball_shape)
                        elif ball.id == 666:
                            print("You made the 6-Ball!")
                            feed = "You made the 6-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(six_ball_body, six_ball_shape)
                        elif ball.id == 777:
                            print("You made the 7-Ball!")
                            feed = "You made the 7-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(seven_ball_body, seven_ball_shape)

                        elif ball.id == 888:
                            print("You made the 8-Ball!")
                            feed = "You made the 8-Ball!"

                    elif ball.id >= 999:
                        player_one_is_solids = False
                        player_one_is_stripes = True
                        player_two_is_solids = True
                        player_two_is_stripes = False

                        solid_txt = "Player 2 (Solids)"
                        stripe_txt = "Player 1 (Stripes)"

                        if ball.id == 999:
                            print("You made the 9-Ball!")
                            feed = "You made the 9-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(nine_ball_body, nine_ball_shape)
                        elif ball.id == 101010:
                            print("You made the 10-Ball!")
                            feed = "You made the 10-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(ten_ball_body, ten_ball_shape)
                        elif ball.id == 111111:
                            print("You made the 11-Ball!")
                            feed = "You made the 11-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(eleven_ball_body, eleven_ball_shape)
                        elif ball.id == 121212:
                            print("You made the 12-Ball!")
                            feed = "You made the 12-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(twelve_ball_body, twelve_ball_shape)
                        elif ball.id == 131313:
                            print("You made the 13-Ball!")
                            feed = "You made the 13-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(thirteen_ball_body,
                                         thirteen_ball_shape)
                        elif ball.id == 141414:
                            print("You made the 14-Ball!")
                            feed = "You made the 14-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fourteen_ball_body,
                                         fourteen_ball_shape)
                        elif ball.id == 151515:
                            print("You made the 15-Ball!")
                            feed = "You made the 15-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fifteen_ball_body, fifteen_ball_shape)

                else:  # PLAYER 2 TURN
                    if ball.id <= 777:
                        player_two_is_solids = True
                        player_two_is_stripes = False
                        player_one_is_solids = False
                        player_one_is_stripes = True

                        solid_txt = "Player 2 (Solids)"
                        stripe_txt = "Player 1 (Stripes)"

                        if ball.id == 111:
                            print("You made the 1-Ball!")
                            feed = "You made the 1-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(one_ball_body, one_ball_shape)
                        elif ball.id == 222:
                            print("You made the 2-Ball!")
                            feed = "You made the 2-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(two_ball_body, two_ball_shape)
                        elif ball.id == 333:
                            print("You made the 3-Ball!")
                            feed = "You made the 3-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(three_ball_body, three_ball_shape)
                        elif ball.id == 444:
                            print("You made the 4-Ball!")
                            feed = "You made the 4-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(four_ball_body, four_ball_shape)
                        elif ball.id == 555:
                            print("You made the 5-Ball!")
                            feed = "You made the 5-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(five_ball_body, five_ball_shape)
                        elif ball.id == 666:
                            print("You made the 6-Ball!")
                            feed = "You made the 6-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(six_ball_body, six_ball_shape)
                        elif ball.id == 777:
                            print("You made the 7-Ball!")
                            feed = "You made the 7-Ball!"
                            solids_remaining.remove(ball)
                            space.remove(seven_ball_body, seven_ball_shape)

                        elif ball.id == 888:
                            print("You made the 8-Ball!")
                            feed = "You made the 8-Ball!"

                    elif ball.id >= 999:
                        player_two_is_solids = False
                        player_two_is_stripes = True
                        player_one_is_solids = True
                        player_one_is_stripes = False

                        solid_txt = "Player 1 (Solids)"
                        stripe_txt = "Player 2 (Stripes)"

                        if ball.id == 999:
                            print("You made the 9-Ball!")
                            feed = "You made the 9-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(nine_ball_body, nine_ball_shape)
                        elif ball.id == 101010:
                            print("You made the 10-Ball!")
                            feed = "You made the 10-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(ten_ball_body, ten_ball_shape)
                        elif ball.id == 111111:
                            print("You made the 11-Ball!")
                            feed = "You made the 11-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(eleven_ball_body, eleven_ball_shape)
                        elif ball.id == 121212:
                            print("You made the 12-Ball!")
                            feed = "You made the 12-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(twelve_ball_body, twelve_ball_shape)
                        elif ball.id == 131313:
                            print("You made the 13-Ball!")
                            feed = "You made the 13-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(thirteen_ball_body,
                                         thirteen_ball_shape)
                        elif ball.id == 141414:
                            print("You made the 14-Ball!")
                            feed = "You made the 14-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fourteen_ball_body,
                                         fourteen_ball_shape)
                        elif ball.id == 151515:
                            print("You made the 15-Ball!")
                            feed = "You made the 15-Ball!"
                            stripes_remaining.remove(ball)
                            space.remove(fifteen_ball_body, fifteen_ball_shape)

            else:
                if ball.id == 111:
                    print("You made the 1-Ball!")
                    feed = "You made the 1-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(one_ball_body, one_ball_shape)
                elif ball.id == 222:
                    print("You made the 2-Ball!")
                    feed = "You made the 2-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(two_ball_body, two_ball_shape)
                elif ball.id == 333:
                    print("You made the 3-Ball!")
                    feed = "You made the 3-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(three_ball_body, three_ball_shape)
                elif ball.id == 444:
                    print("You made the 4-Ball!")
                    feed = "You made the 4-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(four_ball_body, four_ball_shape)
                elif ball.id == 555:
                    print("You made the 5-Ball!")
                    feed = "You made the 5-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(five_ball_body, five_ball_shape)
                elif ball.id == 666:
                    print("You made the 6-Ball!")
                    feed = "You made the 6-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(six_ball_body, six_ball_shape)
                elif ball.id == 777:
                    print("You made the 7-Ball!")
                    feed = "You made the 7-Ball!"
                    solids_remaining.remove(ball)
                    space.remove(seven_ball_body, seven_ball_shape)
                elif ball.id == 888:
                    print("You made the 8-Ball!")
                    feed = "You made the 8-Ball!"
                elif ball.id == 999:
                    print("You made the 9-Ball!")
                    feed = "You made the 9-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(nine_ball_body, nine_ball_shape)
                elif ball.id == 101010:
                    print("You made the 10-Ball!")
                    feed = "You made the 10-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(ten_ball_body, ten_ball_shape)
                elif ball.id == 111111:
                    print("You made the 11-Ball!")
                    feed = "You made the 11-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(eleven_ball_body, eleven_ball_shape)
                elif ball.id == 121212:
                    print("You made the 12-Ball!")
                    feed = "You made the 12-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(twelve_ball_body, twelve_ball_shape)
                elif ball.id == 131313:
                    print("You made the 13-Ball!")
                    feed = "You made the 13-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(thirteen_ball_body, thirteen_ball_shape)
                elif ball.id == 141414:
                    print("You made the 14-Ball!")
                    feed = "You made the 14-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(fourteen_ball_body, fourteen_ball_shape)
                elif ball.id == 151515:
                    print("You made the 15-Ball!")
                    feed = "You made the 15-Ball!"
                    stripes_remaining.remove(ball)
                    space.remove(fifteen_ball_body, fifteen_ball_shape)

    return True

    handler = space.add_default_collision_handler()
    handler.begin = collision_detected


