from pynput.keyboard import Key, Controller
from bs4 import BeautifulSoup
import pyperclip
import requests
import time

if __name__ == '__main__':
    song = 'https://www.elyrics.net/read/c/contours-lyrics/do-you-love-me-lyrics.html'
    lyrics = BeautifulSoup(requests.get(song).content, "html.parser").find('div', {'id': 'inlyr'}).text.split('\n')

    keyboard = Controller()

    print('Starting in 5 seconds...')
    time.sleep(5)

    for line in lyrics:
        if len(line) > 5:
            pyperclip.copy('@everyone ' + line)
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(1)
