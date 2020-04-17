import tkinter
import re
import configparser
import requests
import webbrowser
import subprocess
import socket
import getpass
import distro
import psutil
import platform
import keyboard

from bs4 import BeautifulSoup


def command_info():
    if lang == 'en':
        text = 'Command list:\n\n• Open & close browser\n'
        text += '/youtube\n/facebook\n/twitter\n/github\n/reddit\n/url <link>\n/close (for close any app like browsers)\n\n'
        text += 'note: For youtube you can command like this:\n'
        text += '/youtube <search query>\nexample: /youtube ed sheeran - perfect\n/ytfull (for full screen)\n/ytnext (for next videos)\n\n'
        text += '• PC Settings\n/status\n/restart\n/shutdown'
    elif lang == 'ru':
        text = 'Список комманд:\n\n• Браузерные:\n'
        text += '/vk\n/twitter\n/github\n/reddit\n/url <ссылка>\n/close (приложение)\n\n'
        text += '• Команды для ютуба:\n'
        text += '/youtube(просто открыть youtube)\n/youtube <поисковый запрос>\n/ytfull (открыть на весь экран)\n/ytnext (следующее видео)\n\n'
        text += '• Другие\n/status\n/restart\n/shutdown'
    else:
        text = 'Ay, ay Kapten!\nBerikut perintah yang bisa dilakukan:\n\n'
        text += '• Buka & tutup browser\n'
        text += '/youtube\n/facebook\n/twitter\n/github\n/reddit\n/url <link>\n/close (utk menutup app seperti browser)\n\n'
        text += 'note: Untuk youtube kamu bisa perintahkan seperti ini:\n'
        text += '/youtube <judul video>\ncontoh: /youtube ed sheeran - perfect\n/ytfull (utk fullscreen)\n/ytnext (utk video berikutnya)\n\n'
        text += '• Pengaturan PC\n/status\n/restart\n/shutdown'
    return text


def search_youtube(query):
    url = 'http://www.youtube.com/results?search_query=' + query
    req = requests.get(url).text
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', req)
    linkvideo = "http://www.youtube.com/watch?v="+search_results[0]
    return linkvideo


def shutdown(update):
    global lang, url1
    if lang == 'en':
        replied = 'Shutted down'
    elif lang == 'ru':
        replied = 'Выключаюсь'
    else:
        replied = 'PC Berhasil Dimatikan.'
    if platform.system() == "Windows":
        subprocess.call('shutdown /s')
    else:
        subprocess.call('shutdown -h now')
    requests.get(url1+'sendMessage',
                 params=dict(chat_id=update['message']['chat']['id'], text=replied))


def restart(update):
    global lang, url1
    if lang == 'en':
        replied = 'Rebooted'
    elif lang == 'ru':
        replied = 'Перезагружаюсь'
    else:
        replied = 'PC Berhasil Direstart.'
    if platform.system() == "Windows":
        subprocess.call('shutdown /r')
    else:
        subprocess.call('reboot')
    requests.get(url1+'sendMessage',
                 params=dict(chat_id=update['message']['chat']['id'], text=replied))


def status(update):
    global lang, url1
    if lang == 'en':
        text = ""
        text += ("PC name: ") + socket.gethostname()
        text += ("\nLogged user: ") + getpass.getuser()
        if platform.system() == "Windows":
            text += ("\nOS: Windows ") + platform.win32_ver()[0]
        else:
            text += ("\nOS: ") + " ".join(distro.linux_distribution()[:2])
        text += ("\nCPU: ") + str(psutil.cpu_percent()) + "%"
        text += ("\nMemory: ") + str(
            int(psutil.virtual_memory().percent)) + "%"
        if psutil.sensors_battery():
            if psutil.sensors_battery().power_plugged is True:
                text += ("\nBattery: ") + str(
                    format(psutil.sensors_battery().percent, ".0f")) \
                    + ("% | Charging")
            else:
                text += ("\nBattery: ") + str(
                    format(psutil.sensors_battery().percent, ".0f")) + "%"
    elif lang == 'ru':
        text = ""
        text += "Имя компа: " + socket.gethostname()
        text += "\nПользователь: " + getpass.getuser()
        if platform.system() == "Windows":
            text += "\nOS: Windows " + platform.win32_ver()[0]
        else:
            text += "\nOS: " + " ".join(distro.linux_distribution()[:2])
        text += "\nCPU: " + str(psutil.cpu_percent()) + "%"
        text += "\nОЗУ: " + str(
            int(psutil.virtual_memory().percent)) + "%"
        if psutil.sensors_battery():
            if psutil.sensors_battery().power_plugged is True:
                text += "\nЗаряд: " + str(
                    format(psutil.sensors_battery().percent, ".0f")) \
                        + "% | Заряжается"
            else:
                text += "\nБатарея: " + str(
                    format(psutil.sensors_battery().percent, ".0f")) + "%"
    else:
        text = ""
        text += ("Nama PC: ") + socket.gethostname()
        text += ("\nNama pengguna: ") + getpass.getuser()
        if platform.system() == "Windows":
            text += ("\nSistem operasi: Windows ") + platform.win32_ver()[0]
        else:
            text += ("\nSistem operasi: ") + \
                " ".join(distro.linux_distribution()[:2])
        text += ("\nCPU: ") + str(psutil.cpu_percent()) + "%"
        text += ("\nMemory: ") + str(
            int(psutil.virtual_memory().percent)) + "%"
        if psutil.sensors_battery():
            if psutil.sensors_battery().power_plugged is True:
                text += ("\nBaterai: ") + str(
                    format(psutil.sensors_battery().percent, ".0f")) \
                    + ("% | Charging")
            else:
                text += ("\nBaterai: ") + str(
                    format(psutil.sensors_battery().percent, ".0f")) + "%"
    requests.get(url1+'sendMessage',
                 params=dict(chat_id=update['message']['chat']['id'], text=text))


def main():
    global url1, url, last_update, token, lang, owner
    req = requests.get(url).json()
    if lang == 'en':
        sukses = 'Success!'
    elif lang == 'ru':
        sukses = 'Успех'
    else:
        sukses = 'Sukses bos!'
    for update in req['result']:
        if last_update < update['update_id']:
            last_update = update['update_id']
            if update['message']['from']['username'] == owner:
                if update['message']['text'].startswith('/youtube'):
                    message = update['message']['text'].split()
                    if len(message) > 1:
                        query = ''
                        lst = message[1:]
                        for x in lst:
                            query += x+' '
                        webbrowser.open(search_youtube(query))
                        requests.get(
                            url1+'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=sukses))
                    else:
                        webbrowser.open('https://youtube.com')
                elif update['message']['text'].startswith('/close'):
                    keyboard.send('alt+f4')
                elif update['message']['text'].startswith('/ytfull'):
                    keyboard.send('f')
                elif update['message']['text'].startswith('/ytnext'):
                    keyboard.send('shift+n')
                elif update['message']['text'].startswith('/url'):
                    splited = update['message']['text'].split()
                    if len(splited) > 1:
                        link = splited[1]
                        webbrowser.open(link)
                        requests.get(
                            url1+'sendMessage', params=dict(chat_id=update['message']['chat']['id'], text=sukses))
                    else:
                        if lang == 'en':
                            requests.get(url1+'sendMessage', params=dict(
                                chat_id=update['message']['chat']['id'], text='Command /url need <link>\nexample: /url https://stackoverflow.com/'))
                        else:
                            requests.get(url1+'sendMessage', params=dict(
                                chat_id=update['message']['chat']['id'], text='Perintah /url memerlukan link\ncontoh: /url https://stackoverflow.com/'))
                elif update['message']['text'].startswith('/vk'):
                    webbrowser.open('https://vk.com')
                elif update['message']['text'].startswith('/twitter'):
                    webbrowser.open('https://twitter.com')
                elif update['message']['text'].startswith('/facebook'):
                    webbrowser.open('https://facebook.com')
                elif update['message']['text'].startswith('/reddit'):
                    webbrowser.open('https://reddit.com')
                elif update['message']['text'].startswith('/github'):
                    webbrowser.open('https://github.com')
                elif update['message']['text'].startswith('/shutdown'):
                    shutdown(update)
                elif update['message']['text'].startswith('/status'):
                    status(update)
                elif update['message']['text'].startswith('/restart'):
                    restart(update)
                elif update['message']['text'] == 'hi' or 'halo' or 'Halo' or 'Hi' or '/start':
                    requests.get(url1+'sendMessage', params=dict(
                        chat_id=update['message']['chat']['id'], text=command_info()))
                else:
                    pass

    root.after(2, main)


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
token = config['SETTINGS']['tele_token']
lang = config['SETTINGS']['language']
owner = config['SETTINGS']['owner_username']
last_update = 0
root = tkinter.Tk()
root.title("Running")
root.geometry("500x100")
if lang == 'en':
    teks = """
    Bot is Running
    You can type "/start" or "hi" to the Bot to get your command list

    note: Don't close this window if you want to use your bot!
    """
elif lang == 'ru':
    teks = """
    Бот запущен!
    Вы можете написать "/start" или "hi" боту чтобы получить список комманд.
    Пожалуйста, не закрывайте это окно чтобы бот работал.
    """
else:
    teks = """
    Bot telah Berjalan
    Kamu bisa chat "/start" atau "halo" ke Bot untuk mengetahui perintah yang bisa digunakan

    note: Jangan tutup window ini jika ingin memakai Bot!
    """
label = tkinter.Label(root, text=teks)
label.pack()
url1 = 'https://api.telegram.org/bot'+token+'/'
url = url1+'getUpdates'
reqlast = requests.get(url).json()
try:
    last_update = reqlast['result'][-1]['update_id']
except:
    pass
root.after(2, main)
root.mainloop()
