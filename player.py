from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import time
from mutagen.mp3 import mp3

window=Tk()

window.title("MP3 PLAYER")
window.geometry("500x400")

# initializing pygame
pygame.mixer.init()

# function for time
def play_time():
    if stopped:
        return
    # grab current song time
    current_time = pygame.mixer.music.get_pos()/1000

    #convert number to song format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))


    #recreate song with directory structure stuff
    song = playlist_box.get(ACTIVE)
    song = f'c:/mp3/audio/{sing}.mp3'

    #find song length

    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    #convert format of time
    converted_song_length = time.strftime('%M:%S', time.gmtime(somg_length))

    #check to see if song is finished
    if int(song_slider.get()) ==  int(song_length):
        stop()
    elif paused:
        pass
    else:
        #move slider along one second at time
        next_time = int(song_slider.get()) + 1

        #output new time value to slider
        song_slider.config(to=song_length, value=next_time)

        #convert slider position
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        #output slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} / {converted_song_length}')

    # add current time to status
    if current_time>0:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} / {converted_song_length}')

    #loop to check the time every sec
    status_bar.after(1000,play_time)

#function to add songs as much user want

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="choose a song", filetypes=(("mp3 files", "*mp3"), ))

    #loop through song list and replace directory and mp3 from song
    for song in songs:
        #strips out directory structure
        song = song.replace("c:/mp3/audio/","")
        song = song.replace(".mp3","")
        #add to edn of playlist
        playlist_box.insert(END,song)

#function to del one song from playslist

def delete_song():
    playlist_box.delete(ANCHOR)

#function to delete all songs from playlist

def delete_all_songs():
    playlist_box.delete(0,END)

#play function

def play():
    global stopped
    stopped = False

    #recreate song with directory structure stuff
    song = playlist_box.get(ACTIVE)
    song = f'c:/mp3/audio{song}.mp3'

    #load song
    pygame.mixer.music.load(song)

    #play song
    pygame.mixer.music.play(loops=0)

    #get song time
    play_time()

# stopped vairable
global stopped
stopped = False

def stop():
    #stop song
    pygame.mixer.music.stop()

    #clear playlist bar
    playlist_box.slelection_clear(ACTIVE)

    status_bar.config(text=' ')

    #set silder to 0
    song_slider.config(value=0)

    # stop variable to true
    global stopped
    stopped = True


# function to play next song

def next_song():
    #reset slider position
    status_bar.config(text=' ')
    song_slider.config(value=0)

    #get current song
    next_one = playlist_box.curselection()

    #add one to the current song tuple
    next_one = next_one[0] + 1

    #get song title
    song = playlist_box.get(next_one)

    #add directory stuff to song title
    song = f'c:/mp3/audio/{song}.mp3'

    #load song
    pygame.mixer.music.load(song)

    #play song
    pyagme.mixer.music.play(loop=0)

    #clear active bar
    playlist_box.slection_clear(0,END)

    #move active bar
    playlist_box.activate(next_one)

    #set active bar to next song
    playlist_box.slection_set(next_one, last=None)

#function to play previous song

def previous_song():
    #reset slider
    status_bar.config(text=' ')
    song_slider.config(value=0)

    #get current song number
    next_one = playlist_box.curselection()

    #add one to curretn song number tupple
    next_one = next_one[0] - 1

    # get song title from playlist
    song = playlist_box.get(next_one)

    #add directory to song title
    song = f'c:/mp3/audio/{song}.mp3'

    #load song
    pygame.mixer.music.load(song)

    #play song
    pygame.mixer.music.play(loops=0)

    #clear active bar
    playlist_box.selection_clear(0,END)

    #move active bar
    playlist_box.activate(next_one)

    #set activate
    playlist_box.selection_set(next_one,last=None)
    
#create paused variable
global paused
paused = False

# pause function

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpaused()
        paused = False

    else:
        #pause
        pygame.mixer.music.pause()
        paused = True
        
#volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#slider function for song position
def slide(x):
    #recreate song with directory structure
    song = playlist_box.get(ACTIVE)
    song = f'c:/mp3/audio/{song}.mp3'

    #load song
    pygame.mixer.music.load(song)

    #play song
    pygame.mixer.music.play(loops=0, start=song_slider.get())


# create main frame
main_frame = Frame(window)
main_frame.pack(pady=20)     

# create playlist box

playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

# volume slider frame
volume_frame = LabelFrame(main_frame, text="volume")
volume_frame.grid(row=0,column=1,padx=20)

#create volume slider
volume_slider = ttk.scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

# song slider
song_slider = ttk.scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#button images for controls

back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')


#button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# play stop pause back forward buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda : pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#main menu

my_menu = Menu(window)
window.config(menu=my_menu)

# song menu dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add or Remove Songs", menu=add_song_menu)

add_song_menu.add_command(label="Add songs", command=add_many_songs)
add_song_menu.add_command(label="Remove one song", command=delete_song)
add_song_menu.add_command(label="Remove all songs", command=delete_all_songs)
add_song_menu.add_command(label="Exit player")

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)


window.mainloop()
