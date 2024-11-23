import tarfile
import os
import calendar
import json
from datetime import datetime


class ShellEmulator:
    def __init__(self, vfs_path, log_file="log.json"):
        self.vfs_path = vfs_path
        self.log_file = log_file
        self.current_dir = "/"
        self.vfs = None
        self.files_owners = {}
        self.load_vfs()

        # Инициализация лог-файла
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                json.dump([], file)

    def load_vfs(self):
        """Загружает виртуальную файловую систему из архива tar"""
        try:
            self.vfs = tarfile.open(self.vfs_path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.vfs_path} не найден.")
        except tarfile.TarError:
            raise tarfile.TarError(f"Ошибка при чтении архива {self.vfs_path}.")

        for member in self.vfs.getmembers():
            self.files_owners[member.name] = "default_owner"

    def log_command(self, command, output):
        """Записывает команду и её результат в лог-файл"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "output": output,
            "current_directory": self.current_dir,
        }

        with open(self.log_file, "r+") as file:
            logs = json.load(file)
            logs.append(log_entry)
            file.seek(0)
            json.dump(logs, file, indent=4)

    def change_directory(self, new_dir):
        """Меняет текущую рабочую директорию в эмуляторе"""
        if new_dir == "/":
            self.current_dir = "/"
        elif new_dir == "..":
            if self.current_dir != "/":
                self.current_dir = os.path.dirname(self.current_dir.rstrip("/"))
                if not self.current_dir:
                    self.current_dir = "/"
            elif self.current_dir == "/":
                return f"Текущий каталог: {self.current_dir}"
        elif new_dir.startswith("/"):
            self.current_dir = new_dir
        else:
            self.current_dir = os.path.join(self.current_dir, new_dir)

        if not self.directory_exists(self.current_dir):
            return f"cd: нет такого каталога: {self.current_dir}"

        return f"Текущий каталог: {self.current_dir}"

    def directory_exists(self, dir_path):
        """Проверяет, существует ли каталог в архиве"""
        dir_path = dir_path.lstrip("/")
        for member in self.vfs.getmembers():
            if member.name.lstrip("/") == dir_path or member.name.lstrip("/").startswith(f"{dir_path}/"):
                return True
        return False

    def list_files(self, dir_path="/"):
        """Возвращает список файлов в указанной директории"""
        files = []
        for member in self.vfs.getmembers():
            relative_path = member.name.lstrip("/")
            if relative_path.startswith(dir_path.lstrip("/")) and not member.isdir():
                files.append(relative_path[len(dir_path.lstrip("/")):].lstrip("/"))

        return "\n".join(files) if files else "Нет файлов в директории"

    def execute_command(self, command):
        """Выполняет команду оболочки"""
        # Заменяем cd.. на cd ..
        command = command.replace("cd..", "cd ..")
        args = command.split()
        if not args:
            output = "cd: аргумент отсутствует"
            self.log_command(command, output)
            return output

        cmd = args[0]

        if cmd == "cd":
            if len(args) > 1:
                output = self.change_directory(args[1])
            else:
                output = "cd: аргумент отсутствует"

        elif cmd == "ls":
            output = self.list_files(self.current_dir)

        elif cmd == "cal":
            year = 2024
            month = 11
            output = calendar.month(year, month)

        elif cmd == "chown":
            if len(args) != 3:
                output = "chown: неверное количество аргументов"
            else:
                file, new_owner = args[1], args[2]
                if self.change_owner(file, new_owner):
                    output = f"Права на '{file}' переданы пользователю {new_owner}"
                else:
                    output = f"chown: файл '{file}' не найден"

        elif cmd == "exit":
            output = "Выход из эмулятора."
            self.log_command(command, output)
            print(output)
            exit(0)

        else:
            output = f"Команда {cmd} выполнена"

        self.log_command(command, output)
        return output

    def change_owner(self, file, new_owner):
        """Меняет владельца файла в виртуальной файловой системе"""
        if file in self.files_owners:
            self.files_owners[file] = new_owner
            return True
        return False
