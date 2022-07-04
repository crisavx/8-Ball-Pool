import main as main
from constants import *
from main import *
import pygame, pymunk, pymunk.pygame_util, math

#feed = ""
#message = ""

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


def handle_pocket_rules(space):
    global feed
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
            main.POOL_POCKET.play()

            if ball.id == 111:
                feed = "You made the 1-Ball!"
            elif ball.id == 222:
                feed = "You made the 2-Ball!"
            elif ball.id == 333:
                feed = "You made the 3-Ball!"
            elif ball.id == 444:
                feed = "You made the 4-Ball!"
            elif ball.id == 555:
                feed = "You made the 5-Ball!"
            elif ball.id == 666:
                feed = "You made the 6-Ball!"
            elif ball.id == 777:
                feed = "You made the 7-Ball!"
            elif ball.id == 888:
                feed = "You made the 8-Ball!"
            elif ball.id == 999:
                feed = "You made the 9-Ball!"
            elif ball.id == 101010:
                feed = "You made the 10-Ball!"
            elif ball.id == 111111:
                feed = "You made the 11-Ball!"
            elif ball.id == 121212:
                feed = "You made the 12-Ball!"
            elif ball.id == 131313:
                feed = "You made the 13-Ball!"
            elif ball.id == 141414:
                feed = "You made the 141414-Ball!"
            elif ball.id == 151515:
                feed = "You made the 151515-Ball!"
            
        return True

    handler = space.add_default_collision_handler()
    handler.begin = collision_detected
