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
    WINDOW.blit(draw_text, (100, 50))
    pygame.display.update()
    #pygame.time.delay(5000)

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


    while run:  
        line = [(cue_ball.body.position), pygame.mouse.get_pos()]
        angle = calc_angle(*line)
        angle_deg = (angle * 180) / math.pi
        if angle_deg < 0:
          angle_deg = angle_deg + 360
        
        #angle_deg = 45

        cue_ball.body.angle = angle
        force = calc_distance_formula(*line) * 20
        force_x = math.cos(angle_deg) * force
        force_y = math.sin(angle_deg) * force

        #EVENT CHECKING LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                #cue_ball.body_type = pymunk.Body.DYNAMIC
                #cue_ball.body.apply_impulse_at_local_point((10000, 0), (0, 0))
                #angle = calc_angle(*line)
                #force = calc_distance_formula(*line) * 5
                #force_x = math.cos(angle) * force
                #force_y = math.sin(angle) * force
                cue_ball.body.apply_impulse_at_local_point((force, 0))
                #cue_ball.body.angle = angle
                #velo = cue_ball._get_surface_velocity
                #while velo > 0:
                #    cue_ball.body.angle = 0
                velo = 0
                #winner_text = "ball: " + str((cue_ball.body.angle * 180)/math.pi) + "line: " + str((angle* 180)/math.pi)
                #draw_winner(winner_text)

            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                  #cue_ball.body.angle = 0.7853982
                  cue_ball.body.apply_impulse_at_local_point(
                      (1000, 0))
                  
                

                #while cue_ball._get_surface_velocity > 0:
                #    cue_ball._shape.color = pygame.color(BLACK)

                

        draw(WINDOW, space, draw_options, line)
        winner_text = "Angle: " + str(round(angle_deg,2)) + ", FX: " + str(round(force_x,2)) + ", FY: " + str(round(force_y,2)) + ", Ball angle: " + str(round((cue_ball.body.angle * 180)/math.pi,2)) + ", Line angle: " + str(round((angle* 180)/math.pi,2))
        draw_winner(winner_text)
        space.step(DELTA_TIME)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run(WINDOW, WIDTH, HEIGHT)