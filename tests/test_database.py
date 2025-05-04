import copy
import unittest
import helpers
import csv
from Gestor_Clientes import database as db


class Testdatabase(unittest.TestCase):
    def setUp(self):
        db.Clientes.lista_clientes = [
            db.Cliente("Alice", "Smith", "12345678"),
            db.Cliente("Bob", "Johnson", "87654321"),
            db.Cliente("Charlie", "Brown", "11223344")
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar("87654321")
        cliente_no_existente = db.Clientes.buscar("87654343")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_no_existente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('Héctor', 'Costa', "34665453")
        self.assertEqual(len(db.Clientes.lista_clientes), 4)
        self.assertEqual(nuevo_cliente.dni, '34665453')
        self.assertEqual(nuevo_cliente.nombre, 'Héctor')
        self.assertEqual(nuevo_cliente.apellido, 'Costa')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('87654321'))
        cliente_modificado = db.Clientes.modificar('87654321', 'Mariana', 'Gonzalez')
        self.assertEqual(cliente_a_modificar.nombre, 'Bob')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar("12345678")
        cliente_rebuscado = db.Clientes.buscar("12345678")
        self.assertNotEqual(cliente_borrado, cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista_clientes))
        self.assertFalse(helpers.dni_valido('23223S', db.Clientes.lista_clientes))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista_clientes))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista_clientes))

    def test_escritura_csv(self):
        db.Clientes.guardar()
        with open(db.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            lineas = list(reader)
            self.assertEqual(len(lineas), 4)
            self.assertEqual(lineas[0], ['12345678', 'Alice', 'Smith'])
            self.assertEqual(lineas[1], ['87654321', 'Bob', 'Johnson'])
            self.assertEqual(lineas[2], ['11223344', 'Charlie', 'Brown'])
            self.assertEqual(lineas[3], ['34665453', 'Héctor', 'Costa'])

if __name__ == '__main__':
    unittest.main()