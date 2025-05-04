import re
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from Gestor_Clientes import database as db
from Gestor_Clientes import helpers


class CenterWidgetMixin: 
    def center(self):  # Quita la coma extra
        self.update() 
        w = self.winfo_width() 
        h = self.winfo_height() 
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight() 
        x = int((ws/2) - (w/2)) 
        y = int((hs/2) - (h/2)) 
        self.geometry(f"{w}x{h}+{x}+{y}")
        
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self): 
        super().__init__() 
        self.title('Gestor de clientes') 
        self.build() 
        self.center()
        

    def build(self): 
        # Top Frame 
        frame = Frame(self) 
        frame.pack() 
        
        # Scrollbar 
        scrollbar = Scrollbar(frame) 
        scrollbar.pack(side=RIGHT, fill=Y) 
        
        # Treeview (¡definirlo una sola vez!)
        treeview = ttk.Treeview(frame, yscrollcommand=scrollbar.set) 
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido') 
        
        # Configurar columnas 
        treeview.column("#0", width=0, stretch=NO) 
        treeview.column("DNI", anchor=CENTER) 
        treeview.column("Nombre", anchor=CENTER) 
        treeview.column("Apellido", anchor=CENTER) 
        
        # Configurar cabeceras 
        treeview.heading("#0", anchor=CENTER) 
        treeview.heading("DNI", text="DNI", anchor=CENTER) 
        treeview.heading("Nombre", text="Nombre", anchor=CENTER) 
        treeview.heading("Apellido", text="Apellido", anchor=CENTER) 
        
        # Empaquetar Treeview 
        treeview.pack() 

        # Fill treeview data 
        for cliente in db.Clientes.lista_clientes: 
            treeview.insert( 
                parent='', index='end', iid=cliente.dni, 
                values=(cliente.dni, cliente.nombre, cliente.apellido)) 

        # Bottom Frame 
        frame = Frame(self) 
        frame.pack(pady=20) 
        
        # Buttons 
        Button(frame, text="Crear", command=self.create_client_window).grid(row=1, column=0) 
        Button(frame, text="Modificar", command=self.edit_client_window).grid(row=1, column=1) 
        Button(frame, text="Borrar", command=self.delete).grid(row=1, column=2) 

        # Export treeview to the class 
        self.treeview = treeview

    def delete(self): 
        cliente = self.treeview.focus() 
        if cliente: 
            campos = self.treeview.item(cliente, 'values') 
            confirmar = askokcancel( 
                title='Confirmación', 
                message=f'¿Borrar a {campos[1]} {campos[2]}?', 
                icon=WARNING
            ) 
            if confirmar: 
                self.treeview.delete(cliente)  # Eliminar de la interfaz
                db.Clientes.borrar(campos[0])  # Eliminar de la base de datos
    
    def create_client_window(self): 
        CreateClientWindow(self)

    def edit_client_window(self):
        if self.treeview.focus():  # Solo si hay un cliente seleccionado
            EditClientWindow(self)
            
class CreateClientWindow(Toplevel, CenterWidgetMixin): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.title('Crear cliente') 
        self.build() 
        self.center() 
        self.transient(parent)
        self.grab_set()

    def build(self): 
        # Top frame 
        frame = Frame(self) 
        frame.pack(padx=20, pady=10) 

        # Labels 
        Label(frame, text="DNI (2 números y 1 letra)").grid(row=0, column=0) 
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1) 
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2) 

        # Entries (¡convertirlos en atributos de clase!)
        self.dni = Entry(frame) 
        self.dni.grid(row=1, column=0) 
        self.dni.bind("<KeyRelease>", lambda ev: self.validate(ev, 0)) 
        
        self.nombre = Entry(frame) 
        self.nombre.grid(row=1, column=1) 
        self.nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 1)) 
        
        self.apellido = Entry(frame) 
        self.apellido.grid(row=1, column=2) 
        self.apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 2)) 

        # Bottom frame 
        frame = Frame(self) 
        frame.pack(pady=10) 

        # Botones
        crear = Button(frame, text="Crear", command=self.create_client) 
        crear.configure(state=NORMAL) 
        crear.grid(row=0, column=0) 
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1) 

        # Estado de validaciones y exportar botón
        self.validaciones = [False, False, False] 
        self.crear = crear

    def dni_valido(dni, lista_clientes):
        # Formato: 00A
        if not re.match(r'^\d{2}[A-Z]$', dni):
            return False
        
        # DNI único
        for cliente in lista_clientes:
            if cliente.dni == dni:
                return False
        return True

    def validate(self, event, index): 
        valor = event.widget.get()
        
        # Convertir DNI a mayúsculas
        if index == 0:
            valor = valor.upper()
            event.widget.delete(0, "end")
            event.widget.insert(0, valor)

        # Validar DNI (index 0) o campos de texto (index 1 y 2)
        if index == 0:
            valido = helpers.dni_valido(valor, db.Clientes.lista)
        else:
            valido = valor.isalpha() and 2 <= len(valor) <= 30
        
        event.widget.configure({"bg": "Green" if valido else "Red"}) 
        self.validaciones[index] = valido 
        self.crear.config(state=NORMAL if all(self.validaciones) else DISABLED)

    def create_client(self): 
        dni = self.dni.get().upper() 
        nombre = self.nombre.get().capitalize() 
        apellido = self.apellido.get().capitalize() 
        
        # Añadir a la base de datos 
        db.Clientes.crear(dni, nombre, apellido)
        
        # Actualizar Treeview (forzar refresco)
        self.master.treeview.insert(
            "", "end", iid=dni, 
            values=(dni, nombre, apellido)
        ) 
        self.master.treeview.update_idletasks()
        self.close()
        
class EditClientWindow(Toplevel, CenterWidgetMixin): 
    def __init__(self, parent): 
        super().__init__(parent) 
        self.title('Actualizar cliente') 
        self.build() 
        self.center() 
        # Obligar al usuario a interactuar con la subventana 
        self.transient(parent) 
        self.grab_set() 
    
    def build(self): 
        # Top frame 
        frame = Frame(self) 
        frame.pack(padx=20, pady=10) 
        
        # Labels 
        Label(frame, text="DNI (no editable)").grid(row=0, column=0) 
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, 
        column=1) 
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, 
        column=2) 
        
        # Entries 
        dni = Entry(frame) 
        dni.grid(row=1, column=0) 
        nombre = Entry(frame) 
        nombre.grid(row=1, column=1) 
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 0)) 
        apellido = Entry(frame) 
        apellido.grid(row=1, column=2) 
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 1)) 
        
        # Set entries initial values 
        cliente = self.master.treeview.focus() 
        campos = self.master.treeview.item(cliente, 'values') 
        dni.insert(0, campos[0]) 
        dni.config(state=DISABLED) 
        nombre.insert(0, campos[1]) 
        apellido.insert(0, campos[2]) 
        
        # Bottom frame 
        frame = Frame(self) 
        frame.pack(pady=10) 
        
        # Buttons 
        actualizar = Button(frame, text="Actualizar", 
        command=self.update_client) 
        actualizar.grid(row=0, column=0) 
        Button(frame, text="Cancelar", command=self.close).grid(row=0, 
        column=1) 
        
        # Update button activation 
        self.validaciones = [1, 1] # True, True 
        
        # Class exports 
        self.actualizar = actualizar 
        self.dni = dni 
        self.nombre = nombre 
        self.apellido = apellido 
    
    def validate(self, event, index): 
        valor = event.widget.get() 
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30) 
        event.widget.configure({"bg": "Green" if valido else "Red"}) 
        # Cambiar estado del botón en base a las validaciones 
        self.validaciones[index] = valido 
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED) 
    
    def update_client(self): 
        dni = self.dni.get()
        nuevo_nombre = self.nombre.get().capitalize()
        nuevo_apellido = self.apellido.get().capitalize()
        
        # Actualizar la base de datos
        db.Clientes.modificar(dni, nuevo_nombre, nuevo_apellido)  # <-- Nueva línea
        
        # Actualizar Treeview
        cliente = self.master.treeview.focus()
        self.master.treeview.item(
            cliente, 
            values=(dni, nuevo_nombre, nuevo_apellido)
        )
        self.close()
    
    def close(self): 
        self.destroy() 
        self.update()
        

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()