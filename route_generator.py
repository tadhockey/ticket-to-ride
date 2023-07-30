import networkx as nx
import pandas as pd
import random
import tkinter as tk
import math

from networkx.classes.function import path_weight
from networkx.algorithms.shortest_paths.generic import shortest_path
from tkinter import ttk

class TTRGame():

    def __init__(self, num_players=1):
        self.players = num_players
        self.graph = self.generate_route_graph()
        self.short_deck, self.long_deck = self.generate_deck()
        self.hands = dict()
        for i in range(num_players):
            self.hands[i] = []
        self.candidates = []

    def update_num_players(self, new_players):
        """Confirms player count, for use at beginning of game before dealing"""
        self.players = new_players
        for i in range(self.players):
            self.hands[i] = []

    def generate_route_graph(self):
        """Generates a graph network given a csv of city data"""
        routes_df = pd.read_csv("route_list.csv")
        routes_list = list(zip(list(routes_df.City1), list(routes_df.City2), list(routes_df.Distance)))

        G = nx.Graph()
        G.add_weighted_edges_from(routes_list)

        return G

    def generate_deck(self, deck_size=30):
        """Generates a deck of valid routes from the pool of cities."""
        city_list = list(self.graph.nodes)
        short_deck = []
        long_deck = []

        while len(short_deck) < deck_size:
            path = []
            path_cost = 0
            while path_cost < 4 or path_cost > 14 or len(path) < 3:
                end_cities = random.sample(city_list, 2)
                path = shortest_path(self.graph, end_cities[0], end_cities[1])
                path_cost = path_weight(self.graph, path, "weight")

            route_title = end_cities[0] + '-' + end_cities[1]
            card = (route_title, path_cost)

            route_title_rev = end_cities[1] + '-' + end_cities[0]
            rev_card = (route_title_rev, path_cost)

            if (card not in short_deck) and (rev_card not in short_deck):
                short_deck.append(card)

        while len(long_deck) < 10:
            path = []
            path_cost = 0
            while path_cost < 15 or path_cost > 25:
                end_cities = random.sample(city_list, 2)
                #print(end_cities)
                path = shortest_path(self.graph, end_cities[0], end_cities[1])
                #print(path)
                path_cost = path_weight(self.graph, path, "weight")

            route_title = end_cities[0] + '-' + end_cities[1]
            card = (route_title, path_cost)

            route_title_rev = end_cities[1] + '-' + end_cities[0]
            rev_card = (route_title_rev, path_cost)

            if (card not in long_deck) and (rev_card not in long_deck):
                #print(len(long_deck))
                long_deck.append(card)

        print('short deck')
        print(short_deck)
        print('long deck')
        print(long_deck)
        return short_deck, long_deck

    def deal_cards(self):
        for i in range(3):
            self.candidates.append(self.short_deck.pop(0))

    def deal_long_cards(self):
        for i in range(2):
            self.candidates.append(self.long_deck.pop(0))

    def show_dealt_cards(self):
        return self.candidates

    def choose_cards(self, player_num, cards_chosen, long=False):
        for x in range(len(cards_chosen)):
            if cards_chosen[x]:
                self.hands[player_num].append(self.candidates[x])
                print(self.hands[player_num])
            else:
                if long:
                    self.long_deck.append(self.candidates[x])
                else:
                    self.short_deck.append(self.candidates[x])
        self.candidates = []

    def num_of_players(self):
        return self.players

    def show_hands(self, player=None):
        if player != None:
            return self.hands[player]
        else:
            return self.hands

def card_array(selection, num_options):
    """Chooses between cards when limited to single option via radiobutton or text box"""
    arr = []
    for i in range(num_options):
        if i == selection:
            arr.append(True)
        else:
            arr.append(False)
    return arr

def button_state(button, var, first_deal=False):
    """Adjusts button state based on number of cards chosen. Can require 2 choices during initial deal"""
    if first_deal:
        if sum(var) >= 2:
            button['state'] = "normal"
        else:
            button['state'] = "disable"
    else:
        if any(var):
            button['state'] = "normal"
        else:
            button['state'] = "disable"

def create_game_window(game):
    """Creates a window interface to play the game in, allows choice of player quantity
    """
    root = tk.Tk()
    root.title("Ticket to Ride: Ultimate Edition")
    #mainframe = ttk.Frame(root, padding="60 60 60 60")
    #mainframe.grid(column=0, row=0, sticky='nsew')
    #root.columnconfigure(0, weight=1)
    #root.rowconfigure(0, weight=1)
    #root.rowconfigure(1, weight=1)
    #root.rowconfigure(2, weight=1)
    #root.option_add('*tearOff', False)

    style1 = ttk.Style()
    style1.configure('Ready.TButton', background='black', foreground='green')
    style2 = ttk.Style()
    style2.configure('Exit.TButton', background='black', foreground='red')

    menubar = tk.Menu(root)
    root['menu'] = menubar
    menu_game = tk.Menu(menubar)

    root.geometry('900x600+40+40')
    root.resizable(False,False)
    start_label = ttk.Label(root, text='Create a New Game to Begin!')
    start_label.grid(column=0, row=0, sticky='nsew')

    menubar.add_cascade(menu=menu_game, label='New Game')
    menu_game.add_command(label='2 Players', command=lambda : [game.update_num_players(2), start_label.destroy(), game_window(game, root)])
    menu_game.add_command(label='3 Players', command=lambda : [game.update_num_players(3), start_label.destroy(), game_window(game, root)])
    menu_game.add_command(label='4 Players', command=lambda : [game.update_num_players(4), start_label.destroy(), game_window(game, root)])
    menu_game.add_command(label='5 Players', command=lambda : [game.update_num_players(5), start_label.destroy(), game_window(game, root)])

    return root
    
#TODO: handle edge case where deck is empty or has fewer than three cards to deal
def game_window(game, root):
    """Initial dealing sequence"""

    for i in range(game.num_of_players()):

        text = 'Player ' + str(i + 1) + ', please prepare to choose cards'
        player_label = ttk.Label(root, text=text)
        player_label.grid(column=0, row=1, sticky='nsew')

        click = tk.IntVar()
        confirm = ttk.Button(root, text='Ready!',
                             command=lambda: [player_label.destroy(),
                                 click.set(click.get() + 1), confirm.destroy()])
        confirm.grid(column=2, row=7, sticky='n')
        confirm.wait_variable(click)

        #Long Deal
        text = 'Player ' + str(i + 1) + ', choose your long route card:'
        player_label = ttk.Label(root, text=text)
        player_label.grid(column=0, row=1, sticky='nsew')

        game.deal_long_cards()
        options = game.show_dealt_cards()
        long_card_choice = tk.IntVar()

        long_opt_1 = ttk.Radiobutton(root, text=options[0], variable=long_card_choice, value=0)
        long_opt_2 = ttk.Radiobutton(root, text=options[1], variable=long_card_choice, value=1)
        long_opt_1.grid(column=1, row=3, sticky='w')
        long_opt_2.grid(column=1, row=4, sticky='w')

        click = tk.IntVar()
        confirm = ttk.Button(root, text='Confirm Selection',
                             command=lambda: [game.choose_cards(i, card_array(long_card_choice.get(), 2), True),
                                              player_label.destroy(),
                                              long_opt_1.destroy(), long_opt_2.destroy(),
                                              click.set(click.get() + 1), confirm.destroy()])
        confirm.grid(column=2, row=7, sticky='n')
        confirm.wait_variable(click)

        #Short Deal
        text = 'Player ' + str(i + 1) + ', choose your short route cards:'
        player_label = ttk.Label(root, text=text)
        player_label.grid(column=0, row=1, sticky='nsew')

        game.deal_cards()
        options = game.show_dealt_cards()
        card1 = tk.BooleanVar()
        card2 = tk.BooleanVar()
        card3 = tk.BooleanVar()

        click = tk.IntVar()
        confirm = ttk.Button(root, text='Confirm Selections', state='disabled',
                command=lambda: [game.choose_cards(i, [card1.get(), card2.get(), card3.get()]), player_label.destroy(),
                                 check1.destroy(), check2.destroy(), check3.destroy(), click.set(click.get() + 1), confirm.destroy()])
        confirm.grid(column=2, row=7, sticky='n')

        check1 = ttk.Checkbutton(root, text=options[0], variable=card1,
                                 command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()], True)])
        check2 = ttk.Checkbutton(root, text=options[1], variable=card2,
                                 command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()], True)])
        check3 = ttk.Checkbutton(root, text=options[2], variable=card3,
                                 command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()], True)])
        check1.grid(column=0, row=2, sticky='w')
        check2.grid(column=0, row=3, sticky='w')
        check3.grid(column=0, row=4, sticky='w')

        confirm.wait_variable(click)

    maintain_game(game, root)

def maintain_game(game, root):
    """Choose between additional card dealing and end of game sequence"""

    click = tk.IntVar()
    header = ttk.Label(root, text='Choose Next Action')
    header.grid(column=0, row=0)
    deal_card_button = ttk.Button(root, text='Deal More Cards to Player',
                                  command=lambda: [header.destroy(), click.set(click.get() + 1),
                                                    end_game_button.destroy(),
                                                   deal_card_button.destroy(),
                                                   additional_cards(game, root)])
    deal_card_button.grid(column=0, row=1, sticky='n')
    end_game_button = ttk.Button(root, text='Initiate Game End Procedure',
                                 command=lambda: [header.destroy(), end_of_game(game, root), click.set(click.get() + 1),
                                                    deal_card_button.destroy(), end_game_button.destroy()])
    end_game_button.grid(column=0, row=2, sticky='n')
    deal_card_button.wait_variable(click)
    end_game_button.wait_variable(click)

def rb_destroy(players, rb_dict):
    """Destroys radio buttons when radioButton objects are passed as array"""
    for i in range(players):
        rb_dict[i].destroy()
    print('I got here!')

def additional_cards(game, root):
    """Process for dealing additional cards to players as required by game"""

    text = 'Choose a player to deal cards to:'
    player_label = ttk.Label(root, text=text)
    player_label.grid(column=0, row=1, sticky='nsew')

    players = tk.IntVar()
    player_numbers = ["1", "2", "3", "4", "5"]
    rb = dict()
    click = tk.IntVar()
    for i in range(game.num_of_players()):
        rb[i] = ttk.Radiobutton(root, text=player_numbers[i], variable=players, value=i+1)
        rb[i].grid(column=0, row=i+2, sticky='w')
    confirm = ttk.Button(root, text='Confirm Selection',
                                  command=lambda: [player_label.destroy(),
                                                   rb_destroy(game.num_of_players(), rb),
                                                   click.set(click.get() + 1),
                                                   confirm.destroy()])
    confirm.grid(column=2, row=7, sticky='n')
    confirm.wait_variable(click)

    #prepare statement
    text = 'Player ' + str(players.get()) + ', please prepare to choose cards'
    player_label = ttk.Label(root, text=text)
    player_label.grid(column=0, row=1, sticky='nsew')

    click = tk.IntVar()
    confirm = ttk.Button(root, text='Ready!',
                         command=lambda: [player_label.destroy(),
                                          click.set(click.get() + 1), confirm.destroy()])
    confirm.grid(column=2, row=7, sticky='n')
    confirm.wait_variable(click)

    #choose new cards
    text = 'Player ' + str(players.get()) + ', choose your short route cards:'
    player_label = ttk.Label(root, text=text)
    player_label.grid(column=0, row=1, sticky='nsew')

    game.deal_cards()
    options = game.show_dealt_cards()
    card1 = tk.BooleanVar()
    card2 = tk.BooleanVar()
    card3 = tk.BooleanVar()
    click = tk.IntVar()

    confirm = ttk.Button(root, text='Confirm Selections', state='disabled',
            command=lambda: [game.choose_cards(1, [card1.get(), card2.get(), card3.get()]), player_label.destroy(),
                             check1.destroy(), check2.destroy(), check3.destroy(),
                             click.set(click.get() + 1), confirm.destroy(), maintain_game(game, root)])
    confirm.grid(column=2, row=7, sticky='n')

    check1 = ttk.Checkbutton(root, text=options[0], variable=card1,
                             command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()])])
    check2 = ttk.Checkbutton(root, text=options[1], variable=card2,
                             command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()])])
    check3 = ttk.Checkbutton(root, text=options[2], variable=card3,
                             command=lambda: [button_state(confirm, [card1.get(), card2.get(), card3.get()])])
    check1.grid(column=0, row=2, sticky='w')
    check2.grid(column=0, row=3, sticky='w')
    check3.grid(column=0, row=4, sticky='w')

    confirm.wait_variable(click)

def end_of_game(game, root):
    """Shows all player cards for easier scoring"""

    for i in range(game.num_of_players()):
        player_hand = game.show_hands(i)
        print(player_hand)
        text = 'Player ' + str(i + 1) + ' chosen cards'
        player_label = dict()
        player_label[i] = ttk.Label(root, text=text)
        player_label[i].grid(column=i, row=1, sticky='nsew')
        for j in range(len(player_hand)):
            ttk.Label(root, text=player_hand[j]).grid(column=i, row=2 + j, sticky='nsew')

def run_game():
    """Runs the full game - entrypoint of the script"""
    game = TTRGame()
    window = create_game_window(game)
    window.mainloop()


if __name__ == "__main__":
    run_game()