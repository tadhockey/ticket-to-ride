# Ticket to Ride - Random Deck Generator and Game Control Interface

Ticket to Ride is a board game designed by Alan R. Moon and released in 2004 by Days of Wonder. Since it's release, Ticket to Ride is one of the most popular board games in the world, with numerous variants on the game.
The original, USA version of Ticket to Ride has a 30-card deck of "destination tickets". Each ticket has two listed cities. By connecting the listed cities, a player will score the number of points listed on the card. Often, connecting multiple destination tickets is the key to a successful and winning strategy.
However, this deck does not vary: the 30 cards are fixed. There are also many cities on the board which are not used (ex. Las Vegas, Raleigh, and Charleston are not listed in the deck) or used sparingly (ex. Boston is used in only one ticket). This reduces some of the variability in the gameplay.
The goal of this application is to create a new deck of 30 cards connecting random cities and provide an interface through which to play the board game. This does require a mobile device (preferably a light or small laptop) to be passed between players currently, as there is no online play.

Some other changes to the original rules:
  1. The random deck creation is split into two sections: a random deck of 30 cards worth <15 points and a random deck of 10 cards worth 15+ points. At the beginning of the game, players are dealt two cards from the smaller deck. These cards represent the "long route". Each player must select one card. This deck will not be used again: all future draws are through the random deck. This mechanic is inspired by changes made in Ticket to Ride: Europe.
  2. Other future rule adjustments will be listed here.

How to Run:
  1. Download all files from this directory.
  2. This project is confirmed to work on Python 3.10+: it likely works on other python versions but is not guaranteed. Ensure the packages listed in requirements.txt are installed in your environment.
  3. Run routegenerator.py. The game dialog box should open once started.

Coming Bug Fixes:
  1. Game state is not saved. Do not close the game window: the game state will not be recoverable
  2. Some route cards appear with curly braces ("{"). This does not impact gameplay
  3. Back buttons are not present in the current game. Be careful where clicks are presented
  4. There is no way out of the End Game screen currently. Do not initiate end game until all players agree the game is otherwise over.

Credits:
- This application has been developed in collaboration with Kayla Gronewold, my fiance. She's an amazing person and an inspiration to me!
