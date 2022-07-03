from properties import *
from eight_ball import *
from main import *
import pygame, pymunk, pymunk.pygame_util, math

#global solids_remaining
#solids_remaining = []

#global stripes_remaining
#stripes_remaining = []

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
        ((242, 96), ((0,0), (45,0), (0, 40)), degrees2_radians(90)), #TOP-LEFT
        ((168, 175), ((0,0), (45,0), (0, 40)), degrees2_radians(270)), #TOP-LEFT

        ((WIDTH/2 - 26, 140), ((0,0), (45,0), (45, 15)), degrees2_radians(270)), #TOP-MIDDLE-RIGHT
        ((WIDTH/2 + 30, 94), ((0,0), (45,0), (0, 15)), degrees2_radians(90)), #TOP-MIDDLE-LEFT
        
        ((WIDTH - 238, 100), ((0,0), (45,0), (0, 40)), degrees2_radians(0)), #TOP-LEFT
        ((WIDTH - 160, 174), ((0,0), (45,0), (0, 40)), degrees2_radians(180)), #TOP-RIGHT

        ((163, HEIGHT - 179), ((0,0), (45,0), (0, 40)), degrees2_radians(0)), #BOTTOM-LEFT
        ((242, HEIGHT - 105), ((0,0), (45,0), (0, 40)), degrees2_radians(180)), #BOTTOM-RIGHT

        ((WIDTH/2 - 26, HEIGHT - 98), ((0,0), (45,0), (0, 15)), degrees2_radians(270)), #BOTTOM-MIDDLE-LEFT
        ((WIDTH/2 + 30, HEIGHT - 144), ((0,0), (45,0), (45, 15)), degrees2_radians(90)), #BOTTOM-MIDDLE-RIGHT

        ((WIDTH - 163, HEIGHT - 179), ((0,0), (45,0), (0, 40)), degrees2_radians(90)), #BOTTOM-LEFT
        ((WIDTH - 238, HEIGHT - 100), ((0,0), (45,0), (0, 40)), degrees2_radians(270)) #BOTTOM-RIGHT
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

def degrees2_radians(degree): #CONVERTS DEGREES TO RADIANS
    pi = math.pi
    radians = degree * (pi / 180)
    return radians


    
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