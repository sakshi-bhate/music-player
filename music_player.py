################################################################################################
#                                                                                              #
#                                        MUSIC PLAYER                                          #
#                                                                                              #
################################################################################################

# Importing libraries
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import tkinter.ttk as ttk
import os, sys


# Mixer initiation
mixer.init()

#Defining Funtions for commands 
###############################################################################################

# Function to add songs from directory
def play_time():

    if stopped:
        return

    current_time = mixer.music.get_pos()/1000
    converted_c_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = playlist.get(ACTIVE)

    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    if int(song_slider.get()) == int(song_length):
        stop_btn()

    elif paused:
        pass

    else:
        next_time = int(song_slider.get()) + 1

        song_slider.config(to = song_length, value=next_time)
    
        converted_c_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        status_bar['text'] = f'Time: {converted_c_time} / {converted_song_length}'

   


    if current_time > 0:
        status_bar.config(text = f'Time: {converted_c_time} of {converted_song_length}')

    status_bar.after(1000, play_time)
    
def add_songs():
    global songs_files
    songs_files = filedialog.askopenfilenames()
    for song in songs_files:
        #song_name = re.findall('[ \w-]+?(?=\.)', song)
        playlist.insert(END, song)
        


# Stop button function
global stopped
stopped = False
def stop_btn():
    #song_slider.set(0)
    mixer.music.stop()
    status_bar['text'] = "Music stopped"
    song_slider.config(value = 0)	
    global stopped
    stopped = True

# Play button function    
def play_btn():
    global stopped 
    stopped = False
    global muted
    muted = False
    global paused
    if paused: 
        mixer.music.unpause()	
        #status_bar['text'] = "Music resumed"
        paused = False
		
    else:
        mixer.music.load(playlist.get(ACTIVE))
        mixer.music.play(loops = 0)
        #status_bar['text'] = "Music playing"  
        mute_button.configure(image = volume_img)
        play_time()
        paused = True   

def slide(x):
    # Reconstruct song with directory structure stuff
    song = playlist.get(ACTIVE)
    #Load song with pygame mixer
    mixer.music.load(song)
    #Play song with pygame mixer
    mixer.music.play(loops=0, start=song_slider.get())    


# Forward button function
def fwd_btn():
    #Get current song number
    song_slider.config(value = 0)
    next_one = playlist.curselection()

    # Add One To The Current Song Number Tuple/list
    next_one = next_one[0] + 1
    song = playlist.get(next_one)
    mixer.music.load(song)
    mixer.music.play(loops = 0)
    playlist.selection_clear(0, END)
    playlist.activate(next_one)
    playlist.selection_set(next_one, last = None)

# Backward button function
def bwd_btn():
    #Get current song number
    song_slider.config(value = 0)
    prev_one = playlist.curselection()

    # Add One To The Current Song Number Tuple/list
    prev_one = prev_one[0] - 1
    song = playlist.get(prev_one)
    mixer.music.load(song)
    mixer.music.play(loops = 0)
    playlist.selection_clear(0, END)
    playlist.activate(prev_one)
    playlist.selection_set(prev_one, last = None)

# Pause button function
global paused
paused = False
def pause_btn():
    global paused
    paused = True
    mixer.music.pause()
    status_bar['text'] = "Music paused"

# Mute/Unmute button function
global muted
muted = False
def mute_btn():
    global muted
    if muted:
        mute_button.configure(image = volume_img)
        mixer.music.set_volume(0.6)
        volume_slider.set(0.6)
        muted = False
    else:
        mute_button.configure(image = mute_img)
        mixer.music.set_volume(0)
        muted = True
        status_bar['text'] = "Music muted"
        
# Volume function
def vol_btn():
    pass

def sound_set(x):
    mixer.music.set_volume(volume_slider.get())

###################################################################################################################    
# Defining Interface And Commands To Buttons and Sliders
##################################################################################################################

#Creating Console(Window) 
root = Tk()
root.title("MP3 Player")
root.geometry("1000x850")

first_frame = Frame(root)
first_frame.pack(pady = 20)

# inserting listbox in the window(root)
playlist = Listbox(first_frame, width = 85, height = 30, bg = "#262626", fg = "cyan", selectbackground = 'blue', selectforeground = 'black')
playlist.grid(row = 0, column = 2,padx=70)

## Album Art
#listfilename = playlist.get(ACTIVE)
#mp3 = stagger.read_tag(listfilename)
#by_data = mp3[stagger.id3.APIC][0].data
#im = io.BytesIO(by_data)
#imageFile = Image.open(im)
#albumart = PhotoImage(imageFile) # Final image stored in albumart

#album_art_frame = Listbox(first_frame, width=45, height = 30)
#album_art_frame.grid(row = 0, column = 0, pady=0)

#Creating Main frame for buttons and sliders
main_frame = Frame(root)
main_frame.pack(pady = 20)

#Creation Add Song Frame in main frame
addSong_frame = Frame(main_frame)
addSong_frame.grid(row = 0, column = 0)

#Creating Control Buttons Frame in main frame
control_buttons_frame = Frame(main_frame)
control_buttons_frame.grid(row = 0, column = 1,padx=80)
#control_buttons.pack()

#creating  Volume Frame in main frame
volume_frame = Frame(main_frame)
volume_frame.grid(row = 0, column = 6,padx=40)

############# Adding  Buttons And Slider on Frames #############

# Getting image for  Add song button
add_img = PhotoImage(file = "images/add_songs.png") 
# Adding button (add songs) with image in Add song frame And Giving it command
add_btn=Button(addSong_frame, image = add_img, border = 0, command = add_songs)


# Getting image for  Backward Button  
backward_img = PhotoImage(file = "images/back50.png")
# Adding button (Backward Button) with image in Control Buttons frame And Giving it command
backward_button = Button(control_buttons_frame, image = backward_img , fg = 'Black', border = 0, command = bwd_btn)


# Getting image for play Button 
play_img = PhotoImage(file = "images/play50.png")
# Adding button (Play Button) with image in Control Buttons frame And Giving it command
play_button = Button(control_buttons_frame, image = play_img, command= play_btn, border = 0)



# Getting image for pause Button 
pause_img = PhotoImage(file = "images/pause50.png")
# Adding button (Pause Button) with image in Control Buttons frame And Giving it command
pause_button = Button(control_buttons_frame, image=pause_img,fg = 'Black', command = pause_btn, border = 0)


# Getting image for stop Button 
stop_img=PhotoImage(file = "images/stop50.png")
# Adding button (Stop Button) with image in Control Buttons frame And Giving it command
stop_button = Button(control_buttons_frame,image = stop_img ,fg = 'Black', command = stop_btn, border = 0)


# Getting image for  forward Button 
forward_img = PhotoImage(file = "images/forward50.png")
#Adding button (Forward Button) with image in Control Buttons frame And Giving it command
forward_button = Button(control_buttons_frame, image = forward_img ,fg = 'Black', border = 0, command = fwd_btn)


# Getting image for Mute And Unmute Button
volume_img=PhotoImage(file = "images/volume_on.png")
mute_img=PhotoImage(file = "images/volume_off.png")
#Adding button (Mute\Unmute Button) with image in Volume frame And Giving it command
mute_button=Button(volume_frame, image = mute_img, command= mute_btn)
mute_button.grid(row = 1, column = 0, padx=5)

# Setting volume and volume slider
volume_slider = ttk.Scale(volume_frame, from_ = 0, to_ = 1, orient = HORIZONTAL, value = 0.6, length = 150, command = sound_set)
mixer.music.set_volume(0.6)

song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value = 0, command = slide)
#song_slider.grid(row = 2, column = 0,padx=10, pady = 10)

# Button grids

add_btn.grid(row = 1, column = 0)
backward_button.grid(row = 1, column = 0, padx = 5)
volume_slider.grid(row = 1, column = 1, padx=20)
play_button.grid(row=1, column=1, padx = 5)
pause_button.grid(row=1, column=2, padx = 5)
stop_button.grid(row=1, column=3, padx = 5)
forward_button.grid(row = 1, column = 4, padx = 5)

    
# Status bar
status_bar = Label(root, text = "welcome to player", relief = SUNKEN, anchor = E)
status_bar.pack(fill = X, side = BOTTOM)


root.mainloop()