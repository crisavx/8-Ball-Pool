#from re import T
#from turtle import TurtleScreen
from properties import *
import pygame, pymunk, pymunk.pygame_util, math#, pyglet
from threading import Timer
import os

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Ball Pool by Cristian Lopez")

#global cue_ball_body
#cue_ball_body = pymunk.Body()

#cue_ball_sprite = pygame.image.load('cueBallT.png')
#cue_ball_img = pyglet.image.load(os.path.join('cueballT.png'))
#cue_ball_sprite = pyglet.sprite.Sprite(cue_ball_img, x = cue_ball_body.position.x, y = cue_ball_body.position.y)

POOL_SHOT = pygame.mixer.Sound(os.path.join('pool_shot.mp3'))
POOL_POCKET = pygame.mixer.Sound(os.path.join('pool_pocket.mp3'))
POOL_BALL_CONTACT = pygame.mixer.Sound(os.path.join('pool_ball_contact.mp3'))


def run(display):
    
    run = True
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = GRAVITY
    space.damping = DAMPING

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
    FONT = pygame.font.SysFont('comicsans', 30)

    print("Player 1 - Shoot!")
    global message
    message = "Player 1 - Shoot!"
    
    create_cushions(space)
    handle_pocket_collisions(space)

    draw_options = pymunk.pygame_util.DrawOptions(display)

    while run:
        
        #space.add(cue_ball_shape, cue_ball_body)
        shooting_line = [pygame.mouse.get_pos(), (cue_ball.body.position) ]
        angle = calc_angle(*shooting_line)
        angle_deg = degrees2_radians(angle)
        if angle_deg < 0:
            angle_deg += 360

        force = calc_distance(*shooting_line) * 100

        #EVENT CHECKING LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #SHOOT CUE BALL
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #MOUSE BUTTON 1 IS CLICKED
                    cue_ball.body.apply_impulse_at_local_point((force, 0))
                    line_on = False
                    POOL_SHOT.play()

                    timer_check_pocketed = Timer(5, check_ball_pocketed)
                    timer_check_pocketed.start()

                    timer_reset_pocketed = Timer(5.1, update_ball_pocketed)
                    timer_reset_pocketed.start()

                    timer = Timer(5.5, check_turn)
                    timer.start()

                    timer_reset_line = Timer(5.5, reset_line)
                    timer_reset_line.start()


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


def reset_line():
    global line_on
    line_on = True

def draw_no_line(space, display, draw_options):
    display.fill(GRAY)


    #POCKETS (NO COLLISION)
    pockets = [
        (31, 30), #TOP-LEFT
        (WIDTH / 2 - 2, 25), #TOP-MIDDLE
        (WIDTH - 27, 30), #TOP-RIGHT

        (27, HEIGHT - 30), #BOTTOM-LEFT
        (WIDTH / 2 - 2, HEIGHT - 25), #BOTTOM-MIDDLE
        (WIDTH - 34, HEIGHT - 30) #BOTTOM-RIGHT
    ]
    for position in pockets:
        pygame.draw.circle(display, BLACK, position, POCKET_SIZE)

    #for ball in stripes_remaining:
    #    display.blit(display, (250,250), ball)

    draw_text = FONT.render(message, 1, WHITE)
    display.blit(draw_text,(80,30))

    space.debug_draw(draw_options)
    pygame.display.update()


def draw_line(space, display, draw_options):
    display.fill(GRAY)

    pygame.draw.line(display, BLACK, shooting_line[0], shooting_line[1], 3), #SHOOTING LINE

    #POCKETS (NO COLLISION)
    pockets = [
        (31, 30), #TOP-LEFT
        (WIDTH / 2 - 2, 25), #TOP-MIDDLE
        (WIDTH - 27, 30), #TOP-RIGHT

        (27, HEIGHT - 30), #BOTTOM-LEFT
        (WIDTH / 2 - 2, HEIGHT - 25), #BOTTOM-MIDDLE
        (WIDTH - 34, HEIGHT - 30) #BOTTOM-RIGHT
    ]
    for position in pockets:
        pygame.draw.circle(display, BLACK, position, POCKET_SIZE)

    #for ball in stripes_remaining:
        #display.blit(ball, (250,250))

    draw_text = FONT.render(message, 1, WHITE)
    display.blit(draw_text, (80, 30))

    space.debug_draw(draw_options)
    pygame.display.update()


#GAME


def update_ball_pocketed():
    global ball_pocketed
    ball_pocketed = False

def check_ball_pocketed():
    global turn
    global message
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
        if player_one_is_solids:
            print("Player 1 (SOLIDS) - Shoot!")
            message = "Player 1 (SOLIDS) - Shoot!"
        elif player_one_is_stripes:
            print("Player 1 (STRIPES) - Shoot!")
            message = "Player 1 (STRIPES) - Shoot!"
        elif player_one_is_solids == None or player_one_is_stripes == None:
            print("Player 1 - Shoot!")
            message = "Player 1 - Shoot!"

    else:   #IF PLAYER TWO TURN
        if player_two_is_solids:
            print("Player 2 (SOLIDS) - Shoot!")
            message = "Player 2 (SOLIDS) - Shoot!"
        elif player_two_is_stripes:
            print("Player 2 (STRIPES) - Shoot!")
            message = "Player 2 (STRIPES) - Shoot!"
        elif player_two_is_solids == None or player_two_is_stripes == None:
            print("Player 2 - Shoot!")
            message = "Player 2 - Shoot!"
   

#GAME OBJECTS
def create_cushions(space):
    cushions = [
        #position,          #size
        [(245, 18), (WIDTH/2 - 120 , 35)], #UP-LEFT
        [(WIDTH/2 + 210, 18), (WIDTH/2 - 120 , 35)], #UP-RIGHT
        [(245, HEIGHT - 18), (WIDTH/2 - 120 , 35)], #DOWN-LEFT
        [(WIDTH/2 + 210, HEIGHT - 18), (WIDTH/2 - 120 , 35)], #DOWN-RIGHT
        [(18, HEIGHT/2), (35, HEIGHT/2 + 75)], #LEFT
        [(902, HEIGHT/2), (35, HEIGHT/2 + 75)] #RIGHT

    ]
    for position, size in cushions:
        cushion_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        cushion_body.position = position
        cushion_shape = pymunk.Poly.create_box(cushion_body, size)
        cushion_shape.color = pygame.Color(CREAM)
        cushion_shape.elasticity = CUSHION_ELASTICITY
        cushion_shape.friction = CUSHION_FRICTION
        cushion_shape.id = 3331397 #ID SET TO A HIGH NUMBER TO ENSURE CUSHIONS DONT DETECT COLLISIONS
        space.add(cushion_body, cushion_shape)
    
    cushion_triangles = [
        #POSITION       #VERTICES               #ANGLE
        ((74, -9), ((0,0), (45,0), (0, 40)), degrees2_radians(90)), #TOP-LEFT
        ((-4, 77), ((0,0), (45,0), (0, 40)), degrees2_radians(270)), #TOP-LEFT

        ((WIDTH/2 - 44, 36), ((0,0), (45,0), (45, 25)), degrees2_radians(270)), #TOP-MIDDLE-RIGHT
        ((WIDTH/2 + 39, -9), ((0,0), (45,0), (0, 25)), degrees2_radians(90)), #TOP-MIDDLE-LEFT
        
        ((WIDTH - 79, -4), ((0,0), (45,0), (0, 40)), degrees2_radians(0)), #TOP-LEFT
        ((WIDTH + 8, 77), ((0,0), (45,0), (0, 40)), degrees2_radians(180)), #TOP-RIGHT

        ((-9, HEIGHT - 77), ((0,0), (45,0), (0, 40)), degrees2_radians(0)), #BOTTOM-LEFT
        ((74, HEIGHT + 4), ((0,0), (45,0), (0, 40)), degrees2_radians(180)), #BOTTOM-RIGHT

        ((WIDTH/2 - 44, HEIGHT + 9), ((0,0), (45,0), (0, 25)), degrees2_radians(270)), #BOTTOM-MIDDLE-LEFT
        ((WIDTH/2 + 39, HEIGHT - 36), ((0,0), (45,0), (45, 25)), degrees2_radians(90)), #BOTTOM-MIDDLE-RIGHT

        ((WIDTH + 4, HEIGHT - 77), ((0,0), (45,0), (0, 40)), degrees2_radians(90)), #BOTTOM-LEFT
        ((WIDTH - 79, HEIGHT + 9), ((0,0), (45,0), (0, 40)), degrees2_radians(270)) #BOTTOM-RIGHT
    ]

    for position, vertices, angle in cushion_triangles:
        triangle_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        triangle_body.position = position
        triangle_body.angle = angle
        triangle_shape = pymunk.Poly(triangle_body, vertices)
        triangle_shape.color = pygame.Color(CREAM)
        triangle_shape.elasticity = CUSHION_ELASTICITY
        triangle_shape.friction = CUSHION_FRICTION
        triangle_shape.id = 3331397
        space.add(triangle_body, triangle_shape)

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
    #global cue_ball_body
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


#HANDLE COLLISIONS
def handle_pocket_collisions(space):
    #pocket hit box
    pocket_segments = [
        #POSITION       #ANGLE        #START POINT    #END POINT
        #((27, 39), degrees2_radians(90), (0, 0), (15, 0)),
        #((40, 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((24, 43), degrees2_radians(-45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 14, 27), degrees2_radians(0), (0, 0), (25, 0)),  

        #((WIDTH - 51, 27), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 24, 39), degrees2_radians(90), (0, 0), (15, 0)),
        ((WIDTH - 40, 25), degrees2_radians(45), (0, 0), (25, 0)), 

        #((25, HEIGHT - 55), degrees2_radians(90), (0, 0), (15, 0)),
        #((37, HEIGHT - 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((21, HEIGHT - 40), degrees2_radians(45), (0, 0), (25, 0)), 

        ((WIDTH/2 - 14, HEIGHT - 27), degrees2_radians(0), (0, 0), (25, 0)), 

        #((WIDTH - 58, HEIGHT - 25), degrees2_radians(0), (0, 0), (15, 0)),
        #((WIDTH - 25, HEIGHT - 51), degrees2_radians(90), (0, 0), (15, 0))
        ((WIDTH - 43, HEIGHT - 23), degrees2_radians(-45), (0, 0), (25, 0)) 
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

                        if ball.id == 111:
                            print("Player 1, you made the 1-Ball!")
                            message = "Player 1, you made the 1-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 222:
                            print("Player 1, you made the 2-Ball!")
                            message = "Player 1, you made the 2-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 333:
                            print("Player 1, you made the 3-Ball!")
                            message = "Player 1, you made the 3-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 444:
                            print("Player 1, you made the 4-Ball!")
                            message = "Player 1, you made the 4-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 555:
                            print("Player 1, you made the 5-Ball!")
                            message = "Player 1, you made the 5-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 666:
                            print("Player 1, you made the 6-Ball!")
                            message = "Player 1, you made the 6-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 777:
                            print("Player 1, you made the 7-Ball!")
                            message = "Player 1, you made the 7-Ball!"
                            solids_remaining.remove(ball)


                    elif ball.id >= 999: 
                        player_one_is_solids = False
                        player_one_is_stripes = True
                        player_two_is_solids = True
                        player_two_is_stripes = False

                        if ball.id == 999:
                            print("Player 1, you made the 9-Ball!")
                            message = "Player 1, you made the 9-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 101010:
                            print("Player 1, you made the 10-Ball!")
                            message = "Player 1, you made the 10-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 111111:
                            print("Player 1, you made the 11-Ball!")
                            message = "Player 1, you made the 11-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 121212:
                            print("Player 1, you made the 12-Ball!")
                            message = "Player 1, you made the 12-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 131313:
                            print("Player 1, you made the 13-Ball!")
                            message = "Player 1, you made the 13-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 141414:
                            print("Player 1, you made the 14-Ball!")
                            message = "Player 1, you made the 14-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 151515:
                            print("Player 1, you made the 15-Ball!")
                            message = "Player 1, you made the 15-Ball!"
                            stripes_remaining.remove(ball)

                else:   #PLAYER 2 TURN
                    if ball.id <= 777:
                        player_two_is_solids = True
                        player_two_is_stripes = False
                        player_one_is_solids = False
                        player_one_is_stripes = True

                        if ball.id == 111:
                            print("Player 2, you made the 1-Ball!")
                            message = "Player 2, you made the 1-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 222:
                            print("Player 2, you made the 2-Ball!")
                            message = "Player 2, you made the 2-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 333:
                            print("Player 2, you made the 3-Ball!")
                            message = "Player 2, you made the 3-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 444:
                            print("Player 2, you made the 4-Ball!")
                            message = "Player 2, you made the 4-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 555:
                            print("Player 2, you made the 5-Ball!")
                            message = "Player 2, you made the 5-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 666:
                            print("Player 2, you made the 6-Ball!")
                            message = "Player 2, you made the 6-Ball!"
                            solids_remaining.remove(ball)
                        elif ball.id == 777:
                            print("Player 2, you made the 7-Ball!")
                            message = "Player 2, you made the 7-Ball!"
                            solids_remaining.remove(ball)

                    elif ball.id >= 999: 
                        player_two_is_solids = False
                        player_two_is_stripes = True
                        player_one_is_solids = True
                        player_one_is_stripes = False

                        if ball.id == 999:
                            print("Player 2, you made the 9-Ball!")
                            message = "Player 2, you made the 9-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 101010:
                            print("Player 2, you made the 10-Ball!")
                            message = "Player 2, you made the 10-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 111111:
                            print("Player 2, you made the 11-Ball!")
                            message = "Player 2, you made the 11-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 121212:
                            print("Player 2, you made the 12-Ball!")
                            message = "Player 2, you made the 12-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 131313:
                            print("Player 2, you made the 13-Ball!")
                            message = "Player 2, you made the 13-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 141414:
                            print("Player 2, you made the 14-Ball!")
                            message = "Player 2, you made the 14-Ball!"
                            stripes_remaining.remove(ball)
                        elif ball.id == 151515:
                            print("Player 2, you made the 15-Ball!")
                            message = "Player 2, you made the 15-Ball!"
                            stripes_remaining.remove(ball)

            else:
                if turn % 2 == 0: #PLAYER 1 TURN
                    if ball.id == 111:
                        print("Player 1, you made the 1-Ball!")
                        message = "Player 1, you made the 1-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 222:
                        print("Player 1, you made the 2-Ball!")
                        message = "Player 1, you made the 2-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 333:
                        print("Player 1, you made the 3-Ball!")
                        message = "Player 1, you made the 3-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 444:
                        print("Player 1, you made the 4-Ball!")
                        message = "Player 1, you made the 4-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 555:
                        print("Player 1, you made the 5-Ball!")
                        message = "Player 1, you made the 5-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 666:
                        print("Player 1, you made the 6-Ball!")
                        message = "Player 1, you made the 6-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 777:
                        print("Player 1, you made the 7-Ball!")
                        message = "Player 1, you made the 7-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 888:
                        print("Player 1, you made the 8-Ball!")
                        message = "Player 1, you made the 8-Ball!"
                    elif ball.id == 999:
                        print("Player 1, you made the 9-Ball!")
                        message = "Player 1, you made the 9-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 101010:
                        print("Player 1, you made the 10-Ball!")
                        message = "Player 1, you made the 10-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 111111:
                        print("Player 1, you made the 11-Ball!")
                        message = "Player 1, you made the 11-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 121212:
                        print("Player 1, you made the 12-Ball!")
                        message = "Player 1, you made the 12-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 131313:
                        print("Player 1, you made the 13-Ball!")
                        message = "Player 1, you made the 13-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 141414:
                        print("Player 1, you made the 14-Ball!")
                        message = "Player 1, you made the 14-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 151515:
                        print("Player 1, you made the 15-Ball!")
                        message = "Player 1, you made the 15-Ball!"
                        stripes_remaining.remove(ball)
                else:   #PLAYER 2 TURN
                    if ball.id == 111:
                        print("Player 2, you made the 1-Ball!")
                        message = "Player 2, you made the 1-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 222:
                        print("Player 2, you made the 2-Ball!")
                        message = "Player 2, you made the 2-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 333:
                        print("Player 2, you made the 3-Ball!")
                        message = "Player 2, you made the 3-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 444:
                        print("Player 2, you made the 4-Ball!")
                        message = "Player 2, you made the 4-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 555:
                        print("Player 2, you made the 5-Ball!")
                        message = "Player 2, you made the 5-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 666:
                        print("Player 2, you made the 6-Ball!")
                        message = "Player 2, you made the 6-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 777:
                        print("Player 2, you made the 7-Ball!")
                        message = "Player 2, you made the 7-Ball!"
                        solids_remaining.remove(ball)
                    elif ball.id == 888:
                        print("Player 2, you made the 8-Ball!")
                        message = "Player 2, you made the 8-Ball!"
                    elif ball.id == 999:
                        print("Player 2, you made the 9-Ball!")
                        message = "Player 2, you made the 9-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 101010:
                        print("Player 2, you made the 10-Ball!")
                        message = "Player 2, you made the 10-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 111111:
                        print("Player 2, you made the 11-Ball!")
                        message = "Player 2, you made the 11-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 121212:
                        print("Player 2, you made the 12-Ball!")
                        message = "Player 2, you made the 12-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 131313:
                        print("Player 2, you made the 13-Ball!")
                        message = "Player 2, you made the 13-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 141414:
                        print("Player 2, you made the 14-Ball!")
                        message = "Player 2, you made the 14-Ball!"
                        stripes_remaining.remove(ball)
                    elif ball.id == 151515:
                        print("Player 2, you made the 15-Ball!")
                        message = "Player 2, you made the 15-Ball!"
                        stripes_remaining.remove(ball)
                    

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