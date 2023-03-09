import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
from tkinter import *
from tkinter import ttk

from networkx.classes.function import path_weight
from networkx.algorithms.shortest_paths.generic import shortest_path

def generate_deck():
    # Read in and format route data
    routes_df = pd.read_csv("route_list.csv")
    city_list = list(routes_df.City1)
    routes_list = list(zip(list(routes_df.City1), list(routes_df.City2), list(routes_df.Distance)))

    # Create route graph
    G = nx.Graph()
    G.add_weighted_edges_from(routes_list)
    #nx.draw_networkx(G)

    # Generate deck of 30 destination cards
    deck = []
    deck_size = 30
    while len(deck) < deck_size:
        end_cities = random.sample(city_list, 2)
        path = shortest_path(G, end_cities[0], end_cities[1])
        while len(path) < 3: # check for intermediate city, redraw if necessary
            end_cities = random.sample(city_list, 2)
            path = shortest_path(G, end_cities[0], end_cities[1])
        path_cost = path_weight(G, path, "weight")
        title = end_cities[0] + '-' + end_cities[1]
        title_rev = end_cities[1] + '-' + end_cities[0]
        card = (title, path_cost)
        if not(card in deck or (title_rev, path_cost) in deck): #check for duplicates
            deck.append(card)
    #print(deck)

    return deck

def generate_game(num_players=2):
    cards = dict()
    for x in range(num_players):
        cards[x] = []
    deck = generate_deck()
    cards['deck'] = deck
    print(cards['deck'])
    game_state = (cards, deck)
    return game_state

def deal_to_player(player, game_state, initial_deal=True):
    pass

def end_of_game():
    pass

def main():
    root = Tk()
    root.title("Game Window")
    mainframe = ttk.Frame(root, padding="6 6 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text='Hello!').grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text='How many players are playing Ticket to Ride?').grid(column=1, row=2, sticky=N)
    players = IntVar()
    two = ttk.Radiobutton(mainframe, text='Two', variable=players, value=2).grid(column=1, row=3, sticky=W)
    three = ttk.Radiobutton(mainframe, text='Three', variable=players, value=3).grid(column=1, row=4, sticky=W)
    four = ttk.Radiobutton(mainframe, text='Four', variable=players, value=4).grid(column=1, row=5, sticky=W)
    five = ttk.Radiobutton(mainframe, text='Five', variable=players, value=5).grid(column=1, row=6, sticky=W)
    choice = ttk.Button(mainframe, text='Ready!', command=lambda : generate_game(players.get())).grid(column=2, row=7, sticky=N)
    cancel = ttk.Button(mainframe, text='Cancel Game', command=exit).grid(column=2, row=8, sticky=N)

    root.mainloop()


if __name__ == "__main__":
    main()



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