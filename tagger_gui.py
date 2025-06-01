import tkinter as tk
from gui.song_list_frame import SongListFrame
from gui.player_frame import PlayerFrame
from gui.tag_frame import TagFrame
import os


class TaggerApp:
    def __init__(self, music_folder_path):
        """Инициализация основного GUI-приложения."""
        self.music_folder_path = music_folder_path
        self.music_names_list = self.update_music_names_list(self.music_folder_path)

        # Создание окна
        self.root = tk.Tk()
        self.root.title("Nova Music Mind - Tagger")
        self.root.geometry("900x600")

        # Верхняя панель с возможностью изменять ширину
        self.top_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.top_paned.pack(fill=tk.BOTH, expand=True)

        # Левая часть: список песен
        self.song_list = SongListFrame(self.top_paned, self.music_folder_path)
        self.top_paned.add(self.song_list, minsize=500)

        # Правая часть: блок тегов
        # self.tagger = TagFrame(self.top_paned, self.music_folder_path, self.song_list.get_selected_song)
        # self.top_paned.add(self.tagger, minsize=200)

        # Нижняя часть: плеер
        self.player = PlayerFrame(self.root, self.music_names_list, self.song_list)
        self.player.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        # Подключение события выбора песни
        self.song_list.song_listbox.bind("<<ListboxSelect>>", self.on_song_select)


    def update_music_names_list(self, music_folder_path):
        # Получаем список всех файлов в директории и фильтруем только музыку
        return [f for f in os.listdir(music_folder_path) if f.lower().endswith(('.mp3', '.wav'))]

    def on_song_select(self, event):
        """Обработка выбора песни из списка."""
        song_name = self.song_list.get_selected_song()
        if song_name:
            full_path = os.path.join(self.music_folder_path, song_name)
            self.player.load_and_play(full_path)
            # Передаем индекс песни в плеер
            self.player.update_song_index(self.song_list.song_listbox.curselection()[0])

    def run(self):
        """Запуск главного цикла интерфейса."""
        self.root.mainloop()


def launch_gui(music_folder_path):
    app = TaggerApp(music_folder_path=music_folder_path)
    app.run()
