import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.proveedor_dao import ProveedorDAO
from com.fabrica.muebles.modelo.proveedor import Proveedor


class VentanaProveedores:

    def __init__(self, parent=None):
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.dao = ProveedorDAO()
        self.inicializar()
        self.cargar()

    def inicializar(self):
        self.ventana.title("Gestion de Proveedores")
        self.ventana.geometry("900x600")
        x = (self.ventana.winfo_screenwidth() - 900) // 2
        y = (self.ventana.winfo_screenheight() - 600) // 2
        self.ventana.geometry(f"900x600+{x}+{y}")
        self.ventana.resizable(False, False)

        frm = tk.LabelFrame(self.ventana, text="Datos del Proveedor", font=("Arial", 12, "bold"))
        frm.pack(pady=10, padx=10, fill="x")

        tk.Label(frm, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        self.txt_id = tk.Entry(frm, width=15, state="disabled")
        self.txt_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frm, text="Nombre:").grid(row=0, column=2, padx=10, pady=5)
        self.txt_nombre = tk.Entry(frm, width=30)
        self.txt_nombre.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frm, text="Contacto:").grid(row=1, column=0, padx=10, pady=5)
        self.txt_contacto = tk.Entry(frm, width=15)
        self.txt_contacto.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frm, text="Telefono:").grid(row=1, column=2, padx=10, pady=5)
        self.txt_telefono = tk.Entry(frm, width=30)
        self.txt_telefono.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(frm, text="Direccion:").grid(row=2, column=0, padx=10, pady=5)
        self.txt_direccion = tk.Entry(frm, width=15)
        self.txt_direccion.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frm, text="Correo:").grid(row=2, column=2, padx=10, pady=5)
        self.txt_correo = tk.Entry(frm, width=30)
        self.txt_correo.grid(row=2, column=3, padx=10, pady=5)

        frm2 = tk.LabelFrame(self.ventana, text="Lista de Proveedores", font=("Arial", 12, "bold"))
        frm2.pack(pady=10, padx=10, fill="both", expand=True)

        cols = ("ID", "Nombre", "Contacto", "Telefono", "Direccion", "Correo")
        self.tabla = ttk.Treeview(frm2, columns=cols, show="headings", height=15)
        for col in cols:
            self.tabla.heading(col, text=col)
        self.tabla.column("ID", width=50)
        self.tabla.bind("<ButtonRelease-1>", lambda e: self.seleccionar())
        self.tabla.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(frm2, orient="vertical", command=self.tabla.yview).pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=ttk.Scrollbar(frm2).set)

        frm3 = tk.Frame(self.ventana)
        frm3.pack(pady=10)
        tk.Button(frm3, text="Guardar", bg="#4CAF50", fg="white", width=12, command=self.guardar).pack(side="left",
                                                                                                       padx=5)
        tk.Button(frm3, text="Actualizar", bg="#2196F3", fg="white", width=12, command=self.actualizar).pack(
            side="left", padx=5)
        tk.Button(frm3, text="Eliminar", bg="#F44336", fg="white", width=12, command=self.eliminar).pack(side="left",
                                                                                                         padx=5)
        tk.Button(frm3, text="Limpiar", bg="#9E9E9E", fg="white", width=12, command=self.limpiar).pack(side="left",
                                                                                                       padx=5)
        tk.Button(frm3, text="Refrescar", bg="#9C27B0", fg="white", width=12, command=self.cargar).pack(side="left",
                                                                                                        padx=5)

    def cargar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for p in self.dao.listar():
            self.tabla.insert("", "end", values=(p.id, p.nombre, p.contacto, p.telefono, p.direccion, p.correo))

    def seleccionar(self):
        if self.tabla.selection():
            v = self.tabla.item(self.tabla.selection()[0])['values']
            self.txt_id.config(state="normal")
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, v[0])
            self.txt_id.config(state="disabled")
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, v[1])
            self.txt_contacto.delete(0, tk.END)
            self.txt_contacto.insert(0, v[2])
            self.txt_telefono.delete(0, tk.END)
            self.txt_telefono.insert(0, v[3])
            self.txt_direccion.delete(0, tk.END)
            self.txt_direccion.insert(0, v[4])
            self.txt_correo.delete(0, tk.END)
            self.txt_correo.insert(0, v[5])

    def guardar(self):
        if not self.txt_nombre.get().strip():
            messagebox.showwarning("Validacion", "El nombre es obligatorio")
            return
        p = Proveedor(nombre=self.txt_nombre.get(), contacto=self.txt_contacto.get(),
                      telefono=self.txt_telefono.get(), direccion=self.txt_direccion.get(),
                      correo=self.txt_correo.get())
        if self.dao.agregar(p):
            messagebox.showinfo("Exito", "Proveedor agregado")
            self.limpiar()
            self.cargar()

    def actualizar(self):
        if not self.txt_id.get():
            messagebox.showwarning("Validacion", "Seleccione un proveedor")
            return
        p = Proveedor(int(self.txt_id.get()), self.txt_nombre.get(), self.txt_contacto.get(),
                      self.txt_telefono.get(), self.txt_direccion.get(), self.txt_correo.get())
        if self.dao.actualizar(p):
            messagebox.showinfo("Exito", "Proveedor actualizado")
            self.limpiar()
            self.cargar()

    def eliminar(self):
        if not self.txt_id.get():
            messagebox.showwarning("Validacion", "Seleccione un proveedor")
            return
        if messagebox.askyesno("Confirmar", "Eliminar este proveedor?"):
            if self.dao.eliminar(int(self.txt_id.get())):
                messagebox.showinfo("Exito", "Proveedor eliminado")
                self.limpiar()
                self.cargar()

    def limpiar(self):
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="disabled")
        self.txt_nombre.delete(0, tk.END)
        self.txt_contacto.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_direccion.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)


if __name__ == "__main__":
    v = VentanaProveedores()
    v.ventana.mainloop()