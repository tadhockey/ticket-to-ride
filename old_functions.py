import networkx as nx
import pandas as pd
import random
import tkinter as tk
import math

from networkx.classes.function import path_weight
from networkx.algorithms.shortest_paths.generic import shortest_path
from tkinter import ttk

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