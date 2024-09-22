LOTRO Music Book

A LOTRO (Lord of The Rings Online) side-plugin written in Python 3.12.5


Description:

LOTRO Music Book assists players in organizing and playing over 20,000 available .abc music files with the in-game instruments.


Previous Features Include:

    • Change into and out of music mode quickly, with the [ Music Mode ] button.
    • Play the currently selected song in the game, with the [ Play Song ] button.
    • Add to a favorites list with the [ + Favorite ] button, when you find songs you like.
        Remove them with the [ - Favorites button ], if you change your mind.
    • Quick search your files, for that one you are looking for.
    • Fancy tooltips to explain each button, and advanced tooltips when hovering over the [ Play Song ] 
        or [ + Favorites] buttons, to show detailed information about the selected ABC song file.
    • Can display and link ABC files multiple folders deep, so you can keep them better organized.
    • Buttons blink for confirmation, and do not blink on rejection of action.


New Features Include:

    • A new theme.
    • Queue list to add and remove songs from.
    • Two new buttons: [ + Queue ] and [ - Queue ]
    • New [ Play Queued ] button to play the top song in your queue.
    • [ Play Queued ] button grows darker orange as queue fills up.
        The color indicates when you will need to add more songs,
        and turns yellow when empty.
    • Hovering the mouse over the [ Play Queued ] button displays the queue in a tooltip.
    • Songs are automatically removed from queue upon play.


LOTRO Music Book was made for Linux, but should work on any system that can run python and the required imported modules.


Required modules:
    import pyautogui
    import pyclip
    import os
    import glob
    from time import sleep
    from subprocess import run
    from tkinter import *
    from tkinter import ttk
    from tktooltip import ToolTip


LOTRO Music Book preview image: 
https://raw.githubusercontent.com/Git-Forked/LOTRO-Music-Book/refs/heads/main/LOTRO_Music_Book_v0.0.21_%5B1%5D.png
https://raw.githubusercontent.com/Git-Forked/LOTRO-Music-Book/refs/heads/main/LOTRO_Music_Book_v0.0.21_%5B2%5D.png


Suggested Usage:

Log into the LOTRO game, equip your character with the instrument you want to play.
Launch LOTRO Music Book, and click the [ Music Mode ] button to put your character into music playing mode.
Choose a song from your collection which will appear in the list box.
Press the [ Play Song ] button to have your character play the song in the game on your instrument.


Installation:

Unzip or 'Extact All' of the LOTRO-Music-Book*.zip to the desired location.

See LOTRO_Music_Book.py for additional settings and configuration.


LOTRO Music Book is available from:

https://github.com/Git-Forked/LOTRO-Music-Book        <--(LATEST UPDATES)
https://www.lotrointerface.com/downloads/info1244-LOTROMusicBook.html


Music Files:

LOTRO Music Book does not come with, nor provide, any ABC music files. 
Files can be obtained from other sources such as: 

The Fat Lute and Other .ABC Music Archive : https://www.lotrointerface.com/downloads/info1087-TheFatLuteandOther.ABCMusicArchive.html
Zolton's Music Mega Pack : https://www.lotrointerface.com/downloads/info604-ZoltonsMusicMegaPack.html
Music Band abc's : https://www.lotrointerface.com/downloads/info180-MusicBandabcs.html
Raymiond's ABC Collection : https://bardsofafeather.net/library.php
