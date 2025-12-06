import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.produccion_dao import ProduccionDAO
from com.fabrica.muebles.modelo.produccion import Produccion


class VentanaProduccion:

    def __init__(self, parent=None):
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.dao = ProduccionDAO()
        self.inicializar()
        self.cargar()

    def inicializar(self):
        self.ventana.title("Gestion de Produccion - Fabrica de Muebles")
        self.ventana.geometry("900x600")
        x = (self.ventana.winfo_screenwidth() - 900) // 2
        y = (self.ventana.winfo_screenheight() - 600) // 2
        self.ventana.geometry(f"900x600+{x}+{y}")
        self.ventana.resizable(False, False)

        frm = tk.LabelFrame(self.ventana, text="Datos de Produccion", font=("Arial", 12, "bold"))
        frm.pack(pady=10, padx=10, fill="x")

        tk.Label(frm, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        self.txt_id = tk.Entry(frm, width=15, state="disabled")
        self.txt_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frm, text="Nombre Producto:").grid(row=0, column=2, padx=10, pady=5)
        self.txt_nombre = tk.Entry(frm, width=30)
        self.txt_nombre.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frm, text="Cantidad:").grid(row=1, column=0, padx=10, pady=5)
        self.txt_cantidad = tk.Entry(frm, width=15)
        self.txt_cantidad.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frm, text="Fecha Inicio (YYYY-MM-DD):").grid(row=1, column=2, padx=10, pady=5)
        self.txt_fecha_inicio = tk.Entry(frm, width=30)
        self.txt_fecha_inicio.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(frm, text="Fecha Fin (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.txt_fecha_fin = tk.Entry(frm, width=15)
        self.txt_fecha_fin.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frm, text="Estado:").grid(row=2, column=2, padx=10, pady=5)
        self.txt_estado = tk.Entry(frm, width=30)
        self.txt_estado.grid(row=2, column=3, padx=10, pady=5)

        frm2 = tk.LabelFrame(self.ventana, text="Lista de Produccion", font=("Arial", 12, "bold"))
        frm2.pack(pady=10, padx=10, fill="both", expand=True)

        cols = ("ID", "Producto", "Cantidad", "Inicio", "Fin", "Estado")
        self.tabla = ttk.Treeview(frm2, columns=cols, show="headings", height=15)
        for col in cols:
            self.tabla.heading(col, text=col)
        self.tabla.column("ID", width=50)
        self.tabla.column("Cantidad", width=80)
        self.tabla.column("Inicio", width=100)
        self.tabla.column("Fin", width=100)
        self.tabla.bind("<ButtonRelease-1>", lambda e: self.seleccionar())
        self.tabla.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(frm2, orient="vertical", command=self.tabla.yview).pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=ttk.Scrollbar(frm2).set)

        frm3 = tk.Frame(self.ventana)
        frm3.pack(pady=10)
        tk.Button(frm3, text="Agregar", bg="#4CAF50", fg="white", width=12, command=self.agregar).pack(side="left",
                                                                                                       padx=5)
        tk.Button(frm3, text="Actualizar", bg="#2196F3", fg="white", width=12, command=self.actualizar).pack(
            side="left", padx=5)
        tk.Button(frm3, text="Eliminar", bg="#F44336", fg="white", width=12, command=self.eliminar).pack(side="left",
                                                                                                         padx=5)
        tk.Button(frm3, text="Finalizar", bg="#FFC107", fg="black", width=12, command=self.finalizar).pack(side="left",
                                                                                                           padx=5)
        tk.Button(frm3, text="Limpiar", bg="#9E9E9E", fg="white", width=12, command=self.limpiar).pack(side="left",
                                                                                                       padx=5)

    def cargar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for p in self.dao.consultar_todos():
            self.tabla.insert("", "end",
                              values=(p.id, p.nombre_producto, p.cantidad, p.fecha_inicio, p.fecha_fin or "", p.estado))

    def seleccionar(self):
        if self.tabla.selection():
            v = self.tabla.item(self.tabla.selection()[0])['values']
            self.txt_id.config(state="normal")
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, v[0])
            self.txt_id.config(state="disabled")
            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, v[1])
            self.txt_cantidad.delete(0, tk.END)
            self.txt_cantidad.insert(0, v[2])
            self.txt_fecha_inicio.delete(0, tk.END)
            self.txt_fecha_inicio.insert(0, v[3])
            self.txt_fecha_fin.delete(0, tk.END)
            self.txt_fecha_fin.insert(0, v[4])
            self.txt_estado.delete(0, tk.END)
            self.txt_estado.insert(0, v[5])

    def agregar(self):
        try:
            p = Produccion(
                nombre_producto=self.txt_nombre.get(),
                cantidad=int(self.txt_cantidad.get()),
                fecha_inicio=self.txt_fecha_inicio.get(),
                fecha_fin=self.txt_fecha_fin.get() or None,
                estado=self.txt_estado.get()
            )
            if self.dao.insertar_produccion(p):
                messagebox.showinfo("Exito", "Produccion agregada correctamente")
                self.limpiar()
                self.cargar()
        except Exception as e:
            messagebox.showerror("Error", f"Datos invalidos: {str(e)}")

    def actualizar(self):
        if not self.txt_id.get():
            messagebox.showwarning("Validacion", "Seleccione un registro para actualizar")
            return
        try:
            p = Produccion(
                id=int(self.txt_id.get()),
                nombre_producto=self.txt_nombre.get(),
                cantidad=int(self.txt_cantidad.get()),
                fecha_inicio=self.txt_fecha_inicio.get(),
                fecha_fin=self.txt_fecha_fin.get() or None,
                estado=self.txt_estado.get()
            )
            if self.dao.actualizar_produccion(p):
                messagebox.showinfo("Exito", "Produccion actualizada correctamente")
                self.limpiar()
                self.cargar()
        except Exception as e:
            messagebox.showerror("Error", f"Datos invalidos: {str(e)}")

    def eliminar(self):
        if not self.txt_id.get():
            messagebox.showwarning("Validacion", "Seleccione una produccion para eliminar")
            return
        if messagebox.askyesno("Confirmar", "Desea eliminar esta produccion?"):
            if self.dao.eliminar_produccion(int(self.txt_id.get())):
                messagebox.showinfo("Exito", "Produccion eliminada correctamente")
                self.limpiar()
                self.cargar()

    def finalizar(self):
        if not self.txt_id.get():
            messagebox.showwarning("Validacion", "Seleccione una produccion para finalizar")
            return
        if self.dao.finalizar_produccion(int(self.txt_id.get())):
            messagebox.showinfo("Exito", "Produccion finalizada exitosamente")
            self.limpiar()
            self.cargar()

    def limpiar(self):
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="disabled")
        self.txt_nombre.delete(0, tk.END)
        self.txt_cantidad.delete(0, tk.END)
        self.txt_fecha_inicio.delete(0, tk.END)
        self.txt_fecha_fin.delete(0, tk.END)
        self.txt_estado.delete(0, tk.END)


if __name__ == "__main__":
    v = VentanaProduccion()
    v.ventana.mainloop()