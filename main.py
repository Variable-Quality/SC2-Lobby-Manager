import pyautogui
import keyboard
import csv
from tesseract_ocr import TesseractManager
from time import sleep
from time import perf_counter
import curses
import math


#Reference resolution is 2560x1440
ref_res = (2560, 1440)
current_res = pyautogui.size()

OFFSET_COORDS = [198, 280, 260, 800]

scaled_coords = [int((OFFSET_COORDS[i] * current_res[i % 2]) / ref_res[i % 2]) for i in range(4)]

OFFSET_X = (scaled_coords[0], scaled_coords[2])
OFFSET_Y = (scaled_coords[1], scaled_coords[3])

screen_x, screen_y = pyautogui.size()

IMAGES = "bin/images/"
BANLIST = "bin/banlist.csv"

SLEEP_INTERVAL = .1 #Seconds
AFK_INTERVAL = 180 #Seconds



class OCRManager():

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.banlist = []
        self.exit = False
        self.pause = False
        self.afk = False
        self.host_mode = True
        self.debug = False
        self.update_banlist()
        
    def update_banlist(self):
        self.banlist = []
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
    def click_and_kick(self, user:tuple, stdscr):
        avg_x = ((user[0][2] + user[0][0])/2) + OFFSET_X[0]
        avg_y = ((user[0][3] + user[0][1])/2) + OFFSET_Y[0]
        pyautogui.click(x = avg_x, y = avg_y, button="right")
        sleep(.02)
        try:
            kick_coords = pyautogui.center(pyautogui.locateOnScreen(f"{IMAGES}button.png", confidence=.98))
            pyautogui.click(x = kick_coords.x, y = kick_coords.y, button = "left")
        except pyautogui.ImageNotFoundException:
            stdscr.addstr(8,0,"Kick button not found on screen! Continuing...")
        

    
    
    def read_from_blacklist(self, stdscr):
   
        t = TesseractManager(f"{IMAGES}namelist.png", .5)

        g.get_names()
        result = t.read_image(self.debug)
        keys = []
        #Removes clan tags and the AI
        #Idk if these chars are banned in names tho is the problem
        blacklist_chars = ["<",">","."]
        for key in result.keys():
            keys.append(key)
        keys_to_remove = []
        for key in keys:
            if any(char in key for char in blacklist_chars) or key == " " or key not in self.banlist:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del result[key]
            keys.remove(key)

        stdscr.addstr(3, 0, str(keys))
        if len(keys) > 0 and self.host_mode:
            g.click_and_kick(result[keys[0]], stdscr)

        elif len(keys) > 0 and not self.host_mode:
            stdscr.addstr(4, 0, f"Detected banned player(s) in lobby!")
        else:
            stdscr.addstr(4, 0, "No targets found.")

    def disable_loop(self):
        self.exit = True

    def pause_loop(self):
        self.pause = not self.pause

    def toggle_afk(self):
        self.afk = not self.afk

    def toggle_host_mode(self):
        self.host_mode = not self.host_mode

    def toggle_debug(self):
        self.debug = not self.debug

    def mainloop(self, stdscr):
        curses.curs_set(0)
        keyboard.add_hotkey("ctrl+n", self.disable_loop)
        keyboard.add_hotkey("ctrl+r", self.update_banlist)
        keyboard.add_hotkey("ctrl+p", self.pause_loop)
        keyboard.add_hotkey("ctrl+a", self.toggle_afk)
        keyboard.add_hotkey("ctrl+h", self.toggle_host_mode)
        #This one is just for me :3
        keyboard.add_hotkey("ctrl+d", self.toggle_debug)

        self.exit = False
        prev_click_time = 0



        while not self.exit:
            last_click = perf_counter() - prev_click_time
            last_click_s = f"| Time since last click: {math.floor(last_click)}s" if self.afk else ""
            stdscr.clear()
            stdscr.addstr(0, 0, f"Loop Paused: {self.pause}")
            stdscr.addstr(1, 0, f"Anti-Afk Enabled: {self.afk} {last_click_s}")
            stdscr.addstr(2, 0, f"Host Mode Enabled: {self.host_mode}")
           
            if self.afk and last_click > AFK_INTERVAL:
                tmp_mousepos_x, tmp_mousepos_y = pyautogui.position()
                #Assumes Starcraft is visible on main monitor
                #Cba changing this
                pyautogui.click(x=200,y=200)
                pyautogui.moveTo(x=tmp_mousepos_x, y=tmp_mousepos_y)
                prev_click_time = perf_counter()

            if not self.pause:    
                self.read_from_blacklist(stdscr)

            stdscr.refresh()
            sleep(SLEEP_INTERVAL)
            

        print("Done!")
    


if __name__ == "__main__":
    g = OCRManager()
    curses.wrapper(g.mainloop)
        

