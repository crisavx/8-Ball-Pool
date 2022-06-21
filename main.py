from properties import *
import pygame
import pymunk
import pymunk.pygame_util
import math
#import pyglet

pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

WINNER_FONT = pygame.font.SysFont('comicsans', 20)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def calc_distance_formula(p1, p2): #RETURNS DISTANCE BETWEEN TWO POINTS
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calc_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0]) #gives angle in radians between the two points

def draw(WINDOW, space, draw_options, line):
    WINDOW.fill(BLUE_BABY)

    pygame.draw.line(WINDOW, BLACK, line[0], line[1], 3)

    space.debug_draw(draw_options)

    pygame.display.update()

def create_table(space, width, height):
    cushions = [
        [(245, 18), (width/2 - 120 , 35)], #UP-LEFT
        [(width/2 + 210, 18), (width/2 - 120 , 35)], #UP-RIGHT
        [(245, height - 18), (width/2 - 120 , 35)], #DOWN-LEFT
        [(width/2 + 210, height - 18), (width/2 - 120 , 35)], #DOWN-RIGHT
        [(18, height/2), (35, height/2 + 75)], #LEFT
        [(902, height/2), (35, height/2 + 75)] #RIGHT
        
    ]

    for pos, size in cushions:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        cushion = pymunk.Poly.create_box(body, size)
        cushion.elasticity = 1.5
        cushion.friction = 0.5
        space.add(body, cushion)

    angled_cushions = [
        [(5, 65), (25, 60), 40],
        [(63, 7), (25, 60), 40],
        [(width/2 - 49, 4), (25, 60), 60],
        [(width/2 + 44, 4), (25, 60), -60],
        [(width - 67, 7), (25, 60), -40],
        [(width-5, 65), (25, 60), -40],
        [(6, height-68), (25, 60), 120.2],
        [(63, height-7), (25, 60), 120.2],
        [(width/2 - 47, height - 4), (25, 60), -60],
        [(width/2 + 42, height - 4), (25, 60), 60], #10
        [(width - 67, height - 7), (25, 60), -120.2],
        [(width-5, height - 65), (25, 60), 40]
    ]

    for pos, size, angle in angled_cushions:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        angled_cushion = pymunk.Poly.create_box(body, size)
        angled_cushion.elasticity = 1.5
        angled_cushion.friction = 0.5
        angled_cushion.body.angle = angle
        space.add(body, angled_cushion)

    #angled_cushion_one_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_one_body.position = (5, 65)
    #angled_cushion_one = pymunk.Poly.create_box(angled_cushion_one_body, (25, 60))
    #angled_cushion_one.color = pygame.Color(YELLOW)
    #angled_cushion_one.elasticity = 1.5
    #angled_cushion_one.friction = 0.5
    #angled_cushion_one.body.angle = 40

    #angled_cushion_two_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_two_body.position = (63, 7)
    #angled_cushion_two = pymunk.Poly.create_box(angled_cushion_two_body, (25, 60))
    #angled_cushion_two.color = pygame.Color(RED)
    #angled_cushion_two.elasticity = 1.5
    #angled_cushion_two.friction = 0.5
    #angled_cushion_two.body.angle = 40

    #angled_cushion_three_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_three_body.position = (width/2 - 49, 4)
    #angled_cushion_three = pymunk.Poly.create_box(angled_cushion_three_body, (25, 60))
    #angled_cushion_three.color = pygame.Color(ORANGE)
    #angled_cushion_three.elasticity = 1.5
    #angled_cushion_three.friction = 0.5
    #angled_cushion_three.body.angle = 60

    #angled_cushion_four_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_four_body.position = (width/2 + 44, 4)
    #angled_cushion_four = pymunk.Poly.create_box(angled_cushion_four_body, (25, 60))
    #angled_cushion_four.color = pygame.Color(BLACK)
    #angled_cushion_four.elasticity = 1.5
    #angled_cushion_four.friction = 0.5
    #angled_cushion_four.body.angle = -60

    #angled_cushion_five_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_five_body.position = (width - 67, 7)
    #angled_cushion_five = pymunk.Poly.create_box(angled_cushion_five_body, (25, 60))
    #angled_cushion_five.color = pygame.Color(RED)
    #angled_cushion_five.elasticity = 1.5
    #angled_cushion_five.friction = 0.5
    #angled_cushion_five.body.angle = -40

    #angled_cushion_six_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_six_body.position = (width-5, 65)
    #angled_cushion_six = pymunk.Poly.create_box(angled_cushion_six_body, (25, 60))
    #angled_cushion_six.color = pygame.Color(YELLOW)
    #angled_cushion_six.elasticity = 1.5
    #angled_cushion_six.friction = 0.5
    #angled_cushion_six.body.angle = -40

    #angled_cushion_seven_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_seven_body.position = (6, height-68)
    #angled_cushion_seven = pymunk.Poly.create_box(angled_cushion_seven_body, (25, 60))
    #angled_cushion_seven.color = pygame.Color(YELLOW)
    #angled_cushion_seven.elasticity = 1.5
    #angled_cushion_seven.friction = 0.5
    #angled_cushion_seven.body.angle = 120.2

    #angled_cushion_eight_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_eight_body.position = (63, height-7)
    #angled_cushion_eight = pymunk.Poly.create_box(angled_cushion_eight_body, (25, 60))
    #angled_cushion_eight.color = pygame.Color(RED)
    #angled_cushion_eight.elasticity = 1.5
    #angled_cushion_eight.friction = 0.5
    #angled_cushion_eight.body.angle = 120.2

    #angled_cushion_nine_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_nine_body.position = (width/2 - 47, height - 4)
    #angled_cushion_nine = pymunk.Poly.create_box(angled_cushion_nine_body, (25, 60))
    #angled_cushion_nine.color = pygame.Color(ORANGE)
    #angled_cushion_nine.elasticity = 1.5
    #angled_cushion_nine.friction = 0.5
    #angled_cushion_nine.body.angle = -60

    #angled_cushion_ten_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_ten_body.position = (width/2 + 44, height - 4)
    #angled_cushion_ten = pymunk.Poly.create_box(angled_cushion_ten_body, (25, 60))
    #angled_cushion_ten.color = pygame.Color(BLACK)
    #angled_cushion_ten.elasticity = 1.5
    #angled_cushion_ten.friction = 0.5
    #angled_cushion_ten.body.angle = 60

    #angled_cushion_eleven_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_eleven_body.position = (width - 67, height - 7)
    #angled_cushion_eleven = pymunk.Poly.create_box(angled_cushion_eleven_body, (25, 60))
    #angled_cushion_eleven.color = pygame.Color(RED)
    #angled_cushion_eleven.elasticity = 1.5
    #angled_cushion_eleven.friction = 0.5
    #angled_cushion_eleven.body.angle = -120.2

    #angled_cushion_twelve_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #angled_cushion_twelve_body.position = (width-5, height - 65)
    #angled_cushion_twelve = pymunk.Poly.create_box(angled_cushion_twelve_body, (25, 60))
    #angled_cushion_twelve.color = pygame.Color(YELLOW)
    #angled_cushion_twelve.elasticity = 1.5
    #angled_cushion_twelve.friction = 0.5
    #angled_cushion_twelve.body.angle = 40

    #space.add(
    #    angled_cushion_one_body, angled_cushion_one,
    #    angled_cushion_two_body, angled_cushion_two,
    #    angled_cushion_three_body, angled_cushion_three,
    #    angled_cushion_four_body, angled_cushion_four,
    #    angled_cushion_five_body, angled_cushion_five,
    #    angled_cushion_six_body, angled_cushion_six,
    #    angled_cushion_seven_body, angled_cushion_seven,
    #    angled_cushion_eight_body, angled_cushion_eight,
    #    angled_cushion_nine_body, angled_cushion_nine,
    #    angled_cushion_ten_body, angled_cushion_ten,
    #    angled_cushion_eleven_body, angled_cushion_eleven,
    #    angled_cushion_twelve_body, angled_cushion_twelve
    #)


    #angled_cushions = [
    #    [(63, 7), (25, 60)]
    #]

    #for pos, size in angled_cushions:
    #    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #    body.position = pos
    #    cushion = pymunk.Poly.create_box(body, size)
    #    cushion.color = pygame.Color(RED)
    #    cushion.elasticity = 1.5
    #    cushion.friction = 0.5
    #    cushion.body.angle = 40
    #    space.add(body, cushion)

    #cushion_triangle = [
    #    [(100, 100), (200, 100), (150, 250)  ]
    #]
    #for points in cushion_triangle:
    #    shape = pymunk.Poly(None, points)
    #    moment = pymunk.moment_for_poly(10, shape.get_vertices())
    #    body = pymunk.Body(10, moment)
    #    body.position = 550, 550
    #    shape.body = body
    #    space.add(body, shape)
    #for points in cushion_triangle:
    #    shape 
    #    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    #    moment = pymunk.moment_for_poly(10, shape.get_vertices())
    #    body.position = i



def create_object_balls(space):
    ball_list = []
    for i in range(0, 15):
        body = pymunk.Body()
        ball = pymunk.Circle(body, BALL_RADIUS)
        ball.mass = BALL_MASS
        ball.elasticity = 0.7
        ball.friction = 0.5
        #ball.body.angle = 0.8

        #CUE BALL
        #if i == 0:
        #    ball.color = pygame.Color(WHITE)
        #    body.position = (WIDTH/2 - 229 , HEIGHT/2 - 15)
        #SOLIDS
        if i == 0:
            ball.color = pygame.Color(YELLOW)
            body.position = (WIDTH/2 + 175 , HEIGHT/2)
        elif i == 1:
            ball.color = pygame.Color(ORANGE)
            body.position = (WIDTH/2 + 204, HEIGHT/2 - 18)
        elif i == 2:
            ball.color = pygame.Color(YELLOW)
            body.position = (WIDTH/2 + 204, HEIGHT/2 + 18)
        elif i == 3:
            ball.color = pygame.Color(ORANGE)
            body.position = (WIDTH/2 + 233, HEIGHT/2 - 36)
        elif i == 4:
            ball.color = pygame.Color(BLACK)
            body.position = (WIDTH/2 + 233, HEIGHT/2)
        elif i == 5:
            ball.color = pygame.Color(GREEN)
            body.position = (WIDTH/2 + 233, HEIGHT/2 + 36)
        elif i == 6:
            ball.color = pygame.Color(RED)
            body.position = (WIDTH/2 + 262, HEIGHT/2 - 54)
        elif i == 7:
            ball.color = pygame.Color(RED)
            body.position = (WIDTH/2 + 262, HEIGHT/2 - 18)
        elif i == 8:
            ball.color = pygame.Color(BLUE)
            body.position = (WIDTH/2 + 262, HEIGHT/2 + 18)
        elif i == 9:
            ball.color = pygame.Color(GREEN)
            body.position = (WIDTH/2 + 262, HEIGHT/2 + 54)
        elif i == 10:
            ball.color = pygame.Color(PURPLE)
            body.position = (WIDTH/2 + 291, HEIGHT/2 - 72)
        elif i == 11:
            ball.color = pygame.Color(PURPLE)
            body.position = (WIDTH/2 + 291, HEIGHT/2 - 36)
        elif i == 12:
            ball.color = pygame.Color(BURGUNDY)
            body.position = (WIDTH/2 + 291, HEIGHT/2)
        elif i == 13:
            ball.color = pygame.Color(BURGUNDY)
            body.position = (WIDTH/2 + 291, HEIGHT/2 + 36)
        elif i == 14:
            ball.color = pygame.Color(BLUE)
            body.position = (WIDTH/2 + 291, HEIGHT/2 + 72)
        
        
        
        ball_list.append(ball)
        space.add(ball, body)


def create_cue_ball(space, radius, mass, pos):
    cue_ball_body = pymunk.Body()#body_type=pymunk.Body.STATIC)
    cue_ball_body.position = pos
    cue_ball_shape = pymunk.Circle(cue_ball_body, radius)
    cue_ball_shape.mass = mass
    cue_ball_shape.elasticity = 0.4
    cue_ball_shape.friction = 0.5
    cue_ball_shape.color = (pygame.Color(WHITE))
    space.add(cue_ball_body, cue_ball_shape)

    #cue_ball_img = pyglet.image.load("8 Ball Pool/cueBallT.png")
    #cue_ball_sprite = pyglet.sprite.Sprite(cue_ball_img, x = cue_ball_body.position.x, y = cue_ball_body.position.y)
    #space.add(cue_ball_body, cue_ball_shape, cue_ball_sprite)

    return cue_ball_shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    DELTA_TIME = 1 / FPS

    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = 0.6

    cue_ball = create_cue_ball(space, BALL_RADIUS, 10, (WIDTH/2 - 229 , HEIGHT/2 - 15))
    create_table(space, width, height)
    create_object_balls(space)

    #cue_ball.body.position()
    #cue_ball.body.get_pos()
    #line_pos = cue_ball.cue_ball_body.position
    

    draw_options = pymunk.pygame_util.DrawOptions(WINDOW)

    #pressed_pos = None
    #ball = None

    while run:
        #line = None
        #if ball and pressed_pos:
        #    line = [pressed_pos, pygame.mouse.get_pos()]
        
        line = [(cue_ball.body.position), pygame.mouse.get_pos()]
        #EVENT CHECKING LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                #cue_ball.body_type = pymunk.Body.DYNAMIC
                #cue_ball.body.apply_impulse_at_local_point((10000, 0), (0, 0))
                angle = calc_angle(*line)
                force = calc_distance_formula(*line) * 5
                force_x = math.cos(angle) * force
                force_y = math.sin(angle) * force
                cue_ball.body.apply_impulse_at_local_point((force_x, force_y), (0, 0))
                cue_ball.body.angle = angle
                #velo = cue_ball._get_surface_velocity
                #while velo > 0:
                #    cue_ball.body.angle = 0

                winner_text = "ball: " + str((cue_ball.body.angle * 180)/math.pi) + "line: " + str((angle* 180)/math.pi)
                draw_winner(winner_text)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cue_ball.body.angle = 0.7853982
                    
                

                #while cue_ball._get_surface_velocity > 0:
                #    cue_ball._shape.color = pygame.color(BLACK)

                

        draw(WINDOW, space, draw_options, line)
        space.step(DELTA_TIME)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run(WINDOW, WIDTH, HEIGHT)