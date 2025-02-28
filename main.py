# Import
import eel, os, json, hashlib

# Initialize
eel.init('web')

# List of consoles
consoles = ['XBOX', 'XBOX 360', 'Gamecube', 'Wii', 'Nintendo 64', 'Nintendo Switch', 'Super Nintendo', 'Wii U']

# List of games
games = ['Super Mario World', 'Mario Odyssey', 'Mario Kart', 'Mario Party', 'Mario 64', 'Mario Galaxy', "Luigi's Mansion"]



# Dummy data
for i in range(25):
    games.append(f"Game {i}")

# Passes consoles
@eel.expose
def get_consoles():
    return consoles

@eel.expose
def get_games():
    return games

# Run the program
if __name__ == '__main__':
    eel.start("index.html", host="localhost", port="5000", size=(1920, 1080))