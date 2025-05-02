from Cliente import Cliente

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
            
    