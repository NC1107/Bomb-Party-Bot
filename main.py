from pynput.keyboard import Listener
from re import search
import pyautogui
import os


def clearConsole():
    print('\n' * 75)


def clearTextBox():
    pyautogui.press("backspace", presses=10)
    # clear game textbos


def find_word(_Game):
    print(f"Searching for words in {_Game.textFileName} containing {_Game.currentString}")
    words = open(_Game.textFileName).read().split()
    FOUND = False
    for w in words:
        if w not in _Game.usedWords:
            if search(_Game.currentString, w):
                if not FOUND:
                    _Game.usedWords.append(w)
                    FOUND = True
                    clearTextBox()
                    pyautogui.typewrite(w, interval=.02)
                    pyautogui.press('enter')

    print("-----------DONE-----------")


class CurrentGame:
    def __init__(self):
        self.currentString = ""
        self.usedWords = []
        self.textFileName = "English_Words.txt"

    def addToString(self, letter: str):
        if letter.isalpha():
            self.currentString += letter

    def addToList(self, word: str):
        if word not in self.usedWords:
            self.usedWords.append(word)

    def getList(self):
        return self.usedWords

    def getCurrentString(self):
        return self.currentString

    def clearString(self):
        self.currentString = ""

    def clearList(self):
        self.usedWords = []
    # Create method to clearing box after, searching,clearing,restarting


def on_press(event, _Game):
    SEARCHED = False
    key = str(event).replace("'", "")
    if key == "Key.backspace" and _Game.currentString:
        _Game.currentString = _Game.currentString[:-1]
    if key == "-":
        pyautogui.press('backspace')
        _Game.currentString = ""
        print("Clear String")
    elif key == "=":
        SEARCHED = True
        pyautogui.press('backspace')
        find_word(_Game)

        _Game.currentString = ""
    elif not SEARCHED:
        if not key.startswith("Key."):
            if not key.startswith('\\'):
                if key not in ["-", "=", "Key.backspace"]:
                    if key.isalpha():
                        _Game.addToString(key)
    if SEARCHED:
        _Game.currentString = ""
    clearConsole()
    print(f"Current String: {_Game.currentString}")


if __name__ == '__main__':
    print(
        "Type in the letters given in the center and then click '+', after clicking '+' a word will be found and "
        "printed into the textbox you are currently using")
    print(
        "CONTROLS:\n + : searches for given phrase (ex: 'en', 'ir', etc)\n - : clears the stored phrases, "
        "do this after each search ")
    Game = CurrentGame()
    with Listener(on_press=lambda event: on_press(event, _Game=Game)) as listener:
        listener.join()
