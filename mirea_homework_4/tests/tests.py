import unittest
import os
from assemble.assemble import Assemble
from interpret.interpret import Interpret


class TestAssemble(unittest.TestCase):
    def setUp(self):
        os.makedirs("files", exist_ok=True)
        self.input_file = "files/test_input.asm"
        self.output_file = "files/test_output.bin"
        self.log_file = "files/test_log.csv"

    def tearDown(self):
        for file in [self.input_file, self.output_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_assembler_load(self):
        # Подготовка исходного файла
        with open(self.input_file, "w") as f:
            f.write("LOAD_CONSTANT R22, #482")

        # Запуск ассемблера
        Assemble(self.input_file, self.output_file, self.log_file)

        # Ожидаемый результат: 5 байт (код для LOAD_CONSTANT)
        expected_data = b'\x10'  # Пример (после кодирования)

        with open(self.output_file, "rb") as f:
            byte_data = f.read()

        self.assertEqual(byte_data, expected_data, f"Expected {expected_data}, but got {byte_data}")


class TestInterpret(unittest.TestCase):
    def setUp(self):
        # Проверим наличие директории и создадим, если она не существует
        os.makedirs("files", exist_ok=True)
        self.input_file = "files/test_input.asm"
        self.output_file = "files/test_output.bin"
        self.result_file = "files/result.csv"
        self.log_file = "files/test_log.csv"

    def tearDown(self):
        # Удаляем все созданные файлы после тестов
        for file in [self.input_file, self.output_file, self.result_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_interpret_write(self):
        # Подготовка команды для ассемблера
        with open(self.input_file, "w") as f:
            f.write("LOAD_CONSTANT R0 #52\n")
            f.write("MEMORY_WRITE [R31 + 0], R0\n")

        # Запуск ассемблера
        try:
            Assemble(self.input_file, self.output_file, self.log_file)
        except Exception as e:
            self.fail(f"Assembler failed with error: {e}")

        # Запуск интерпретатора
        try:
            Interpret(self.output_file, self.result_file, 0, 2, debug=False)
        except Exception as e:
            self.fail(f"Interpreter failed with error: {e}")

        # Проверка результата
        self.assertTrue(os.path.exists(self.result_file), f"Result file {self.result_file} was not created.")

        with open(self.result_file, "r") as f:
            lines = f.readlines()

        self.assertEqual(lines[0].strip(), "ID,VALUE")
        self.assertEqual(lines[1].strip(), "0,52")

if __name__ == "__main__":
    unittest.main()
