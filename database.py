#Este archivo es el que se encarga de la base de datos

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
    @staticmethod
    def buscar(dni):
        for cliente in Cliente.lista_clientes:
            if cliente.dni == dni:
                return cliente
        return None
    
    @staticmethod
    def crear(nombre, apellido, dni):
        cliente = Cliente(nombre, apellido, dni)
        Cliente.lista_clientes.append(cliente)
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Cliente.lista_clientes):
            if cliente.dni == dni:
                Clientes.lista_clientes[i].nombre = nombre
                Clientes.lista_clientes[i].apellido = apellido
                return Clientes.lista_clientes[i]
            
    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Cliente.lista_clientes):
            if cliente.dni == dni:
                cliente = Cliente.lista_clientes.pop(i)
                return cliente