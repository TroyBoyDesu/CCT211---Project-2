import os
import pygame
from tkinter import *
from tkinter import filedialog, PhotoImage, ttk

# Initialize Pygame mixer
pygame.mixer.init()

# Create a Tkinter window
root = Tk()
root.title("Simple Music Player")
root.geometry("500x350")

# Set window background color
root.configure(bg='#2b2b2b')

# Define global variables
paused = False
music_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")

# Check if the music folder exists; create it if it doesn't
if not os.path.exists(music_folder):
    os.makedirs(music_folder)

# Load images
play_image = PhotoImage(file="play.png")
pause_image = PhotoImage(file="pause.png")
previous_image = PhotoImage(file="previous.png")
next_image = PhotoImage(file="next.png")

# Define functions
def update_music_list():
    music_list.delete(0, END)
    for file in os.listdir(music_folder):
        if file.lower().endswith(('.mp3', '.wav')):
            music_list.insert(END, file)

def play_music():
    selected_music = music_list.get(ACTIVE)
    music_file = os.path.join(music_folder, selected_music)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    update_play_pause_button()

def toggle_play_pause_music():
    global paused
    if pygame.mixer.music.get_busy():
        if paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        paused = not paused
    else:
        play_music()
    update_play_pause_button()

def update_play_pause_button():
    if pygame.mixer.music.get_busy():
        if paused:
            play_pause_button.config(image=play_image)
        else:
            play_pause_button.config(image=pause_image)
    else:
        play_pause_button.config(image=play_image)

def set_volume(val):
    volume = int(float(val)) / 100
    pygame.mixer.music.set_volume(volume)

def on_music_double_click(event):
    play_music()

def previous_song():
    current_selection = music_list.curselection()
    if current_selection:
        music_list.selection_clear(current_selection)
        music_list.selection_set(current_selection[0] - 1)
        play_music()

def next_song():
    current_selection = music_list.curselection()
    if current_selection:
        music_list.selection_clear(current_selection)
        music_list.selection_set(current_selection[0] + 1)
        play_music()

# Create buttons and labels
music_list = Listbox(root, width=50, selectmode=SINGLE, bg='#3c3c3c', fg='white', borderwidth=0, highlightthickness=0)
music_list.pack(pady=10)
music_list.bind("<Double-1>", on_music_double_click)

# Update music list
update_music_list()

controls_frame = Frame(root, bg='#2b2b2b')
controls_frame.pack(pady=10)

previous_button = Button(controls_frame, image=previous_image, command=previous_song, bg='#2b2b2b', fg='white', borderwidth=0)
previous_button.pack(side=LEFT, padx=5)

play_pause_button = Button(controls_frame, image=play_image, command=toggle_play_pause_music, bg='#2b2b2b', fg='white', borderwidth=0)
play_pause_button.pack(side=LEFT, padx=5)

next_button = Button(controls_frame, image=next_image, command=next_song, bg='#2b2b2b', fg='white', borderwidth=0)
next_button.pack(side=LEFT, padx=5)

# Create custom style for volume slider
style = ttk.Style()
style.configure("Minimal.Horizontal.TScale", background='#2b2b2b', troughcolor='#3c3c3c', sliderrelief='flat')

volume_slider = ttk.Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=set_volume, style="Minimal.Horizontal.TScale")
volume_slider.set(50)  # Set the initial volume to 50%
volume_slider.pack(side=LEFT)

# Run the main loop
root.mainloop()
