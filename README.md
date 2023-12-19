# SC2AutoGui
Automates kicking of players from the lobby screen, managed by a csv banlist. Requires [tesseract-ocr](https://github.com/tesseract-ocr/tessdoc).

## Installation
Step 1. Install [tesseract-ocr](https://github.com/tesseract-ocr/tessdoc) and add to PATH

Step 2. Clone repo

Step 3. Set up virtual environment and `pip install requirements.txt`

Step 4. Add/Remove names from `bin/banlist.csv`

Step 5. Ensure names in SC2 lobby are not obsctructed by other windows and run script

## Usage
Keybinds:

`ctrl+n`: Stops checking for players and exits.

`ctrl+r`: Reloads ban list, so if you make changes to it while the program is running, use this

`ctrl+p`: Pause the script until hotkey is pressed again

`ctrl+a`: Enable Anti-AFK autoclick. Happens every 3 minutes.
