import pyautogui
import easyocr

IMAGES = "bin/images/"
ocr = easyocr.Reader(['en'])


class GuiManager():

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.update_mouse()

    def update_mouse(self):
        self.mouseX, self.mouseY = pyautogui.position()

    def get_names(self):
        tmp_filename = f"{IMAGES}test_namelist.png"

        #Hardcoded coordinates for name column
        x1, y1 = 210, 260
        x2, y2 = 380, 1066
        
        #name_img = pyautogui.screenshot(tmp_filename,region=(x1,y1,x2,y2))
        names = ocr.readtext(tmp_filename, detail = 0)
        print(names)
       

if __name__ == "__main__":
    g = GuiManager()

    g.get_names()

