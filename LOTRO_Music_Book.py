############################
#     LOTRO Music Book     #
############################

# version 0.0.18

##################################################
# Required Configuration

# Set the path to your LOTRO Music folder here:
path = '/home/<user>/.local/share/Steam/steamapps/compatdata/212500/pfx/drive_c/users/steamuser/Documents/The Lord of the Rings Online/Music'

# Settings
dual_monitors = False
screen_width = 1920
screen_height = 1080
book_width = round(screen_width/3)
book_height = round(screen_height)

##################################################

import pyautogui, os, glob
from time import sleep
from subprocess import run
from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip
import pyclip


def removeprefix(self: str, prefix: str, /) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

# Collection
files = []
def list_files_glob(pattern=path+'/**/*.abc', recursive=True):
    all_files = glob.glob(pattern, recursive=recursive)
    for this_file in all_files:
        this_file = removeprefix(this_file, path+'/')
        files.append(this_file)
list_files_glob()
files.sort()

# Favorites
favorites = []
favorites_file = path + '/Favorites.txt'
if os.path.isfile(favorites_file):
    with open(favorites_file, 'r') as f:
        favorites = f.read().splitlines()

# Populate Listbox
def populate_listbox():
    files_listbox.delete(0,END)
    files_listbox.insert(0, *files)
    files_listbox.insert(0, '♫ Collection ♫')
    files_listbox.insert(0, *favorites)
    files_listbox.insert(0, '❤ Favorites ❤')

def populate_listbox_search_results():
    files_listbox.delete(0,END)
    files_listbox.insert(0, *files_searched)
    files_listbox.insert(0, '🔎 Search Results 🔍')

# Add to Favorites
def add_to_favorites():
    for selected in files_listbox.curselection():
        song = files_listbox.get(selected)
        if song not in favorites:
            add_favorite_button.flash()
            favorites.append(song)
            favorites.sort()
            if searching == False:
                populate_listbox()
                files_listbox.selection_set(selected+1) # Select last selected
                files_listbox.see(selected+1) # jump to last selected
            with open(favorites_file, 'a') as f:
                f.write(song + '\n')

# Remove from Favorites
def remove_from_favorites():
    remove_favorite_button.flash()
    for selected in files_listbox.curselection():
        song = files_listbox.get(selected)
        favorites.remove(song)
        favorites.sort()
        populate_listbox()
        files_listbox.selection_set(selected-1) # Select last selected
        files_listbox.see(selected-1) # jump to last selected
        with open(favorites_file, 'w') as f:
            for song in favorites:
                f.write(song + '\n')

# Search
files_searched = []
searching = False
def search():
    search_button.flash()
    files_searched.clear()
    search_terms = search_input.get()
    for song in files:
        if search_terms.lower() in song.lower():
            files_searched.append(song)
            files_searched.sort()
    populate_listbox_search_results()
    global searching
    searching = True
    tooltip_cleanup()

def clear_search():
    clear_button.flash()
    search_input.delete(0, END)
    files_searched.clear()
    populate_listbox()
    global searching
    searching = False
    tooltip_cleanup()

# Music Mode
def music_mode():
    music_mode_button.flash()
    run(['xdotool', 'search', '--name', 'The Lord of the Rings Online', 'windowactivate'])
    sleep(0.25)
    pyclip.copy('/music')
    pyautogui.press('enter')
    sleep(0.25)
    pyautogui.hotkey('ctrl', 'v', interval=0.150)
    sleep(0.25)
    pyautogui.press('enter')

# Play Song
def play_song():
    play_song_button.flash()
    for selected in files_listbox.curselection():
        song = files_listbox.get(selected)
        run(['xdotool', 'search', '--name', 'The Lord of the Rings Online', 'windowactivate'])
        sleep(0.25)
        pyclip.copy('/play "' + song + '"')
        pyautogui.press('enter')
        sleep(0.25)
        pyautogui.hotkey('ctrl', 'v', interval=0.150)
        sleep(0.25)
        pyautogui.press('enter')

# Tooltips
def on_select(event):
    selection = event.widget.curselection()
    if selection:
        play_song_button.flash()
        index = selection[0]
        song = event.widget.get(index)
        information = ''
        with open(path + '/' + song, 'r') as f:
            for line in f:
                if 'T:' in line:
                    title  = 'title: ' + line.split('T:')[1].strip()
                    information += title
                if 'C:' in line:
                    composer = 'composer: ' + line.split('C:')[1].strip()
                    information += '\n' + composer
                if 'Z:' in line:
                    z = 'id: ' + line.split('Z:')[1].strip()
                    information += '\n' + z
            global play_song_button_tooltip
            global add_favorite_button_tooltip
            if information != '':
                play_song_button_tooltip.destroy()
                add_favorite_button_tooltip.destroy()
                play_song_button_tooltip = ToolTip(play_song_button, information, delay=0, follow=True, x_offset=(-(100+round(len(information)))), y_offset=(-(100+round(len(information)/20))), parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_favorite_button_tooltip = ToolTip(add_favorite_button, information, delay=0, follow=True, x_offset=(-(100+round(len(information)))), y_offset=(-(100+round(len(information)/20))), parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                # These tooltips need to be: x_offset=-100, y_offset=-100
            else:
                play_song_button_tooltip.destroy()
                add_favorite_button_tooltip.destroy()
                play_song_button_tooltip = ToolTip(play_song_button, 'Error reading song file information.', delay=0, follow=True, x_offset=-50, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_favorite_button_tooltip = ToolTip(add_favorite_button, 'Error reading song file information.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                # These tooltips need to be: x_offset=-100, y_offset=-100

# Tooltip cleanup
def tooltip_cleanup():
    global play_song_button_tooltip
    global add_favorite_button_tooltip
    play_song_button_tooltip.destroy()
    add_favorite_button_tooltip.destroy()
    play_song_button_tooltip = ToolTip(play_song_button, 'Play the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
    add_favorite_button_tooltip = ToolTip(add_favorite_button, 'Add a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")

# Tkinter GUI
book = Tk()
book.title('LOTRO Music Book')
book.attributes('-topmost',True)

# Where the GUI will be placed on screen.
if dual_monitors == True:
    screen_position = screen_width+1
else:
    screen_position = screen_width - book_width
book.geometry(str(book_width) + 'x' + str(book_height) + '+' + str(screen_position) + '+0')

# Create Frames
search_frame=Frame(book)
search_frame.pack()

listbox_frame=Frame(book)
listbox_frame.pack(fill='both', expand=True)
listbox_frame.columnconfigure(0, weight=1)
listbox_frame.rowconfigure(0,weight=1)
listbox_frame.rowconfigure(1, weight=1)

buttons_frame=Frame(book)
buttons_frame.pack()

# Create Searchbox and its features
search_input = Entry(search_frame, width=33)
search_input.grid(row=0, column=0, sticky='we', padx=1, pady=1)
search_input.focus_set()
search_input.bind('<Return>', lambda event=None: search_button.invoke())

search_button = Button(search_frame, text='🔎', width=3, activebackground='gray', command=search)
search_button_tooltip = ToolTip(search_button, 'Search your collection.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
search_button.grid(row=0, column=1, sticky='we', pady=1)

clear_button = Button(search_frame, text='❌', width=3, activebackground='gray', command=clear_search)
clear_button_tooltip = ToolTip(clear_button, 'Clear your search results.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
clear_button.grid(row=0, column=2, sticky='we', pady=1)

# Create Listbox
files_listbox = Listbox(listbox_frame, selectmode='single')
#files_listbox = Listbox(listbox_frame, name='files_listbox')
files_listbox.bind('<<ListboxSelect>>', on_select)
files_listbox.pack(fill='both', expand=True)
populate_listbox()

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(files_listbox, orient='vertical')
scrollbar.pack(side='right', fill='both')
files_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=files_listbox.yview)

# Create Buttons
play_song_button = Button(buttons_frame, text='Play Song', bg='green', fg='white', activebackground='red', activeforeground='white', command=play_song)
play_song_button_tooltip = ToolTip(play_song_button, 'Play the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
play_song_button.grid(row=0, column=0, sticky='ew')
music_mode_button = Button(buttons_frame, text='Music Mode', bg='blue', fg='white', activebackground='red', activeforeground='white', command=music_mode)
music_mode_button_tooltip = ToolTip(music_mode_button, 'Music mode [on] or [off] toggle.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
music_mode_button.grid(row=0, column=1, sticky='ew')
add_favorite_button = Button(buttons_frame, text='+ Favorite', bg='purple', fg='white', activebackground='red', activeforeground='white', command=add_to_favorites)
add_favorite_button_tooltip = ToolTip(add_favorite_button, 'Add a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
add_favorite_button.grid(row=1, column=0, sticky='ew')
remove_favorite_button = Button(buttons_frame, text='- Favorite', bg='pink', fg='white', activebackground='red', activeforeground='white', command=remove_from_favorites)
remove_favorite_button_tooltip = ToolTip(remove_favorite_button,'Remove a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
remove_favorite_button.grid(row=1, column=1, sticky='ew')

# Start main loop for GUI to display
book.mainloop()
