import tkinter as tk
from tkinter import ttk, messagebox
import os
import json


class TagFrame(tk.Frame):
    def __init__(self, parent, music_folder, get_current_song_callback):
        super().__init__(parent, borderwidth=2, relief="solid")

        self.music_folder = music_folder
        self.get_current_song = get_current_song_callback

        # Жанр
        tk.Label(self, text="Жанр").pack()
        self.genre_cb = ttk.Combobox(self, values=["Рок", "Поп", "Джаз", "Классика", "Электроника"])
        self.genre_cb.pack()

        # Настроение
        tk.Label(self, text="Настроение").pack()
        self.mood_cb = ttk.Combobox(self, values=["Весёлое", "Грустное", "Энергичное", "Расслабляющее"])
        self.mood_cb.pack()

        # Язык
        tk.Label(self, text="Язык").pack()
        self.language_cb = ttk.Combobox(self, values=["Английский", "Русский", "Испанский", "Французский"])
        self.language_cb.pack()

        # Кастомные теги
        tk.Label(self, text="Кастомные теги").pack()
        self.custom_tag_entry = tk.Entry(self)
        self.custom_tag_entry.pack()

        # Сохранить теги
        save_button = tk.Button(self, text="Сохранить теги", command=self.save_tags)
        save_button.pack(pady=10)

    def save_tags(self):
        genre = self.genre_cb.get()
        mood = self.mood_cb.get()
        language = self.language_cb.get()
        custom_tag = self.custom_tag_entry.get()

        if not genre or not mood or not language:
            messagebox.showwarning("Ошибка", "Заполни все обязательные поля.")
            return

        song_name = self.get_current_song()
        if not song_name:
            messagebox.showerror("Ошибка", "Не выбрана песня.")
            return

        tags = {
            "genre": genre,
            "mood": mood,
            "language": language,
            "custom_tag": custom_tag
        }

        tag_file = os.path.join(self.music_folder, f"{os.path.splitext(song_name)[0]}_tags.json")
        with open(tag_file, "w", encoding="utf-8") as f:
            json.dump(tags, f, indent=4)

        messagebox.showinfo("Готово", "Теги сохранены.")
