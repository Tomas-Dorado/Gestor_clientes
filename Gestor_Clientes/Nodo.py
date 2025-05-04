class Nodo:
    def __init__(self, cliente):
        self.cliente = cliente
        self.siguiente = None
        
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  # Primer nodo de la lista

    def agregar(self, cliente):
        nuevo_nodo = Nodo(cliente)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar(self, dni):
        actual = self.cabeza
        anterior = None
        while actual and actual.cliente.dni != dni:
            anterior = actual
            actual = actual.siguiente
        if not actual:
            return False  # Cliente no encontrado
        if not anterior:
            self.cabeza = actual.siguiente  # Eliminar el primer nodo
        else:
            anterior.siguiente = actual.siguiente  # Saltar el nodo actual
        return True

    def buscar(self, dni):
        actual = self.cabeza
        while actual:
            if actual.cliente.dni == dni:
                return actual.cliente
            actual = actual.siguiente
        return None

    def listar(self):
        clientes = []
        actual = self.cabeza
        while actual:
            clientes.append(actual.cliente)
            actual = actual.siguiente
        return clientes
    