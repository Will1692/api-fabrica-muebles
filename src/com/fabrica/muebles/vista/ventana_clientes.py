import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.cliente_dao import ClienteDAO
from com.fabrica.muebles.modelo.cliente import Cliente


class VentanaClientes:
    """
    Ventana de Gestion de Clientes
    CRUD completo con interfaz grafica

    Autor: William Alonso Samaca Lopez
    """

    def __init__(self, parent=None):
        if parent:
            self.ventana = tk.Toplevel(parent)
        else:
            self.ventana = tk.Tk()
        self.cliente_dao = ClienteDAO()
        self.id_cliente_seleccionado = None
        self.inicializar_componentes()
        self.cargar_datos()

    def inicializar_componentes(self):
        self.ventana.title("Gestion de Clientes")
        self.ventana.geometry("900x600")
        self.ventana.resizable(False, False)

        ancho = 900
        alto = 600
        x = (self.ventana.winfo_screenwidth() - ancho) // 2
        y = (self.ventana.winfo_screenheight() - alto) // 2
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        panel_form = self.crear_panel_formulario()
        panel_form.pack(pady=10, padx=10, fill="x")

        panel_tabla = self.crear_panel_tabla()
        panel_tabla.pack(pady=10, padx=10, fill="both", expand=True)

        panel_botones = self.crear_panel_botones()
        panel_botones.pack(pady=10, padx=10, fill="x")

    def crear_panel_formulario(self):
        frame = tk.LabelFrame(self.ventana, text="Datos del Cliente", font=("Arial", 12, "bold"))

        tk.Label(frame, text="Nombre:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.txt_nombre = tk.Entry(frame, font=("Arial", 10), width=30)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Telefono:", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.txt_telefono = tk.Entry(frame, font=("Arial", 10), width=30)
        self.txt_telefono.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frame, text="Direccion:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txt_direccion = tk.Entry(frame, font=("Arial", 10), width=30)
        self.txt_direccion.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Email:", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.txt_email = tk.Entry(frame, font=("Arial", 10), width=30)
        self.txt_email.grid(row=1, column=3, padx=10, pady=5)

        return frame

    def crear_panel_tabla(self):
        frame = tk.LabelFrame(self.ventana, text="Lista de Clientes", font=("Arial", 12, "bold"))

        columnas = ("ID", "Nombre", "Telefono", "Direccion", "Email", "Fecha", "Estado")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=15)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Telefono", text="Telefono")
        self.tabla.heading("Direccion", text="Direccion")
        self.tabla.heading("Email", text="Email")
        self.tabla.heading("Fecha", text="Fecha Registro")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Telefono", width=100)
        self.tabla.column("Direccion", width=150)
        self.tabla.column("Email", width=150)
        self.tabla.column("Fecha", width=100, anchor="center")
        self.tabla.column("Estado", width=80, anchor="center")

        self.tabla.bind("<ButtonRelease-1>", lambda e: self.seleccionar_fila())

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        return frame

    def crear_panel_botones(self):
        frame = tk.Frame(self.ventana, bg="#F0F0F0")

        self.btn_guardar = tk.Button(frame, text="Guardar", bg="#2ECC71", fg="white",
                                     font=("Arial", 12, "bold"), width=12, cursor="hand2",
                                     command=self.guardar_cliente)
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_actualizar = tk.Button(frame, text="Actualizar", bg="#3498DB", fg="white",
                                        font=("Arial", 12, "bold"), width=12, cursor="hand2",
                                        command=self.actualizar_cliente, state="disabled")
        self.btn_actualizar.pack(side="left", padx=5)

        self.btn_eliminar = tk.Button(frame, text="Eliminar", bg="#E74C3C", fg="white",
                                      font=("Arial", 12, "bold"), width=12, cursor="hand2",
                                      command=self.eliminar_cliente, state="disabled")
        self.btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = tk.Button(frame, text="Limpiar", bg="#95A5A6", fg="white",
                                font=("Arial", 12, "bold"), width=12, cursor="hand2",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)

        btn_refrescar = tk.Button(frame, text="Refrescar", bg="#9B59B6", fg="white",
                                  font=("Arial", 12, "bold"), width=12, cursor="hand2",
                                  command=self.cargar_datos)
        btn_refrescar.pack(side="left", padx=5)

        return frame

    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        lista_clientes = self.cliente_dao.consultar_todos()

        for cliente in lista_clientes:
            self.tabla.insert("", "end", values=(
                cliente.id_cliente,
                cliente.nombre,
                cliente.telefono,
                cliente.direccion,
                cliente.email,
                cliente.fecha_registro,
                cliente.get_estado_texto()
            ))

    def seleccionar_fila(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item['values']

            self.id_cliente_seleccionado = valores[0]
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, valores[1])
            self.txt_telefono.delete(0, tk.END)
            self.txt_telefono.insert(0, valores[2])
            self.txt_direccion.delete(0, tk.END)
            self.txt_direccion.insert(0, valores[3])
            self.txt_email.delete(0, tk.END)
            self.txt_email.insert(0, valores[4])

            self.btn_guardar.config(state="disabled")
            self.btn_actualizar.config(state="normal")
            self.btn_eliminar.config(state="normal")

    def guardar_cliente(self):
        if self.validar_campos():
            cliente = Cliente(
                nombre=self.txt_nombre.get().strip(),
                telefono=self.txt_telefono.get().strip(),
                direccion=self.txt_direccion.get().strip(),
                email=self.txt_email.get().strip()
            )

            if self.cliente_dao.insertar_cliente(cliente):
                messagebox.showinfo("Exito", "Cliente guardado correctamente")
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "Error al guardar el cliente")

    def actualizar_cliente(self):
        if self.id_cliente_seleccionado and self.validar_campos():
            cliente = self.cliente_dao.consultar_por_id(self.id_cliente_seleccionado)

            if cliente:
                cliente.nombre = self.txt_nombre.get().strip()
                cliente.telefono = self.txt_telefono.get().strip()
                cliente.direccion = self.txt_direccion.get().strip()
                cliente.email = self.txt_email.get().strip()

                if self.cliente_dao.actualizar_cliente(cliente):
                    messagebox.showinfo("Exito", "Cliente actualizado correctamente")
                    self.limpiar_formulario()
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "Error al actualizar el cliente")

    def eliminar_cliente(self):
        if self.id_cliente_seleccionado:
            respuesta = messagebox.askyesno("Confirmar", "Esta seguro de eliminar este cliente?")

            if respuesta:
                if self.cliente_dao.eliminar_cliente(self.id_cliente_seleccionado):
                    messagebox.showinfo("Exito", "Cliente eliminado correctamente")
                    self.limpiar_formulario()
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "Error al eliminar el cliente")

    def limpiar_formulario(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_direccion.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.id_cliente_seleccionado = None

        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

        self.btn_guardar.config(state="normal")
        self.btn_actualizar.config(state="disabled")
        self.btn_eliminar.config(state="disabled")

    def validar_campos(self):
        if not self.txt_nombre.get().strip():
            messagebox.showwarning("Validacion", "El nombre es obligatorio")
            self.txt_nombre.focus()
            return False
        if not self.txt_telefono.get().strip():
            messagebox.showwarning("Validacion", "El telefono es obligatorio")
            self.txt_telefono.focus()
            return False
        return True

    def mostrar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    ventana = VentanaClientes()
    ventana.mostrar()