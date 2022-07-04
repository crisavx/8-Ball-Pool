from eight_ball import *
from free_play import *
from main import *
from constants import *
import eight_ball as eight
import free_play as fp
import table as table
import pygame, pymunk, pymunk.pygame_util, math
from threading import Timer
import os

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Ball Pool by Cristian Lopez")


FONT = pygame.font.SysFont('arial-bold', 50)
FONT2 = pygame.font.SysFont('arial-bold', 26)
FONT3 = pygame.font.SysFont('arial-bold', 60)

#AUDIO
POOL_SHOT = pygame.mixer.Sound(os.path.join('pool_shot.mp3'))
POOL_POCKET = pygame.mixer.Sound(os.path.join('pool_pocket.mp3'))
POOL_BALL_CONTACT = pygame.mixer.Sound(os.path.join('pool_ball_contact.mp3'))
#PICS
BACKGROUND = pygame.image.load(os.path.join('pool_table.png'))
cue_ball_img = pygame.image.load('cue_ball.png')
one_ball_img = pygame.image.load('one_ball.png')
two_ball_img = pygame.image.load('two_ball.png')
three_ball_img = pygame.image.load('three_ball.png')
four_ball_img = pygame.image.load('four_ball.png')
five_ball_img = pygame.image.load('five_ball.png')
six_ball_img = pygame.image.load('six_ball.png')
seven_ball_img = pygame.image.load('seven_ball.png')
eight_ball_img = pygame.image.load('eight_ball.png')
nine_ball_img = pygame.image.load('nine_ball.png')
ten_ball_img = pygame.image.load('ten_ball.png')
eleven_ball_img = pygame.image.load('eleven_ball.png')
twelve_ball_img = pygame.image.load('twelve_ball.png')
thirteen_ball_img = pygame.image.load('thirteen_ball.png')
fourteen_ball_img = pygame.image.load('fourteen_ball.png')
fifteen_ball_img = pygame.image.load('fifteen_ball.png')



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

    global game_mode
    game_mode = "eight ball"
    #game_mode = "free play"

    print("Player 1 - Shoot!")
    
    
    cue_ball = table.create_cue_ball(space)
    table.create_cushions(space)
    table.create_object_balls(space)

    if game_mode == "eight ball":
        eight.handle_pocket_rules(space)
        #eight.display_object_balls(space)
    elif game_mode == "free play":
        fp.handle_pocket_rules(space)

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

    if game_mode == "eight ball":
        draw_text = FONT.render(eight.message, 1, WHITE)
        stripe_text = FONT2.render(eight.stripe_txt, 1, WHITE)
        solid_text = FONT2.render(eight.solid_txt, 1, WHITE)
        feed_text = FONT3.render(eight.feed, 1, WHITE)
        display.blit(draw_text, (WIDTH/2 - 135, 13))
        display.blit(stripe_text,(WIDTH - 162, 22))
        display.blit(solid_text, (15, 22))
        display.blit(feed_text, (WIDTH / 2 - 275, HEIGHT - 65))
    
    display.blit(cue_ball_img, (table.cue_ball_body.position.x - 12, table.cue_ball_body.position.y - 12))
    display.blit(one_ball_img, (table.one_ball_body.position.x - 12, table.one_ball_body.position.y - 12))
    display.blit(two_ball_img, (table.two_ball_body.position.x - 12, table.two_ball_body.position.y - 12))
    display.blit(three_ball_img, (table.three_ball_body.position.x - 12, table.three_ball_body.position.y - 12))
    display.blit(four_ball_img, (table.four_ball_body.position.x - 12, table.four_ball_body.position.y - 12))
    display.blit(five_ball_img, (table.five_ball_body.position.x - 12, table.five_ball_body.position.y - 12))
    display.blit(six_ball_img, (table.six_ball_body.position.x - 12, table.six_ball_body.position.y - 12))
    display.blit(seven_ball_img, (table.seven_ball_body.position.x - 12, table.seven_ball_body.position.y - 12))
    display.blit(eight_ball_img, (table.eight_ball_body.position.x - 12, table.eight_ball_body.position.y - 12))
    display.blit(nine_ball_img, (table.nine_ball_body.position.x - 12, table.nine_ball_body.position.y - 12))
    display.blit(ten_ball_img, (table.ten_ball_body.position.x - 12, table.ten_ball_body.position.y - 12))
    display.blit(eleven_ball_img, (table.eleven_ball_body.position.x - 12, table.eleven_ball_body.position.y - 12))
    display.blit(twelve_ball_img, (table.twelve_ball_body.position.x - 12, table.twelve_ball_body.position.y - 12))
    display.blit(thirteen_ball_img, (table.thirteen_ball_body.position.x - 12, table.thirteen_ball_body.position.y - 12))
    display.blit(fourteen_ball_img, (table.fourteen_ball_body.position.x - 12, table.fourteen_ball_body.position.y - 12))
    display.blit(fifteen_ball_img, (table.fifteen_ball_body.position.x - 12, table.fifteen_ball_body.position.y - 12))
    
    
    #space.debug_draw(draw_options)
    pygame.display.update()

def draw_line(space, display, draw_options):
    display.blit(BACKGROUND, ((0,0)))

    pygame.draw.line(display, BLACK, shooting_line[0], shooting_line[1], 3), #SHOOTING LINE

    if game_mode == "eight ball":
        draw_text = FONT.render(eight.message, 1, WHITE)
        stripe_text = FONT2.render(eight.stripe_txt, 1, WHITE)
        solid_text = FONT2.render(eight.solid_txt, 1, WHITE)
        feed_text = FONT3.render(eight.feed, 1, WHITE)
        display.blit(draw_text, (WIDTH/2 - 135, 13))
        display.blit(stripe_text,(WIDTH - 162, 22))
        display.blit(solid_text, (15, 22))
        display.blit(feed_text, (WIDTH / 2 - 275, HEIGHT - 65))


    display.blit(cue_ball_img, (table.cue_ball_body.position.x - 12, table.cue_ball_body.position.y - 12))
    display.blit(one_ball_img, (table.one_ball_body.position.x - 12, table.one_ball_body.position.y - 12))
    display.blit(two_ball_img, (table.two_ball_body.position.x - 12, table.two_ball_body.position.y - 12))
    display.blit(three_ball_img, (table.three_ball_body.position.x - 12, table.three_ball_body.position.y - 12))
    display.blit(four_ball_img, (table.four_ball_body.position.x - 12, table.four_ball_body.position.y - 12))
    display.blit(five_ball_img, (table.five_ball_body.position.x - 12, table.five_ball_body.position.y - 12))
    display.blit(six_ball_img, (table.six_ball_body.position.x - 12, table.six_ball_body.position.y - 12))
    display.blit(seven_ball_img, (table.seven_ball_body.position.x - 12, table.seven_ball_body.position.y - 12))
    display.blit(eight_ball_img, (table.eight_ball_body.position.x - 12, table.eight_ball_body.position.y - 12))
    display.blit(nine_ball_img, (table.nine_ball_body.position.x - 12, table.nine_ball_body.position.y - 12))
    display.blit(ten_ball_img, (table.ten_ball_body.position.x - 12, table.ten_ball_body.position.y - 12))
    display.blit(eleven_ball_img, (table.eleven_ball_body.position.x - 12, table.eleven_ball_body.position.y - 12))
    display.blit(twelve_ball_img, (table.twelve_ball_body.position.x - 12, table.twelve_ball_body.position.y - 12))
    display.blit(thirteen_ball_img, (table.thirteen_ball_body.position.x - 12, table.thirteen_ball_body.position.y - 12))
    display.blit(fourteen_ball_img, (table.fourteen_ball_body.position.x - 12, table.fourteen_ball_body.position.y - 12))
    display.blit(fifteen_ball_img, (table.fifteen_ball_body.position.x - 12, table.fifteen_ball_body.position.y - 12))
    
    #space.debug_draw(draw_options)
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