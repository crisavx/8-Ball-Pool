from constants import *
from main import *
import main as main

import pygame, pymunk, pymunk.pygame_util

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

    global one_ball_body, one_ball_shape
    global two_ball_body, two_ball_shape
    global three_ball_body, three_ball_shape
    global four_ball_body, four_ball_shape
    global five_ball_body, five_ball_shape
    global six_ball_body, six_ball_shape
    global seven_ball_body, seven_ball_shape
    global eight_ball_body, eight_ball_shape
    global nine_ball_body, nine_ball_shape
    global ten_ball_body, ten_ball_shape
    global eleven_ball_body, eleven_ball_shape
    global twelve_ball_body, twelve_ball_shape
    global thirteen_ball_body, thirteen_ball_shape
    global fourteen_ball_body, fourteen_ball_shape
    global fifteen_ball_body, fifteen_ball_shape
    
    one_ball_body = pymunk.Body()
    one_ball_body.position = (WIDTH/2 + 175 , HEIGHT/2)
    one_ball_shape = pymunk.Circle(one_ball_body, BALL_RADIUS)
    one_ball_shape.mass = BALL_MASS
    one_ball_shape.elasticity = BALL_ELASTICITY
    one_ball_shape.friction = BALL_FRICTION
    one_ball_shape.color = pygame.Color(YELLOW)
    one_ball_shape.id = 111
    object_balls.append(one_ball_shape)
    space.add(one_ball_shape, one_ball_body)
    

    two_ball_body = pymunk.Body()
    two_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 - 18)
    two_ball_shape = pymunk.Circle(two_ball_body, BALL_RADIUS)
    two_ball_shape.mass = BALL_MASS
    two_ball_shape.elasticity = BALL_ELASTICITY
    two_ball_shape.friction = BALL_FRICTION
    two_ball_shape.color = pygame.Color(BLUE)
    two_ball_shape.id = 222
    object_balls.append(two_ball_shape)
    space.add(two_ball_shape, two_ball_body)

    three_ball_body = pymunk.Body()
    three_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 72)
    three_ball_shape = pymunk.Circle(three_ball_body, BALL_RADIUS)
    three_ball_shape.mass = BALL_MASS
    three_ball_shape.elasticity = BALL_ELASTICITY
    three_ball_shape.friction = BALL_FRICTION
    three_ball_shape.color = pygame.Color(RED)
    three_ball_shape.id = 333
    object_balls.append(three_ball_shape)
    space.add(three_ball_shape, three_ball_body)

    four_ball_body = pymunk.Body()
    four_ball_body.position = (WIDTH/2 + 291, HEIGHT/2)
    four_ball_shape = pymunk.Circle(four_ball_body, BALL_RADIUS)
    four_ball_shape.mass = BALL_MASS
    four_ball_shape.elasticity = BALL_ELASTICITY
    four_ball_shape.friction = BALL_FRICTION
    four_ball_shape.color = pygame.Color(PURPLE)
    four_ball_shape.id = 444
    object_balls.append(four_ball_shape)
    space.add(four_ball_shape, four_ball_body)

    five_ball_body = pymunk.Body()
    five_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 + 36)
    five_ball_shape = pymunk.Circle(five_ball_body, BALL_RADIUS)
    five_ball_shape.mass = BALL_MASS
    five_ball_shape.elasticity = BALL_ELASTICITY
    five_ball_shape.friction = BALL_FRICTION
    five_ball_shape.color = pygame.Color(ORANGE)
    five_ball_shape.id = 555
    object_balls.append(five_ball_shape)
    space.add(five_ball_shape, five_ball_body)

    six_ball_body = pymunk.Body()
    six_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 54)
    six_ball_shape = pymunk.Circle(six_ball_body, BALL_RADIUS)
    six_ball_shape.mass = BALL_MASS
    six_ball_shape.elasticity = BALL_ELASTICITY
    six_ball_shape.friction = BALL_FRICTION
    six_ball_shape.color = pygame.Color(GREEN)
    six_ball_shape.id = 666
    object_balls.append(six_ball_shape)
    space.add(six_ball_shape, six_ball_body)

    seven_ball_body = pymunk.Body()
    seven_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 18)
    seven_ball_shape = pymunk.Circle(seven_ball_body, BALL_RADIUS)
    seven_ball_shape.mass = BALL_MASS
    seven_ball_shape.elasticity = BALL_ELASTICITY
    seven_ball_shape.friction = BALL_FRICTION
    seven_ball_shape.color = pygame.Color(BURGUNDY)
    seven_ball_shape.id = 777
    object_balls.append(seven_ball_shape)
    space.add(seven_ball_shape, seven_ball_body)

    eight_ball_body = pymunk.Body()
    eight_ball_body.position = (WIDTH/2 + 233, HEIGHT/2)
    eight_ball_shape = pymunk.Circle(eight_ball_body, BALL_RADIUS)
    eight_ball_shape.mass = BALL_MASS
    eight_ball_shape.elasticity = BALL_ELASTICITY
    eight_ball_shape.friction = BALL_FRICTION
    eight_ball_shape.color = pygame.Color(BLACK)
    eight_ball_shape.id = 888
    object_balls.append(eight_ball_shape)
    space.add(eight_ball_shape, eight_ball_body)

    nine_ball_body = pymunk.Body()
    nine_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 18)
    nine_ball_shape = pymunk.Circle(nine_ball_body, BALL_RADIUS)
    nine_ball_shape.mass = BALL_MASS
    nine_ball_shape.elasticity = BALL_ELASTICITY
    nine_ball_shape.friction = BALL_FRICTION
    nine_ball_shape.color = pygame.Color(LIGHT_YELLOW)
    nine_ball_shape.id = 999
    object_balls.append(nine_ball_shape)
    space.add(nine_ball_shape, nine_ball_body)

    ten_ball_body = pymunk.Body()
    ten_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 54)
    ten_ball_shape = pymunk.Circle(ten_ball_body, BALL_RADIUS)
    ten_ball_shape.mass = BALL_MASS
    ten_ball_shape.elasticity = BALL_ELASTICITY
    ten_ball_shape.friction = BALL_FRICTION
    ten_ball_shape.color = pygame.Color(LIGHT_BLUE)
    ten_ball_shape.id = 101010
    object_balls.append(ten_ball_shape)
    space.add(ten_ball_shape, ten_ball_body)

    eleven_ball_body = pymunk.Body()
    eleven_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 + 18)
    eleven_ball_shape = pymunk.Circle(eleven_ball_body, BALL_RADIUS)
    eleven_ball_shape.mass = BALL_MASS
    eleven_ball_shape.elasticity = BALL_ELASTICITY
    eleven_ball_shape.friction = BALL_FRICTION
    eleven_ball_shape.color = pygame.Color(LIGHT_RED)
    eleven_ball_shape.id = 111111
    object_balls.append(eleven_ball_shape)
    space.add(eleven_ball_shape, eleven_ball_body)

    twelve_ball_body = pymunk.Body()
    twelve_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 36)
    twelve_ball_shape = pymunk.Circle(twelve_ball_body, BALL_RADIUS)
    twelve_ball_shape.mass = BALL_MASS
    twelve_ball_shape.elasticity = BALL_ELASTICITY
    twelve_ball_shape.friction = BALL_FRICTION
    twelve_ball_shape.color = pygame.Color(LIGHT_PURPLE)
    twelve_ball_shape.id = 121212
    object_balls.append(twelve_ball_shape)
    space.add(twelve_ball_shape, twelve_ball_body)

    thirteen_ball_body = pymunk.Body()
    thirteen_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 - 36)
    thirteen_ball_shape = pymunk.Circle(thirteen_ball_body, BALL_RADIUS)
    thirteen_ball_shape.mass = BALL_MASS
    thirteen_ball_shape.elasticity = BALL_ELASTICITY
    thirteen_ball_shape.friction = BALL_FRICTION
    thirteen_ball_shape.color = pygame.Color(LIGHT_ORANGE)
    thirteen_ball_shape.id = 131313
    object_balls.append(thirteen_ball_shape)
    space.add(thirteen_ball_shape, thirteen_ball_body)

    fourteen_ball_body = pymunk.Body()
    fourteen_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 36)
    fourteen_ball_shape = pymunk.Circle(fourteen_ball_body, BALL_RADIUS)
    fourteen_ball_shape.mass = BALL_MASS
    fourteen_ball_shape.elasticity = BALL_ELASTICITY
    fourteen_ball_shape.friction = BALL_FRICTION
    fourteen_ball_shape.color = pygame.Color(LIGHT_GREEN)
    fourteen_ball_shape.id = 141414
    object_balls.append(fourteen_ball_shape)
    space.add(fourteen_ball_shape, fourteen_ball_body)

    fifteen_ball_body = pymunk.Body()
    fifteen_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 72)
    fifteen_ball_shape = pymunk.Circle(fifteen_ball_body, BALL_RADIUS)
    fifteen_ball_shape.mass = BALL_MASS
    fifteen_ball_shape.elasticity = BALL_ELASTICITY
    fifteen_ball_shape.friction = BALL_FRICTION
    fifteen_ball_shape.color = pygame.Color(LIGHT_BURGUNDY)
    fifteen_ball_shape.id = 151515
    object_balls.append(fifteen_ball_shape)
    space.add(fifteen_ball_shape, fifteen_ball_body)
    
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