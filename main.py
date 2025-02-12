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
    eel.start("index.html", size=(600,600))