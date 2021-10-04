#author : Dvir Alafi
"""
This is the graphics Module for the Country City Quiz Game.
This Python file runs the Graphics Module of the Country city Game .
the file itself can't be run and it only have a set of Essential Functions and Constants.
"""

#Cyber Project - The Graphics of The Game.
from Client_CountryCity import *
import pygame
import pygame.font
import pygame.event
import pygame.draw
import pygame.image
import pygame.mixer
import os

pygame.init()
pygame.font.init()

OFFWHITE = (250, 250, 210)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
HANDWRITE_FONT = pygame.font.SysFont("comicsansms", 30)
DEFAULT_FONT = pygame.font.Font(None, 24)
TIMER_FONT = pygame.font.SysFont("consolas", 42)
ANSWERS_FONT = pygame.font.SysFont("calibri", 30)
TIMER_WIDTH_AND_HEIGHT = (200, 40)
SCREEN_XY = (1152, 600)
SCREEN_STARTING_XY = (0, 0)
CURRENT_DIRECTORY = os.getcwd()
numbers_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
BACKGROUND_SONG_PATH = CURRENT_DIRECTORY + '\media\\Country_City_song_mp3.mp3'

BACKGROUND_IMAGE_PATH = CURRENT_DIRECTORY + '\media\\background_countrycity_3.png'

PINK = (255, 20, 147)
ORANGE = (255, 69, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEAL = (0, 128, 128)
STARTING_RESULTS_LINE_XY = (85, SCREEN_XY[1]/3)
RECT_DEFAULT_HEIGHT = 40
RECT_DEFAULT_WIDTH = 400
NAME_ENTER_DEFAULT_RECT_XY = (40, SCREEN_XY[1]/3, RECT_DEFAULT_WIDTH*2.5, RECT_DEFAULT_HEIGHT*3)
LETTER_XY = (SCREEN_XY[0]/3+150, SCREEN_XY[1]/10+40)

NUM_OF_PLAYERS_RECT_XY = (SCREEN_XY[0]*4/5+10, SCREEN_XY[1]*4/5, RECT_DEFAULT_WIDTH/2, (RECT_DEFAULT_HEIGHT+50)/2)
TIMER_XY = (150, 25)
TIME_XY = (25, 25)

GAME_OVER_PRINTING_FONT_SIZE = 80

boy_name_rect_xy = (SCREEN_XY[0]/3, SCREEN_XY[1]/2.5)
girl_name_rect_xy = (SCREEN_XY[0]/3, SCREEN_XY[1]/2.5+80)
country_rect_xy = (SCREEN_XY[0]/3, SCREEN_XY[1]/2.5+240)
animal_rect_xy = (SCREEN_XY[0]/3, SCREEN_XY[1]/2.5+160)

GAME_OVER_PRINTING_XY = (SCREEN_XY[0]/3, SCREEN_XY[1]/5+70)

#RECTS_XY = [boy_name_rect_xy, girl_name_rect_xy, animal_rect_xy, country_rect_xy]
TEXT_X = SCREEN_XY[0]/6 - 20
boy_name_text_xy = (TEXT_X, boy_name_rect_xy[1])
girl_name_text_xy = (TEXT_X, girl_name_rect_xy[1])
animal_text_xy = (TEXT_X, animal_rect_xy[1])
country_text_xy = (TEXT_X, country_rect_xy[1])

BOY_IMG_PATH = CURRENT_DIRECTORY + '\media\\boy_img2.png'
GIRL_IMG_PATH = CURRENT_DIRECTORY + '\media\girl_img.png'
COUNTRY_IMG_PATH = CURRENT_DIRECTORY + '\media\country_img3.png'
ANIMAL_IMG_PATH = CURRENT_DIRECTORY + '\media\\animal_img3.png'

FIRST_PAGE_IMG_PATH = CURRENT_DIRECTORY + '\media\\first_page2.png'
HOME_PAGE_IMG_PATH = CURRENT_DIRECTORY + '\media\home_page2.png'
HELP_PAGE_IMG_PATH = CURRENT_DIRECTORY + '\media\\help_page.png'
COUNTRY_CITY_ANIMATE_IMG_PATH = CURRENT_DIRECTORY + '\media\\country_city_img.jpg'
RESULT_PAGE_IMG_PATH = CURRENT_DIRECTORY + '\media\\results_page_img.png'
NAME_ENTER_IMG_PATH = CURRENT_DIRECTORY + '\media\\enter_name_page.png'
PLAYER_CHOICE_IMG_PATH = CURRENT_DIRECTORY + '\media\\players_choice_img.png'

X_IMG_PATH = CURRENT_DIRECTORY + '\media\\x_img.png'
V_IMG_PATH = CURRENT_DIRECTORY + '\media\\v_img.png'

CANT_CONNECT_IMG_PATH = CURRENT_DIRECTORY + '\media\\cant_connect_img.png'

WAITING_FOR_PLAYERS_IMG_PATH = CURRENT_DIRECTORY + '\media\\waiting_for_players_page.png'


COUNTRY_TEXT = 'country'
ANIMAL_TEXT = 'animal'
GIRL_TEXT = 'girl'
BOY_TEXT = 'boy'

GIRL_NAME_TEXT = 'Girl Name:'
BOY_NAME_TEXT = 'Boy Name:'
ANIMAL_NAME_TEXT = 'Animal Name:'
COUNTRY_NAME_TEXT = 'Country Name:'

TIME_TEXT = 'Time: '
OUT_OF_50_TEXT = '/40(+10 Bonus) '

NUM_OF_PLAYERS_TEXT = 'Num Of Players:'

BOY_IMG_XY = (boy_name_rect_xy[0]+RECT_DEFAULT_WIDTH+10, boy_name_rect_xy[1]-20)
GIRL_IMG_XY = (girl_name_rect_xy[0]+RECT_DEFAULT_WIDTH+10, girl_name_rect_xy[1]-20)
ANIMAL_IMG_XY = (animal_rect_xy[0]+RECT_DEFAULT_WIDTH+10, animal_rect_xy[1]-20)
COUNTRY_IMG_XY = (country_rect_xy[0]+RECT_DEFAULT_WIDTH+10, country_rect_xy[1]-20)


def update_text_box(screen, current_object):
    pygame.draw.rect(screen, WHITE, (current_object.get_rect_xy()[0]+1,
                                     current_object.get_rect_xy()[1]+1, RECT_DEFAULT_WIDTH-2, RECT_DEFAULT_HEIGHT-2), 0)

    if len(current_object.get_answer()) > 26:
        current_object.set_answer('')
    screen.blit(ANSWERS_FONT.render(current_object.get_answer(), 1, BLUE), (current_object.get_rect_xy()[0]+5,
                                                                            current_object.get_rect_xy()[1]+3))
    pygame.display.flip()


def draw_text_and_rect_background(screen, text, (rect_x_pos, rect_y_pos), (text_x_pos, text_y_pos)):

    pygame.draw.rect(screen, TEAL, (rect_x_pos, rect_y_pos, RECT_DEFAULT_WIDTH, RECT_DEFAULT_HEIGHT), 1)
    if len(text) != 0:
        screen.blit(HANDWRITE_FONT.render(text, 1, BLACK), (text_x_pos, text_y_pos))
    pygame.display.flip()


def draw_background(screen, random_letter, list_of_objects):
    screen.fill(CYAN)
    if BACKGROUND_IMAGE_PATH:
        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        screen.blit(background_image, SCREEN_STARTING_XY)

    if BOY_IMG_PATH:
        boy_image = pygame.image.load(BOY_IMG_PATH)
        screen.blit(boy_image, BOY_IMG_XY)

    if GIRL_IMG_XY:
        girl_image = pygame.image.load(GIRL_IMG_PATH)
        screen.blit(girl_image, GIRL_IMG_XY)

    if COUNTRY_IMG_PATH:
        country_image = pygame.image.load(COUNTRY_IMG_PATH)
        screen.blit(country_image, COUNTRY_IMG_XY)

    if ANIMAL_IMG_PATH:
        animal_image = pygame.image.load(ANIMAL_IMG_PATH)
        screen.blit(animal_image, ANIMAL_IMG_XY)

    draw_text_and_rect_background(screen, GIRL_NAME_TEXT, girl_name_rect_xy, girl_name_text_xy)
    draw_text_and_rect_background(screen, COUNTRY_NAME_TEXT, country_rect_xy, country_text_xy)
    draw_text_and_rect_background(screen, BOY_NAME_TEXT, boy_name_rect_xy, boy_name_text_xy)
    draw_text_and_rect_background(screen, ANIMAL_NAME_TEXT, animal_rect_xy, animal_text_xy)

    screen.blit(TIMER_FONT.render(TIME_TEXT, 1, BLUE), TIME_XY)
    font_object = pygame.font.Font(None, 150)
    screen.blit(font_object.render(random_letter, 1, PINK), LETTER_XY)

    for category_object in list_of_objects:
        update_text_box(screen, category_object)

    pygame.display.flip()


def draw_cant_connect_to_server(screen):
    cant_connect_img = pygame.image.load(CANT_CONNECT_IMG_PATH)
    screen.blit(cant_connect_img, SCREEN_STARTING_XY)
    pygame.display.flip()


def draw_help_page(screen):
    help_page_image = pygame.image.load(HELP_PAGE_IMG_PATH)
    screen.blit(help_page_image, SCREEN_STARTING_XY)
    pygame.display.flip()


def draw_first_page(screen):
    first_page_image = pygame.image.load(FIRST_PAGE_IMG_PATH)
    screen.blit(first_page_image, SCREEN_STARTING_XY)
    pygame.display.flip()


def draw_home_page(screen):
    home_page_image = pygame.image.load(HOME_PAGE_IMG_PATH)
    screen.blit(home_page_image, SCREEN_STARTING_XY)
    pygame.display.flip()


def draw_results_page(results_list, screen):

    result_page_img = pygame.image.load(RESULT_PAGE_IMG_PATH)
    screen.blit(result_page_img, SCREEN_STARTING_XY)
    new_line_y = 0
    font_object = pygame.font.Font(None, 130)

    for result_line in results_list:
        screen.blit(font_object.render(result_line + OUT_OF_50_TEXT, 1, WHITE),
                    (STARTING_RESULTS_LINE_XY[0], STARTING_RESULTS_LINE_XY[1]+new_line_y))
        new_line_y += 80
    pygame.display.flip()


def draw_and_get_name_enter_page(screen):
    """
    This function getting the name of the player from the player\user , in the game .
    it returns the name of the player that the player input.
    """
    name_enter_page_img = pygame.image.load(NAME_ENTER_IMG_PATH)
    screen.blit(name_enter_page_img, SCREEN_STARTING_XY)
    pygame.draw.rect(screen, PINK, (NAME_ENTER_DEFAULT_RECT_XY[0]-5, NAME_ENTER_DEFAULT_RECT_XY[1]-5,
                                    NAME_ENTER_DEFAULT_RECT_XY[2], NAME_ENTER_DEFAULT_RECT_XY[3]), 1)

    pygame.draw.rect(screen, WHITE, NAME_ENTER_DEFAULT_RECT_XY, 1)
    pygame.display.flip()

    player_name = ''
    while True:
        if len(player_name) > 20:
            player_name = ''
        pressed_key = get_key()
        if pressed_key is None:
            pass
        elif pressed_key == pygame.K_RETURN:
            break

        elif pressed_key == pygame.K_SPACE:
            player_name += ' '
        elif pressed_key <= 127 and chr(pressed_key).isalpha():
            player_name += chr(pressed_key)

        elif pressed_key == pygame.K_BACKSPACE:
            player_name = player_name[:-1]

        update_name_on_screen(screen,player_name, name_enter_page_img)

    return player_name


def draw_and_get_num_of_players_from_user(screen):
    """
    This function runs the multiplier or one player \ offline mode , in the game .
    it returns the num of the players that the player input. if it 0 or 1 its in offline mode and the player will play
    alone , and if its more than 1 its multiplier.
    this func returns the number of the players the user wrote.
    """
    multiplier_page_imp = pygame.image.load(PLAYER_CHOICE_IMG_PATH)
    screen.blit(multiplier_page_imp, SCREEN_STARTING_XY)
    pygame.display.flip()
    num_of_players = ''
    while True:
        pressed_key = get_key()
        if pressed_key is None:
            pass
        elif pressed_key == pygame.K_LEFT:
            return '1'
        elif pressed_key == pygame.K_RIGHT:
            font_object = pygame.font.Font(None, 40)
            screen.blit(font_object.render(NUM_OF_PLAYERS_TEXT, 1, BLACK),
                        (NUM_OF_PLAYERS_RECT_XY[0]-225, NUM_OF_PLAYERS_RECT_XY[1]))

            pygame.draw.rect(screen, WHITE, NUM_OF_PLAYERS_RECT_XY, 0)

            while pressed_key != pygame.K_RETURN:

                pressed_key = get_key()
                if pressed_key in range(47, 58):
                    num_of_players += chr(pressed_key)

                elif pressed_key == pygame.K_BACKSPACE:
                    num_of_players = num_of_players[:-1]

                pygame.draw.rect(screen, WHITE, NUM_OF_PLAYERS_RECT_XY, 0)
                screen.blit(font_object.render(str(num_of_players), 1, PINK),
                                (NUM_OF_PLAYERS_RECT_XY[0]+10, NUM_OF_PLAYERS_RECT_XY[1]+10))

                pygame.display.flip()
            return num_of_players


def draw_v_and_x(screen, dict_of_corrects):
    """
    This function draw V and X images corresponding to the correct ot NOT correct answers that the player/user wrote.
    """
    x_img = pygame.image.load(X_IMG_PATH)
    v_img = pygame.image.load(V_IMG_PATH)

    if dict_of_corrects[BOY_TEXT]:
        screen.blit(v_img, (BOY_IMG_XY[0]+80, BOY_IMG_XY[1]))

    else:
        screen.blit(x_img, (BOY_IMG_XY[0]+80, BOY_IMG_XY[1]))

    if dict_of_corrects[GIRL_TEXT]:
        screen.blit(v_img, (GIRL_IMG_XY[0]+80, GIRL_IMG_XY[1]))

    else:
        screen.blit(x_img, (GIRL_IMG_XY[0]+80, GIRL_IMG_XY[1]))

    if dict_of_corrects[COUNTRY_TEXT]:
        screen.blit(v_img, (COUNTRY_IMG_XY[0]+80, COUNTRY_IMG_XY[1]))

    else:
        screen.blit(x_img, (COUNTRY_IMG_XY[0]+80, COUNTRY_IMG_XY[1]))

    if dict_of_corrects[ANIMAL_TEXT]:
        screen.blit(v_img, (ANIMAL_IMG_XY[0]+80, ANIMAL_IMG_XY[1]))

    else:
        screen.blit(x_img, (ANIMAL_IMG_XY[0]+80, ANIMAL_IMG_XY[1]))

    pygame.display.flip()


def update_name_on_screen(screen, player_name, name_enter_page_img):
    """
    This function gets a screen(display object) the updated player name and the name enter image.
    it paints the rectangle of the player name and then paints the name again to update it on the screen.
    """
    screen.blit(name_enter_page_img, SCREEN_STARTING_XY)
    pygame.draw.rect(screen, WHITE, NAME_ENTER_DEFAULT_RECT_XY, 1)
    pygame.draw.rect(screen, PINK, (NAME_ENTER_DEFAULT_RECT_XY[0]-5, NAME_ENTER_DEFAULT_RECT_XY[1]-5,
                                    NAME_ENTER_DEFAULT_RECT_XY[2], NAME_ENTER_DEFAULT_RECT_XY[3]), 1)

    font_object = pygame.font.Font(None, 130)
    screen.blit(font_object.render(player_name, 1, PINK),
                    (NAME_ENTER_DEFAULT_RECT_XY[0]+10, NAME_ENTER_DEFAULT_RECT_XY[1]+10))

    pygame.display.flip()


def init_screen():
    """
    This Function Initialize a Display Object From the module Pygame
    Returns : the Display Object
    """
    return pygame.display.set_mode(SCREEN_XY)


def main():
    """
    The Main Func of the Graphics Module /
    Do Nothing    /
    """
    pass

if __name__ == '__main__':
    main()