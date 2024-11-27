import argparse
import yaml
import re


class ConfigTranslator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.constants = {}

    def validate_name(self, name):
        """Проверяет, соответствует ли имя требованиям синтаксиса."""
        pattern = r'^[_a-zA-Z][_a-zA-Z0-9]*$'  # Разрешить строчные буквы
        if not re.match(pattern, name):
            raise ValueError(f"Invalid name: {name}")

    def translate_value(self, value, indent=0):
        """Преобразует значение с учётом вложенности и форматирования."""
        spacing = " " * indent
        if isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            translated_items = ", ".join(self.translate_value(item) for item in value)
            return f"( {translated_items} )"
        elif isinstance(value, dict):
            translated_items = ",\n".join(
                f"{spacing}    {self.translate_name(key)} = {self.translate_value(val, indent + 4)}"
                for key, val in value.items()
            )
            return f"{{\n{translated_items}\n{spacing}}}"
        elif isinstance(value, str):
            # Если строка — это ссылка на константу
            if value.startswith("^"):
                const_name = value[1:]
                if const_name not in self.constants:
                    raise ValueError(f"Undefined constant: {const_name}")
                return str(self.constants[const_name])
            # Простая строка
            return value  # Убираем кавычки
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def translate_name(self, name):
        """Переводит имя, проверяя его синтаксис."""
        self.validate_name(name)
        return name

    def translate(self):
        """Выполняет основное преобразование."""
        with open(self.input_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        result = []
        for key, value in data.items():
            self.validate_name(key)
            if isinstance(value, str) and value.startswith("^"):
                const_name = value[1:]
                if const_name not in self.constants:
                    raise ValueError(f"Undefined constant: {const_name}")
                result.append(f"{key} is {self.constants[const_name]}")
            else:
                translated_value = self.translate_value(value)
                result.append(f"{key} is {translated_value}")
                if isinstance(value, (int, float)):
                    self.constants[key] = value

        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(result))

    @staticmethod
    def parse_args():
        """Разбирает аргументы командной строки."""
        parser = argparse.ArgumentParser(description="YAML to Config Translator")
        parser.add_argument("-i", "--input", required=True, help="Input YAML file")
        parser.add_argument("-o", "--output", required=True, help="Output file")
        return parser.parse_args()


if __name__ == "__main__":
    args = ConfigTranslator.parse_args()
    translator = ConfigTranslator(args.input, args.output)
    try:
        translator.translate()
    except Exception as e:
        print(f"Error: {e}")
