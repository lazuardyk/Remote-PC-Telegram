import tkinter
from tkinter import filedialog
import subprocess
import configparser
import platform
import sys

def run_bot(root):
    root.destroy()
    subprocess.call("python main.py")

def create_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'Tele_Token':token.get(),
                          'Owner_Username':owner.get(),
                          'Language':lang.get()}
    with open('config.ini','w') as configfile:
        config.write(configfile)

def install_req():
    if platform.system() == "Windows":
        subprocess.call(
            "pip install -r requirements.txt")
    else:
        if sys.version_info[0] < 3:
            subprocess.call(
                "pip install -r requirements.txt")
        else:
            subprocess.call(
                "pip3 install -r requirements.txt")

def submit():
    success = tkinter.Label(root, text="Your setting has been saved!")
    create_config()
    success.pack()

root = tkinter.Tk()
root.title("Bot Configuration")
root.geometry("370x370")
label = tkinter.Label(root, text="\n\nControl your PC with Telegram Bot\nPlease complete all fields below!\n\nTelegram Bot Token:")
token = tkinter.Entry(root, width=50)
labol = tkinter.Label(root, text="Owner's username (to prevent other users to use it) without @:")
owner = tkinter.Entry(root)
labul = tkinter.Label(root, text="Type your language (en/id):")
lang = tkinter.Entry(root)
tombolsubmit = tkinter.Button(root, text="Submit your Input", command=submit)
label3 = tkinter.Label(root, text="")
tombolreq = tkinter.Button(root, text="Install requirements files", command=install_req)
tombolrun = tkinter.Button(root, text="Run your Bot!", command= lambda: run_bot(root))
label4 = tkinter.Label(root, text="\n\nMade with ♥ by Lazuardy Khatulistiwa")

label.pack()
token.pack()
labol.pack()
owner.pack()
labul.pack()
lang.pack()
tombolsubmit.pack()
label3.pack()
tombolreq.pack()
tombolrun.pack()
label4.pack()
root.mainloop()
