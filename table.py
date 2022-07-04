from constants import *
from main import *
import main as main

import pygame, pymunk, pymunk.pygame_util, math

def create_cushions(space):
    cushions = [
        #position,          #size
        [(428, 117), (370, 48)], #UP-LEFT
        [(856, 117), (370, 48)], #UP-RIGHT
        [(428, HEIGHT - 121), (370, 48)], #DOWN-LEFT
        [(856, HEIGHT - 121), (370, 48)], #DOWN-RIGHT
        [(184, HEIGHT/2 - 2), (48, HEIGHT/2 + 5)], #LEFT
        [(1285 - 186, HEIGHT/2 - 2), (48, HEIGHT/2 + 6)] #RIGHT

    ]
    for position, size in cushions:
        cushion_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        cushion_body.position = position
        cushion_shape = pymunk.Poly.create_box(cushion_body, size)
        cushion_shape.color = pygame.Color(NAVY)
        cushion_shape.elasticity = CUSHION_ELASTICITY
        cushion_shape.friction = CUSHION_FRICTION
        cushion_shape.id = 3331397 #ID SET TO A HIGH NUMBER TO ENSURE CUSHIONS DONT DETECT COLLISIONS
        space.add(cushion_body, cushion_shape)
    
    cushion_triangles = [
        #POSITION       #VERTICES               #ANGLE
        ((242, 96), ((0,0), (45,0), (0, 40)), main.degrees2_radians(90)), #TOP-LEFT
        ((168, 175), ((0,0), (45,0), (0, 40)), main.degrees2_radians(270)), #TOP-LEFT

        ((WIDTH/2 - 26, 140), ((0,0), (45,0), (45, 15)), main.degrees2_radians(270)), #TOP-MIDDLE-RIGHT
        ((WIDTH/2 + 30, 94), ((0,0), (45,0), (0, 15)), main.degrees2_radians(90)), #TOP-MIDDLE-LEFT
        
        ((WIDTH - 238, 100), ((0,0), (45,0), (0, 40)), main.degrees2_radians(0)), #TOP-LEFT
        ((WIDTH - 160, 174), ((0,0), (45,0), (0, 40)), main.degrees2_radians(180)), #TOP-RIGHT

        ((163, HEIGHT - 179), ((0,0), (45,0), (0, 40)), main.degrees2_radians(0)), #BOTTOM-LEFT
        ((242, HEIGHT - 105), ((0,0), (45,0), (0, 40)), main.degrees2_radians(180)), #BOTTOM-RIGHT

        ((WIDTH/2 - 26, HEIGHT - 98), ((0,0), (45,0), (0, 15)), main.degrees2_radians(270)), #BOTTOM-MIDDLE-LEFT
        ((WIDTH/2 + 30, HEIGHT - 144), ((0,0), (45,0), (45, 15)), main.degrees2_radians(90)), #BOTTOM-MIDDLE-RIGHT

        ((WIDTH - 163, HEIGHT - 179), ((0,0), (45,0), (0, 40)), main.degrees2_radians(90)), #BOTTOM-LEFT
        ((WIDTH - 238, HEIGHT - 100), ((0,0), (45,0), (0, 40)), main.degrees2_radians(270)) #BOTTOM-RIGHT
    ]

    for position, vertices, angle in cushion_triangles:
        triangle_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        triangle_body.position = position
        triangle_body.angle = angle
        triangle_shape = pymunk.Poly(triangle_body, vertices)
        triangle_shape.color = pygame.Color(NAVY)
        triangle_shape.elasticity = 0.2
        triangle_shape.friction = CUSHION_FRICTION
        triangle_shape.id = 3331397
        space.add(triangle_body, triangle_shape)

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

def create_cue_ball(space):
    global cue_ball_body
    cue_ball_body = pymunk.Body()
    cue_ball_body.position = (WIDTH/2 - 229 , HEIGHT/2)
    cue_ball_shape = pymunk.Circle(cue_ball_body, BALL_RADIUS)
    cue_ball_shape.color = pygame.Color(WHITE)
    cue_ball_shape.mass = BALL_MASS
    cue_ball_shape.elasticity = BALL_ELASTICITY
    cue_ball_shape.friction = BALL_FRICTION
    cue_ball_shape.id = 1

    space.add(cue_ball_shape, cue_ball_body)
    return cue_ball_shape