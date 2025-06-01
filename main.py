import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

from tagger_gui import launch_gui

SETTINGS_PATH = "data/settings.json"
MUSIC_EXTENSIONS = ('.mp3', '.wav', '.flac')


def ensure_data_directory():
    os.makedirs("data", exist_ok=True)


def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("music_folder")
        except json.JSONDecodeError:
            return None
    return None


def save_settings(path):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump({"music_folder": path}, f, indent=4)


def folder_has_music_files(path):
    return any(
        file.lower().endswith(MUSIC_EXTENSIONS)
        for file in os.listdir(path)
        if os.path.isfile(os.path.join(path, file))
    )


def ask_for_music_folder():
    root = tk.Tk()
    root.withdraw()  # скрыть главное окно
    return filedialog.askdirectory(title="Выберите папку с музыкальными файлами")


def show_warning(msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Предупреждение", msg)


def get_valid_music_folder():
    while True:
        folder = load_settings()

        if folder and os.path.isdir(folder) and folder_has_music_files(folder):
            return folder

        folder = ask_for_music_folder()
        if not folder:
            show_warning("Папка не выбрана. Приложение будет закрыто.")
            exit()

        if not folder_has_music_files(folder):
            show_warning("В выбранной папке нет музыкальных файлов (.mp3, .wav, .flac). Попробуйте другую папку.")
            continue

        save_settings(folder)
        return folder


def main():
    ensure_data_directory()
    music_folder_path = get_valid_music_folder()
    launch_gui(music_folder_path)


if __name__ == "__main__":
    main()
