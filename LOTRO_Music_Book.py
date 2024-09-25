############################
#     LOTRO Music Book     #
############################

# programmed by: Git-Forked

##################################################
# Required Configuration

# Set the path to your LOTRO Music folder here:
path = '/home/<user>/.local/share/Steam/steamapps/compatdata/212500/pfx/drive_c/users/steamuser/Documents/The Lord of the Rings Online/Music'

# Settings
share_to_game = True
dual_monitors = False
screen_width = 1920
screen_height = 1080
book_width = round(screen_width/3)
book_height = round(screen_height-80)

##################################################

import pyautogui
import pyclip
import os
import glob
from time import sleep
from subprocess import run
from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip

version = '0.0.30'

title_and_version = 'LOTRO Music Book - made with love ❤ by Git-Forked - v'+version

titles = ['♫ Collection ♫', '❤ Favorites ❤', '♪ Queue ♪', '⌘ Played ⌘', '🔎 Search Results 🔍', '']

print(title_and_version)

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

# Get song from one of the listboxes
def get_song_from_listbox():
    global selected_listbox
    song = ''
    if selected_listbox == 'files_listbox':
        for selected in files_listbox.curselection():
            song = files_listbox.get(selected)

    if selected_listbox == 'queue_listbox':
        for selected in queue_listbox.curselection():
            song = queue_listbox.get(selected)

    if selected_listbox == 'played_listbox':
        for selected in played_listbox.curselection():
            song = played_listbox.get(selected)
    return song

# Add to Favorites
def add_to_favorites():
    save_selected()
    song = get_song_from_listbox()
    if song not in favorites and song not in titles:
        add_favorite_button.flash()
        favorites.append(song)
        print('Song added to favorites: \t'+song)
        favorites.sort()
        if searching == False:
            populate_listbox()
            restore_selected(+1)
        with open(favorites_file, 'a') as f:
            f.write(song + '\n')

# Remove from Favorites
def remove_from_favorites():
    save_selected()
    song = get_song_from_listbox()
    favorites.remove(song)
    print('Song removed from: \t\t'+song)
    remove_favorite_button.flash()
    favorites.sort()
    if searching == False:
        populate_listbox()
        restore_selected(-1)
    with open(favorites_file, 'w') as f:
        for song in favorites:
            f.write(song + '\n')

# Add to Queue
queue = []
def add_to_queue():
    save_selected()
    song = get_song_from_listbox()
    if song not in queue and song not in titles:
        add_queue_button.flash()
        queue.append(song)
        print('Song added to queue: \t\t'+song)
        #if searching == False:
        #    populate_listbox()
        #    restore_selected()
        populate_queue()
        check_queue()
    restore_selected()

# Remove from Queue
def remove_from_queue():
    save_selected()
    song = get_song_from_listbox()
    if song in queue:
        remove_queue_button.flash()
        queue.remove(song)
        print('Song removed from queue: \t\t'+song)
        #if searching == False:
        #    populate_listbox()
        #    restore_selected()
        populate_queue()
    check_queue()

# Clear Queue
def clear_queue():
    save_selected()
    queue.clear()
    if searching == False:
        populate_listbox()
        restore_selected()
    clear_queue_button.flash()
    populate_queue()
    check_queue()

# Set Play Queue button color to length of queue
def check_queue():
    global play_queue_button_tooltip
    # Play Queue button will turn darker orange as queue fills up.
    if len(queue) == 0: play_queue_button.config(bg='yellow')
    if len(queue) == 1: play_queue_button.config(bg='orange')
    if len(queue) == 2: play_queue_button.config(bg='dark orange')
    if len(queue) == 3: play_queue_button.config(bg='DarkOrange1')
    if len(queue) == 4: play_queue_button.config(bg='DarkOrange2')
    if len(queue) == 5: play_queue_button.config(bg='DarkOrange3')
    if len(queue) >  5: play_queue_button.config(bg='DarkOrange4')

    # Play Queue button tooltip will be updated to show songs in queue.
    if len(queue) > 0:
        queue_string = ''
        for song in queue:
            queue_string += '\n' + song.split('/')[1].split('.abc')[0]
        tooltip_information = 'Play the top song in your queue:\n'+str(queue_string)
        additional_offset = len(queue)*40
        #offset_x = (-(100+round(len(tooltip_information))))
        offset_x = -book_width
        offset_y = (-(100+additional_offset+round(len(tooltip_information)/20)))
        play_queue_button_tooltip.destroy()
        play_queue_button_tooltip = ToolTip(play_queue_button, tooltip_information, delay=0, follow=True, x_offset=offset_x, y_offset=offset_y, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        # This tooltip need to be: x_offset=-100, y_offset=-100
    else:
        play_queue_button_tooltip.destroy()
        play_queue_button_tooltip = ToolTip(play_queue_button, 'Play the top song in your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")

# Populate Listbox
def populate_listbox():
    files_listbox.delete(0,END)
    files_listbox.insert(0, *files)
    files_listbox.insert(0, '♫ Collection ♫')
    files_listbox.insert(0, *favorites)
    files_listbox.insert(0, '❤ Favorites ❤')
    #files_listbox.insert(0, *queue)
    #files_listbox.insert(0, '♪ Queue ♪')

def populate_listbox_search_results():
    files_listbox.delete(0,END)
    files_listbox.insert(0, *files_searched)
    files_listbox.insert(0, '🔎 Search Results 🔍')

# Retain previously selected song
previously_selected = 0

def save_selected():
    global previously_selected
    for selected in files_listbox.curselection():
        previously_selected = selected
        break

def restore_selected(modifier=0):
    global previously_selected
    files_listbox.selection_set(previously_selected+modifier) # Select last selected
    files_listbox.see(previously_selected+modifier) # jump to last selected

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
    file_count_label.configure(text=count())

def clear_search():
    clear_button.flash()
    search_input.delete(0, END)
    files_searched.clear()
    populate_listbox()
    restore_selected()
    global searching
    searching = False
    tooltip_cleanup()
    file_count_label.configure(text=count())

def paste_to_game():
    if share_to_game == True:
        run(['xdotool', 'search', '--name', 'The Lord of the Rings Online', 'windowactivate'])
        sleep(0.25)
        pyautogui.press('enter')
        sleep(0.25)
        pyautogui.hotkey('ctrl', 'v', interval=0.150)
        sleep(0.25)
        pyautogui.press('enter')
        sleep(0.25)
        #book.lift()

# Music Mode
def music_mode():
    music_mode_button.flash()
    pyclip.copy('/music')
    paste_to_game()

# Play Song
def play_song():
    save_selected()
    song = get_song_from_listbox()
    if song not in titles:
        play_song_button.flash()
        if song in queue:
            queue.remove(song)
        #if searching == False:
        #    populate_listbox()
        #    restore_selected()
        if sync.get() == 1:
            pyclip.copy('/play "' + song + '" sync')
        else:
            pyclip.copy('/play "' + song + '"')
        paste_to_game()
        played(song)
    populate_queue()
    check_queue()
    restore_selected()

# Play Queue
def play_queue():
    save_selected()
    song = queue[0]
    if song in queue:
        queue.remove(song)
        play_queue_button.flash()
        #if searching == False:
        #    populate_listbox()
        #    restore_selected()
        if sync.get() == 1:
            pyclip.copy('/play "' + song + '" sync')
        else:
            pyclip.copy('/play "' + song + '"')
        paste_to_game()
        played(song)
        populate_queue()
        check_queue()
    restore_selected()

# Start Sync
def play_start_sync():
    pyclip.copy('/playstart')
    paste_to_game()
    played(song)
    populate_queue()
    check_queue()
    play_start_sync_button.flash()

def sync_state():
    global sync
    global play_start_sync_button
    global play_start_sync_button_tooltip
    global play_song_button
    global play_song_button_tooltip
    global play_queue_button
    global play_queue_button_tooltip
    if sync.get() == 1:
        play_start_sync_button.configure(state=NORMAL, bg='green2')
        play_song_button.configure(text='Sync Song')
        play_song_button_tooltip.destroy()
        play_song_button_tooltip = ToolTip(play_song_button, 'Synchronize the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_start_sync_button_tooltip.destroy()
        play_start_sync_button_tooltip = ToolTip(play_start_sync_button, 'Start playing the synchronized music.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_queue_button.configure(text='Sync Queued')
        play_queue_button_tooltip.destroy()
        play_queue_button_tooltip = ToolTip(play_queue_button, 'Synchronize the top song in your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_song_button.flash()
    else:
        play_start_sync_button.configure(state=DISABLED, bg='gray')
        play_song_button.configure(text='Play Song')
        play_song_button_tooltip.destroy()
        play_song_button_tooltip = ToolTip(play_song_button, 'Play the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_start_sync_button_tooltip.destroy()
        play_start_sync_button_tooltip = ToolTip(play_start_sync_button, 'Sync is disabled.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_queue_button.configure(text='Play Queued')
        play_queue_button_tooltip.destroy()
        play_queue_button_tooltip = ToolTip(play_queue_button, 'Play the top song in your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
        play_song_button.flash()

# On select event + Tooltips
def on_select(event):
    #print('Event: \t\t'+str(event)) # Debug
    save_selected()
    selection = event.widget.curselection()
    if selection:
        print('Selection Number: \t\t'+str(selection))
        index = selection[0]
        song = event.widget.get(index)
        print('Song Selected: \t\t\t'+song)
        if song not in titles:
            information = ''
            with open(path + '/' + song, 'r') as f:
                for line in f:
                    if 'T:' in line:
                        title  = '• title: ' + line.split('T:')[1].strip()
                        information += title
                    if 'C:' in line:
                        composer = '• composer: ' + line.split('C:')[1].strip()
                        information += '\n' + composer
                    if 'Z:' in line:
                        z = '• id: ' + line.split('Z:')[1].strip()
                        information += '\n' + z
            # Tooltips
            global play_song_button_tooltip
            global add_favorite_button_tooltip
            global add_queue_button_tooltip
            if information != '':
                print('Song File Information: \n'+information)
                play_song_button_tooltip.destroy()
                add_favorite_button_tooltip.destroy()
                add_queue_button_tooltip.destroy()
                play_song_button_tooltip = ToolTip(play_song_button, information, delay=0, follow=True, x_offset=(-(100+round(len(information)))), y_offset=(-(100+round(len(information)/20))), parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_favorite_button_tooltip = ToolTip(add_favorite_button, information, delay=0, follow=True, x_offset=(-(100+round(len(information)))), y_offset=(-(100+round(len(information)/20))), parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_queue_button_tooltip = ToolTip(add_queue_button, information, delay=0, follow=True, x_offset=(-(100+round(len(information)))), y_offset=(-(100+round(len(information)/20))), parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                # These tooltips need to be: x_offset=-100, y_offset=-100
            else:
                print('File contains no song information.')
                play_song_button_tooltip.destroy()
                add_favorite_button_tooltip.destroy()
                add_queue_button_tooltip.destroy()
                play_song_button_tooltip = ToolTip(play_song_button, 'File contains no song information.', delay=0, follow=True, x_offset=-50, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_favorite_button_tooltip = ToolTip(add_favorite_button, 'File contains no song information.', delay=0, follow=True, x_offset=-50, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
                add_queue_button_tooltip = ToolTip(add_queue_button, 'File contains no song information.', delay=0, follow=True, x_offset=-50, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
            play_song_button.flash()


# Determine which listbox has focus
selected_listbox = ''

def on_select_files_listbox(event):
    print('####################################################################################################')
    print('Selected Listbox: \t\tfiles_listbox')
    global selected_listbox
    selected_listbox = 'files_listbox'
    #files.listbox.activate()
    on_select(event)

def on_select_queue_listbox(event):
    print('####################################################################################################')
    print('Selected Listbox: \t\tqueue_listbox')
    global selected_listbox
    selected_listbox = 'queue_listbox'
    #queue_listbox.activate()
    on_select(event)

def on_select_played_listbox(event):
    print('####################################################################################################')
    print('Selected Listbox: \t\tplayed_listbox')
    global selected_listbox
    selected_listbox = 'played_listbox'
    #played_listbox.activate()
    on_select(event)

# Tooltip cleanup
def tooltip_cleanup():
    global play_song_button_tooltip
    global add_favorite_button_tooltip
    global add_queue_button_tooltip
    play_song_button_tooltip.destroy()
    add_favorite_button_tooltip.destroy()
    add_queue_button_tooltip.destroy()
    play_song_button_tooltip = ToolTip(play_song_button, 'Play the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
    add_favorite_button_tooltip = ToolTip(add_favorite_button, 'Add a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
    add_queue_button_tooltip = ToolTip(add_queue_button, 'Add a song to your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")

# Tkinter GUI
book = Tk()
book.title(title_and_version)
book.iconphoto(False, PhotoImage(file='LOTRO_Music_Book_icon.png'))
book.attributes('-topmost',True)
book.configure(bg='black')

# Where the GUI will be placed on screen
if dual_monitors == True:
    screen_position = screen_width+1
else:
    screen_position = screen_width - book_width
book.geometry(str(book_width) + 'x' + str(book_height) + '+' + str(screen_position) + '+0')

# Create Frames
search_frame=Frame(book)
search_frame.configure(bg='black')
search_frame.pack()

listbox_frame=Frame(book)
listbox_frame.pack(fill='both', expand=True)

queue_frame=Frame(book)
queue_frame.configure(height=10)
queue_frame.pack(fill='both', expand=True)

played_frame=Frame(book)
played_frame.configure(height=3)
played_frame.pack(side='bottom', fill='both', expand=True)

buttons_frame=Frame(book)
buttons_frame.configure(background='black')
buttons_frame.pack()

# Count for songs and results
def count():
    if searching == False:
        count = 'Songs: ' + str(len(files))
    if searching == True:
        count = 'Results: ' + str(len(files_searched))
    return count

# Create Search box and its features
file_count_label = Label(search_frame, text=count())
file_count_label.configure(bg='black', fg='white')
file_count_label.grid(row=0, column=0, sticky='w', padx=80)

search_input = Entry(search_frame, width=33)
search_input.grid(row=0, column=2, sticky='we', padx=1, pady=1)
search_input.focus_set()
search_input.bind('<Return>', lambda event=None: search_button.invoke())

search_button = Button(search_frame, text='🔎', width=3, activebackground='black', bg='black', command=search)
search_button_tooltip = ToolTip(search_button, 'Search your collection.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
search_button.grid(row=0, column=3, sticky='we', pady=1)

clear_button = Button(search_frame, text='❌', width=3, activebackground='black', bg='black', command=clear_search)
clear_button_tooltip = ToolTip(clear_button, 'Clear your search results.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
clear_button.grid(row=0, column=4, sticky='we', pady=1)

# Create files listbox
files_listbox = Listbox(listbox_frame, selectmode='single') #, exportselection=False)
files_listbox.bind('<<ListboxSelect>>', on_select_files_listbox)
files_listbox.config(bg='white', selectbackground='Azure2', selectforeground='black')
files_listbox.pack(fill='both', expand=True)
populate_listbox()

# Create Queue listbox
queue_listbox = Listbox(queue_frame, selectmode='single', height=10) #, exportselection=False)
queue_listbox.bind('<<ListboxSelect>>', on_select_queue_listbox)
queue_listbox.config(bg='white', selectbackground='Azure2', selectforeground='black')
queue_listbox.pack(fill='both', expand=True)

# Create Played listbox
played_listbox = Listbox(played_frame, selectmode='single', height=3) #, exportselection=False)
played_listbox.bind('<<ListboxSelect>>', on_select_played_listbox)
played_listbox.config(bg='white', selectbackground='Azure2', selectforeground='black')
played_listbox.pack(fill='both', expand=True)
#played_listbox.place(x=300,  y=300,  relx=0.01,  rely=0.01)
#played_listbox.grid(column=0, row=1, columnspan=10, rowspan=10, sticky='we')

# Queue
queue_listbox.insert(0, '♪ Queue ♪')

def populate_queue():
    global queue_listbox
    queue_listbox.delete(0,END)
    queue_listbox.insert(0, *queue)
    queue_listbox.insert(0, '♪ Queue ♪')

# Played
played_list = []
played_listbox.insert(0, '⌘ Played ⌘')

def played(song):
    global played_listbox
    played_list.reverse()   # Pre-reverse so songs end up in reverse order after next reverse
    played_list.append(song)
    played_list.reverse()   # Reverse to show most recent songs played at the top.
    played_listbox.delete(0,END)
    played_listbox.insert(0, *played_list)
    played_listbox.insert(0, '⌘ Played ⌘')

# Vertical scrollbar for files_listbox
files_listbox_scrollbar = ttk.Scrollbar(files_listbox, orient='vertical')
files_listbox.config(yscrollcommand=files_listbox_scrollbar.set)
files_listbox_scrollbar.config(command=files_listbox.yview)
files_listbox_scrollbar.pack(side='right', fill='both')

#'''
# Vertical scrollbar for Queue
queue_listbox_scrollbar = ttk.Scrollbar(queue_listbox, orient='vertical')
queue_listbox.config(yscrollcommand=queue_listbox_scrollbar.set)
queue_listbox_scrollbar.config(command=queue_listbox.yview)
queue_listbox_scrollbar.pack(side='right', fill='both')

# Vertical scrollbar for Played
played_listbox_scrollbar = ttk.Scrollbar(played_listbox, orient='vertical')
played_listbox.config(yscrollcommand=played_listbox_scrollbar.set)
played_listbox_scrollbar.config(command=played_listbox.yview)
#played_listbox_scrollbar.pack(side='right', fill='both')
played_listbox_scrollbar.pack(side='right', fill='both')
#'''

# Create Buttons
play_song_button = Button(buttons_frame, text='Play Song', bg='green2', fg='black', activebackground='red', activeforeground='white', command=play_song)
play_song_button_tooltip = ToolTip(play_song_button, 'Play the selected song.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
play_song_button.configure(font=('Arial','14','bold'))
play_song_button.grid(row=0, column=0, sticky='ew')

music_mode_button = Button(buttons_frame, text='Music Mode', bg='deep sky blue', fg='black', activebackground='red', activeforeground='white', command=music_mode)
music_mode_button_tooltip = ToolTip(music_mode_button, 'Music mode [on] or [off] toggle.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
music_mode_button.configure(font=('Arial','14','bold'))
music_mode_button.grid(row=1, column=0, sticky='ew')

add_favorite_button = Button(buttons_frame, text='+ Favorite', bg='magenta3', fg='black', activebackground='red', activeforeground='white', command=add_to_favorites)
add_favorite_button_tooltip = ToolTip(add_favorite_button, 'Add a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
add_favorite_button.configure(font=('Arial','14','bold'))
add_favorite_button.grid(row=0, column=1, sticky='ew')

remove_favorite_button = Button(buttons_frame, text='- Favorite', bg='pink', fg='black', activebackground='red', activeforeground='white', command=remove_from_favorites)
remove_favorite_button_tooltip = ToolTip(remove_favorite_button,'Remove a song to your favorites list.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
remove_favorite_button.configure(font=('Arial','14','bold'))
remove_favorite_button.grid(row=1, column=1, sticky='ew')

add_queue_button = Button(buttons_frame, text='+ Queue', bg='orange', fg='black', activebackground='red', activeforeground='white', command=add_to_queue)
add_queue_button_tooltip = ToolTip(add_queue_button, 'Add a song to your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
add_queue_button.configure(font=('Arial','14','bold'))
add_queue_button.grid(row=0, column=2, sticky='ew')

remove_queue_button = Button(buttons_frame, text='- Queue', bg='yellow', fg='black', activebackground='red', activeforeground='white', command=remove_from_queue)
remove_queue_button_tooltip = ToolTip(remove_queue_button, 'Remove a song from your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
remove_queue_button.configure(font=('Arial','14','bold'))
remove_queue_button.grid(row=1, column=2, sticky='ew')

play_queue_button = Button(buttons_frame, text='Play Queued', bg='yellow', fg='black', activebackground='red', activeforeground='white', command=play_queue)
play_queue_button_tooltip = ToolTip(play_queue_button, 'Play the top song in your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
play_queue_button.configure(font=('Arial','14','bold'))
play_queue_button.grid(row=0, column=3, sticky='ew')

clear_queue_button = Button(buttons_frame, text='Clear Queue', bg='yellow', fg='black', activebackground='red', activeforeground='white', command=clear_queue)
clear_queue_button_tooltip = ToolTip(clear_queue_button, 'Clear your queue.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
clear_queue_button.configure(font=('Arial','14','bold'))
clear_queue_button.grid(row=1, column=3, sticky='ew')

play_start_sync_button = Button(buttons_frame, text='Start Sync', bg='green2', fg='black', activebackground='red', activeforeground='white', command=play_start_sync)
play_start_sync_button_tooltip = ToolTip(play_start_sync_button, 'Sync is disabled.', delay=0, follow=True, x_offset=-100, y_offset=-50, parent_kwargs={"bg": "black", "padx":5, "pady":5}, fg="#ffffff", bg="#1c1c1c")
play_start_sync_button.configure(font=('Arial','14','bold'))
play_start_sync_button.configure(state=DISABLED, bg='gray')
play_start_sync_button.grid(row=2, column=0, sticky='ew')

sync = IntVar()
sync_checkbox = Checkbutton(buttons_frame, text='Sync Mode', variable=sync, onvalue=1, offvalue=0, selectcolor="gray", activebackground="black", activeforeground='white', bg='black', padx=5, pady=5, fg='white', command=sync_state)
sync_checkbox.grid(row=2, column=1, sticky='ew')

# Start main loop for GUI to display
book.mainloop()
