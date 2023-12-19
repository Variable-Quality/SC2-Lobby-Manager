from tkinter import *


class GuiManager():

    def __init__(self, OCRM):
        #OCRManager Class passed in for access to boolean values
        self.OCRM = OCRM
        self.root = Tk()
        self.root.title("SC2 Lobby Manager Dashboard")

        self.paused = Label(self.root, text=f"Scanning Paused:\n{OCRM.pause}")
        self.paused.pack()

        self.host_mode = Label(self.root, text=f"Host Mode Enabled:\n{OCRM.host_mode}")
        self.host_mode.pack()

        self.anti_afk = Label(self.root, text=f"Anti AFK Enabled:\n{OCRM.afk}")
        self.anti_afk.pack()

        self.debug = Label(self.root, text=f"Debug Enabled:\n{OCRM.debug}")
        self.debug.pack()

        self.banned_players_list = Text(self.root, height=10, width=50)
        self.banned_players_list.pack()

    def update_text(self):
        print("Text updated!")
        self.paused = Label(self.root, text=f"Scanning Paused:\n{self.OCRM.pause}")
        self.host_mode = Label(self.root, text=f"Host Mode Enabled:\n{self.OCRM.host_mode}")
        self.anti_afk = Label(self.root, text=f"Anti AFK Enabled:\n{self.OCRM.afk}")
        self.debug = Label(self.root, text=f"Debug Enabled:\n{self.OCRM.debug}")

        if self.banned_players_list.get("1.0", END) != str(self.OCRM.detected_players):
            self.banned_players_list.delete("1.0", END)
            self.banned_players_list.insert(END, str(self.OCRM.detected_players))

        self.root.after(500, self.update_text)