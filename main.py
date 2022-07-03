from eight_ball import *
import eight_ball as eight
import table as t

from properties import *
import pygame, pymunk, pymunk.pygame_util, math#, pyglet
from threading import Timer
import os

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Ball Pool by Cristian Lopez")

#ASSETS

FONT = pygame.font.SysFont('arial-bold', 50)
FONT2 = pygame.font.SysFont('arial-bold', 26)
FONT3 = pygame.font.SysFont('arial-bold', 60)

#AUDIO
POOL_SHOT = pygame.mixer.Sound(os.path.join('pool_shot.mp3'))
POOL_POCKET = pygame.mixer.Sound(os.path.join('pool_pocket.mp3'))
POOL_BALL_CONTACT = pygame.mixer.Sound(os.path.join('pool_ball_contact.mp3'))
#PICS
BACKGROUND = pygame.image.load(os.path.join('pool_table.png'))
CUSHIONS = pygame.image.load(os.path.join('cushions.png'))


def run(display):
    run = True
    clock = pygame.time.Clock()

    global space

    space = pymunk.Space()
    space.gravity = GRAVITY
    space.damping = DAMPING

    global shooting_line
    global line_on
    line_on = True

    print("Player 1 - Shoot!")
    
    eight.create_object_balls(space)
    cue_ball = eight.create_cue_ball(space)
    t.create_cushions(space)
    eight.handle_pocket_collisions(space)
    eight.display_object_balls(space)

    draw_options = pymunk.pygame_util.DrawOptions(display)

    while run:
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

                    timer_check_pocketed = Timer(5.5, eight.check_ball_pocketed)
                    timer_check_pocketed.start()

                    timer_reset_pocketed = Timer(5.6, eight.update_ball_pocketed)
                    timer_reset_pocketed.start()

                    timer = Timer(6, eight.check_turn)
                    timer.start()

                    timer_reset_line = Timer(6, reset_line)
                    timer_reset_line.start()

                    timer_reset_feed = Timer(6, eight.reset_feed)
                    timer_reset_feed.start()

        if line_on == True:
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN) #ENABLE MOUSE INPUT
            cue_ball.body.angle = angle
            draw_line(space, display, draw_options)

        elif line_on == False:
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN) #DISABLE MOUSE INPUT
            draw_no_line(space, display, draw_options)

        space.step(DELTA_TIME)
        clock.tick(FPS)

    pygame.quit()

def reset_line():
    global line_on
    line_on = True

def draw_no_line(space, display, draw_options):
    display.blit(BACKGROUND, ((0,0)))

    draw_text = FONT.render(eight.message, 1, WHITE)
    stripe_text = FONT2.render(eight.stripe_txt, 1, WHITE)
    solid_text = FONT2.render(eight.solid_txt, 1, WHITE)
    feed_text = FONT3.render(eight.feed, 1, WHITE)
    display.blit(draw_text, (WIDTH/2 - 135, 13))
    display.blit(stripe_text,(WIDTH - 162, 22))
    display.blit(solid_text, (15, 22))
    display.blit(feed_text, (WIDTH / 2 - 275, HEIGHT - 65))
    

    space.debug_draw(draw_options)
    pygame.display.update()

def draw_line(space, display, draw_options):
    display.blit(BACKGROUND, ((0,0)))

    pygame.draw.line(display, BLACK, shooting_line[0], shooting_line[1], 3), #SHOOTING LINE

    draw_text = FONT.render(eight.message, 1, WHITE)
    stripe_text = FONT2.render(eight.stripe_txt, 1, WHITE)
    solid_text = FONT2.render(eight.solid_txt, 1, WHITE)
    feed_text = FONT3.render(eight.feed, 1, WHITE)
    display.blit(draw_text, (WIDTH/2 - 135, 13))
    display.blit(stripe_text,(WIDTH - 162, 22))
    display.blit(solid_text, (15, 22))
    display.blit(feed_text, (WIDTH / 2 - 275, HEIGHT - 65))

    space.debug_draw(draw_options)
    pygame.display.update()

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