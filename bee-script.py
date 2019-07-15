from pynput.keyboard import Key, Controller
import pyperclip
import time

if __name__ == '__main__':
    text_file = open("bee.txt", "r")
    lines = text_file.read().split('\n')

    keyboard = Controller()

    print('Starting in 5 seconds...')
    time.sleep(5)

    buffer_count = 0
    buf = ""
    for line in lines:
        curr_total = len(buf)
        curr_line = len(line)

        if curr_total + curr_line < 2000:
            buf += line + '\n'
        else:
            pyperclip.copy(buf)
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(1)
            buf = ""
            buffer_count += 1

    print(buffer_count)
