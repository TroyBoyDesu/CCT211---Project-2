import os
import tkinter as tk
import pygame
import sqlite3
from PIL import ImageTk, Image
from tkinter import filedialog, Menu

'''
CCT211 - Project 2: Persistent Form

Ahnaf Kamal
Hai Nguyen
Samuel Din

Note: To start, make sure to select a playlist from the menu on the top left of the window

References:

Chapters 8 and 9 from: http://bilal-qudah.com/mm/Programming%20Python%20Fourth%20Edition.pdf

Music Player: https://www.youtube.com/watch?v=SCos1o368iE&ab_channel=ShawCode

Reference for root.after(arg1, arg2):
https://www.geeksforgeeks.org/python-after-method-in-tkinter/

Reference for time.time():
https://docs.python.org/3/library/time.html

Reference for IntVar(value="val") variables:
https://www.askpython.com/python-modules/tkinter/tkinter-intvar

Reference for button state configuration:
https://www.tutorialspoint.com/how-to-disable-enable-a-button-in-tkinter

'''

class PomodoroTimer:
    def __init__(self, parent):
        self.root = parent
        self.frame = tk.Frame(parent, bg='#2b2b2b')
        self.frame.pack(side='right', padx=10)

        # Initialize timer variables
        # placeholder for work duration (minutes)
        self.work_duration = tk.IntVar(value=25)
        # placeholder for break duration (minutes)
        self.break_duration = tk.IntVar(value=5)
        self.num_cycles = tk.IntVar(value=3)  # placeholder for the cycle count
        self.backup_cycles = 0
        self.timer_running = False  # indicator for timer activity
        # initial current phase as breaks happen after work sessions
        self.current_phase = "Work"
        # conversion of minutes to seconds
        self.time_remaining = self.work_duration.get() * 60

        # Create widgets
        # label for work duration
        self.work_label = tk.Label(self.frame, text="Work Duration (mins):", bg='#2b2b2b', fg='white')
        # input for work duration
        self.work_entry = tk.Entry(self.frame, textvariable=self.work_duration)
        # label for break duration
        self.break_label = tk.Label(self.frame, text="Break Duration (mins):", bg='#2b2b2b', fg='white')
        # input for break duration
        self.break_entry = tk.Entry(self.frame, textvariable=self.break_duration)
        self.cycles_label = tk.Label(
            self.frame, text="Number of Cycles:", bg='#2b2b2b', fg='white')  # label for cycle count
        self.cycles_entry = tk.Entry(
            self.frame, textvariable=self.num_cycles)  # input for cycle count
        self.timer_label = tk.Label(self.frame, text="25:00", font=(
            "Helvetica", 48, "bold"), bg='#2b2b2b', fg='white')  # countdown label
        self.timer_label_phase = tk.Label(
            self.frame, text=" ", font=('Arial', 18), bg='#2b2b2b')  # phase label
        self.start_button = tk.Button(
            self.frame, text="Start", command=self.start_timer, bg='#3c3c3c', fg='white', borderwidth=0, highlightthickness=0, padx=10, pady=5)  # start button
        self.pause_button = tk.Button(
            self.frame, text="Pause", state=tk.DISABLED, command=self.pause_timer, bg='#3c3c3c', fg='white', borderwidth=0, highlightthickness=0, padx=10, pady=5)  # pause button
        self.reset_button = tk.Button(
            self.frame, text="Reset", state=tk.DISABLED, command=self.reset_timer, bg='#3c3c3c', fg='white', borderwidth=0, highlightthickness=0, padx=10, pady=5)  # reset button

        # Pack widgets
        self.work_label.pack()
        self.work_entry.pack()
        self.break_label.pack()
        self.break_entry.pack()
        self.cycles_label.pack()
        self.cycles_entry.pack()
        self.timer_label.pack()
        self.start_button.pack(pady=(10, 5))
        self.pause_button.pack(pady=(5, 5))
        self.reset_button.pack(pady=(5, 10))
        self.timer_label_phase.pack()

    def start_timer(self):
        self.backup_cycles = self.num_cycles.get()
        # Set the time remaining to the work duration entered by the user, in seconds
        self.time_remaining = self.work_duration.get() * 60
        # Update the timer label on the GUI to display the initial time remaining
        self.update_timer_label()
        # Set the timer_running variable to True, indicating that the timer is now active
        self.timer_running = True
        # Disable the start button and enable the pause and reset buttons on the GUI
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        # Call the update_timer function to update the timer label every second
        self.update_timer()

    def pause_timer(self):
        # Set the timer_running flag to False, indicating that the timer is paused
        self.timer_running = False
        # Enable the start button so that the user can resume the timer if they want to
        self.start_button.config(state=tk.NORMAL)
        # Disable the pause button so that the user cannot pause the timer again while it is already paused
        self.pause_button.config(state=tk.DISABLED)


    def reset_timer(self):
        # Set the timer_running flag to False, indicating that the timer is reset
        self.timer_running = False
        # Enable the start button so that the user can start the timer again
        self.start_button.config(state=tk.NORMAL)
        # Disable the pause and reset buttons so that the user cannot pause or reset the timer again while it is already reset
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        # Set the current phase to "Work"
        self.current_phase = "Work"
        # Set the time remaining to the work duration (in minutes) multiplied by 60 (to convert to seconds)
        self.time_remaining = self.work_duration.get() * 60
        # Clear the timer phase label
        self.timer_label_phase.config(text=" ")
        # Set the number of cycles to its initial value
        self.num_cycles.set(self.backup_cycles)
        # Update the timer label to show the new time remaining
        self.update_timer_label()


    def update_timer(self):
        # Check if the timer is currently running
        if self.timer_running:
            # Decrement the time remaining by one second
            self.time_remaining -= 1

        # Update the timer label to show the new time remaining
        self.update_timer_label()
        # Check if the time has run out
        if self.time_remaining == 0:
            # If the current phase is "Work", switch to "Break" and set the time remaining to the break duration
            if self.current_phase == "Work":
                self.current_phase = "Break"
                self.time_remaining = self.break_duration.get() * 60
            # If the current phase is "Break", switch to "Work" and set the time remaining to the work duration
            else:
                self.current_phase = "Work"
                self.time_remaining = self.work_duration.get() * 60

            # Update the timer label to show the new time remaining and the new phase
            self.update_timer_label()

            # If the current phase is "Work", decrement the number of cycles remaining and check if all cycles have been completed
            if self.current_phase == "Work":
                self.num_cycles.set(self.num_cycles.get() - 1)

                # If all cycles have been completed, stop the timer and update the UI accordingly
                if self.num_cycles.get() == 0:
                    self.timer_running = False
                    self.start_button.config(state=tk.DISABLED)
                    self.pause_button.config(state=tk.DISABLED)
                    self.reset_button.config(state=tk.NORMAL)
                    self.timer_label_phase.config(text="All done!", fg="cyan")

        # Schedule the update_timer function to run again in 1 second
        self.root.after(1000, self.update_timer)

    def update_timer_label(self):
        # Calculate the number of minutes and seconds remaining
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        # Update the timer label to show the new time remaining
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        # Check if the timer is currently running
        if self.timer_running:
            # If the current phase is "Work", update the timer phase label to show "Time to work!" in red
            if self.current_phase == "Work":
                self.timer_label_phase.config(text='Time to work!', fg='#FF6E6E')
            # If the current phase is "Break", update the timer phase label to show "Time to take a break." in green
            else:
                self.timer_label_phase.config(text='Time to take a break.', fg='#6EFF72')
        # Pack the timer phase label so that it is displayed in the UI
        self.timer_label_phase.pack()


class MusicPlayer:
    def __init__(self, window):
        # Basic window properties
        self.window = window
        self.window.title('Pomodoro Tunes')
        self.frame = tk.Frame(window, bg='#2b2b2b')
        self.frame.pack(side='left', padx=10)
        self.window.geometry('450x450')

        # Initial Labels
        self.song_name_label = tk.Label(self.window, text="Song Name:", bg='#2b2b2b', fg='white')
        self.artist_name_label = tk.Label(self.window, text="Artist Name:", bg='#2b2b2b', fg='white')
        self.playlist_label = tk.Label(self.window, text="Playlist", bg='#2b2b2b', fg='white')

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create widgets
        self.musiclist = tk.Listbox(self.window, bg='#3c3c3c', fg='white', width=100, height=15, borderwidth=0, highlightthickness=0)

        self.play_button_image = ImageTk.PhotoImage(Image.open('play.png').resize((38,40)))
        self.pause_button_image = ImageTk.PhotoImage(Image.open('pause.png').resize((38,40)))
        self.next_button_image = ImageTk.PhotoImage(Image.open('next.png'))
        self.previous_button_image = ImageTk.PhotoImage(Image.open('previous.png'))

        self.play_button = tk.Button(self.window, image=self.play_button_image, bg='#2b2b2b', borderwidth=0, command=self.play_music)
        self.pause_button = tk.Button(self.window, image=self.pause_button_image, bg='#2b2b2b', borderwidth=0, command=self.pause_music)
        self.next_button = tk.Button(self.window, image=self.next_button_image, bg='#2b2b2b', borderwidth=0, command=self.next_music)
        self.previous_button = tk.Button(self.window, image=self.previous_button_image, bg='#2b2b2b', borderwidth=0, command=self.previous_music)

        # Placing widgets
        self.playlist_label.pack(anchor='w', pady=10)
        self.musiclist.pack(padx=0)

        self.song_name_label.pack(anchor='w', pady=10)
        self.artist_name_label.pack(anchor='w')

        frames = tk.Frame(self.window, bg='#2b2b2b')
        frames.pack(pady=10, padx=0) 

        self.previous_button.pack(side='left', padx=20, pady=7, anchor="n")
        self.play_button.pack(side='left', padx=10, anchor="n")
        self.pause_button.pack(side='left', padx=10, pady= 1, anchor="n")
        self.next_button.pack(side='left', padx=20, pady=7, anchor="n")

        # Create Menu
        menubar = Menu(root)
        root.config(menu=menubar)
        choose_file = Menu(menubar, tearoff=False)
        choose_file.add_command(label='Playlist 1', command=self.load_music)
        menubar.add_cascade(label="Select Playlist", menu=choose_file)

        self.songs = []
        self.current_song = ""
        self.paused = False
    
    def load_music(self):
        # Loads music from 'music' folder
        root.directory = os.path.join(os.getcwd(), 'music')
        for song in os.listdir(root.directory):
            name, ext = os.path.splitext(song)
            # Ensure that the file is an mp3 file
            if ext == '.mp3':
                self.songs.append(song)
        for song in self.songs:
            self.musiclist.insert("end", song)

        # Select first song by default
        self.musiclist.selection_set(0)
        self.current_song = self.songs[self.musiclist.curselection()[0]]
        self.update_song_artist_labels(self.current_song)

    def update_song_artist_labels(self, song):
        # Update Song Name and Artist Name labels based on current song. 
        # Pulls data from SQL database to determine artist name based on song name
        name, ext = os.path.splitext(song)
        connection = sqlite3.connect('songs_and_artists.db')
        cursor = connection.cursor()

        cursor.execute("SELECT Artist FROM 'Songs and Artists' WHERE Songs = ?", (name,))
        artist = cursor.fetchone()

        artist_name = artist[0]
        
        self.song_name_label.config(text=f"Song Name: {name}")
        self.artist_name_label.config(text=f"Artist Name: {artist_name}")

    def play_music(self):
        # If not paused, plays current song from the beginning
        # If paused, plays song from where it was paused from
        if not self.paused:
            pygame.mixer.music.load(os.path.join(root.directory, self.current_song))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_music(self):
        # Plays the next song in self.songs. 
        # If the end of the playlist is reached, it cycles back to the beginning
        current_index = self.songs.index(self.current_song)
        next_index = (current_index + 1) % len(self.songs)
        self.current_song = self.songs[next_index]
        self.musiclist.selection_clear(0, tk.END)
        self.musiclist.selection_set(next_index)
        self.musiclist.activate(next_index)
        self.update_song_artist_labels(self.current_song)
        self.play_music()

    def previous_music(self):
        # Plays the previous song in self.songs. 
        # If the beginning of the playlist is reached, it cycles back to the end 
        current_index = self.songs.index(self.current_song)
        previous_index = (current_index - 1) % len(self.songs)
        self.current_song = self.songs[previous_index]
        self.musiclist.selection_clear(0, tk.END)
        self.musiclist.selection_set(previous_index)
        self.musiclist.activate(previous_index)
        self.update_song_artist_labels(self.current_song)
        self.play_music()

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg='#2b2b2b')
    pomodoro_timer = PomodoroTimer(root)
    player = MusicPlayer(root)
    root.mainloop()

