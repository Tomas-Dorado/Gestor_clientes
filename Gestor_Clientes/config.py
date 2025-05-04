import sys

DATABASE_PATH = 'Datos/clientes.csv'
if "pytest" in sys.argv[0]:
    DATABASE_PATH = 'tests/clientes_test.csv'