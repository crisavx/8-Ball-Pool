#from re import T
#from turtle import TurtleScreen
from email import feedparser
from properties import *
import pygame, pymunk, pymunk.pygame_util, math#, pyglet
from threading import Timer
import os

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Ball Pool by Cristian Lopez")

#global cue_ball_body
#cue_ball_body = pymunk.Body()

#global cue_ball_body
#global cue_ball_shape

#cue_ball_img = pyglet.image.load(os.path.join('cueballT.png'))
#cue_ball_sprite = pygame.image.load(os.path.join('cueballT.png')
#cue_ball_sprite = pyglet.sprite.Sprite(cue_ball_img, x = cue_ball_body.position.x, y = cue_ball_body.position.y)

#ASSETS

#AUDIO
POOL_SHOT = pygame.mixer.Sound(os.path.join('pool_shot.mp3'))
POOL_POCKET = pygame.mixer.Sound(os.path.join('pool_pocket.mp3'))
POOL_BALL_CONTACT = pygame.mixer.Sound(os.path.join('pool_ball_contact.mp3'))
#PICS
BACKGROUND = pygame.image.load(os.path.join('pool_table.png'))
CUSHIONS = pygame.image.load(os.path.join('cushions.png'))


def run(display):
    #global cue_ball_sprite, cue_ball_img
    #global cue_ball_body
    
    run = True

    
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = GRAVITY
    space.damping = DAMPING

    #global cushion_body
    #global cushion_shape
    #global cushions

    global shooting_line
    global line_on
    line_on = True

    global object_balls
    object_balls = []
    object_balls = create_object_balls(space)

    global cue_ball
    cue_ball = create_cue_ball(space)


    global timer


    global player_one_is_solids
    player_one_is_solids = None
    global player_one_is_stripes
    player_one_is_stripes = None
    global player_two_is_solids
    player_two_is_solids = None
    global player_two_is_stripes
    player_two_is_stripes = None

    global turn
    turn = 0

    global ball_pocketed
    ball_pocketed = False

    global pocketed_balls
    pocketed_balls = []

    global solids_remaining
    #solids_remaining = []

    global stripes_remaining
    #stripes_remaining = []

    global FONT
    global FONT2
    global FONT3
    FONT = pygame.font.SysFont('arial-bold', 50)
    FONT2 = pygame.font.SysFont('arial-bold', 26)
    FONT3 = pygame.font.SysFont('arial-bold', 60)

    print("Player 1 - Shoot!")
    global message
    message = "Player 1 - Shoot!"

    global solid_txt
    solid_txt = ""
    global stripe_txt
    stripe_txt = ""

    global feed
    feed = ""
    
    create_cushions(space)
    handle_pocket_collisions(space)
    display_object_balls(space)

    draw_options = pymunk.pygame_util.DrawOptions(display)

    while run:
        
        #draw_cushions(space)
        #create_cushions(space)
        #space.add(cue_ball_shape, cue_ball_body)
        shooting_line = [(cue_ball.body.position), pygame.mouse.get_pos()]
        angle = calc_angle(*shooting_line)
        angle_deg = degrees2_radians(angle)
        if angle_deg < 0:
            angle_deg += 360

        force = calc_distance(*shooting_line) * 50

        #EVENT CHECKING LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: #'Q' --> QUIT
                    run = False
                    break

            #SHOOT CUE BALL
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #MOUSE BUTTON 1 IS CLICKED
                    cue_ball.body.apply_impulse_at_local_point((force, 0))
                    line_on = False
                    POOL_SHOT.play()

                    timer_check_pocketed = Timer(7, check_ball_pocketed)
                    timer_check_pocketed.start()

                    timer_reset_pocketed = Timer(7.1, update_ball_pocketed)
                    timer_reset_pocketed.start()

                    timer = Timer(7.5, check_turn)
                    timer.start()

                    timer_reset_line = Timer(7.5, reset_line)
                    timer_reset_line.start()

                    timer_reset_feed = Timer(7.5, reset_feed)
                    timer_reset_feed.start()


        if line_on == True:
            cue_ball.body.angle = angle
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            draw_line(space, display, draw_options)
        elif line_on == False:
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            draw_no_line(space, display, draw_options)

        space.step(DELTA_TIME)
        clock.tick(FPS)

    pygame.quit()

def reset_feed():
    global feed
    feed = ""

def reset_line():
    global line_on
    line_on = True

def draw_no_line(space, display, draw_options):
    #global solid_txt, stripe_txt
    #display.fill(GRAY)
    #display.blit(CUSHIONS, ((0,0)))
    display.blit(BACKGROUND, ((0,0)))

    #for ball in stripes_remaining:
    #    display.blit(display, (250,250), ball)
    #cue_ball_sprite.draw()

    draw_text = FONT.render(message, 1, WHITE)
    stripe_text = FONT2.render(stripe_txt, 1, WHITE)
    solid_text = FONT2.render(solid_txt, 1, WHITE)
    feed_text = FONT3.render(feed, 1, WHITE)
    display.blit(draw_text, (WIDTH/2 - 135, 13))
    display.blit(stripe_text,(WIDTH - 162, 22))
    display.blit(solid_text, (15, 22))
    display.blit(feed_text, (WIDTH / 2 - 200, HEIGHT - 65))
    

    space.debug_draw(draw_options)
    pygame.display.update()


def draw_line(space, display, draw_options):
    #global solid_txt, stripe_txt
    #global cue_ball_sprite, cue_ball_img
    #display.fill(GRAY)
    #display.blit(CUSHIONS, ((0,0)))
    display.blit(BACKGROUND, ((0,0)))

    #cue_ball_sprite.draw()

    pygame.draw.line(display, BLACK, shooting_line[0], shooting_line[1], 3), #SHOOTING LINE

    #for ball in stripes_remaining:
        #display.blit(ball, (250,250))

    draw_text = FONT.render(message, 1, WHITE)
    stripe_text = FONT2.render(stripe_txt, 1, WHITE)
    solid_text = FONT2.render(solid_txt, 1, WHITE)
    feed_text = FONT3.render(feed, 1, WHITE)
    display.blit(draw_text, (WIDTH/2 - 135, 13))
    display.blit(stripe_text,(WIDTH - 162, 22))
    display.blit(solid_text, (15, 22))
    display.blit(feed_text, (WIDTH / 2 - 200, HEIGHT - 65))

    space.debug_draw(draw_options)
    pygame.display.update()


#GAME


def update_ball_pocketed():
    global ball_pocketed
    ball_pocketed = False

def check_ball_pocketed():
    global turn
    global message
    global stripe_txt, solid_txt
    global run
    #turn = 0    #EVEN --> P1 TURN;  ODD --> P2 TURN
    if ball_pocketed == False: #NO BALL POCKETED, UPDATE TURN
        #global turn
        turn+=1

    else: #BALL GETS POCKETED
        if turn % 2 == 0:   #PLAYER ONE TURN
            if player_one_is_solids:
                for ball in pocketed_balls:
                    if ball.id <= 777 and not (ball.id == 1): #IF SOLID GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(solids_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 1, YOU LOSE")
                        message = "PLAYER 1, YOU LOSE"
                    elif ball.id == 888 and (len(solids_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 1, YOU WIN")
                        message = "PLAYER 1, YOU WIN"
                    elif ball.id >= 999 or ball.id == 1:   #IF STRIPE GETS MADE OR CUE BALL
                        turn+=1
            if player_one_is_stripes:
                for ball in pocketed_balls:
                    if ball.id >= 999 and not (ball.id == 1): #IF STRIPED GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(stripes_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 1, YOU LOSE")
                        message = "PLAYER 1, YOU LOSE"
                    elif ball.id == 888 and (len(stripes_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 1, YOU WIN")
                        message = "PLAYER 1, YOU WIN"
                    elif ball.id <= 777 or ball.id == 1:   #IF SOLID GETS MADE
                        turn+=1
        else:   #PLAYER TWO TURN
            if player_two_is_solids:
                for ball in pocketed_balls:
                    if ball.id <= 777 and not (ball.id == 1): #IF SOLID GETS MADE, AND NOT CUE BALL
                        pass
                    elif ball.id == 888 and (len(solids_remaining) > 0): #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 2, YOU LOSE")
                        message = "PLAYER 2, YOU LOSE"
                    elif ball.id == 888 and (len(solids_remaining) == 0) and not (ball.id == 1): #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 2, YOU WIN")
                        message = "PLAYER 2, YOU WIN"
                    elif ball.id >= 999 or ball.id == 1: #IF STRIPE GETS MADE OR CUE BALL
                        turn+=1
            if player_two_is_stripes:
                for ball in pocketed_balls:
                    if ball.id >= 999 and not (ball.id == 1):   #IF IF STRIPE GETS MADE, AND NOT THE CUE BALL
                        pass
                    elif ball.id == 888 and (len(stripes_remaining) > 0):    #IF 8 BALL GETS MADE ILLEGALLY
                        print("PLAYER 2, YOU LOSE")
                        message = "PLAYER 2, YOU LOSE"
                    elif ball.id == 888 and (len(stripes_remaining) == 0) and not (ball.id == 1):    #IF 8 BALL GETS MADE LEGALLY
                        print("PLAYER 2, YOU WIN")
                        message = "PLAYER 2, YOU WIN"
                    elif ball.id >= 777 or ball.id == 1:   #IF SOLID GETS MADE OR CUE BALL
                        turn+=1

    
def check_turn():
    global message

    if turn % 2 == 0:   #IF PLAYER ONE TURN
        print("Player 1 - Shoot!")
        message = "Player 1 - Shoot!"

    else:   #IF PLAYER TWO TURN
        print("Player 2 - Shoot!")
        message = "Player 2 - Shoot!"
   

#GAME OBJECTS
#def draw_cushions(space):
    #global cushions
    #for position, size in cushions:
        #cushion_body.position = position
    #space.add(cushion_body, cushion_shape)

def create_cushions(space):
    #global cushion_body
    #global cushion_shape
    #global cushions
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
        triangle_shape.elasticity = CUSHION_ELASTICITY
        triangle_shape.friction = CUSHION_FRICTION
        triangle_shape.id = 3331397
        space.add(triangle_body, triangle_shape)

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
    

def create_object_balls(space):
    global solid_balls, striped_balls
    solid_balls = []
    striped_balls = []
    global solids_remaining
    solids_remaining = []
    global stripes_remaining
    stripes_remaining = []

    for ball in range (0, 15):

        object_ball_body = pymunk.Body()
        #object_ball_body2 = pymunk.Body()
        object_ball_shape = pymunk.Circle(object_ball_body, BALL_RADIUS)
        #object_ball_shape2 = pymunk.Circle(object_ball_body2, BALL_RADIUS)
        object_ball_shape.mass = BALL_MASS
        object_ball_shape.elasticity = BALL_ELASTICITY
        object_ball_shape.friction = BALL_FRICTION

        #SOLIDS
        if ball == 0:  #1-BALL
            object_ball_shape.color = pygame.Color(YELLOW)
            #object_ball_shape2.color = pygame.Color(YELLOW)
            object_ball_body.position = (WIDTH/2 + 175 , HEIGHT/2)
            #object_ball_body2.position = (WIDTH/2 , HEIGHT/2)
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
        space.add(object_ball_shape, object_ball_body)#, object_ball_body2, object_ball_shape2 )
    
    return object_balls

def create_cue_ball(space):
    #global cue_ball_sprite, cue_ball_img
    
    global cue_ball_body
    cue_ball_body = pymunk.Body()
    cue_ball_body.position = (WIDTH/2 - 229 , HEIGHT/2)
    cue_ball_shape = pymunk.Circle(cue_ball_body, BALL_RADIUS)
    cue_ball_shape.color = pygame.Color(WHITE)
    cue_ball_shape.mass = BALL_MASS
    cue_ball_shape.elasticity = BALL_ELASTICITY
    cue_ball_shape.friction = BALL_FRICTION
    cue_ball_shape.id = 1

    #cue_ball_img = pyglet.image.load(os.path.join('cueballT.png'))
    #cue_ball_sprite = pyglet.sprite.Sprite(cue_ball_img, x = cue_ball_body.position.x, y = cue_ball_body.position.y)

    space.add(cue_ball_shape, cue_ball_body)
    return cue_ball_shape


#HANDLE COLLISIONS
def handle_pocket_collisions(space):
    #pocket hit box
    pocket_segments = [
        #POSITION       #ANGLE        #START POINT    #END POINT
        #((27, 39), degrees2_radians(90), (0, 0), (15, 0)),
        #((40, 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((188, 138), degrees2_radians(-45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 10, 120), degrees2_radians(0), (0, 0), (25, 0)),  

        #((WIDTH - 51, 27), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 24, 39), degrees2_radians(90), (0, 0), (15, 0)),
        ((WIDTH - 203, 123), degrees2_radians(45), (0, 0), (25, 0)), 

        #((25, HEIGHT - 55), degrees2_radians(90), (0, 0), (15, 0)),
        #((37, HEIGHT - 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((190, HEIGHT - 145), degrees2_radians(45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 10, HEIGHT - 122), degrees2_radians(0), (0, 0), (25, 0)), 

        #((WIDTH - 58, HEIGHT - 25), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 25, HEIGHT - 51), degrees2_radians(90), (0, 0), (15, 0))
        ((WIDTH - 205, HEIGHT - 128), degrees2_radians(-45), (0, 0), (25, 0)) 
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
        global message
        global solid_txt, stripe_txt
        global feed
        
        ball = arbiter.shapes[0]



        if arbiter.shapes[1].id <= 151515: #(1 or ball.id <= 151515):
            #message = "BALL CONTACT"
            POOL_BALL_CONTACT.play()

        #if arbiter.shapes[1].id == 3331397:
            #message = "RAIL CONTACT"
            #pass

        
        
        #COLLISION DETECTED / BALL POCKETED
        if arbiter.shapes[1].id == 2 and not (ball.id == 1): #OUTISDE ID NO. IS THE COLLISION DETECTOR    AND: IGNORE CUE BALL POCKET TEMP
            space.remove(ball) #ball.body,
            #space.remove(display_ball) #ball.body,
            ball_pocketed = True
            pocketed_balls.append(ball)
            POOL_POCKET.play()

            if player_one_is_solids == None or player_one_is_stripes == None or player_two_is_solids == None or player_two_is_stripes == None:
                if turn % 2 == 0: #PLAYER 1 TURN
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

                else:   #PLAYER 2 TURN
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

#MATH FUNCTIONS
def degrees2_radians(degree): #CONVERTS DEGREES TO RADIANS
    pi = math.pi
    radians = degree * (pi / 180)
    
    return radians
def calc_angle(point_one, point_two):     #RETURNS ANGLE BETWEEN TWO POINTS
    return math.atan2(point_two[1] - point_one[1], point_two[0] - point_one[0])
def calc_distance(point_one, point_two): #RETURNS DISTANCE BETWEEN TWO POINTS, DISTANCE FORMULA
    return math.sqrt((point_two[1] - point_one[1])**2 + (point_two[0] - point_one[0])**2)

if __name__ == "__main__":
    run(display)