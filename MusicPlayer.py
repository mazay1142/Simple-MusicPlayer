import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pygame
import random

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        #Initialize Pygame mixer and event loop
        pygame.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        #Variables to store the folder path, playback state, and mode
        self.folder_path = None
        self.is_paused = False
        self.current_song_index = 0
        self.playback_mode = "sequential"

        #Create widgets
        self.create_widgets()

    def create_widgets(self):
        #Buttons
        self.open_button = tk.Button(self.root, text="Open Folder", command=self.open_folder)
        self.open_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_music)
        self.resume_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        #Playback Mode Selection
        self.mode_label = tk.Label(self.root, text="Playback Mode")
        self.mode_label.pack(pady=(10, 0))

        self.mode_var = tk.StringVar(value=self.playback_mode)

        self.sequential_radio = tk.Radiobutton(self.root, text="Sequential", variable=self.mode_var, value="sequential", command=self.set_playback_mode)
        self.sequential_radio.pack(anchor=tk.W)

        self.loop_radio = tk.Radiobutton(self.root, text="Loop", variable=self.mode_var, value="loop", command=self.set_playback_mode)
        self.loop_radio.pack(anchor=tk.W)

        self.shuffle_radio = tk.Radiobutton(self.root, text="Shuffle", variable=self.mode_var, value="shuffle", command=self.set_playback_mode)
        self.shuffle_radio.pack(anchor=tk.W)

        #Listbox to display songs
        self.songs_listbox = tk.Listbox(self.root, width=60, height=10)
        self.songs_listbox.pack(pady=20)

        #Volume Slider
        self.volume_label = tk.Label(self.root, text="Volume")
        self.volume_label.pack(pady=(5, 0))

        self.volume_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(25)#Default volume level, change if needed
        self.volume_slider.pack(pady=5)

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            try:
                self.folder_path = folder_path
                self.load_songs(folder_path)
            except Exception as e:
                print("Error while: open_folder")
                messagebox.showerror("Error: open_folder", str(e))

    def load_songs(self, folder_path):
        self.songs_listbox.delete(0, tk.END)
        self.all_songs = []
        for song in os.listdir(folder_path):
            if song.endswith(('.mp3','.wav','.ogg')):
                self.all_songs.append(song)
                self.songs_listbox.insert(tk.END, song)

    def play_music(self):
        try:
            selected_song = self.songs_listbox.get(tk.ACTIVE)
            song_index = self.all_songs.index(selected_song)
            self.current_song_index = song_index
            pygame.mixer.music.load(os.path.join(self.folder_path, selected_song))
            pygame.mixer.music.play()
            self.is_paused = False
        except Exception as e:
            print("Error while: play_music")
            messagebox.showerror("Error: play_music", str(e))

    def pause_music(self):
        try:
            pygame.mixer.music.pause()
            self.is_paused = True
        except Exception as e:
            print("Error while: pause_music")
            messagebox.showerror("Error: pause_music", str(e))

    def resume_music(self):
        if self.is_paused:
            try:
                pygame.mixer.music.unpause()
                self.is_paused = False
            except Exception as e:
                print("Error while: resume_music")
                messagebox.showerror("Error: resume_music", str(e))

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            self.is_paused = True
        except Exception as e:
            print("Error while: stop_music")
            messagebox.showerror("Error: stop_music", str(e))

    #Convert the volume level from 0-100 to a float between 0.0 and 1.0
    def set_volume(self, volume_level):
        volume_float = float(volume_level) / 100
        pygame.mixer.music.set_volume(volume_float)

    #I don`t know how THE FUCK 132-152 works, good luck debugging it
    def next_song(self):
        if self.playback_mode == "sequential":
            self.current_song_index += 1
            if self.current_song_index >= len(self.all_songs):
                self.current_song_index = 0
                print("Reached end of playlist, looping back to start.")
        elif self.playback_mode == "shuffle":
            self.current_song_index = random.randint(0, len(self.all_songs) - 1)

        next_song = self.all_songs[self.current_song_index]
        print(f"Playing next song: {next_song}")
        self.songs_listbox.selection_clear(0, tk.END)
        self.songs_listbox.selection_set(self.current_song_index)

        try:
            pygame.mixer.music.load(os.path.join(self.folder_path, next_song))
            pygame.mixer.music.play()
            self.is_paused = False
        except Exception as e:
            print(f"Error loading or playing song: {e}")

    def set_playback_mode(self):
        self.playback_mode = self.mode_var.get()
        print(f"Playback mode changed to {self.mode_var.get()}")

def check_song_end(self):
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if not self.is_paused:
               self.next_song()
    root.after(25, check_song_end, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    check_song_end(app)
    root.mainloop()