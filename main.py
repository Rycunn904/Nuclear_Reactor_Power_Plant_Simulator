import sys
import os
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == "--test-DISPLAY":
            os.system("python -m pytest tests/test_reactor_systems.py")
            quit()
        if arg == "--test":
            os.system("python -m pytest")
            quit()
from gui import create_gui

debug = False

if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == "--debug" or arg == "-d":
            debug = True
        if arg == "--info":
            print("This is NOT FOR EDUCATIONAL USE\n"
            "Author: Ryan Cunningham\n"
            "Contact: itshim.ex@gmail.com\n"
            "\n"
            "Nuclear Reactor Power Plant Simulator\n"
            "This is a small game that I have been making. It was partially inspired by Naramo Nuclear Power Plant V2 on Roblox.\n"
            "Start the reactor, you got the rest! Go find it out!")
            quit()

create_gui(debug=debug)