import pyautogui
import keyboard
import csv
from tesseract_ocr import TesseractManager
from time import sleep

IMAGES = "bin/images/"
BANLIST = "bin/banlist.csv"
OFFSET_X = (210, 260)
OFFSET_Y = (240 , 800)
SLEEP_INTERVAL = .1


class GuiManager():

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.banlist = []
        self.exit = False
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
        print("Screenshot taken!")
        #names = ocr.readtext(tmp_filename, detail = 0)
        #print(names)

    #Passes in one of the tuples from t.read_image()
    #Assumes the tuple has been verified as a user who needs to be kicked
    def click_and_kick(self, user:tuple):
        avg_x = ((user[0][2] + user[0][0])/2) + OFFSET_X[0]
        avg_y = ((user[0][3] + user[0][1])/2) + OFFSET_Y[0]
        print(f"Average X: {avg_x}\nAverage Y: {avg_y}")
        #Make sure SC2 is in focus then right click
        pyautogui.click(x = avg_x, y = avg_y, button="left")
        pyautogui.click(x = avg_x, y = avg_y, button="right")
        sleep(.03)
        kick_coords = pyautogui.center(pyautogui.locateOnScreen(f"{IMAGES}button.png", confidence=.95))
        pyautogui.click(x = kick_coords.x, y = kick_coords.y, button = "left")
        

    
    
    def kick_from_blacklist(self):
   
        t = TesseractManager(f"{IMAGES}namelist.png", .5)

        #g.get_names()
        result = t.read_image()
        keys = []
        blacklist_chars = ["<",">","."]
        for key in result.keys():
            print(result[key])
            keys.append(key)
        print(keys)
        keys_to_remove = []
        print(f"Banlist: {self.banlist}")
        for key in keys:
            if any(char in key for char in blacklist_chars) or key == " " or key not in self.banlist:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del result[key]
            keys.remove(key)

        print(keys)
        g.click_and_kick(result[keys[0]])

    def disable_loop(self, e):
        self.exit = False
    
    def mainloop(self):
        keyboard.add_hotkey("ctrl+n", self.disable_loop)
        keyboard.add_hotkey("ctrl+r", self.update_banlist)
        self.add_to_banlist(names=[["TheKilla"], ["Procyon"], ["Killagal"], ["HighVoltage"],["Markus"],["Yugo"],["cat"]])
        input("Init done. Press enter to begin.")
        self.exit = False
        while not self.exit:
            self.kick_from_blacklist()
            sleep(SLEEP_INTERVAL)
            #TheKilla, Procyon, Killagal, HighVoltage, Markus, Yugo, LegIt

        print("Done!")
    


if __name__ == "__main__":
    g = GuiManager()
    g.mainloop()
        

