import sys
from assemble.assemble import Assemble  # Импорт класса Assemble

def main():
    if len(sys.argv) < 4:
        print("Использование: assembler <входной файл> <выходной файл> <файл журнала>")
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assembler = Assemble(input_file, output_file, log_file)
    assembler.assemble()  # Запуск процесса ассемблирования
    return 0

if __name__ == "__main__":
    sys.exit(main())
