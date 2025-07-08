#!/usr/bin/python3

import webbrowser, sys, pyperclip

# Check if command line arguments were passed
if len(sys.argv) > 1:
    # ['mapit.py', '879', 'Valencia', 'St.'] -> '879 Valencia St.'
    address = ' '.join(sys.argv[1:])
else:
    address = pyperclip.paste()

# http://www.google.com/maps/place/
website = 'http://google.com/maps/place/'
webbrowser.open(website + address)

