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

def create_game_window(game):
    """Creates a window interface to play the game in"""
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
    # menu_game.add_command(label='2 Players', command=lambda : [game.update_num_players(2), cards_windows(game)])
    # menu_game.add_command(label='3 Players', command=lambda : [game.update_num_players(3), cards_windows(game)])
    # menu_game.add_command(label='4 Players', command=lambda : [game.update_num_players(4), cards_windows(game)])
    # menu_game.add_command(label='5 Players', command=lambda : [game.update_num_players(5), cards_windows(game)])

    '''
    ttk.Label(mainframe, text='Create a New Game').grid(column=1, row=1, sticky='w')
    ttk.Label(mainframe, text='How many players are playing Ticket to Ride?').grid(column=1, row=2, sticky='n')
    
    players = tk.IntVar()
    
    ttk.Radiobutton(mainframe, text='Two', variable=players, value=2).grid(column=1, row=3, sticky='w')
    ttk.Radiobutton(mainframe, text='Three', variable=players, value=3).grid(column=1, row=4, sticky='w')
    ttk.Radiobutton(mainframe, text='Four', variable=players, value=4).grid(column=1, row=5, sticky='w')
    ttk.Radiobutton(mainframe, text='Five', variable=players, value=5).grid(column=1, row=6, sticky='w')
    
    ttk.Button(mainframe, text='Ready!', style='Ready.TButton',
               command=lambda : [game.update_num_players(players.get()), cards_windows(game)]).grid(column=2,
                                                                                                    row=7, sticky='n')
    ttk.Button(mainframe, text='Cancel Game', style='Exit.TButton', command=exit).grid(column=2, row=8, sticky='n')
    '''
    return root

#TODO: exclusivity of radio button choices
#TODO: block player from choosing fewer than minimum required cards
#TODO: handle edge case where deck is empty or has fewer than three cards to deal
def game_window(game, root):
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
        long_card_choice1 = tk.BooleanVar()
        long_card_choice2 = tk.BooleanVar()

        long_opt_1 = ttk.Radiobutton(root, text=options[0], variable=long_card_choice1)
        long_opt_2 = ttk.Radiobutton(root, text=options[1], variable=long_card_choice2)
        long_opt_1.grid(column=1, row=3, sticky='w')
        long_opt_2.grid(column=1, row=4, sticky='w')

        click = tk.IntVar()
        confirm = ttk.Button(root, text='Confirm Selection',
                             command=lambda: [game.choose_cards(1, [long_card_choice1.get(), long_card_choice2.get()], True),
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

        check1 = ttk.Checkbutton(root, text=options[0], variable=card1)
        check2 = ttk.Checkbutton(root, text=options[1], variable=card2)
        check3 = ttk.Checkbutton(root, text=options[2], variable=card3)
        check1.grid(column=0, row=2, sticky='w')
        check2.grid(column=0, row=3, sticky='w')
        check3.grid(column=0, row=4, sticky='w')
        click = tk.IntVar()
        confirm = ttk.Button(root, text='Confirm Selections',
                command=lambda: [game.choose_cards(1, [card1.get(), card2.get(), card3.get()]), player_label.destroy(),
                                 check1.destroy(), check2.destroy(), check3.destroy(), click.set(click.get() + 1), confirm.destroy()])
        confirm.grid(column=2, row=7, sticky='n')
        confirm.wait_variable(click)

    maintain_game(game, root)

'''
deprecated from earlier revisions
'''
def cards_windows(game):
    root = tk.Toplevel()
    root.title("Ticket to Ride: Ultimate Edition")
    mainframe = ttk.Frame(root, padding="6 6 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text='Deal Cards').grid(column=1, row=1, sticky='w')
    ttk.Label(mainframe, text='Which player should get cards?').grid(column=1, row=2, sticky='n')
    players = tk.StringVar()
    firstdeal = tk.BooleanVar()
    ttk.Entry(mainframe, width=5, textvariable=players).grid(column=1, row=3, sticky='n')
    ttk.Label(mainframe, text='First 3 Cards?').grid(column=1, row=4, sticky='n')
    ttk.Radiobutton(mainframe, text='Yes', variable=firstdeal, value=True).grid(column=1, row=6, sticky='w')
    ttk.Radiobutton(mainframe, text='No', variable=firstdeal, value=False).grid(column=1, row=7, sticky='w')
    #if firstdeal.get():
    #    minimum = 2
    #else:
    #    minimum = 1
    ttk.Button(mainframe, text='Deal Cards',
               command=lambda : [game.deal_cards(),
                                 display_three(game, firstdeal.get(), players.get())]).grid(column=2, row=7, sticky='n')

    return root

def display_three(game, first_deal, player_num):
    root = tk.Toplevel()
    root.title("Ticket to Ride: Ultimate Edition")
    mainframe = ttk.Frame(root, padding="6 6 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    player = int(player_num)
    ttk.Label(mainframe, text='3 Cards - Player ' + player_num).grid(column=1, row=1, sticky='w')
    card1 = tk.BooleanVar()
    card2 = tk.BooleanVar()
    card3 = tk.BooleanVar()
    options = game.show_dealt_cards()
    ttk.Checkbutton(mainframe, text=options[0], variable=card1).grid(column=1, row=6, sticky='w')
    ttk.Checkbutton(mainframe, text=options[1], variable=card2).grid(column=1, row=7, sticky='w')
    ttk.Checkbutton(mainframe, text=options[2], variable=card3).grid(column=1, row=8, sticky='w')
    ttk.Button(mainframe, text='Confirm Selections',
               command=lambda: [game.choose_cards(player - 1, [card1.get(), card2.get(), card3.get()]),
                                root.destroy()]).grid(column=2, row=7, sticky='n')

def maintain_game(game, root):
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
    for i in range(players):
        rb_dict[i].destroy()
    print('I got here!')

def additional_cards(game, root):
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

    check1 = ttk.Checkbutton(root, text=options[0], variable=card1)
    check2 = ttk.Checkbutton(root, text=options[1], variable=card2)
    check3 = ttk.Checkbutton(root, text=options[2], variable=card3)
    check1.grid(column=0, row=2, sticky='w')
    check2.grid(column=0, row=3, sticky='w')
    check3.grid(column=0, row=4, sticky='w')
    click = tk.IntVar()
    confirm = ttk.Button(root, text='Confirm Selections',
            command=lambda: [game.choose_cards(1, [card1.get(), card2.get(), card3.get()]), player_label.destroy(),
                             check1.destroy(), check2.destroy(), check3.destroy(),
                             click.set(click.get() + 1), confirm.destroy(), maintain_game(game, root)])
    confirm.grid(column=2, row=7, sticky='n')
    confirm.wait_variable(click)

def end_of_game(game, root):
    pass


def run_game():
    """Runs the full game - entrypoint of the script"""
    game = TTRGame()
    window = create_game_window(game)
    window.mainloop()


if __name__ == "__main__":
    run_game()



'''
# Distribute routes (need some sort of front end framework?)
player_count = input("How many players?")

for i in range(player_count):
    print(f"Route Distribution: Player {i}")
    # Randomly choose 3 destinations from the deck and present them to the player
    # Ex:
    # 1: Sault St. Marie --> Portland (18)
    # 2: Montreal --> St. Louis (9)
    # 3: El Paso --> Calgary (12)
    accepted_routes = input("Which routes would you like to accept? Enter the numbers of the routes " 
        "you'd like to accept separated by commas and press \"Enter\". You must accept at least two routes.")
    
    # Store accepted routes in player route structure
    
    # Remove accepted routes from the deck

def draw_additional_routes(player):
    pass
    # Used when a player chooses to draw new routes on their turn

    # Choose 3 new routes from the deck and present them following the previous logic

    # Probably put all this logic in one modular function
'''