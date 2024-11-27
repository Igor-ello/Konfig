
### Описание команд:
- **Конвертация файлов**:
  - `python config_translator.py --input <путь к файлу>.yaml --output <путь к выходному файлу>.txt`: Запуск инструмента для конвертации YAML в формат учебного языка.

  - `python config_translator.py --input db_config.yaml --output db_config_translated.txt`
  - `python config_translator.py --input network_config.yaml --output network_config_translated.txt`
`
- **Запуск тестов**:
  - `python -m unittest test_config_translator.py`: Запуск юнит-тестов для проверки корректности работы преобразования.
