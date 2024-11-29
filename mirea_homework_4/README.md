python -m unittest tests/tests.py

python assembler.py files/input.asm files/output.bin files/log.txt

python interpreter.py files/output.bin files/result.csv 0 1024 