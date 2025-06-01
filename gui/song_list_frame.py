import os
import tkinter as tk


class SongListFrame(tk.Frame):
    def __init__(self, parent, music_folder):
        super().__init__(parent, borderwidth=2, relief="solid")

        self.music_folder = music_folder

        # Настройка сетки внутри SongListFrame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Список песен с рамкой
        self.song_listbox = tk.Listbox(self, height=20, width=40, borderwidth=2, relief="solid")
        self.song_listbox.grid(row=0, column=0, sticky="nsew")

        # Вертикальный скроллбар
        scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.song_listbox.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.song_listbox.config(yscrollcommand=scrollbar_y.set)

        # Горизонтальный скроллбар
        scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.song_listbox.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.song_listbox.config(xscrollcommand=scrollbar_x.set)

        # Пустая ячейка под нижним углом (чтобы красиво закрыть угол между скроллбарами)
        spacer = tk.Label(self)
        spacer.grid(row=1, column=1)

        self.load_songs()

    def load_songs(self):
        """Загружает список музыкальных файлов в Listbox."""
        songs = [f for f in os.listdir(self.music_folder) if f.endswith((".mp3", ".wav", ".flac"))]
        for song in songs:
            self.song_listbox.insert(tk.END, song)

    def get_selected_song(self):
        """Возвращает выбранную песню из списка."""
        return self.song_listbox.get(tk.ACTIVE)