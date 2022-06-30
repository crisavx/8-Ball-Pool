#from re import T
#from turtle import TurtleScreen
from properties import *
import pygame, pymunk, pymunk.pygame_util, math#, time
from threading import Timer

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))

cue_ball_sprite = pygame.image.load('cueBallT.png')

#def draw_text(text):
#    draw_text = FONT.render(text, 1, WHITE)
#    display.blit(draw_text, (100, 50))
#    pygame.display.update()

def run(display):
    
    run = True
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = GRAVITY
    space.damping = DAMPING

    global shooting_line

    global object_balls
    object_balls = []
    object_balls = create_object_balls(space)

    global cue_ball
    cue_ball = create_cue_ball(space)


    global timer


    global player_one_is_solid
    player_one_is_solid = None
    global player_two_is_solid
    player_two_is_solid = None

    global turn
    turn = 0

    global ball_pocketed
    ball_pocketed = False

    global pocketed_balls
    pocketed_balls = []

    global solids_remaining
    solids_remaining = 7

    global stripes_remaining
    stripes_remaining = 7

    global FONT
    FONT = pygame.font.SysFont('comicsans', 40)

    print("Player 1 - Shoot!")
    global message
    message = "Player 1 - Shoot!"
    
    create_cushions(space)
    handle_pocket_collisions(space)

    draw_options = pymunk.pygame_util.DrawOptions(display)

    while run:
        shooting_line = [(cue_ball.body.position), pygame.mouse.get_pos()]
        angle = calc_angle(*shooting_line)
        angle_deg = degrees2_radians(angle)
        if angle_deg < 0:
            angle_deg += 360

        cue_ball.body.angle = angle
        force = calc_distance(*shooting_line) * 35

        #EVENT CHECKING LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #SHOOT CUE BALL
            if event.type == pygame.MOUSEBUTTONDOWN:
                cue_ball.body.apply_impulse_at_local_point((force, 0))
                #turn+=1

                
                timer_check_pocketed = Timer(3, check_ball_pocketed)
                timer_check_pocketed.start()

                timer_reset_pocketed = Timer(4, update_ball_pocketed)
                timer_reset_pocketed.start()

                timer = Timer(5, check_turn)
                timer.start()

        draw(space, display, draw_options)
        space.step(DELTA_TIME)
        clock.tick(FPS)

    pygame.quit()

def draw(space, display, draw_options):
    display.fill(GRAY)

    pygame.draw.line(display, BLACK, shooting_line[0], shooting_line[1], 3) #SHOOTING LINE

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

    draw_text = FONT.render(message, 1, WHITE)
    display.blit(draw_text, (100, 50))

    space.debug_draw(draw_options)
    pygame.display.update()


#GAME


def update_ball_pocketed():
    global ball_pocketed
    ball_pocketed = False

def check_ball_pocketed():
    global turn
    global message
    #turn = 0    #EVEN --> P1 TURN;  ODD --> P2 TURN
    if ball_pocketed == False:
        #global turn
        turn+=1

    #PLAYER ONE EVENTS
    elif ball_pocketed == True and (turn % 2 == 0) and (len(pocketed_balls) > 0) and (player_one_is_solid == True): #IF PLAYER ONE POCKETS A BALL AFTER GROUPS DECIDED, P1 IS SOLID
        for ball in pocketed_balls:
            if ball.id <= 777 and not 1: #MAKES SOLID, IGNORE CUE BALL
                pass
            elif ball.id == 888 and (solids_remaining > 0):
                print("PLAYER 1, YOU LOSE")
                message = "PLAYER 1, YOU LOSE"
                pygame.quit()
            elif ball.id == 888 and solids_remaining == 0:
                print("PLAYER 1, YOU WIN")
                message = "PLAYER 1, YOU WIN"
            elif ball.id >= 999 and player_one_is_solid == True:
                turn+=1
            #else:
                #turn+=1
    elif ball_pocketed == True and (turn % 2 == 0) and (len(pocketed_balls) > 0) and not (player_one_is_solid == True): #PLAYER ONE STRIPES
        for ball in pocketed_balls:
            if ball.id >= 999 and not 1: #MAKES STRIPE, IGNORE CUE BALL
                pass
            elif ball.id == 888 and (stripes_remaining > 0):
                print("PLAYER 1, YOU LOSE")
                message = "PLAYER 1, YOU LOSE"

                pygame.quit()
            elif ball.id == 888 and stripes_remaining == 0:
                print("PLAYER 1, YOU WIN")
                message = "PLAYER 1, YOU WIN"
            elif ball.id <= 777 and not (player_one_is_solid == True):
                turn+=1
            #else:
                #turn+=1

    #PLAYER TWO EVENTS
    elif ball_pocketed == True and (turn % 2 == 1) and (len(pocketed_balls) > 0) and (player_two_is_solid == True): #PLAYER TWO SOLIDS
        for ball in pocketed_balls:
            if ball.id <= 777 and not 1:    #MAKES SOLID, IGNORE CUE BALL
                pass
            elif ball.id == 888 and (solids_remaining > 0):
                print("PLAYER 2, YOU LOSE")
                message = "PLAYER 2, YOU LOSE"
            elif ball.id == 888 and solids_remaining == 0:
                print("PLAYER 2, YOU WIN")
                message = "PLAYER 2, YOU WIN"
            elif ball.id >= 999 and player_two_is_solid == True:
                turn+=1
            #else:
                #turn+=1
    elif ball_pocketed == True and (turn % 2 == 1) and (len(pocketed_balls) > 0) and not (player_two_is_solid == True): #PLAYER TWO STRIPES
        for ball in pocketed_balls:
            if ball.id >= 999 and not 1:    #MAKES STRIPED, IGNORE CUE BALL
                pass
            elif ball.id == 888 and (stripes_remaining > 0):
                print("PLAYER 2, YOU LOSE")
                message = "PLAYER 2, YOU LOSE"
            elif ball.id == 888 and stripes_remaining == 0:
                print("PLAYER 2, YOU WIN")
                message = "PLAYER 2, YOU WIN"
            elif ball.id <= 777 and not (player_two_is_solid == True):
                turn+=1
            #else:
                #turn+=1
    

    else:
        pass
    
def check_turn():
    global message
    if turn % 2 == 0:
        if player_one_is_solid == True:
            print("Player 1 (RED) - Shoot!")
            message = "Player 1 (RED) - Shoot!"
        elif player_one_is_solid == False:
            print("Player 1 (YELLOW) - Shoot!")
            message = "Player 1 (YELLOW) - Shoot!"
        elif player_one_is_solid == None:
            print("Player 1 - Shoot!")
            message = "Player 1 - Shoot!"

    else:
        if player_two_is_solid == True:
            print("Player 2 (RED) - Shoot!")
            message = "Player 2 (RED) - Shoot!"
        elif player_two_is_solid == False:
            print("Player 2 (YELLOW) - Shoot!")
            message = "Player 2 (YELLOW) - Shoot!"
        elif player_two_is_solid == None:
            print("Player 2 - Shoot!")
            message = "Player 2 - Shoot!"
   

#GAME OBJECTS
def create_cushions(space):
    #print(turn)
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
        cushion_shape.id = 99999 #ID SET TO A HIGH NUMBER TO ENSURE CUSHIONS DONT DETECT COLLISIONS
        space.add(cushion_body, cushion_shape)
    
    #(14, -4), ((0,0), (60,0), (60, 40)), 0),
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
        triangle_shape.id = 99999
        space.add(triangle_body, triangle_shape)

def create_object_balls(space):
    global solid_balls, striped_balls
    solid_balls = []
    striped_balls = []
    for i in range (0, 15):
        object_ball_body = pymunk.Body()
        object_ball_shape = pymunk.Circle(object_ball_body, BALL_RADIUS)
        object_ball_shape.mass = BALL_MASS
        object_ball_shape.elasticity = BALL_ELASTICITY
        object_ball_shape.friction = BALL_FRICTION

        #SOLIDS
        if i == 0:  #1-BALL
            object_ball_shape.color = pygame.Color(RED)#YELLOW)
            object_ball_body.position = (WIDTH/2 + 175 , HEIGHT/2)
            object_ball_shape.id = 111
            solid_balls.append(object_ball_shape)
            
        elif i == 1: #2-BALL
            object_ball_shape.color = pygame.Color(RED)#BLUE)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 - 18)
            object_ball_shape.id = 222
            solid_balls.append(object_ball_shape)
        elif i == 2: #3-BALL
            object_ball_shape.color = pygame.Color(RED)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 72) 
            object_ball_shape.id = 333
            solid_balls.append(object_ball_shape)
        elif i == 3: #4-BALL
            object_ball_shape.color = pygame.Color(RED)#PURPLE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2) 
            object_ball_shape.id = 444
            solid_balls.append(object_ball_shape)
        elif i == 4: #5-BALL
            object_ball_shape.color = pygame.Color(RED)#ORANGE)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 + 36)
            object_ball_shape.id = 555
            solid_balls.append(object_ball_shape)
        elif i == 5: #6-BALL
            object_ball_shape.color = pygame.Color(RED)#GREEN)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 54)
            object_ball_shape.id = 666
            solid_balls.append(object_ball_shape)
        elif i == 6: #7-BALL
            object_ball_shape.color = pygame.Color(RED)#BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 18)
            object_ball_shape.id = 777
            solid_balls.append(object_ball_shape)
        elif i == 7: #8-BALL
            object_ball_shape.color = pygame.Color(BLACK)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2)
            object_ball_shape.id = 888
        
        #STRIPES
        elif i == 8: #9-BALL
            object_ball_shape.color = pygame.Color(YELLOW)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 18)
            object_ball_shape.id = 999
            striped_balls.append(object_ball_shape)
        elif i == 9: #10-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#BLUE)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 54)
            object_ball_shape.id = 101010
            striped_balls.append(object_ball_shape)
        elif i == 10: #11-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#RED)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 + 18)
            object_ball_shape.id = 111111
            striped_balls.append(object_ball_shape)
        elif i == 11: #12-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#PURPLE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 36)
            object_ball_shape.id = 121212
            striped_balls.append(object_ball_shape)
        elif i == 12: #13-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#ORANGE) 
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 - 36) 
            object_ball_shape.id = 131313
            striped_balls.append(object_ball_shape)
        elif i == 13: #14-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#GREEN)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 36)
            object_ball_shape.id = 141414
            striped_balls.append(object_ball_shape)
        else: #15-BALL
            object_ball_shape.color = pygame.Color(YELLOW)#BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 72) 
            object_ball_shape.id = 151515
            striped_balls.append(object_ball_shape)

        object_balls.append(object_ball_shape)
        space.add(object_ball_shape, object_ball_body)
    
    return object_balls

def create_cue_ball(space):
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
    #global ball_pocketed
    #ball_pocketed = False
    #pocket hit box
    pocket_segments = [
        #POSITION       #ANGLE        #START POINT    #END POINT
        ((27, 39), degrees2_radians(90), (0, 0), (15, 0)),
        ((40, 27), degrees2_radians(0), (0, 0), (15, 0)),    

        ((WIDTH/2 - 14, 27), degrees2_radians(0), (0, 0), (25, 0)),  

        ((WIDTH - 51, 27), degrees2_radians(0), (0, 0), (15, 0)),
        ((WIDTH - 24, 39), degrees2_radians(90), (0, 0), (15, 0)),

        ((25, HEIGHT - 55), degrees2_radians(90), (0, 0), (15, 0)),
        ((37, HEIGHT - 27), degrees2_radians(0), (0, 0), (15, 0)),

        ((WIDTH/2 - 14, HEIGHT - 27), degrees2_radians(0), (0, 0), (25, 0)), 

        ((WIDTH - 58, HEIGHT - 25), degrees2_radians(0), (0, 0), (15, 0)),
        ((WIDTH - 25, HEIGHT - 51), degrees2_radians(90), (0, 0), (15, 0))
    ]
    for position, angle, start_point, end_point in pocket_segments:
        pocket_segment_moment = pymunk.moment_for_segment(1, start_point, end_point, 2)
        pocket_segment_body = pymunk.Body(1, pocket_segment_moment, body_type = pymunk.Body.STATIC)
        pocket_segment_body.position = position
        pocket_segment_body.angle = angle
        pocket_segment_shape = pymunk.Segment(pocket_segment_body, start_point, end_point, 2)
        pocket_segment_shape.id = 2
        pocket_segment_shape.color = pygame.Color(BLACK)
        space.add(pocket_segment_body, pocket_segment_shape)

    def collision_detected(arbiter, space, data):
        global pocketed_balls
        global ball_pocketed
        global player_one_is_solid
        global player_two_is_solid
        global solids_remaining
        global stripes_remaining
        global message
        
        
        #pocketed_balls = []
        ball = arbiter.shapes[0]
        
        #COLLISION DETECTED / BALL POCKETED
        if arbiter.shapes[1].id == 2 and ball.id != 1: #OUTISDE ID NO. IS THE COLLISION DETECTOR    AND: IGNORE CUE BALL POCKET TEMP
            space.remove(ball) #ball.body,

            if len(pocketed_balls) == 0:
                if turn % 2 == 0: #PLAYER 1 TURN
                    if ball.id <= 777:
                        player_one_is_solid = True
                        player_two_is_solid = False
                    elif ball.id >= 999: 
                        player_one_is_solid = False
                        player_two_is_solid = True
                else:   #PLAYER 2 TURN
                    if ball.id <= 777:
                        player_two_is_solid = True
                        player_one_is_solid = False
                    elif ball.id >= 999: 
                        player_two_is_solid = False
                        player_one_is_solid = True

            ball_pocketed = True

            #update_ball_pocketed()
            #update_ball_pocketed(ball_pocketed)
            
            #print("Ball pocketed")
            
            #reset_ball_pocketed_t = Timer(10, update_ball_pocketed(ball_pocketed))
            #reset_ball_pocketed_t.start

            if ball in object_balls: #ONLY REMOVE BALL FROM ARRAY IF BALL IS ACTUALLY IN ARRAY. (CUE BALL ISNT IN ARRAY, SO DONT TRY TO REMOVE)
                #object_balls.remove(ball)
                pocketed_balls.append(ball)

            if ball.id == 111:
                if turn % 2 == 0:
                    print("Player 1, you made the 1-Ball!")
                    message = "Player 1, you made the 1-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 1-Ball!")
                    message = "Player 2, you made the 1-Ball!"   
                    solids_remaining-=1          
            elif ball.id == 222:
                if turn % 2 == 0:
                    print("Player 1, you made the 2-Ball!")
                    message = "Player 1, you made the 2-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 2-Ball!")
                    message = "Player 2, you made the 2-Ball!"
                    solids_remaining-=1
            elif ball.id == 333:
                if turn % 2 == 0:
                    print("Player 1, you made the 3-Ball!")
                    message = "Player 1, you made the 3-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 3-Ball!")
                    message = "Player 2, you made the 3-Ball!"
                    solids_remaining-=1
            elif ball.id == 444:
                if turn % 2 == 0:
                    print("Player 1, you made the 4-Ball!")
                    message = "Player 1, you made the 4-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 4-Ball!")
                    message = "Player 2, you made the 4-Ball!"
                    solids_remaining-=1
            elif ball.id == 555:
                if turn % 2 == 0:
                    print("Player 1, you made the 5-Ball!")
                    message = "Player 1, you made the 5-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 5-Ball!")
                    message = "Player 2, you made the 5-Ball!"
                    solids_remaining-=1
            elif ball.id == 666:
                if turn % 2 == 0:
                    print("Player 1, you made the 6-Ball!")
                    message = "Player 1, you made the 6-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 6-Ball!")
                    message = "Player 2, you made the 6-Ball!"
                    solids_remaining-=1
            elif ball.id == 777:
                if turn % 2 == 0:
                    print("Player 1, you made the 7-Ball!")
                    message = "Player 1, you made the 7-Ball!"
                    solids_remaining-=1
                else:
                    print("Player 2, you made the 7-Ball!")
                    message = "Player 2, you made the 7-Ball!"
            elif ball.id == 888:
                if turn % 2 == 0:
                    print("Player 1, you made the 8-Ball!")
                    message = "Player 1, you made the 8-Ball!"
                else:
                    print("Player 2, you made the 8-Ball!")
                    message = "Player 2, you made the 8-Ball!"
            elif ball.id == 999:
                if turn % 2 == 0:
                    print("Player 1, you made the 9-Ball!")
                    message = "Player 1, you made the 9-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 9-Ball!")
                    message = "Player 2, you made the 9-Ball!"
                    stripes_remaining-=1
            elif ball.id == 101010:
                if turn % 2 == 0:
                    print("Player 1, you made the 10-Ball!")
                    message = "Player 1, you made the 10-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 10-Ball!")
                    message = "Player 2, you made the 10-Ball!"
                    stripes_remaining-=1
            elif ball.id == 111111:
                if turn % 2 == 0:
                    print("Player 1, you made the 11-Ball!")
                    message = "Player 1, you made the 11-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 11-Ball!")
                    message = "Player 2, you made the 11-Ball!"
                    stripes_remaining-=1
            elif ball.id == 121212:
                if turn % 2 == 0:
                    print("Player 1, you made the 12-Ball!")
                    message = "Player 1, you made the 12-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 12-Ball!")
                    message = "Player 2, you made the 12-Ball!"
                    stripes_remaining-=1
            elif ball.id == 131313:
                if turn % 2 == 0:
                    print("Player 1, you made the 13-Ball!")
                    message = "Player 1, you made the 13-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 13-Ball!")
                    message = "Player 2, you made the 13-Ball!"
                    stripes_remaining-=1
            elif ball.id == 141414:
                if turn % 2 == 0:
                    print("Player 1, you made the 14-Ball!")
                    message = "Player 1, you made the 14-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 14-Ball!")
                    message = "Player 2, you made the 14-Ball!"
                    stripes_remaining-=1
            elif ball.id == 151515:
                if turn % 2 == 0:
                    print("Player 1, you made the 15-Ball!")
                    message = "Player 1, you made the 15-Ball!"
                    stripes_remaining-=1
                else:
                    print("Player 2, you made the 15-Ball!")
                    message = "Player 2, you made the 15-Ball!"
                    stripes_remaining-=1
            

            
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