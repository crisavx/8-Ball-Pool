from properties import *
import pygame, pymunk, pymunk.pygame_util, math

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))

def run(display):
    run = True
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = GRAVITY
    space.damping = DAMPING

    global turn
    turn = 0 #EVEN NUMBER --> PLAYER 1 TURN;    ODD NUMBER --> PLAYER 2 TURN


    global shooting_line

    global object_balls
    object_balls = []
    object_balls = create_object_balls(space)

    global cue_ball
    cue_ball = create_cue_ball(space)

    global striped_balls
    striped_balls = []
    for ball in object_balls:
        if ball.id >= 999:
            striped_balls.append(ball)

    global solid_balls
    solid_balls = []
    for ball in object_balls:
        if ball.id <= 777:
            solid_balls.append(ball)

    global pocketed_balls
    pocketed_balls = []

    create_cushions(space)
    handle_pocket_collisions(space)
    start_game()

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

            #IF MOUSE EVENT
            if event.type == pygame.MOUSEBUTTONDOWN:
                cue_ball.body.apply_impulse_at_local_point((force, 0)) #SHOOT BALL
                
                turn += 1 #UPDATE TURN
                if turn % 2 == 0:
                    print("\n\n\n\nPlayer 1 - Shoot!")
                else:
                    print("\n\n\n\nPlayer 2 - Shoot!")


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

    space.debug_draw(draw_options)
    pygame.display.update()

#GAME & RULES
def start_game():
    print("Player 1 - Shoot!")

def draw_pocketed_balls(space): #CALL THIS FUNCTION IN HANDLER FUNCTION, HAVE PRESET LOCATIONS FOR EACH BALL(ID)

    pass


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
    #object_balls = [] #ARRAY OF BALL 'SHAPES'
    #solid_balls = []
    #striped_balls = []
    
    for i in range (0, 15):
        object_ball_body = pymunk.Body()
        object_ball_shape = pymunk.Circle(object_ball_body, BALL_RADIUS)
        object_ball_shape.mass = BALL_MASS
        object_ball_shape.elasticity = BALL_ELASTICITY
        object_ball_shape.friction = BALL_FRICTION

        #SOLIDS
        if i == 0:  #1-BALL
            object_ball_shape.color = pygame.Color(YELLOW)
            object_ball_body.position = (WIDTH/2 + 175 , HEIGHT/2)
            object_ball_shape.id = 111
            
        elif i == 1: #2-BALL
            object_ball_shape.color = pygame.Color(BLUE)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 - 18)
            object_ball_shape.id = 222
        elif i == 2: #3-BALL
            object_ball_shape.color = pygame.Color(RED)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 72)
            object_ball_shape.id = 333
        elif i == 3: #4-BALL
            object_ball_shape.color = pygame.Color(PURPLE)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 - 36)
            object_ball_shape.id = 444
        elif i == 4: #5-BALL
            object_ball_shape.color = pygame.Color(ORANGE)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2 + 36)
            object_ball_shape.id = 555
        elif i == 5: #6-BALL
            object_ball_shape.color = pygame.Color(GREEN)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 54)
            object_ball_shape.id = 666
        elif i == 6: #7-BALL
            object_ball_shape.color = pygame.Color(BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 - 18)
            object_ball_shape.id = 777
        elif i == 7: #8-BALL
            object_ball_shape.color = pygame.Color(BLACK)
            object_ball_body.position = (WIDTH/2 + 233, HEIGHT/2)
            object_ball_shape.id = 888
        
        #STRIPES
        elif i == 8: #9-BALL
            object_ball_shape.color = pygame.Color(YELLOW)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 18)
            object_ball_shape.id = 999
        elif i == 9: #10-BALL
            object_ball_shape.color = pygame.Color(BLUE)
            object_ball_body.position = (WIDTH/2 + 262, HEIGHT/2 + 54)
            object_ball_shape.id = 101010
        elif i == 10: #11-BALL
            object_ball_shape.color = pygame.Color(RED)
            object_ball_body.position = (WIDTH/2 + 204, HEIGHT/2 + 18)
            object_ball_shape.id = 111111
        elif i == 11: #12-BALL
            object_ball_shape.color = pygame.Color(PURPLE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 - 36)
            object_ball_shape.id = 121212
        elif i == 12: #13-BALL
            object_ball_shape.color = pygame.Color(ORANGE)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2)
            object_ball_shape.id = 131313
        elif i == 13: #14-BALL
            object_ball_shape.color = pygame.Color(GREEN)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 36)
            object_ball_shape.id = 141414
        else: #15-BALL
            object_ball_shape.color = pygame.Color(BURGUNDY)
            object_ball_body.position = (WIDTH/2 + 291, HEIGHT/2 + 72)
            object_ball_shape.id = 151515

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

    pocket_segments = [
        #POSITION       #ANGLE
        ((27, 39), degrees2_radians(90)),
        ((40, 27), degrees2_radians(0)),    

        ((WIDTH/2 - 12, 27), degrees2_radians(0)), 
        ((WIDTH/2 - 4, 27), degrees2_radians(0)), 

        ((WIDTH - 51, 27), degrees2_radians(0)),
        ((WIDTH - 24, 39), degrees2_radians(90)),

        ((25, HEIGHT - 55), degrees2_radians(90)),
        ((37, HEIGHT - 27), degrees2_radians(0)), 

        ((WIDTH/2 - 12, HEIGHT - 27), degrees2_radians(0)), 
        ((WIDTH/2 - 4, HEIGHT - 27), degrees2_radians(0)), 

        ((WIDTH - 58, HEIGHT - 25), degrees2_radians(0)),
        ((WIDTH - 25, HEIGHT - 51), degrees2_radians(90))
    ]
    for position, angle in pocket_segments:
        pocket_segment_moment = pymunk.moment_for_segment(1, (0, 0), (15, 0), 2)
        pocket_segment_body = pymunk.Body(1, pocket_segment_moment, body_type = pymunk.Body.STATIC)
        pocket_segment_body.position = position
        pocket_segment_body.angle = angle
        pocket_segment_shape = pymunk.Segment(pocket_segment_body, (0, 0), (15, 0), 2)
        pocket_segment_shape.id = 2
        pocket_segment_shape.color = pygame.Color(BLACK)
        space.add(pocket_segment_body, pocket_segment_shape)

    def collision_detected(arbiter, space, data):
        #pocketed_balls = []
        ball = arbiter.shapes[0]
        
        #COLLISION DETECTED / BALL POCKETED
        if arbiter.shapes[1].id == 2: #OUTISDE ID NO. IS THE COLLISION DETECTOR
            space.remove(ball.body, ball)
            if ball in object_balls: #ONLY REMOVE BALL FROM ARRAY IF BALL IS ACTUALLY IN ARRAY. (CUE BALL ISNT IN ARRAY, SO DONT TRY TO REMOVE)
                object_balls.remove(ball)
                pocketed_balls.append(ball)
            if ball.id <= 777:  #IF SOLID BALL GETS POCKETED
                solid_balls.remove(ball)    #REMOVE SOLID BALL FROM LIST

                if ball.id == 111:
                    print("You made the 1-Ball!")
                if ball.id == 222:
                    print("You made the 2-Ball!")
                if ball.id == 333:
                    print("You made the 3-Ball!")
                if ball.id == 444:
                    print("You made the 4-Ball!")
                if ball.id == 555:
                    print("You made the 5-Ball!")
                if ball.id == 666:
                    print("You made the 6-Ball!")
                if ball.id == 777:
                    print("You made the 7-Ball!")
                #print(solid_balls)

            if ball.id >= 999: #IF STRIPED BALL GETS POCKETED
                striped_balls.remove(ball)  #REMOVE STRIPED BALL FROM LIST

                if ball.id == 999:
                    print("You made the 9-Ball!")
                if ball.id == 101010:
                    print("You made the 10-Ball!")
                if ball.id == 111111:
                    print("You made the 11-Ball!")
                if ball.id == 121212:
                    print("You made the 12-Ball!")
                if ball.id == 131313:
                    print("You made the 13-Ball!")
                if ball.id == 141414:
                    print("You made the 14-Ball!")
                if ball.id == 151515:
                    print("You made the 15-Ball!")
            
            if ball.id == 888:
                print("You made the 8-Ball!")
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