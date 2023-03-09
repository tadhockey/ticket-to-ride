import networkx as nx
import pandas as pd
import random
import tkinter as tk

from networkx.classes.function import path_weight
from networkx.algorithms.shortest_paths.generic import shortest_path
from tkinter import ttk


def generate_route_graph(route_csv):
    """Generates a graph network given a csv of city data"""
    routes_df = pd.read_csv(route_csv)
    routes_list = list(zip(list(routes_df.City1), list(routes_df.City2), list(routes_df.Distance)))

    G = nx.Graph()
    G.add_weighted_edges_from(routes_list)

    return G

def generate_deck(G, deck_size=30):
    """Generates a deck of valid routes from the pool of cities."""
    city_list = list(G.nodes)
    deck = []
    
    while len(deck) < deck_size:
        path = []
        while len(path) < 3:
            end_cities = random.sample(city_list, 2)
            path = shortest_path(G, end_cities[0], end_cities[1])
        path_cost = path_weight(G, path, "weight")

        route_title = end_cities[0] + '-' + end_cities[1]
        card = (route_title, path_cost)

        route_title_rev = end_cities[1] + '-' + end_cities[0]
        rev_card = (route_title_rev, path_cost)

        if (card not in deck) and (rev_card not in deck):
            deck.append(card)
        
    return deck

def generate_game(G, num_players=2):
    """Generates an empty game state for a new game"""
    deck = generate_deck(G)
    player_cards = {"deck": deck}

    for x in range(num_players):
        player_cards[x] = []

    return (player_cards, deck)
    

def create_game_window(G):
    """Creates a window interface to play the game in"""
    root = tk.Tk()
    root.title("Ticket to Ride: Ultimate Edition")
    mainframe = ttk.Frame(root, padding="6 6 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text='Create a New Game').grid(column=1, row=1, sticky='w')
    ttk.Label(mainframe, text='How many players are playing Ticket to Ride?').grid(column=1, row=2, sticky='n')
    players = tk.IntVar()
    ttk.Radiobutton(mainframe, text='Two', variable=players, value=2).grid(column=1, row=3, sticky='w')
    ttk.Radiobutton(mainframe, text='Three', variable=players, value=3).grid(column=1, row=4, sticky='w')
    ttk.Radiobutton(mainframe, text='Four', variable=players, value=4).grid(column=1, row=5, sticky='w')
    ttk.Radiobutton(mainframe, text='Five', variable=players, value=5).grid(column=1, row=6, sticky='w')
    ttk.Button(mainframe, text='Ready!', command=lambda : generate_game(G, players.get())).grid(column=2, row=7, sticky='n')
    ttk.Button(mainframe, text='Cancel Game', command=exit).grid(column=2, row=8, sticky='n')

    return root


def deal_to_player(player, game_state, initial_deal=True):
    pass


def end_of_game():
    pass


def run_game():
    """Runs the full game - entrypoint of the script"""
    G = generate_route_graph("route_list.csv")
    window = create_game_window(G)
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