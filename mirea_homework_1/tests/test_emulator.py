import unittest
from emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Подготовка окружения для тестов."""
        self.emulator = ShellEmulator("vfs.tar", "test_log.json")

    # Тестирование команды ls
    def test_ls(self):
        result = self.emulator.execute_command("ls")
        self.assertIn("file.txt", result)  # Проверка, что файл есть в списке

    # Тестирование команды cd с абсолютным путем
    def test_cd_absolute(self):
        self.emulator.execute_command("cd /subdir")
        self.assertEqual(self.emulator.current_dir, "/subdir")  # Проверка, что директория изменилась на /subdir

    # Тестирование команды cd с относительным путем
    def test_cd_relative(self):
        self.emulator.execute_command("cd subdir")
        self.assertEqual(self.emulator.current_dir, "/subdir")  # Проверка, что директория изменилась на /subdir

    # Тестирование команды cd с попыткой перехода в несуществующую директорию
    def test_cd_invalid(self):
        result = self.emulator.execute_command("cd /nonexistent")
        self.assertIn("cd: нет такого каталога", result)  # Проверка на ошибку перехода в несуществующую директорию

    # Тестирование команды cd .. (переход на уровень выше)
    def test_cd_parent(self):
        self.emulator.execute_command("cd /subdir")
        result = self.emulator.execute_command("cd ..")
        self.assertEqual(self.emulator.current_dir, "/")  # Проверка, что директория изменилась на /

    # Тестирование команды cal
    def test_cal(self):
        result = self.emulator.execute_command("cal")
        self.assertIn("November 2024", result)  # Проверка, что в выводе присутствует название месяца и года

    # Тестирование команды chown с корректными аргументами
    def test_chown_valid(self):
        result = self.emulator.execute_command("chown file.txt new_owner")
        self.assertIn("Права на 'file.txt' переданы пользователю new_owner", result)  # Проверка корректной передачи прав

    # Тестирование команды chown с некорректным количеством аргументов
    def test_chown_invalid_arguments(self):
        result = self.emulator.execute_command("chown file.txt")  # Только один аргумент
        self.assertIn("chown: неверное количество аргументов", result)  # Проверка на ошибку

    # Тестирование команды chown для несуществующего файла
    def test_chown_file_not_found(self):
        result = self.emulator.execute_command("chown nonexistent_file new_owner")
        self.assertIn("chown: файл 'nonexistent_file' не найден", result)  # Проверка на ошибку для несуществующего файла


if __name__ == "__main__":
    unittest.main()
