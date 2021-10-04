#Author : Dvir Alafi

#Cyber Project - The Server of The Country City Game.

"""
This is The Server That Provides The Data and Represents the Connection Between the 2 or more Clients that are
in the game .

What is it do? :
Before The Game starts , the Server Connect with the Clients , and save their private accounts , for safe connection
throughout the Game.

Then The Server Chooses Randomly an English letter and send it to the Clients , then , the clients begin to play.

When the game ends , the server gets the results \ the score that the player achieved .(the server knows it by accepting
a message from one of the clients if he finishes first the game , or the server gets from the all clients messages .
in the 2 options the clients
and their score in the game).

The server , after seeking the results from all the clients , sends the result of one client to the other.
"""

import socket
import sys
import threading
import string
import random
import select
from time import time

#CONSTANTS:

TIMER_SECONDS = 60

players_details_dict = {}

ThreadLock = threading.Lock()

MAX_RECEIVING_BYTES_FROM_CLIENT = 1024

SERVER_PORT = 52000
HOST = '0.0.0.0'

BIND_ERR_MESSAGE = 'Bind to the Port '+str(SERVER_PORT)+' failed. The Error Message : '
GAME_OVER_MESSAGE = 'GAME OVER'


class GetPlayerDetailsThread(threading.Thread):
    def __init__(self, player_ip_and_port, player_socket, players_details_dict):
        threading.Thread.__init__(self, name=GetPlayerDetailsThread)

        self.player_socket = player_socket
        self.player_ip_and_port = player_ip_and_port
        self.players_details_dict = players_details_dict

    def run(self):

        #LOCKING this section of code
        ThreadLock.acquire()

        self.players_details_dict[self.player_ip_and_port] = self.player_socket
        num_of_players_never_mind = self.player_socket.recv(MAX_RECEIVING_BYTES_FROM_CLIENT)
        ThreadLock.release()
        #RELEASES this section of code


class ReceivingPlayerResultsThread(threading.Thread):
    def __init__(self, player_socket, players_results_list):
        threading.Thread.__init__(self, name=ReceivingPlayerResultsThread)
        self.player_socket = player_socket
        self.players_results_list = players_results_list

    def run(self):

        #LOCKING this section of code
        ThreadLock.acquire()
        self.player_socket.setblocking(True)
        player_results = self.player_socket.recv(MAX_RECEIVING_BYTES_FROM_CLIENT)

        if player_results.endswith('d'):
            #send to players that the game is over.
            send_to_players(GAME_OVER_MESSAGE)
            #put in the list the result without the 'd' at the end:
            self.players_results_list.append(player_results[:-1])


        else:
            #if the message its the result only without 'd' at the end , it means that the timer is over \ server sent
            #Game Over message.
            self.players_results_list.append(player_results)
        ThreadLock.release()
        #RELEASES this section of code


def send_to_players(message):
    for player_socket in players_details_dict.values():
        #send to the player the message:
        player_socket.send(message)


def get_random_letter():
    return random.choice(string.letters).lower()


def init_server():
    """
    creates a server socket  and binds it with a PORT and HOST.
    Gets : Nothing
    Returns : A socket Server binds to a PORT and HOST.
    """

    #Initialize a TCP Protocol Socket Server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind server socket to local host and port , and if it doesn't work , I print an error message and exit the program.
    try:
        server_socket.bind(('0.0.0.0', SERVER_PORT))
    except socket.error as bind_err_msg:
        print BIND_ERR_MESSAGE + bind_err_msg[1]
        sys.exit()
    server_socket.listen(1)
    return server_socket


def convert_list_to_str(lst):
    return '-'.join(item for item in lst)


def main():
    """
    This is The Main Function
    """
    #creats a socket server that listen to "MAX_NUM_OF_PLAYERS" clients
    server_socket = init_server()

    print 'Generate Random Letter..'
    random_letter = get_random_letter()
    print 'The Random Letter : '+random_letter

    player_socket, player_ip_and_port = server_socket.accept()

    print 'First Player Connected With :'+str(player_ip_and_port)

    num_of_players = player_socket.recv(MAX_RECEIVING_BYTES_FROM_CLIENT)
    num_of_players = int(num_of_players)

    players_details_dict[player_ip_and_port] = player_socket

    #because i already got from the first player..
    num_of_players -= 1

    num_of_threads = 0
    details_getting_threads_list = []
    #A thread for each player

    while num_of_threads < num_of_players:

        player_socket, player_ip_and_port = server_socket.accept()
        print 'Connected With :'+str(player_ip_and_port)
        #Initialize the thread.
        get_player_details_thread = GetPlayerDetailsThread(player_ip_and_port, player_socket, players_details_dict)
        #starts the thread
        get_player_details_thread.start()

        #add the thread to a list . the purpose : wait to all the threads in the list to complete before moving on.
        details_getting_threads_list.append(get_player_details_thread)
        num_of_threads += 1

    #Wait for all the Threads to complete
    for Player_Thread in details_getting_threads_list:
        Player_Thread.join()

    #sends to the players a random letter
    send_to_players(random_letter)
    print 'Random Letter : "'+random_letter+'" ,sent to players'
    #------------------------------------------------------------------------------------------------------------------

    players_results_list = []
    player_pressed_enter = False
    over_time = int(time()) + TIMER_SECONDS
    game_over_sent = False
    receiving_player_result_threads_list = []

    while not player_pressed_enter or len(players_details_dict) > len(players_results_list):
        #only invokes when all the players send their results simultaneously... in the over time!
        if time() == over_time:
            for player_socket in players_details_dict.values():
                if not game_over_sent:
                    send_to_players(GAME_OVER_MESSAGE)
                    game_over_sent = True
                receiving_player_result_thread = ReceivingPlayerResultsThread(player_socket, players_results_list)
                receiving_player_result_thread.start()
                receiving_player_result_threads_list.append(receiving_player_result_thread)
            break

        for player_socket in players_details_dict.values():

            player_socket.setblocking(False)

            ready = select.select([player_socket], [], [], 0)

            if ready[0]:
                print 'ready!'
                message_from_client = player_socket.recv(MAX_RECEIVING_BYTES_FROM_CLIENT)
                if message_from_client.endswith('d'):
                    print 'One of the Players pressed enter\nsend to other players GAME OVER'
                    players_results_list.append(message_from_client[:-1])
                    player_pressed_enter = True
                    if not game_over_sent:
                        send_to_players(GAME_OVER_MESSAGE)
                    game_over_sent = True
                else:
                    players_results_list.append(message_from_client)

            player_socket.setblocking(True)

    if not game_over_sent:
        print 'the Timer is Done , GAME OVER sent to players'
        send_to_players(GAME_OVER_MESSAGE)

    for receiving_player_result_thread in receiving_player_result_threads_list:
        receiving_player_result_thread.join()
    print 'The Results of the Game :'+str(players_results_list)
    send_to_players(convert_list_to_str(players_results_list))
    server_socket.close()
    print 'server closed'


if __name__ == '__main__':
    main()