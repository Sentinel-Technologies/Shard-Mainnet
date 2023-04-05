"""
    gui.py
    Shard Core V 0.10
    Copyright (c) 2023 The ShardCoin developers
    Distributed under the MIT software license, see the accompanying
    For copying see http://opensource.org/licenses/mit-license.php.
"""
import requests, madzpy, qrcode, time
from PIL import Image
from customtkinter import *
from tkinter import Menu
from tkinter.messagebox import showerror, showinfo, showwarning
from src.vars import *
from src.funcs import get_priv, rgbPrint, read_yaml_config

def getaddr():
    cfg = get_priv()["public"]
    return cfg

class App():
    def __init__(self) -> None:
        self.app = CTk()
        w, h = self.app.winfo_screenwidth(), self.app.winfo_screenheight()
        self.app.geometry("%dx%d+0+0" % (w, h))
        self.app.iconbitmap("data/Shardcoin.ico")
        self.app.title(f"Shard Core V{VER}")

        self.tabview = CTkTabview(self.app)
        self.tabview.pack(fill="both", expand=1)

        self.tabview.add("Dashboard")
        self.tabview.add("Send")
        self.tabview.add("Transactions")
        self.tabview.add("Network stats")
        self.tabview.set("Dashboard")

        menu = Menu(self.app)
        self.app.config(menu=menu)

        fileMenu = Menu(menu, tearoff="off")
        menu.add_cascade(label="File", menu=fileMenu)

        fileMenu.add_command(label="Exit", command=exit)

        optionMenu = Menu(menu, tearoff="off")
        menu.add_cascade(label="Options", menu=optionMenu)

        optionMenu.add_cascade(label="Connected Peers", command=self.connectedPeers)

        helpMenu = Menu(menu, tearoff="off")
        menu.add_cascade(label="Help", menu=helpMenu)

        self.addr = get_priv()
        self.cfg = read_yaml_config(print_host = False)[0]
        self.madz = madzpy.madz(self.cfg["url"])

        self.dashboard()
        self.netstats()

    def dashboard(self):
        progressbar = CTkProgressBar(master=self.tabview.tab("Dashboard"), mode="indeterminate")
        CTkLabel(self.tabview.tab("Dashboard"), text="Checking Peers for any updates...",font=("Arial",12)).pack(side=TOP, anchor="n")
        progressbar.pack(padx=10, pady=10)
        progressbar.start()

        self.cur_acc = CTkLabel(self.tabview.tab("Dashboard"), text =f"Connected Account: {getaddr()}\n", font=("Arial",20))
        self.cur_bal = CTkLabel(self.tabview.tab("Dashboard"), text=f"Network Balance: {self.madz.balance(getaddr())} Madz", font=("Arial",25,"bold"))
        self.cur_tx = CTkLabel(self.tabview.tab("Dashboard"), text=f"Transactions sent/recieved: {self.webdata()['txcount']}", font=("Arial",25))
        self.cur_rec = CTkButton(self.tabview.tab("Dashboard"), text="Receive Shard", command=self.receivemadz)
        self.refreshbutton = CTkButton(self.tabview.tab("Dashboard"), text="Refresh", command=self.refresh_dashboard)

        self.cur_acc.pack(side=TOP, anchor="n")
        self.cur_bal.pack(side=TOP, anchor="w")
        self.cur_tx.pack(side=TOP, anchor="w")

        self.cur_rec.pack(side=LEFT, anchor="n", padx=0.5, pady=0.5)
        self.refreshbutton.pack(side=LEFT, anchor="n")

    def sendpage():
        pass

    def txpage():
        pass

    def netstats(self):
        url = self.cfg["url"]
        stats = requests.get(url+"/stats").json()["result"]
        self.title = CTkLabel(self.tabview.tab("Network stats"), text="Network Statistics", font=("Arial",30)).pack(side=TOP, anchor="n")
        self.height = CTkLabel(self.tabview.tab("Network stats"), text=f"Block Height: {stats['chain']['length']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.transcount = CTkLabel(self.tabview.tab("Network stats"), text=f"Network Tx count: {stats['coin']['transactions']}" , font=("Arial",20)).pack(side=TOP, anchor="w")
        self.supply = CTkLabel(self.tabview.tab("Network stats"), text=f"Circulating Supply: {stats['coin']['supply']} MADZ", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.blocktime = CTkLabel(self.tabview.tab("Network stats"), text=f"Last Block Time: {stats['chain']['LastBlockTime']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.blockreward = CTkLabel(self.tabview.tab("Network stats"), text=f"Block Reward: {stats['chain']['blockReward']} MADZ", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.owner = CTkLabel(self.tabview.tab("Network stats"), text=f"Owner: {stats['node']['owner']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.version = CTkLabel(self.tabview.tab("Network stats"), text=f"Network Version: V{stats['node']['version']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.smalltext = CTkLabel(self.tabview.tab("Network stats"), text=f"Results taken from {url} aka your node.", font=("Arial", 10)).pack(side=TOP, anchor="w")

    def receivemadz(self):
        win = CTkToplevel()
        win.wm_title("Receive Madz")
        win.wm_geometry("310x250")
        win.wm_iconbitmap("data/Shard.ico")
        win.resizable(False, False)
        qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
        )
        img = qrcode.make(getaddr())
        type(img)  # qrcode.image.pil.PilImage
        img.save("data/addressqr.png")
        qrimg = CTkImage(dark_image=Image.open("data/addressqr.png"), size=(100,100))
        qraddr = CTkLabel(win, image=qrimg, text="")
        qraddr.grid(row=1, column=0)

        instr = CTkLabel(win, text="Instruct the sender to send Madz to this Address:")
        instr.grid(row=0, column=0)

        entry = CTkLabel(master=win, text=getaddr())
        entry.grid(row=2, column=0)

        bt = CTkButton(win, text="Copy to clipboard", command=self.copy())
        bt.grid(row=3, column=0, padx=5, pady=5)

        b = CTkButton(win, text="Okay", command=win.destroy)
        b.grid(row=4, column=0)

    def copy(self):
        inp = getaddr()
        self.app.clipboard_clear() # Clear the tkinter clipboard
        self.app.clipboard_append(inp) # Append to system clipboard

    def webdata(self):
        url = self.cfg["url"]
        blockheight = requests.get(url+"/chain/length").json()["result"]
        webdata = requests.get(url+"/stats").json()
        supply = webdata["result"]["coin"]["supply"]
        blocktime = webdata["result"]["chain"]["LastBlockTime"]
        txcount = requests.get(url+"/accounts/accountInfo/"+getaddr()).json()["result"]["transactions"]

        return ({"Block":blockheight, "supply":supply, "time":blocktime, "txcount":len(txcount)})

    def connectedPeers(self):
        url = self.cfg["url"]
        onlinepeers = requests.get(url+"/net/getOnlinePeers").json()["result"]
        showinfo("Connected to", onlinepeers)

    def refresh_dashboard(self):
        self.cur_bal.destroy()
        self.cur_tx.destroy()
        self.cur_bal = CTkLabel(self.tabview.tab("Dashboard"), text=f"Network Balance: {self.madz.balance(getaddr())} Madz", font=("Arial",25,"bold"))
        self.cur_tx = CTkLabel(self.tabview.tab("Dashboard"), text=f"Transactions sent/recieved: {self.webdata()['txcount']}", font=("Arial",25))
        self.cur_bal.pack(side=TOP, anchor="w")
        self.cur_tx.pack(side=TOP, anchor="w")

    def refresh_netstats(self):
        self.title.destroy()
        self.height.destroy()
        self.transcount.destory()

        url = self.cfg["url"]
        stats = requests.get(url+"/stats").json()["result"]

        self.title = CTkLabel(self.tabview.tab("Network stats"), text="Network Statistics", font=("Arial",30)).pack(side=TOP, anchor="n")
        self.height = CTkLabel(self.tabview.tab("Network stats"), text=f"Block Height: {stats['chain']['length']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.transcount = CTkLabel(self.tabview.tab("Network stats"), text=f"Network Tx count: {stats['coin']['transactions']}" , font=("Arial",20)).pack(side=TOP, anchor="w")
        self.supply = CTkLabel(self.tabview.tab("Network stats"), text=f"Circulating Supply: {stats['coin']['supply']} MADZ", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.blocktime = CTkLabel(self.tabview.tab("Network stats"), text=f"Last Block Time: {stats['chain']['LastBlockTime']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.blockreward = CTkLabel(self.tabview.tab("Network stats"), text=f"Block Reward: {stats['chain']['blockReward']} MADZ", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.owner = CTkLabel(self.tabview.tab("Network stats"), text=f"Owner: {stats['node']['owner']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.version = CTkLabel(self.tabview.tab("Network stats"), text=f"Network Version: V{stats['node']['version']}", font=("Arial",20)).pack(side=TOP, anchor="w")
        self.smalltext = CTkLabel(self.tabview.tab("Network stats"), text=f"Results taken from {url} aka your node.", font=("Arial", 10)).pack(side=TOP, anchor="w")

    def runGui(self):
        self.app.mainloop()

def runapp():
    rgbPrint(f"Starting GUI V{VER}", "green")
    app = App()
    app.runGui()
