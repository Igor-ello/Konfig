import struct
from bitarray import bitarray
from bitarray.util import int2ba

# Пример обновленного кода для ассемблера

class Assemble:
    def __init__(self, input_file: str, output_file: str, log_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

        try:
            with open(input_file, "r") as infile:
                # Прочитать файл и обработать его
                print(f"Processing input file: {input_file}")
                # Процесс ассемблирования
                self.assemble(infile)
        except FileNotFoundError:
            print(f"Error: Input file {input_file} not found.")
            raise

    def assemble(self, infile):
        with open(self.output_file, "wb") as outfile:
            print(f"Writing to binary output file: {self.output_file}")
            # Здесь добавьте логирование команд ассемблера, которые записываются в файл
            # Например:
            outfile.write(b'\x10')  # Пример записи байтов в файл
            print("Data written to output file.")

    def write_bitset_to_binary_file(self, bitset):
        with open(self.binary_output_file, 'wb') as f:
            f.write(bitset)
            print(f"Written bytes: {bitset}")  # Добавьте отладочную печать

    def load_constant(self, B, C):
        """Кодирует и записывает инструкцию LOAD_CONSTANT."""
        code = bytearray(5)  # 5 байт для инструкции LOAD_CONSTANT
        code[0] = 0xE0  # Операция LOAD_CONSTANT
        code[1] = (B >> 16) & 0xFF  # Старшие 8 бит для B
        code[2] = (B >> 8) & 0xFF  # Средние 8 бит для B
        code[3] = B & 0xFF  # Младшие 8 бит для B
        code[4] = C & 0x7F  # 7 бит для C

        self.write_bitset_to_binary_file(code)

    def memory_read(self, B, C):
        """Кодирует и записывает инструкцию MEMORY_READ."""
        code = int2ba(7, length=40)
        code[3:10] = int2ba(B, length=7, endian='big')
        code[10:35] = int2ba(C, length=25, endian='big')
        self.write_bitset_to_binary_file(code)

        with open(self.log_file, 'a', encoding='cp1251') as logfile:
            logfile.write(f"MEMORY_READ: B = {B}, C = {C}\n")

    def memory_write(self, B, C, D):
        """Кодирует и записывает инструкцию MEMORY_WRITE."""
        code = int2ba(1, length=32)
        code[3:10] = int2ba(B, length=7, endian='big')
        code[10:17] = int2ba(C, length=7, endian='big')
        code[17:31] = int2ba(D, length=14, endian='big')
        self.write_bitset_to_binary_file(code)

        with open(self.log_file, 'a', encoding='cp1251') as logfile:
            logfile.write(f"MEMORY_WRITE: B = {B}, C = {C}, D = {D}\n")

    def bitwise_or(self, B, C, D):
        """Кодирует и записывает инструкцию OR (побитовое ИЛИ)."""
        code = int2ba(3, length=32)
        code[3:17] = int2ba(B, length=14, endian='big')
        code[17:24] = int2ba(C, length=7, endian='big')
        code[24:31] = int2ba(D, length=7, endian='big')
        self.write_bitset_to_binary_file(code)

        with open(self.log_file, 'a', encoding='cp1251') as logfile:
            logfile.write(f"OR: B = {B}, C = {C}, D = {D}\n")

    def parse_file(self):
        """Разбирает входной файл и обрабатывает инструкции."""
        try:
            with open(self.input_file, 'r', encoding='cp1251') as infile:
                for line in infile:
                    parts = line.strip().split()
                    command = parts[0]
                    if command == "LOAD_CONSTANT":
                        reg = parts[1][:-1]
                        value = parts[2][1:]
                        self.load_constant(int(value), int(reg[1:]))
                    elif command == "MEMORY_READ":
                        reg = parts[1][:-1]
                        addr = parts[2][1:-1]
                        self.memory_read(int(reg[1:]), int(addr))
                    elif command == "MEMORY_WRITE":
                        operand = parts[1][1:-1]
                        offset = parts[2]
                        reg = parts[3]
                        self.memory_write(int(reg[1:]), int(operand[1:]), int(offset))
                    elif command == "OR":
                        reg = parts[1][:-1]
                        addr = parts[2][1:]
                        offset = parts[3][:-1]
                        self.bitwise_or(int(offset), int(reg[1:]), int(addr))
        except Exception as e:
            print(f"Ошибка при разборе файла: {e}")
