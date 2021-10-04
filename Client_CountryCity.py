#Author : Dvir Alafi

"""
Client Program For Country City Quiz Game.
This Python file is the client module of the game that runs the client side .
it controls the

"""

#Cyber Project - The Client of The Game.

from Graphics_CountryCity import *
import string
import random
import os
import sys
import select
import socket
from time import time
from time import sleep
import pygame
#-----------------------YOU NEED TO PUT THE PYTHON FILES IN THE SAME DIRECTORY AS THE 'media' folder.------------------
CURRENT_DIRECTORY = os.getcwd()

#CONSTANTS:

SERVER_PORT = 52000
HOST = '127.0.0.1'
GAME_OVER_MESSAGE = 'GAME OVER'
MAX_RECEIVING_BYTES_FROM_SERVER = 4096

CANT_CONNECT_SECONDS_WAITING = 5
TIMER_SECONDS = 60
ENTER_PRESSING_BONUS_POINTS = 10

GAME_OVER_PRINTING = 'Game Over!'
YOU_TEXT = 'You'
START_DECISION = 'start'
QUIT_DECISION = 'quit'
HELP_DECISION = 'help'


TWO_POINTS_FLOAT_SIGN = "%.2f"

BOY_CATEGORY_FILE_PATH = CURRENT_DIRECTORY + '\\media\\boys.txt'
GIRL_CATEGORY_FILE_PATH = CURRENT_DIRECTORY + '\\media\\girls.txt'
ANIMAL_CATEGORY_FILE_PATH = CURRENT_DIRECTORY + '\\media\\animals.txt'
COUNTRY_CATEGORY_FILE_PATH = CURRENT_DIRECTORY + '\\media\\countries.txt'


class Category():
    """
    This Class Represents the Category Objects : Girl , Animal , Boy , Girl of the Game.
    Every instance of the Class has :
    1.rect_xy = the x and y coordinates of the rect when the user writes the answer to the object
    2.text_xy = the actual text - x and y coordinates that printing on the screen for the user to see
    3.answer = the current updated answer that the user wrote.

    every instance's attribute have a get function,  and the answer attribute have a set function.
    """
    def __init__(self, rect_xy, text_xy, answer=''):
        self.rect_xy = rect_xy
        self.text_xy = text_xy
        self.answer = answer

    def get_rect_xy(self):
        return self.rect_xy

    def get_text_xy(self):
        return self.text_xy

    def get_answer(self):
        return self.answer

    def set_answer(self, new_answer):
        self.answer = new_answer

    def run(self):
        pass


def get_player_result(countries_set, animals_set, boys_set, girls_set,
                      boy_name_answer, girl_name_answer, animal_answer, country_answer, random_letter,
                      dict_of_corrects):

    """
    This function gets the category sets and the answers from the user and checks if the user's answers are in the
    Category sets .
    every correct answer adds to the final result 10 points .
    Returns : the final result
    """
    result = 0
    if country_answer in countries_set and country_answer.startswith(random_letter):
        dict_of_corrects[COUNTRY_TEXT] = True
        result += 10
    if animal_answer in animals_set and animal_answer.startswith(random_letter):
        dict_of_corrects[ANIMAL_TEXT] = True
        result += 10
    if boy_name_answer in boys_set and boy_name_answer.startswith(random_letter):
        dict_of_corrects[BOY_TEXT] = True
        result += 10
    if girl_name_answer in girls_set and girl_name_answer.startswith(random_letter):
        dict_of_corrects[GIRL_TEXT] = True
        result += 10
    return result


def get_category_files_content_in_sets(path_to_countries_file, path_to_animals_file, path_to_boys_names_file,
                                       path_to_girls_names_file):
    """
    initialize the information from the files to the Category sets.
    every file that been opened closed immediately , because of the " with ...  as ... " command.
    """
    countries_set = set()
    animals_set = set()
    boys_set = set()
    girls_set = set()
    with open(path_to_countries_file) as countries_file_handler:
        for line in countries_file_handler:
            countries_set.add(line.rstrip().lower())

    with open(path_to_animals_file) as animals_file_handler:
        for line in animals_file_handler:
            animals_set.add(line.rstrip().lower())

    with open(path_to_boys_names_file) as boys_file_handler:
        for line in boys_file_handler:
            boys_set.add(line.rstrip().lower())

    with open(path_to_girls_names_file) as girls_file_handler:
        for line in girls_file_handler:
            girls_set.add(line.rstrip().lower())

    return countries_set, animals_set, boys_set, girls_set


def convert_str_to_list(x_string):
    """
    the sign for splitting is '-'/
    Gets : a string , that was a list of results before
    Returns : the list , by splitting the text with '-' sign
    (that was the method that used to make the list a text)
    """
    return x_string.split('-')


def is_pressed_any_key():
    """
    Gets: Nothing
    Returns : True if a key was pressed and if not keeps trying to get a key from the user.
    """
    while True:
        pressed_key = pygame.event.poll()
        if pressed_key.type == pygame.KEYDOWN or pressed_key.type == pygame.MOUSEBUTTONUP:
            return True


def get_answers_from_objects(list_of_objects):
    """
    Gets:list of Category objects
    Returns: a list of answers from the objects corresponding to the list it gets
    """
    list_of_answers = []
    for category_object in list_of_objects:
        list_of_answers.append(category_object.get_answer().rstrip())
    return list_of_answers


def is_mouse_on_rect(rect_xy, rect_range):
    """
    Gets : rectangle x and y coordinates and a range of the rect (height and width)
    Returns : (gets the mouse position by its own) if the mouse (when the user clicked the mouse) was on the rectangle
    on the screen.
    """
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = int(mouse_pos[0])
    mouse_y = int(mouse_pos[1])
    rect_x = int(rect_xy[0])
    rect_y = int(rect_xy[1])
    for y in range(rect_y, rect_y+rect_range[1]):
        for x in range(rect_x, rect_x+rect_range[0]):
            if mouse_x == x and mouse_y == y:
                return True
    return False


def change_object(list_of_objects, current_object):
    """
    Gets : list of Category objects and a current writing object
    Returns : Nothing
    Changing : the current Category Object corresponding to the mouse click from the user .
    """
    for category_object in list_of_objects:
        if is_mouse_on_rect(category_object.get_rect_xy(), (RECT_DEFAULT_WIDTH, RECT_DEFAULT_HEIGHT)):
            return category_object
    return current_object


def get_key():
    """
    Gets : Nothing
    Returns : the key pressed from the user (from the keyboard)
    """
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
        return event.key
    elif event.type == pygame.MOUSEBUTTONUP:
        return event
    else:
        pass
    return None


def update_timer(over_time, screen):
    """
    this function updates the Timer on the screen .
    its painting a rect of White and painting the timer .
    Gets: screen = display object
    Returns : Nothing
    """
    time_color = BLUE
    if over_time - time() < 10:
        time_color = RED
    pygame.draw.rect(screen, WHITE, (TIMER_XY[0], TIMER_XY[1], TIMER_WIDTH_AND_HEIGHT[0], TIMER_WIDTH_AND_HEIGHT[1]), 0)

    screen.blit(TIMER_FONT.render(str(TWO_POINTS_FLOAT_SIGN % (over_time-time())), 1, time_color), TIMER_XY)
    pygame.display.flip()


def get_and_update_answer_from_player(screen, list_of_objects, current_object, pressed_key, game_over):
    """
    Gets :
    screen = Display Object
    list of Category object
    the current writing object
    the key that pressed by the user
    game_over = sign if one of the players pressed enter

    Returns : player_pressed_enter, current_object

    Changing : the previous answer from the user . for example if the answer wsa "dvi" and the user pressed "r" it adds
    to the answer "dvi" the letter "r" ' and it becomes "dvir" , same thing with backspace , space , and other.

    """
    if game_over:
        return False, current_object

    current_answer = current_object.get_answer()

    if pressed_key is None:
        pass

    elif pressed_key == pygame.K_BACKSPACE:
        current_answer = current_answer[:-1]
        current_object.set_answer(current_answer)

    elif pressed_key == pygame.K_RETURN:
        return True, current_object

        #because the client send to the server the results joined by '-'.
    elif pressed_key == pygame.K_MINUS:
        current_answer += '_'
        current_object.set_answer(current_answer)

    elif pressed_key == pygame.K_DOWN and list_of_objects.index(current_object)+1 < len(list_of_objects):
        current_object = list_of_objects[list_of_objects.index(current_object)+1]

    elif pressed_key == pygame.K_UP and list_of_objects.index(current_object) != 0:
        current_object = list_of_objects[list_of_objects.index(current_object)-1]

    elif pressed_key == pygame.K_SPACE:
        current_answer += ' '
        current_object.set_answer(current_answer)

        #check if its in the range of Ascii letters:

    elif pressed_key <= 127 and chr(pressed_key).isalpha():
        current_answer += chr(pressed_key)
        current_object.set_answer(current_answer)

    try:
        #if mouse pressed
        if pressed_key != int and pressed_key.type == pygame.MOUSEBUTTONUP:

            current_object = change_object(list_of_objects, current_object)
    except:
        pass

    update_text_box(screen, current_object)

    return False, current_object


def get_decision_from_user():
    """
    Gets: Nothing
    Returns : the decision from the user = "q" for quit or "s" for start or "h" for help
    this func runs in the menu.
    """
    pressed_key = get_key()
    if pressed_key is None:
        return ''
    if pressed_key <= 127 and chr(pressed_key).isalpha():
        if chr(pressed_key) == 's':
            return START_DECISION
        elif chr(pressed_key) == 'h':
            return HELP_DECISION
        elif chr(pressed_key) == 'q':
            return QUIT_DECISION


def exit_the_program():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def main():
    """
    This is The Main Function
    Runs and controls the Game until the user press 'q'
    """

    #initialzie the pygame modules
    pygame.init()
    pygame.font.init()

    path_to_countries_file, path_to_animals_file, path_to_boys_names_file, path_to_girls_names_file = \
        COUNTRY_CATEGORY_FILE_PATH, ANIMAL_CATEGORY_FILE_PATH, BOY_CATEGORY_FILE_PATH, GIRL_CATEGORY_FILE_PATH

    countries_set, animals_set, boys_set, girls_set = get_category_files_content_in_sets(
        path_to_countries_file, path_to_animals_file, path_to_boys_names_file, path_to_girls_names_file)

    screen = init_screen()

    draw_first_page(screen)
    if is_pressed_any_key():
        pass

    pygame.mixer.init()
    pygame.mixer.music.load(BACKGROUND_SONG_PATH)
    pygame.mixer.music.play(-1)
    song_current_pos = 0
    while True:
        if not pygame.mixer.music.get_busy():
            song_current_pos = pygame.mixer.music.get_pos()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.play(0, (song_current_pos))
        pygame.time.Clock().tick(TIMER_SECONDS)

        #Initialize the Category Objects :
        dict_of_corrects = {BOY_TEXT: False, GIRL_TEXT: False, ANIMAL_TEXT: False, COUNTRY_TEXT: False}
        boy = Category(boy_name_rect_xy, boy_name_text_xy)
        girl = Category(girl_name_rect_xy, girl_name_rect_xy)
        animal = Category(animal_rect_xy, animal_text_xy)
        country = Category(country_rect_xy, country_text_xy)

        list_of_objects = [boy, girl, animal, country]

        while True:
            draw_home_page(screen)
            decision_from_user = get_decision_from_user()
            if decision_from_user is START_DECISION:
                break
            if decision_from_user is QUIT_DECISION:
                exit_the_program()
            if decision_from_user is HELP_DECISION:
                draw_help_page(screen)
                if is_pressed_any_key():
                    continue
            pygame.display.flip()

        num_of_players = draw_and_get_num_of_players_from_user(screen)
        num_of_players = int(num_of_players)

        player_pressed_enter = False
        game_over_sign = []
        random_letter = random.choice(string.letters).lower()
        current_object = list_of_objects[0]

#------------------------------------------OFFLINE :-------------------------------------------------------------------
        if num_of_players == 0 or num_of_players == 1:
            draw_background(screen, random_letter, list_of_objects)
            over_time = int(time()) + TIMER_SECONDS
            while time() < over_time and not player_pressed_enter:

                pressed_key = get_key()
                player_pressed_enter, current_object = get_and_update_answer_from_player(
                    screen, list_of_objects, current_object, pressed_key, game_over_sign)
                update_timer(over_time, screen)

            list_of_answers = get_answers_from_objects(list_of_objects)
            boy_name_answer, girl_name_answer, country_answer, animal_answer = [answer for answer in list_of_answers]
            result = get_player_result(
                countries_set, animals_set, boys_set, girls_set, boy_name_answer,
                girl_name_answer, country_answer, animal_answer, random_letter, dict_of_corrects)
            if player_pressed_enter:
                if result > 0:
                    result += 10
            draw_v_and_x(screen, dict_of_corrects)
            if is_pressed_any_key():
                pass

            draw_results_page([YOU_TEXT + ':' + str(result)], screen)
            if is_pressed_any_key():
                continue
#-------------------------------------------------------------ONLINE :-------------------------------------------------

        player_name = draw_and_get_name_enter_page(screen)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, SERVER_PORT))
        except socket.error:
            draw_cant_connect_to_server(screen)
            seconds_waiting = time() + 5
            while time() < seconds_waiting:
                pass
            break

        client_socket.send(str(num_of_players))

        waiting_for_players_img = pygame.image.load(WAITING_FOR_PLAYERS_IMG_PATH)
        screen.blit(waiting_for_players_img, SCREEN_STARTING_XY)
        pygame.display.flip()

        try:
            random_letter = client_socket.recv(MAX_RECEIVING_BYTES_FROM_SERVER)
        except socket.error:
            draw_cant_connect_to_server(screen)
            sleep(CANT_CONNECT_SECONDS_WAITING)
            continue
        draw_background(screen, random_letter, list_of_objects)

        #list_of_objects[0] as default:
        current_object = list_of_objects[0]
        player_pressed_enter = False
        game_over_sign = []

        over_time = int(time()) + TIMER_SECONDS

        client_socket.setblocking(0)

        while time() < over_time and not player_pressed_enter and not game_over_sign:
            ready = select.select([client_socket], [], [], 0)
            if ready[0]:
                message_from_server = client_socket.recv(MAX_RECEIVING_BYTES_FROM_SERVER)
                if message_from_server == GAME_OVER_MESSAGE:
                    game_over_sign.append('d')
                    break
            pressed_key = get_key()
            player_pressed_enter, current_object = get_and_update_answer_from_player(
                screen, list_of_objects, current_object, pressed_key, game_over_sign)

            update_timer(over_time, screen)

        font_object = pygame.font.Font(None, GAME_OVER_PRINTING_FONT_SIZE)
        screen.blit(font_object.render(GAME_OVER_PRINTING, 1, BLUE), GAME_OVER_PRINTING_XY)

        list_of_answers = get_answers_from_objects(list_of_objects)
        boy_name_answer, girl_name_answer, country_answer, animal_answer = [answer for answer in list_of_answers]
        result = get_player_result(
            countries_set, animals_set, boys_set, girls_set, boy_name_answer, girl_name_answer,
            country_answer, animal_answer, random_letter, dict_of_corrects)

        draw_v_and_x(screen, dict_of_corrects)

        if player_pressed_enter:
            if result > 0:
                result += ENTER_PRESSING_BONUS_POINTS
            client_socket.send(player_name+':'+str(result)+'d')
        elif time() >= over_time or game_over_sign:
            client_socket.send(player_name+':'+str(result))

        draw_v_and_x(screen, dict_of_corrects)

        client_socket.setblocking(True)
        all_players_results_list = client_socket.recv(MAX_RECEIVING_BYTES_FROM_SERVER)
        # if this player is the one that sent a result with 'd' , he well be getting a GAME OVER message...
        # and the while is to ensure the message is the result and not a GAME OVER message.

        #because im getting STRING from the server
        while all_players_results_list == GAME_OVER_MESSAGE:
            all_players_results_list = client_socket.recv(MAX_RECEIVING_BYTES_FROM_SERVER)

        all_players_results_list = convert_str_to_list(all_players_results_list)

        if is_pressed_any_key():
            pass

        draw_results_page(all_players_results_list, screen)

        if is_pressed_any_key():
            pass
        client_socket.close()

if __name__ == '__main__':
    main()