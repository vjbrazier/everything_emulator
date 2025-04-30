# Welcome to The Everything Emulator
This is not an emulator itself, it is a hub for other emulators. The idea is to eliminate the need to remember various emulator names, and instead have one single app for accessing everything.
However, it isn't just emulators, as it reads through games as well, identifying them and providing an easy way to open them. This comes with a search functionality, so that you can easily search for a game desired and open it right away. No need to bother with console, emulator, or opening the file. It is done for you.
<br/><br/>
It also has a custom menu for in the event that a ROM is unable to be identified (program mess up or modded) or if it is missing an image (database could be missing one). It is presented easily, and allows you to input your own data to fill these gaps.
<br/><br/>
List of consoles supported: 3DS, DS, Gameboy, Gameboy advance, Gamecube, NES, Nintendo 64, SNES, Switch, Wii, Xbox, Xbox-360
<br/><br/>
The main value of having this app is convenience and easy-access. The convenience was explained above, but easy-access comes in a different way. This program makes running older games extremely easy. This allows the ability to throw it up on a TV, and then those who have never heard of emulators can join you for fun in the games you get. Additionally, this eliminates the need to have dozens of retro consoles sitting underneath your TV.
<br/><br/>
Technologies used:
<br/>Eel - A python library that allows the creation of offline web pages. This made the GUI easy and flexible in creation.
<br/><br/>
Retroarch/No-database - Used for identifying most ROMs based on hash/serial, and getting data like name, image, etc.
<br/> -https://github.com/libretro/libretro-database 
<br/> -https://github.com/libretro-thumbnails/libretro-thumbnails
<br/><br/>
Emumovies - Provided Nintendo Switch and Xbox-360 image databases
<br/> -https://emumovies.com/files/file/5175-nintendo-switch-unified-25d-boxart/	
<br/> -https://emumovies.com/files/file/3802-microsoft-xbox-360-2d-boxes-pack-1201/ 
<br/><br/>
Blawar - Provided JSON data for Nintendo Switch games
<br/> -https://github.com/blawar/titledb_02112024/tree/master 
<br/><br/>
Hactool - Used to extract data from Nintendo Switch games
<br/> -https://github.com/SciresM/hactool/releases 
<br/><br/>
Built-in python libraries - json, re, os, shutil, pathlib, subprocess, sys, tempfile
<br/><br/>
Languages:
<br/> Python - Backend, interacting with files and reading data
<br/> HTML/CSS - GUI 
<br/> JS - Frontend, serving data received from the backend. 
<br/><br/>
Setup:
<br/> Download the repo
<br/> Install eel to your computer to run this program natively (pip install eel)
<br/><br/>
You will need:
<br/> -The databases. You will need the .dat file, boxart images, and snapshot images. Under src/data, create a folder called rom-info. Run the script once, and it will generate a console folder within this. Name the .dat file the same as this superfolder, then put boxart into a folder called cover, and snapshot into a folder called hover. The switch uses a .json file, just name it according to the folder. The Switch and Xbox 360 databases provided lack hover images. There is a menu to add your own, but if you don't want to do this yourself, just copy the cover images and rename the folder. The Switch .json also has less detailed naming, to accout for this there is a cleaner.py file under src. Move this file, and the images gallery to their own folder, and put the images under a folder called 'images', then just run the script to clean the images
<br/> -A prod.keys file if you intend on using switch games. Throw it in the switch directory
<br/><br/>
Once you have downloaded and setup the database, just create a shortcut to main.py under src/, and add it to where you want this program. There is an icon attached that you can use if you'd like
