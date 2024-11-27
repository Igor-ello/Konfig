import unittest
import tempfile
import os
from config_translator import ConfigTranslator


class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        """Создает временные файлы для тестов."""
        self.input_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
        self.output_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")

    def tearDown(self):
        """Удаляет временные файлы после каждого теста."""
        try:
            self.input_file.close()
            self.output_file.close()
            os.unlink(self.input_file.name)
            os.unlink(self.output_file.name)
        except PermissionError as e:
            print(f"Error cleaning up test files: {e}")

    def write_input(self, content):
        """Записывает контент во входной файл."""
        self.input_file.write(content)
        self.input_file.close()

    def read_output(self):
        """Читает содержимое выходного файла."""
        with open(self.output_file.name, "r", encoding="utf-8") as file:
            return file.read()

    def test_simple_translation(self):
        """Тест простого перевода YAML в учебный конфигурационный язык."""
        self.write_input("""
    name: example
    value: 42
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)
        translator.translate()
        output = self.read_output()

        expected_output = """name is example
value is 42"""
        self.assertEqual(output.strip(), expected_output.strip())

    def test_nested_structures(self):
        """Тест обработки вложенных структур (массивов и словарей)."""
        self.write_input("""
array:
  - 1
  - 2
  - 3
dictionary:
  key1: value1
  key2: value2
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)
        translator.translate()
        output = self.read_output()

        expected_output = """array is ( 1, 2, 3 )
dictionary is {
    key1 = value1,
    key2 = value2
}"""
        self.assertEqual(output.strip(), expected_output.strip())

    def test_constants(self):
        """Тест обработки констант."""
        self.write_input("""
constant: 100
reference: "^constant"
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)
        translator.translate()
        output = self.read_output()

        expected_output = """constant is 100
reference is 100"""
        self.assertEqual(output.strip(), expected_output.strip())

    def test_invalid_name(self):
        """Тест обработки некорректного имени."""
        self.write_input("""
invalid-name: value
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)

        with self.assertRaises(ValueError) as context:
            translator.translate()
        self.assertIn("Invalid name", str(context.exception))

    def test_undefined_constant(self):
        """Тест ссылки на неопределенную константу."""
        self.write_input("""
    reference: "^undefined_constant"
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)

        with self.assertRaises(ValueError) as context:
            translator.translate()
        self.assertIn("Undefined constant", str(context.exception))

    def test_complex_case(self):
        """Тест сложного случая с вложенными структурами и константами."""
        self.write_input("""
constant: 5
nested:
  array:
    - "^constant"
    - 10
  dict:
    key: "^constant"
        """)
        translator = ConfigTranslator(self.input_file.name, self.output_file.name)
        translator.translate()
        output = self.read_output()

        expected_output = """constant is 5
nested is {
    array = ( 5, 10 ),
    dict = {
        key = 5
    }
}"""
        self.assertEqual(output.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
