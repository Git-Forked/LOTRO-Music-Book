LOTRO Music Book

A LOTRO (Lord of The Rings Online) side-plugin written in Python 3.12.5


Description:

LOTRO Music Book assists players in organizing and playing over 20,000 available .abc music files with the in-game instruments.


Features Include:

    • Change into and out of music mode quickly, with the [ Music Mode ] button.
    • Play the currently selected song in the game, with the [ Play Song ] button.
    • Add to a favorites list with the [ + Favorite ] button, when you find songs you like.
        Remove them with the [ - Favorites button ], if you change your mind.
    • Quick search your files, for that one you are looking for.
    • Fancy tooltips to explain each button, and advanced tooltips when hovering over the [ Play Song ] or [ + Favorites] buttons,
        to show detailed information about the selected ABC song file.
    • Can display and link ABC files multiple folders deep, so you can keep them better organized.


LOTRO Music Book should work on all systems that can run python and the required import modules, including on the following operating systems: Linux, MacOs, Windows.


Required modules:
    import pyautogui, os, glob
    from time import sleep
    from subprocess import run
    from tkinter import *
    from tkinter import ttk
    from tktooltip import ToolTip
    import pyclip


Suggested Usage:

Log into the LOTRO game, equip your character with the instrument you want to play.
Launch LOTRO Music Book, and click the [ Music Mode ] button to put your character into music playing mode.
Choose a song from your collection which will appear in the list box.
Press the [ Play Song ] button to have your character play the song in the game on your instrument.


Installation:

Unzip or 'Extact All' of the LOTRO Music Book*.zip to the desired location.


Available from:

https://github.com/Git-Forked/LOTRO-Music-Book        <--(LATEST UPDATES)
https://www.lotrointerface.com/downloads/infoXXXX-LOTRO Music Book.html

