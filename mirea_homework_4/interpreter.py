import sys
from interpret.interpret import Interpret  # Импортируем класс Interpret

def main():
    if len(sys.argv) != 5:
        print(f"Использование: {sys.argv[0]} <binaryFile> <resultFile> <start> <end>")
        return 1

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    try:
        start = int(sys.argv[3])
        end = int(sys.argv[4])
    except ValueError:
        print("Ошибка: start и end должны быть целыми числами.")
        return 1

    # Дебаг режим включён для аналогичного поведения
    interpreter = Interpret(binary_file, result_file, start, end, debug=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
