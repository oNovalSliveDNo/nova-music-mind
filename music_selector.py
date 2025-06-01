import os
import json
import tkinter as tk
from tkinter import filedialog

# Путь к файлу настроек
SETTINGS_PATH = "data/settings.json"


def ensure_data_directory():
    """
    Проверяет наличие папки data. Если её нет, создает.
    """
    os.makedirs("data", exist_ok=True)


def save_music_folder_to_settings(folder_path):
    """
    Сохраняет выбранный путь к папке в файл settings.json.
    """
    ensure_data_directory()  # Убедимся, что папка data существует
    settings = {"music_folder": folder_path}

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def select_music_folder(save_to_settings=True):
    """
    Открывает диалоговое окно для выбора папки с музыкой.

    Если пользователь выбирает папку:
    - Возвращает путь к папке.
    - Если save_to_settings=True, сохраняет путь в settings.json.

    Если пользователь нажимает "Отмена":
    - Возвращает None.
    """
    # Создаём скрытое главное окно для диалоговых окон
    root = tk.Tk()
    root.withdraw()

    # Открываем диалог для выбора папки
    selected_folder = filedialog.askdirectory(title="Выберите папку с музыкальными файлами")

    # Если папка была выбрана
    if selected_folder:
        # Сохраняем путь в settings.json, если указано
        if save_to_settings:
            save_music_folder_to_settings(selected_folder)
        return selected_folder
    else:
        # Если папка не была выбрана (пользователь нажал "Отмена")
        return None
