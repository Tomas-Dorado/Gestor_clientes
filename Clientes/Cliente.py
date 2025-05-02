class Cliente:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}, DNI: {self.dni}"
    
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