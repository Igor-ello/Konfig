import tkinter as tk
from emulator import ShellEmulator
import xml.etree.ElementTree as ET

"""
python -m unittest discover -s tests
python main.py                       
"""


def parse_config(config_path):
    """
    Парсинг конфигурационного файла XML.

    :param config_path: Путь к XML-файлу.
    :return: Словарь с настройками.
    """
    tree = ET.parse(config_path)
    root = tree.getroot()
    return {
        "computer_name": root.find("computer_name").text,
        "vfs_path": root.find("vfs_path").text,
        "log_path": root.find("log_path").text,
        "start_script": root.find("start_script").text,
    }


def create_gui(emulator, computer_name):
    """
    Создание графического интерфейса.

    :param emulator: Экземпляр эмулятора.
    :param computer_name: Имя компьютера для приглашения.
    """
    root = tk.Tk()
    root.title(f"Эмулятор оболочки ({computer_name})")

    # Поле вывода результатов
    output_area = tk.Text(root, height=20, width=80)
    output_area.pack(pady=10)

    # Поле ввода команды
    command_entry = tk.Entry(root, width=80)
    command_entry.pack(pady=10)

    def execute_command():
        """Обработка команды, введённой пользователем."""
        command = command_entry.get()
        output = emulator.execute_command(command)
        output_area.insert(tk.END, f"$ {command}\n{output}\n")
        command_entry.delete(0, tk.END)

    # Кнопка для выполнения команды
    submit_button = tk.Button(root, text="Выполнить", command=execute_command)
    submit_button.pack()

    root.mainloop()


if __name__ == "__main__":
    # Парсим конфигурацию
    config = parse_config("config.xml")
    # Инициализируем эмулятор
    emulator = ShellEmulator(config["vfs_path"], config["log_path"])
    # Запускаем GUI
    create_gui(emulator, config["computer_name"])
