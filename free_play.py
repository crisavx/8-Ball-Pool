import main as main
from constants import *
from main import *
import pygame, pymunk, pymunk.pygame_util





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

        return True

    handler = space.add_default_collision_handler()
    handler.begin = collision_detected