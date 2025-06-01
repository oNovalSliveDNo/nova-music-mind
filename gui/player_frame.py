import tkinter as tk
import os
import vlc


class PlayerFrame(tk.Frame):
    def __init__(self, parent, playlist, song_list_frame):
        super().__init__(parent, borderwidth=2, relief="solid")

        vlc_path = r"C:\Program Files\VideoLAN\VLC"
        os.environ['PATH'] = vlc_path + os.pathsep + os.environ['PATH']

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.repeat_mode = 0
        self.song_list_frame = song_list_frame  # Ссылка на SongListFrame

        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=2, uniform="col")

        # === 1. Название трека ===
        self.song_title_label = tk.Label(self, text="Название композиции", anchor="w", borderwidth=1, relief="solid")
        self.song_title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # === 2. Видео ===
        self.video_panel = tk.Frame(self, bg="black", width=200, borderwidth=1, relief="solid")
        self.video_panel.grid(row=1, column=0, rowspan=2, sticky="nswe", padx=10, pady=5)
        self.embed_vlc()

        # === 3. Перемотка и длительность ===
        self.seek_frame = tk.Frame(self, borderwidth=1, relief="solid")
        self.seek_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        self.seek_frame.columnconfigure(1, weight=1)

        # === 4. Управление ===
        self.controls_frame = tk.Frame(self, borderwidth=1, relief="solid")
        self.controls_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        self.prev_button = tk.Button(self.controls_frame, text="<<", command=self.prev_song, borderwidth=1,
                                     relief="solid")
        self.prev_button.pack(side=tk.LEFT, padx=2)

        self.play_button = tk.Button(self.controls_frame, text="Старт", command=self.toggle_play, borderwidth=1,
                                     relief="solid")
        self.play_button.pack(side=tk.LEFT, padx=2)

        self.next_button = tk.Button(self.controls_frame, text=">>", command=self.next_song, borderwidth=1,
                                     relief="solid")
        self.next_button.pack(side=tk.LEFT, padx=2)

        self.volume_slider = tk.Scale(self.controls_frame, from_=0, to=100, orient="horizontal", label="Громкость",
                                      command=self.set_volume, borderwidth=1, relief="solid")
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        self.player.audio_set_volume(50)

    def embed_vlc(self):
        self.after(100, lambda: self.player.set_hwnd(self.video_panel.winfo_id()))

    def load_and_play(self, path):
        media = self.instance.media_new(path)
        self.player.set_media(media)
        self.player.play()
        self.song_title_label.config(text=os.path.basename(path))
        self.play_button.config(text="Пауза")
        self.is_playing = True

    def toggle_play(self):
        if self.is_playing:
            self.player.pause()
            self.play_button.config(text="Старт")
        else:
            self.player.play()
            self.play_button.config(text="Пауза")
        self.is_playing = not self.is_playing

    def set_volume(self, value):
        self.player.audio_set_volume(int(value))

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_and_play(self.playlist[self.current_index])
        self.update_song_index(self.current_index)

    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_and_play(self.playlist[self.current_index])
        self.update_song_index(self.current_index)

    def set_playlist(self, songs):
        self.playlist = songs
        self.current_index = 0
        if songs:
            self.load_and_play(songs[0])

    def update_song_index(self, new_index):
        """Обновляет индекс песни в SongListFrame."""
        self.current_index = new_index
        self.song_list_frame.song_listbox.selection_clear(0, tk.END)  # Снимаем выделение
        self.song_list_frame.song_listbox.select_set(self.current_index)  # Выбираем новую песню
        self.song_list_frame.song_listbox.activate(self.current_index)  # Активируем ее