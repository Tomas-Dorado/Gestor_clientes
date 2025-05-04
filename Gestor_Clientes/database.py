#Este archivo es el que se encarga de la base de datos
import csv

class Cliente:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}, DNI: {self.dni}"
    
class Clientes:
    #Lista clientes
    lista_clientes = []
    with open("clientes.csv", newline="\n") as fichero:
        reader = csv.reader(fichero, delimiter=";")
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista_clientes.append(cliente)

    @staticmethod
    def guardar():
        with open("clientes.csv", "w", newline="\n") as fichero:
            writer = csv.writer(fichero, delimiter=";")
            for cliente in Clientes.lista_clientes:
                writer.writerow([cliente.dni, cliente.nombre, cliente.apellido])
    
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista_clientes:
            if cliente.dni == dni:
                return cliente
        return None
    
    @staticmethod
    def crear(nombre, apellido, dni):
        cliente = Cliente(nombre, apellido, dni)
        Clientes.lista_clientes.append(cliente)
        Clientes.guardar()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista_clientes):
            if cliente.dni == dni:
                Clientes.lista_clientes[i].nombre = nombre
                Clientes.lista_clientes[i].apellido = apellido
                Clientes.guardar()
                return Clientes.lista_clientes[i]
            
    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista_clientes):
            if cliente.dni == dni:
                cliente = Clientes.lista_clientes.pop(i)
                Clientes.guardar()
                return cliente