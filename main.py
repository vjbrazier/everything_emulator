# Import
import eel, os, json

# Initialize
eel.init('web')

# List of consoles
consoles = ['Wii', 'NES', 'SNES', 'Switch', 'Gameboy']

# Passes consoles
@eel.expose
def get_consoles():
    return consoles

# Run the program
if __name__ == '__main__':
    eel.start("index.html", host="localhost", port="5000", size=(1200, 1200))