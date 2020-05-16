import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
import time
import threading
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')
maintextLabel = Label(root, text='Welcome to EarBuddy Lets make some noise ! ')
maintextLabel.pack()

statusbar = ttk.Label(root, text='Welcome to EarBuddy - For any Suggestions Contact Developer :::: Help - About us ',
                  relief=SUNKEN,
                  anchor=W, font='Arial 15 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# create the sub menu
subMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=subMenu)

# PLAYLIST IT CONTAINS THE FULL PATH AND FILENAME
# PLAYLISTBOX CONTAINS JUST THE FILENAME
# FULLPATH + FILENAME IS REQUIRED TO PLAY THE MUSIC INSIDE PLAY_MUSIC LOAD FUNCTION


playlist = []


def open_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


def exit():
    msgbox = tkinter.messagebox.askquestion('Exit Application', 'Do you really want to close ?')
    if msgbox == 'yes':
        stop_music()
        root.destroy()
    else:
        tkinter.messagebox.showinfo('Return', 'Returning to the Main Window')


subMenu.add_command(label='Open', command=open_file)
subMenu.add_command(label='Exit', command=exit)


def about_us():
    tkinter.messagebox.showinfo('EarBuddy',
                                message='Thank You For Installing EarBuddy.\nVersion 0.0.1\nFor Suggestions Contact Developer :\nEmail : sujayshekhar162@gmail.com\n\n\n\nBuild Using Python 3.7.7.\n\nPackages Used : Tkinter, Mutagen, Pygame, OS, Sys, Threading, Time, cx_Freeze')


subMenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)

mixer.init()  # Initailizing pygame mixer
# root.geometry('1000x400')
root.title('EarBuddy (Beta) v0.0.1')
root.iconbitmap('icon.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame = TheListBox (Playlist)
# RightFrame = Top,Middle,Bottom Frames
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=50, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text='+ Add', command=open_file)
addBtn.pack(side=LEFT)


def delete_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text=' - Del', command=delete_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(padx=50,pady=30)

topframe = Frame(rightframe)
topframe.pack()

# Label


lengthLabel = ttk.Label(topframe, text='Total Length : --:--')
lengthLabel.pack(pady=5)

currenttimeLabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimeLabel.pack()


def show_details(play_it):
    filedata = os.path.splitext(play_it)
    if filedata[1] == '.mp3':
        audio = MP3(play_it)
        totallength = audio.info.length
    else:  # for wav files
        a = mixer.Sound(play_it)
        totallength = a.get_length()
    maintextLabel['text'] = f'Welcome to Earbuddy Currently Playing :::: {os.path.basename(play_it)}'
    # div - totallength/60, mod - totallength%60
    mins, secs = divmod(totallength, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = f'{mins:02d}:{secs:02d}'
    lengthLabel['text'] = f'Total Length - {timeformat}'

    t1 = threading.Thread(target=start_count, args=(totallength,))
    t1.start()


def start_count(t):
    global paused
    # mixer.get_busy() : return false when we press the stop button or music stops playing
    # continue ignores all of the statement below it we check if music is paused or not
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = f'{mins:02d}:{secs:02d}'
            currenttimeLabel['text'] = f'Current Time - {timeformat}'
            time.sleep(1)
            current_time += 1


def play_music():
    global paused
    # check wheter the paused global variable is initaialized or not if not initialized then executes the code under
    # except condition if initialized it goes to else condition
    if paused == True:
        mixer.music.unpause()
        statusbar['text'] = f'Music Resumed : {os.path.basename(filename_path)}'
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = f'Currently Playing ----> {os.path.basename(play_it)}'
            show_details(play_it)
        except ValueError:
            tkinter.messagebox.showerror('File Not Found', message='Please Check the file')


# Pause
paused = False


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = 'Paused..!'


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Stopped..!'


def rewind_music():
    play_music()
    statusbar['text'] = f'Rewinded : {filename_path}'


def volume_control(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = False


def mute_music():
    global muted
    if muted == True:  # unmute
        mixer.music.set_volume(0.8)
        volumeBtn.configure(image=volumePhoto)
        scale.set(80)
        muted = False
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = True


middle = Frame(rightframe, relief=RAISED)
middle.pack(pady=30, padx=30)

playPhoto = PhotoImage(file=r'files/play.png')
playBtn = ttk.Button(middle, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

pausePhoto = PhotoImage(file=r'files/pause.png')
pauseBtn = ttk.Button(middle, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file=r'files/stop.png')
stopBtn = ttk.Button(middle, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

# bottom frame for the volume rewind mute unmute etc

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file=r'files/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file=r'files/mute.png')
volumePhoto = PhotoImage(file=r'files/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=volume_control)
scale.set(80)
mixer.music.set_volume(0.8)  # pygame set_volume return 0 to 1 for low to high
scale.grid(row=0, column=2, padx=30, pady=15)


def on_closing():
    abc = tkinter.messagebox.askyesno("Exit", "Do You Really Want To Close ?")
    if abc == True:
        stop_music()
        root.destroy()
    else:
        tkinter.messagebox.showinfo('Returning', 'Returning to the main Window')


root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
