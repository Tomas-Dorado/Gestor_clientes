from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from Gestor_Clientes import database as db

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
        for cliente in db.Clientes.lista: 
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
            


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()