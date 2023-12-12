import pyautogui
import keyboard
import csv
from tesseract_ocr import TesseractManager
from time import sleep
from time import perf_counter

screen_x, screen_y = pyautogui.size()

if screen_x == 2560 and screen_y == 1440:
    OFFSET_X = (210, 260)
    OFFSET_Y = (240, 800)
elif screen_x == 1920 and screen_y == 1080:
    OFFSET_X = (158, 323)
    OFFSET_Y = (197, 815)
else:
    Exception("Unsupported monitor size! Sorry, I'm a lazy fuck.")

IMAGES = "bin/images/"
BANLIST = "bin/banlist.csv"
SLEEP_INTERVAL = .1


class GuiManager():

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.banlist = []
        self.exit = False
        self.pause = False
        self.update_banlist()
        
    def update_banlist(self):
        with open(BANLIST, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.banlist.append(str(row[0]))
        
    def add_to_banlist(self, name=None, names=[]):
        if len(names) > 0:
            with open(BANLIST, "w", newline='') as csvfile:

                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for n in names:
                    writer.writerow(n)

        else:
            with open(BANLIST, "w", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(name)

        
        self.update_banlist()


    def get_names(self):
        tmp_filename = f"{IMAGES}namelist.png"

        #Hardcoded coordinates for name column
        x1, y1 = OFFSET_X[0], OFFSET_X[1]
        x2, y2 = OFFSET_Y[0], OFFSET_Y[1]
        
        pyautogui.screenshot(tmp_filename,region=(x1,y1,x2,y2))

    #Passes in one of the tuples from t.read_image()
    #Assumes the tuple has been verified as a user who needs to be kicked
    def click_and_kick(self, user:tuple):
        avg_x = ((user[0][2] + user[0][0])/2) + OFFSET_X[0]
        avg_y = ((user[0][3] + user[0][1])/2) + OFFSET_Y[0]

        pyautogui.click(x = avg_x, y = avg_y, button="right")
        sleep(.02)
        try:
            kick_coords = pyautogui.center(pyautogui.locateOnScreen(f"{IMAGES}button.png", confidence=.95))
            pyautogui.click(x = kick_coords.x, y = kick_coords.y, button = "left")
        except pyautogui.ImageNotFoundException:
            print("Kick button not found on screen! Continuing...")
        

    
    
    def kick_from_blacklist(self):
   
        t = TesseractManager(f"{IMAGES}namelist.png", .5)

        g.get_names()
        result = t.read_image()
        keys = []
        #Removes clan tags and the AI
        #Idk if these chars are banned in names tho is the problem
        blacklist_chars = ["<",">","."]
        for key in result.keys():
            print(result[key])
            keys.append(key)
        print(keys)
        keys_to_remove = []
        for key in keys:
            if any(char in key for char in blacklist_chars) or key == " " or key not in self.banlist:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del result[key]
            keys.remove(key)

        print(keys)
        if len(keys) > 0:
            g.click_and_kick(result[keys[0]])
        else:
            print("No targets found.")

    def disable_loop(self):
        self.exit = True

    def pause_loop(self):
        if self.pause:
            print("Unpausing...")
        else:
            print("Pausing...")
        self.pause = not self.pause
    
    def mainloop(self):
        keyboard.add_hotkey("ctrl+n", self.disable_loop)
        keyboard.add_hotkey("ctrl+r", self.update_banlist)
        keyboard.add_hotkey("ctrl+p", self.pause_loop)
        input("Init done. Press enter to begin.")
        self.exit = False
        while not self.exit:
            s_time = perf_counter()
            self.kick_from_blacklist()
            e_time = perf_counter()
            sleep(SLEEP_INTERVAL)

            while self.pause:
                sleep(.5)
            

        print("Done!")
    


if __name__ == "__main__":
    g = GuiManager()
    g.mainloop()
        

