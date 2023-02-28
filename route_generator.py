import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random

from networkx.classes.function import path_weight
from networkx.algorithms.shortest_paths.generic import shortest_path

# Read in and format route data
routes_df = pd.read_csv("route_list.csv")
city_list = list(routes_df.City1)
routes_list = list(zip(list(routes_df.City1), list(routes_df.City2), list(routes_df.Distance)))

# Create route graph
G = nx.Graph()
G.add_weighted_edges_from(routes_list)
#nx.draw_networkx(G)

# Generate deck of 30 destination cards
# while len(deck structure) < 30:
end_cities = random.sample(city_list, 2)
path = shortest_path(G, end_cities[0], end_cities[1])
path_cost = path_weight(G, path, "weight")

    # Remove invalid routes
    # if invalid:
    #     continue
    # else:
    #     save to deck strucure


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
