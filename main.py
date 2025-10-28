from gui import create_gui
import sys

debug = False

if len(sys.argv) >= 1:
    print("more")
    for arg in sys.argv:
        if arg == "--debug":
            debug = True

create_gui(debug=debug)