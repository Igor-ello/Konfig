import struct
from typing import List

# Пример обновленного кода для интерпретатора

class Interpret:
    def __init__(self, binary_file: str, result_file: str, start: int, end: int, debug: bool = False):
        print(f"Loading binary file: {binary_file}")
        try:
            with open(binary_file, "rb") as infile:
                # Прочитаем бинарный файл
                print("Binary file successfully opened.")
                self.execute_binary_file(infile)
        except FileNotFoundError:
            print(f"Error: Binary file {binary_file} not found.")
            raise

        print(f"Saving result to {result_file}")
        self.save_memory_to_csv(result_file, start, end)

    def execute_binary_file(self, infile):
        # Ваш код для интерпретации
        print("Executing binary file...")  # Логирование работы интерпретатора

    def save_memory_to_csv(self, result_file: str, start: int, end: int):
        # Логирование процесса записи
        print(f"Saving memory to CSV: {result_file}")
        try:
            with open(result_file, "w") as out:
                out.write("ID,VALUE\n")
                # Пример записи
                out.write("0,52\n")
                print("Memory data saved to CSV.")
        except Exception as e:
            print(f"Error writing to result file: {e}")
            raise

    def debug_output(self):
        """Вывод состояния регистров и памяти, если включён дебаг режим"""
        print(f"Регистрa: {', '.join(f'R{i}: {val}' for i, val in enumerate(self.registers))}")
        print(f"Память: {', '.join(f'M{i}: {val}' for i, val in enumerate(self.memory[:16]))}")
        print()

    def read_bitset_from_binary_file(self, infile, bit_count):
        """Чтение битового набора из бинарного файла"""
        byte_count = (bit_count + 7) // 8
        raw_bytes = infile.read(byte_count)
        if len(raw_bytes) != byte_count:
            raise EOFError("Неожиданный конец файла.")
        return int.from_bytes(raw_bytes, "little")

    def load_constant_from_code(self, code: int):
        """Загрузка константы в регистр."""
        A = code & 0b111
        B = (code >> 3) & ((1 << 24) - 1)
        C = (code >> 27) & ((1 << 7) - 1)
        if self.debug:
            print(f"LOAD_CONSTANT: A={A}, B={B}, C={C}")
        self.registers[C] = B

    def memory_read_from_code(self, code: int):
        """Чтение из памяти и запись в регистр"""
        A = code & 0b111
        B = (code >> 3) & ((1 << 7) - 1)
        C = (code >> 10) & ((1 << 25) - 1)
        if C < len(self.memory):
            self.registers[B] = self.memory[C]
        if self.debug:
            print(f"MEMORY_READ: A={A}, B={B}, C={C}")

    def memory_write_from_code(self, code: int):
        """Запись в память из регистра"""
        A = code & 0b111
        B = (code >> 3) & ((1 << 7) - 1)
        C = (code >> 10) & ((1 << 7) - 1)
        D = (code >> 17) & ((1 << 14) - 1)
        if C < len(self.registers) and (self.registers[C] + D) < len(self.memory):
            self.memory[self.registers[C] + D] = self.registers[B]
        if self.debug:
            print(f"MEMORY_WRITE: A={A}, B={B}, C={C}, D={D}")

    def bitwise_or_from_code(self, code: int):
        """Побитовое ИЛИ между регистрами и памятью"""
        A = code & 0b111
        B = (code >> 3) & ((1 << 14) - 1)
        C = (code >> 17) & ((1 << 7) - 1)
        D = (code >> 24) & ((1 << 7) - 1)
        if C < len(self.registers) and D < len(self.registers) and (self.registers[D] + B) < len(self.memory):
            self.registers[C] |= self.memory[self.registers[D] + B]
        if self.debug:
            print(f"BITWISE_OR: A={A}, B={B}, C={C}, D={D}")
