import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.proveedor_dao import ProveedorDAO
from com.fabrica.muebles.modelo.proveedor import Proveedor


class VentanaProveedores:
    """
    Ventana de gestión de proveedores con diseño moderno
    Estilo: Búsqueda con tarjetas visuales
    Autor: William Alonso Samaca Lopez
    """

    def __init__(self, parent=None):
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.ventana.title("Gestión de Proveedores - Fábrica de Muebles")
        self.ventana.geometry("1300x600")

        # Centrar ventana
        x = (self.ventana.winfo_screenwidth() - 1300) // 2
        y = (self.ventana.winfo_screenheight() - 600) // 2
        self.ventana.geometry(f"1300x600+{x}+{y}")

        self.dao = ProveedorDAO()
        self.proveedor_seleccionado = None
        self.resultados_visible = False

        self.crear_header()
        self.crear_formulario()
        self.crear_panel_busqueda()
        self.crear_botones()
        self.crear_frame_resultados()

    def crear_header(self):
        """Crea el encabezado con título"""
        panel = tk.Frame(self.ventana, bg="#2C3E50", height=80)
        panel.pack(fill=tk.X)
        panel.pack_propagate(False)
        tk.Label(panel, text="GESTIÓN DE PROVEEDORES", font=("Arial", 20, "bold"),
                 bg="#2C3E50", fg="white").pack(pady=20)

    def crear_formulario(self):
        """Crea el formulario de datos del proveedor"""
        frame = tk.LabelFrame(self.ventana, text="Datos del Proveedor", font=("Arial", 12, "bold"),
                              bg="#ECF0F1", fg="#2C3E50", padx=20, pady=15)
        frame.pack(fill=tk.X, padx=20, pady=10)

        grid = tk.Frame(frame, bg="#ECF0F1")
        grid.pack(fill=tk.X)

        # Fila 1: Nombre, Contacto, Teléfono
        tk.Label(grid, text="Nombre Proveedor:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.txt_nombre = tk.Entry(grid, font=("Arial", 10), width=35)
        self.txt_nombre.grid(row=0, column=1, columnspan=2, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Contacto:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=3, sticky="w", padx=5, pady=8)
        self.txt_contacto = tk.Entry(grid, font=("Arial", 10), width=25)
        self.txt_contacto.grid(row=0, column=4, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Teléfono:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=5, sticky="w", padx=5, pady=8)
        self.txt_telefono = tk.Entry(grid, font=("Arial", 10), width=18)
        self.txt_telefono.grid(row=0, column=6, padx=5, pady=8, sticky="ew")

        # Fila 2: Dirección, Correo
        tk.Label(grid, text="Dirección:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.txt_direccion = tk.Entry(grid, font=("Arial", 10), width=50)
        self.txt_direccion.grid(row=1, column=1, columnspan=3, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Correo:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=1, column=4, sticky="w", padx=5, pady=8)
        self.txt_correo = tk.Entry(grid, font=("Arial", 10), width=30)
        self.txt_correo.grid(row=1, column=5, columnspan=2, padx=5, pady=8, sticky="ew")

    def crear_panel_busqueda(self):
        """Crea el panel de búsqueda"""
        frame = tk.LabelFrame(self.ventana, text="Búsqueda de Proveedores",
                              font=("Arial", 12, "bold"), bg="#ECF0F1", fg="#2C3E50",
                              padx=20, pady=10)
        frame.pack(fill=tk.X, padx=20, pady=10)

        frame_contenido = tk.Frame(frame, bg="#ECF0F1")
        frame_contenido.pack(fill=tk.X)

        # Criterio de búsqueda
        tk.Label(frame_contenido, text="Buscar por:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").pack(side=tk.LEFT, padx=(0, 10))

        self.criterio_busqueda = ttk.Combobox(frame_contenido, font=("Arial", 10),
                                              width=20, state="readonly",
                                              values=["Nombre Proveedor", "Teléfono"])
        self.criterio_busqueda.current(0)
        self.criterio_busqueda.pack(side=tk.LEFT, padx=(0, 20))

        # Campo de búsqueda
        tk.Label(frame_contenido, text="Valor:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").pack(side=tk.LEFT, padx=(0, 10))

        self.txt_busqueda = tk.Entry(frame_contenido, font=("Arial", 10), width=50)
        self.txt_busqueda.pack(side=tk.LEFT, padx=(0, 20))
        self.txt_busqueda.bind("<Return>", lambda e: self.buscar_proveedor())

        # Botón buscar
        tk.Button(frame_contenido, text="BUSCAR", bg="#9B59B6", fg="white",
                  font=("Arial", 10, "bold"), cursor="hand2", width=15,
                  command=self.buscar_proveedor).pack(side=tk.LEFT)

    def crear_botones(self):
        """Crea los botones de acción"""
        frame = tk.Frame(self.ventana, bg="#ECF0F1")
        frame.pack(fill=tk.X, padx=20, pady=10)

        botones = [
            ("NUEVO", "#3498DB", self.nuevo),
            ("GUARDAR", "#27AE60", self.guardar),
            ("MODIFICAR", "#F39C12", self.modificar),
            ("ELIMINAR", "#E74C3C", self.eliminar),
            ("LIMPIAR", "#95A5A6", self.limpiar_formulario),
            ("SALIR", "#34495E", self.salir)
        ]

        for texto, color, comando in botones:
            tk.Button(frame, text=texto, bg=color, fg="white",
                      font=("Arial", 10, "bold"), cursor="hand2",
                      width=12, command=comando).pack(side=tk.LEFT, padx=5)

    def crear_frame_resultados(self):
        """Crea el frame para mostrar resultados de búsqueda"""
        self.frame_resultados = tk.LabelFrame(self.ventana, text="Resultados de Búsqueda",
                                              font=("Arial", 12, "bold"), bg="#ECF0F1",
                                              fg="#2C3E50", padx=10, pady=10)

        # Canvas con scrollbar para tarjetas
        canvas = tk.Canvas(self.frame_resultados, bg="#ECF0F1", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_resultados, orient="vertical", command=canvas.yview)

        self.frame_tarjetas = tk.Frame(canvas, bg="#ECF0F1")

        canvas.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame_tarjetas.bind("<Configure>",
                                 lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def buscar_proveedor(self):
        """Busca proveedores según criterio"""
        criterio = self.criterio_busqueda.get()
        valor = self.txt_busqueda.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Ingrese un valor para buscar")
            return

        proveedores = self.dao.listar()
        resultados = []

        for p in proveedores:
            if criterio == "Nombre Proveedor":
                if valor.lower() in p.nombre.lower():
                    resultados.append(p)
            elif criterio == "Teléfono":
                if valor in str(p.telefono):
                    resultados.append(p)

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron proveedores con ese criterio")
            return

        self.mostrar_resultados(resultados)
        messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} proveedor(es)")

    def mostrar_resultados(self, proveedores):
        """Muestra los resultados en tarjetas"""
        # Limpiar tarjetas anteriores
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        # Mostrar frame de resultados
        if not self.resultados_visible:
            self.frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            self.ventana.geometry("1300x900")
            self.resultados_visible = True

        # Crear tarjeta para cada proveedor
        for idx, proveedor in enumerate(proveedores):
            self.crear_tarjeta_proveedor(proveedor, idx)

    def crear_tarjeta_proveedor(self, proveedor, idx):
        """Crea una tarjeta visual para un proveedor"""
        tarjeta = tk.Frame(self.frame_tarjetas, bg="#FFFFFF", relief=tk.RAISED, bd=2)
        tarjeta.pack(fill=tk.X, padx=10, pady=10)

        frame_contenido = tk.Frame(tarjeta, bg="#FFFFFF")
        frame_contenido.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Fila 1: ID, Nombre, Contacto
        fila1 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila1.pack(fill=tk.X, pady=5)

        tk.Label(fila1, text="ID:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#E74C3C").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila1, text=proveedor.id, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila1, text="Proveedor:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#2C3E50").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila1, text=proveedor.nombre, font=("Arial", 9, "bold"),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila1, text="Contacto:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#8E44AD").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila1, text=proveedor.contacto, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT)

        # Fila 2: Teléfono, Correo
        fila2 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila2.pack(fill=tk.X, pady=5)

        tk.Label(fila2, text="📞 Teléfono:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#27AE60").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila2, text=proveedor.telefono, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila2, text="📧 Correo:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#3498DB").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila2, text=proveedor.correo, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT)

        # Fila 3: Dirección
        fila3 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila3.pack(fill=tk.X, pady=5)

        tk.Label(fila3, text="📍 Dirección:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#F39C12").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila3, text=proveedor.direccion, font=("Arial", 9),
                 bg="#FFFFFF", wraplength=800, justify="left").pack(side=tk.LEFT)

        # Fila 4: Botones
        fila4 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila4.pack(fill=tk.X, pady=(10, 0))

        tk.Button(fila4, text="SELECCIONAR", bg="#3498DB", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda p=proveedor: self.seleccionar_proveedor_tarjeta(p)).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(fila4, text="❌ QUITAR DE LA LISTA", bg="#E74C3C", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda: self.ocultar_tarjeta(tarjeta)).pack(side=tk.LEFT)

    def seleccionar_proveedor_tarjeta(self, proveedor):
        """Selecciona un proveedor de la tarjeta y carga sus datos"""
        self.proveedor_seleccionado = proveedor
        self.cargar_datos_formulario()
        messagebox.showinfo("Selección", f"Proveedor seleccionado: {proveedor.nombre}")

    def ocultar_tarjeta(self, tarjeta):
        """Oculta una tarjeta de la lista"""
        tarjeta.pack_forget()
        tarjeta.destroy()

    def cargar_datos_formulario(self):
        """Carga los datos del proveedor seleccionado en el formulario"""
        if not self.proveedor_seleccionado:
            return

        p = self.proveedor_seleccionado

        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, p.nombre)

        self.txt_contacto.delete(0, tk.END)
        self.txt_contacto.insert(0, p.contacto)

        self.txt_telefono.delete(0, tk.END)
        self.txt_telefono.insert(0, p.telefono)

        self.txt_direccion.delete(0, tk.END)
        self.txt_direccion.insert(0, p.direccion)

        self.txt_correo.delete(0, tk.END)
        self.txt_correo.insert(0, p.correo)

    def validar_formulario(self):
        """Valida que los campos obligatorios estén llenos"""
        if not self.txt_nombre.get().strip():
            messagebox.showwarning("Validación", "El nombre del proveedor es obligatorio")
            self.txt_nombre.focus()
            return False
        if not self.txt_telefono.get().strip():
            messagebox.showwarning("Validación", "El teléfono es obligatorio")
            self.txt_telefono.focus()
            return False
        return True

    def nuevo(self):
        """Limpia el formulario para nuevo registro"""
        self.limpiar_formulario()
        self.txt_nombre.focus()

    def guardar(self):
        """Guarda un nuevo proveedor"""
        if not self.validar_formulario():
            return

        if not messagebox.askyesno("Confirmar", "¿Desea guardar este proveedor?"):
            return

        proveedor = Proveedor(
            nombre=self.txt_nombre.get().strip(),
            contacto=self.txt_contacto.get().strip(),
            telefono=self.txt_telefono.get().strip(),
            direccion=self.txt_direccion.get().strip(),
            correo=self.txt_correo.get().strip()
        )

        if self.dao.agregar(proveedor):
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente")
            self.limpiar_formulario()
            if self.resultados_visible:
                self.buscar_proveedor()
        else:
            messagebox.showerror("Error", "No se pudo guardar el proveedor")

    def modificar(self):
        """Modifica el proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un proveedor")
            return

        if not self.validar_formulario():
            return

        if not messagebox.askyesno("Confirmar", "¿Desea modificar este proveedor?"):
            return

        self.proveedor_seleccionado.nombre = self.txt_nombre.get().strip()
        self.proveedor_seleccionado.contacto = self.txt_contacto.get().strip()
        self.proveedor_seleccionado.telefono = self.txt_telefono.get().strip()
        self.proveedor_seleccionado.direccion = self.txt_direccion.get().strip()
        self.proveedor_seleccionado.correo = self.txt_correo.get().strip()

        if self.dao.actualizar(self.proveedor_seleccionado):
            messagebox.showinfo("Éxito", "Proveedor modificado correctamente")
            if self.resultados_visible:
                self.buscar_proveedor()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo modificar el proveedor")

    def eliminar(self):
        """Elimina el proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un proveedor")
            return

        if not messagebox.askyesno("Confirmar",
                                   f"¿Está seguro de eliminar al proveedor '{self.proveedor_seleccionado.nombre}'?"):
            return

        if self.dao.eliminar(self.proveedor_seleccionado.id):
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            if self.resultados_visible:
                self.buscar_proveedor()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el proveedor")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.txt_nombre.delete(0, tk.END)
        self.txt_contacto.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_direccion.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_busqueda.delete(0, tk.END)
        self.proveedor_seleccionado = None

    def salir(self):
        """Cierra la ventana"""
        if messagebox.askyesno("Salir", "¿Desea salir de la gestión de proveedores?"):
            self.ventana.destroy()

    def mostrar(self):
        """Muestra la ventana"""
        self.ventana.mainloop()


if __name__ == "__main__":
    ventana = VentanaProveedores()
    ventana.mostrar()