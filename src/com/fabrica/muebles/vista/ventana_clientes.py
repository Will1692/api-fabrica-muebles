import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import sys
from pathlib import Path
from PIL import Image, ImageTk
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.cliente_dao import ClienteDAO
from com.fabrica.muebles.modelo.cliente import Cliente


class VentanaClientes:
    def __init__(self, root=None):
        self.ventana = tk.Toplevel(root) if root else tk.Tk()
        self.dao = ClienteDAO()
        self.cliente_seleccionado = None
        self.tabla_visible = False
        self.ruta_foto = None
        self.inicializar()

    def inicializar(self):
        self.ventana.title("Gestión de Clientes - Fábrica de Muebles")
        self.ventana.geometry("1300x540")  # ← Reducido porque observaciones es 1 línea
        self.ventana.configure(bg="#ECF0F1")
        self.centrar_ventana()
        self.crear_panel_superior()
        self.crear_formulario()
        self.crear_panel_busqueda()
        self.crear_botones()
        self.crear_panel_resultados()

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() - 1300) // 2
        y = (self.ventana.winfo_screenheight() - 540) // 2
        self.ventana.geometry(f'1300x540+{x}+{y}')

    def crear_panel_superior(self):
        panel = tk.Frame(self.ventana, bg="#2C3E50", height=80)
        panel.pack(fill=tk.X, side=tk.TOP)
        panel.pack_propagate(False)
        tk.Label(panel, text="GESTIÓN DE CLIENTES", font=("Arial", 20, "bold"),
                 bg="#2C3E50", fg="white").pack(pady=20)

    def crear_formulario(self):
        frame = tk.LabelFrame(self.ventana, text="Datos del Cliente", font=("Arial", 12, "bold"),
                              bg="#ECF0F1", fg="#2C3E50", padx=20, pady=15)
        frame.pack(fill=tk.X, padx=20, pady=10)
        grid = tk.Frame(frame, bg="#ECF0F1")
        grid.pack(fill=tk.X)

        self.tipo_doc_var = tk.StringVar(value="CC")

        campos = {
            0: [("Nombre:", "nombre", 30, 0, 1, "#E74C3C"),
                ("Tipo Doc:", None, None, 2, 3, "#E74C3C"),
                ("Núm. Documento:", "num_documento", 18, 4, 5, "#E74C3C")],
            1: [("Teléfono:", "telefono", 18, 0, 1, "#E74C3C"),
                ("Dirección:", "direccion", 25, 2, 3, "#E74C3C"),
                ("Email:", "email", 25, 4, 5, "#E74C3C")],
            2: [("Código Mueble:", "codigo_mueble", 15, 0, 1, "#E74C3C"),
                ("Tipo Mueble:", "tipo_mueble", 20, 2, 3, "#E74C3C"),
                ("Cantidad:", "cantidad", 8, 4, 5, "#E74C3C"),
                ("Valor:", "valor_mueble", 12, 6, 7, "#E74C3C")]
        }

        for row, items in campos.items():
            for label, campo, ancho, col_lbl, col_entry, color in items:
                tk.Label(grid, text=label, font=("Arial", 10, "bold"),
                         bg="#ECF0F1", fg=color).grid(row=row, column=col_lbl, sticky="w", padx=5, pady=8)

                if campo == "cantidad":
                    self.txt_cantidad = tk.Entry(grid, font=("Arial", 10), width=ancho)
                    self.txt_cantidad.insert(0, "1")
                    self.txt_cantidad.grid(row=row, column=col_entry, padx=5, pady=8, sticky="w")
                elif campo:
                    entry = tk.Entry(grid, font=("Arial", 10), width=ancho)
                    entry.grid(row=row, column=col_entry, padx=5, pady=8, sticky="ew" if ancho > 15 else "w")
                    setattr(self, f"txt_{campo}", entry)
                else:
                    frame_tipo = tk.Frame(grid, bg="#ECF0F1")
                    frame_tipo.grid(row=row, column=col_entry, sticky="w", padx=5, pady=8)
                    for txt, val, pad in [("C.C", "CC", 10), ("NIT", "NIT", 0)]:
                        tk.Radiobutton(frame_tipo, text=txt, variable=self.tipo_doc_var, value=val,
                                       bg="#ECF0F1", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, pad))

        # Foto del mueble
        tk.Label(grid, text="Foto del Mueble:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").grid(row=3, column=0, sticky="w", padx=5, pady=8)
        frame_foto = tk.Frame(grid, bg="#ECF0F1")
        frame_foto.grid(row=3, column=1, columnspan=5, sticky="w", padx=5, pady=8)
        tk.Button(frame_foto, text="Cargar Foto", bg="#3498DB", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=self.cargar_foto).pack(side=tk.LEFT, padx=(0, 10))
        self.lbl_foto = tk.Label(frame_foto, text="No se ha seleccionado foto",
                                 font=("Arial", 9, "italic"), bg="#ECF0F1", fg="#7F8C8D")
        self.lbl_foto.pack(side=tk.LEFT)

        # ✅ NUEVO: Campo de Observaciones (Entry de 1 línea)
        tk.Label(grid, text="Observaciones:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#9B59B6").grid(row=4, column=0, sticky="w", padx=5, pady=8)
        self.txt_observaciones = tk.Entry(grid, font=("Arial", 10), width=95)
        self.txt_observaciones.grid(row=4, column=1, columnspan=7, padx=5, pady=8, sticky="ew")

        for i in [1, 3, 5]:
            grid.columnconfigure(i, weight=1)

    def crear_panel_busqueda(self):
        frame = tk.LabelFrame(self.ventana, text="Búsqueda de Cliente",
                              font=("Arial", 11, "bold"), bg="#ECF0F1", fg="#2C3E50", padx=15, pady=10)
        frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        grid = tk.Frame(frame, bg="#ECF0F1")
        grid.pack(fill=tk.X)

        tk.Label(grid, text="Buscar por:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.criterio_busqueda = ttk.Combobox(grid, font=("Arial", 10), width=20,
                                              state="readonly", values=["Nombre", "Número de Documento"])
        self.criterio_busqueda.current(0)
        self.criterio_busqueda.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(grid, text="Valor:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.txt_busqueda = tk.Entry(grid, font=("Arial", 10), width=30)
        self.txt_busqueda.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.txt_busqueda.bind('<Return>', lambda e: self.buscar_cliente())

        tk.Button(grid, text="BUSCAR", bg="#9B59B6", fg="white",
                  font=("Arial", 10, "bold"), width=12, cursor="hand2",
                  command=self.buscar_cliente).grid(row=0, column=4, padx=10, pady=5)
        grid.columnconfigure(3, weight=1)

    def crear_botones(self):
        frame = tk.Frame(self.ventana, bg="#ECF0F1")
        frame.pack(fill=tk.X, padx=20, pady=10)

        botones = [("NUEVO", "#3498DB", self.nuevo), ("GUARDAR", "#27AE60", self.guardar),
                   ("MODIFICAR", "#F39C12", self.modificar), ("ELIMINAR", "#E74C3C", self.eliminar),
                   ("LIMPIAR", "#95A5A6", self.limpiar_formulario)]

        for texto, color, comando in botones:
            tk.Button(frame, text=texto, bg=color, fg="white", font=("Arial", 10, "bold"),
                      width=10, height=1, cursor="hand2", command=comando).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="SALIR", bg="#34495E", fg="white", font=("Arial", 10, "bold"),
                  width=10, height=1, cursor="hand2", command=self.salir).pack(side=tk.RIGHT, padx=5)

    def crear_panel_resultados(self):
        """Panel con scroll para mostrar tarjetas de clientes"""
        self.frame_resultados = tk.LabelFrame(self.ventana, text="Resultados de Búsqueda",
                                              font=("Arial", 12, "bold"), bg="#ECF0F1",
                                              fg="#2C3E50", padx=10, pady=10)

        # Canvas con scroll
        canvas = tk.Canvas(self.frame_resultados, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_resultados, orient="vertical", command=canvas.yview)
        self.frame_tarjetas = tk.Frame(canvas, bg="#FFFFFF")

        self.frame_tarjetas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas_resultados = canvas

    def cargar_foto(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar foto del mueble",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos", "*.*")])
        if archivo:
            self.ruta_foto = archivo
            self.lbl_foto.config(text=f"📷 {os.path.basename(archivo)}", fg="#27AE60")

    def buscar_cliente(self):
        criterio = self.criterio_busqueda.get()
        valor = self.txt_busqueda.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Ingrese un valor para buscar")
            return

        clientes = self.dao.consultar_todos()
        resultados = [c for c in clientes if
                      (criterio == "Nombre" and valor.lower() in c.nombre.lower()) or
                      (criterio != "Nombre" and valor in str(getattr(c, 'numero_documento', '')))]

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron clientes con ese criterio")
            return

        self.mostrar_resultados(resultados)
        messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} cliente(s)")

    def mostrar_resultados(self, clientes):
        """Muestra los clientes en tarjetas con foto"""
        # Limpiar tarjetas anteriores
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        for idx, cliente in enumerate(clientes):
            self.crear_tarjeta_cliente(cliente, idx)

        if not self.tabla_visible:
            self.frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
            self.ventana.geometry("1300x920")  # ← Ajustado
            self.tabla_visible = True

    def crear_tarjeta_cliente(self, cliente, idx):
        """Crea una tarjeta visual para un cliente"""
        # Frame principal de la tarjeta
        tarjeta = tk.Frame(self.frame_tarjetas, bg="#FFFFFF", relief=tk.RAISED, bd=2)
        tarjeta.pack(fill=tk.X, padx=10, pady=10)

        # Frame izquierdo (Foto)
        frame_izq = tk.Frame(tarjeta, bg="#FFFFFF", width=150)
        frame_izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        frame_izq.pack_propagate(False)

        # Cargar y mostrar foto
        foto_label = tk.Label(frame_izq, bg="#E8E8E8", text="Sin foto\n📷",
                              font=("Arial", 10), fg="#7F8C8D")

        if hasattr(cliente, 'ruta_foto') and cliente.ruta_foto and os.path.exists(cliente.ruta_foto):
            try:
                img = Image.open(cliente.ruta_foto)
                img.thumbnail((140, 140))
                photo = ImageTk.PhotoImage(img)
                foto_label.config(image=photo, text="")
                foto_label.image = photo  # Mantener referencia
            except:
                pass

        foto_label.pack(expand=True, fill=tk.BOTH)

        # Frame derecho (Datos)
        frame_der = tk.Frame(tarjeta, bg="#FFFFFF")
        frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Fila 1: Datos principales
        fila1 = tk.Frame(frame_der, bg="#FFFFFF")
        fila1.pack(fill=tk.X, pady=5)

        datos_fila1 = [
            ("Código Mueble:", getattr(cliente, 'codigo_mueble', cliente.id_cliente), "#E74C3C"),
            ("Nombre:", cliente.nombre, "#2C3E50"),
            ("Tipo Doc:", getattr(cliente, 'tipo_documento', 'CC'), "#7F8C8D"),
            ("Núm. Doc:", getattr(cliente, 'numero_documento', 'N/A'), "#7F8C8D")
        ]

        for label, valor, color in datos_fila1:
            tk.Label(fila1, text=label, font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg=color).pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(fila1, text=valor, font=("Arial", 9),
                     bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        # Fila 2: Contacto
        fila2 = tk.Frame(frame_der, bg="#FFFFFF")
        fila2.pack(fill=tk.X, pady=5)

        datos_fila2 = [
            ("Teléfono:", cliente.telefono, "#27AE60"),
            ("Email:", cliente.email, "#3498DB"),
            ("Dirección:", cliente.direccion, "#7F8C8D")
        ]

        for label, valor, color in datos_fila2:
            tk.Label(fila2, text=label, font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg=color).pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(fila2, text=valor, font=("Arial", 9),
                     bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        # Fila 3: Mueble
        fila3 = tk.Frame(frame_der, bg="#FFFFFF")
        fila3.pack(fill=tk.X, pady=5)

        datos_fila3 = [
            ("Tipo Mueble:", getattr(cliente, 'tipo_mueble_vendido', 'N/A'), "#9B59B6"),
            ("Cantidad:", getattr(cliente, 'cantidad', '1'), "#F39C12"),
            ("Valor:", f"${getattr(cliente, 'valor_mueble', '0')}", "#27AE60"),
            ("Fecha:", cliente.fecha_registro, "#7F8C8D")
        ]

        for label, valor, color in datos_fila3:
            tk.Label(fila3, text=label, font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg=color).pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(fila3, text=valor, font=("Arial", 9),
                     bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        # ✅ NUEVO: Fila 4 - Observaciones (si existen)
        if hasattr(cliente, 'observaciones') and cliente.observaciones:
            fila4 = tk.Frame(frame_der, bg="#FFFFFF")
            fila4.pack(fill=tk.X, pady=5)

            tk.Label(fila4, text="Observaciones:", font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg="#9B59B6").pack(side=tk.LEFT, padx=(0, 5), anchor="nw")
            tk.Label(fila4, text=cliente.observaciones, font=("Arial", 9),
                     bg="#FFFFFF", wraplength=900, justify="left").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Botones de acción
        btn_frame = tk.Frame(frame_der, bg="#FFFFFF")
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="SELECCIONAR", bg="#3498DB", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda: self.seleccionar_cliente_tarjeta(cliente)).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(btn_frame, text="❌ QUITAR DE LA LISTA", bg="#E74C3C", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda t=tarjeta: self.ocultar_tarjeta(t)).pack(side=tk.LEFT)

    def seleccionar_cliente_tarjeta(self, cliente):
        """Selecciona un cliente desde la tarjeta"""
        self.cliente_seleccionado = cliente
        self.cargar_datos_formulario()
        messagebox.showinfo("✅ Cliente Cargado",
                            f"Datos de {cliente.nombre} cargados en el formulario.\n\n"
                            f"Revise los campos de arriba para ver los datos.")

    def ocultar_tarjeta(self, tarjeta):
        """Oculta una tarjeta de los resultados sin eliminar el cliente de la BD"""
        tarjeta.pack_forget()
        tarjeta.destroy()

    def cargar_datos_formulario(self):
        if not self.cliente_seleccionado:
            return

        cliente = self.cliente_seleccionado

        # Limpiar campos
        for campo in ['codigo_mueble', 'nombre', 'num_documento', 'telefono',
                      'direccion', 'email', 'tipo_mueble', 'valor_mueble']:
            if hasattr(self, f'txt_{campo}'):
                getattr(self, f'txt_{campo}').delete(0, tk.END)

        self.txt_cantidad.delete(0, tk.END)
        self.txt_observaciones.delete(0, tk.END)  # ← Limpiar observaciones (Entry)

        # Cargar datos
        campos = {
            'codigo_mueble': getattr(cliente, 'codigo_mueble', ''),
            'nombre': cliente.nombre or "",
            'telefono': cliente.telefono or "",
            'direccion': cliente.direccion or "",
            'email': cliente.email or "",
            'num_documento': getattr(cliente, 'numero_documento', ''),
            'tipo_mueble': getattr(cliente, 'tipo_mueble_vendido', ''),
            'cantidad': getattr(cliente, 'cantidad', '1'),
            'valor_mueble': getattr(cliente, 'valor_mueble', '')
        }

        for campo, valor in campos.items():
            if campo == 'cantidad':
                self.txt_cantidad.insert(0, str(valor))
            elif hasattr(self, f'txt_{campo}'):
                getattr(self, f'txt_{campo}').insert(0, str(valor))

        self.tipo_doc_var.set(getattr(cliente, 'tipo_documento', 'CC'))

        # ✅ Cargar observaciones
        if hasattr(cliente, 'observaciones') and cliente.observaciones:
            self.txt_observaciones.insert(0, cliente.observaciones)

        # Cargar foto
        foto = getattr(cliente, 'ruta_foto', None)
        if foto:
            self.ruta_foto = foto
            self.lbl_foto.config(text=f"📷 {os.path.basename(foto)}", fg="#27AE60")

    def nuevo(self):
        self.limpiar_formulario()
        self.txt_nombre.focus()  # ✅ CORREGIDO: era txt_codigo_mueble.focus()
        messagebox.showinfo("Nuevo Cliente", "Ingrese los datos del nuevo cliente")

    def guardar(self):
        if not self.validar_formulario():
            return
        if not messagebox.askyesno("Confirmar", "¿Desea guardar este cliente?"):
            return

        cliente = Cliente(
            nombre=self.txt_nombre.get().strip(),
            telefono=self.txt_telefono.get().strip(),
            direccion=self.txt_direccion.get().strip(),
            email=self.txt_email.get().strip(),
            fecha_registro=date.today())

        cliente.codigo_mueble = self.txt_codigo_mueble.get().strip()
        cliente.tipo_documento = self.tipo_doc_var.get()
        cliente.numero_documento = self.txt_num_documento.get().strip()
        cliente.tipo_mueble_vendido = self.txt_tipo_mueble.get().strip()
        cliente.cantidad = self.txt_cantidad.get().strip()
        cliente.valor_mueble = self.txt_valor_mueble.get().strip()
        cliente.ruta_foto = self.ruta_foto
        cliente.observaciones = self.txt_observaciones.get().strip()  # ✅ NUEVO (Entry)

        if self.dao.insertar_cliente(cliente):
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def modificar(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente")
            return
        if not self.validar_formulario():
            return
        if not messagebox.askyesno("Confirmar", "¿Desea modificar este cliente?"):
            return

        attrs = {
            'codigo_mueble': self.txt_codigo_mueble.get().strip(),
            'nombre': self.txt_nombre.get().strip(),
            'telefono': self.txt_telefono.get().strip(),
            'direccion': self.txt_direccion.get().strip(),
            'email': self.txt_email.get().strip(),
            'tipo_documento': self.tipo_doc_var.get(),
            'numero_documento': self.txt_num_documento.get().strip(),
            'tipo_mueble_vendido': self.txt_tipo_mueble.get().strip(),
            'cantidad': self.txt_cantidad.get().strip(),
            'valor_mueble': self.txt_valor_mueble.get().strip(),
            'ruta_foto': self.ruta_foto,
            'observaciones': self.txt_observaciones.get().strip()  # ✅ NUEVO (Entry)
        }

        for attr, val in attrs.items():
            setattr(self.cliente_seleccionado, attr, val)

        if self.dao.actualizar_cliente(self.cliente_seleccionado):
            messagebox.showinfo("Éxito", "Cliente modificado correctamente")
            if self.tabla_visible:
                self.buscar_cliente()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo modificar el cliente")

    def eliminar(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente")
            return

        if messagebox.askyesno("Confirmar",
                               f"¿Eliminar al cliente:\n\n{self.cliente_seleccionado.nombre}?\n\nEsta acción no se puede deshacer."):
            if self.dao.eliminar_cliente(self.cliente_seleccionado.id_cliente):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                if self.tabla_visible:
                    self.buscar_cliente()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")

    def validar_formulario(self):
        campos = [
            (self.txt_codigo_mueble, "código del mueble"),
            (self.txt_nombre, "nombre"),
            (self.txt_num_documento, "número de documento"),
            (self.txt_telefono, "teléfono"),
            (self.txt_email, "email"),
            (self.txt_tipo_mueble, "tipo de mueble"),
            (self.txt_cantidad, "cantidad"),
            (self.txt_valor_mueble, "valor del mueble")
        ]

        for campo, nombre in campos:
            if not campo.get().strip():
                messagebox.showwarning("Validación", f"El campo {nombre} es obligatorio")
                campo.focus()
                return False

        try:
            int(self.txt_cantidad.get().strip())
        except ValueError:
            messagebox.showwarning("Validación", "La cantidad debe ser un número")
            return False

        try:
            float(self.txt_valor_mueble.get().strip())
        except ValueError:
            messagebox.showwarning("Validación", "El valor del mueble debe ser un número")
            return False

        return True

    def limpiar_formulario(self):
        for campo in ['codigo_mueble', 'nombre', 'num_documento', 'telefono',
                      'direccion', 'email', 'tipo_mueble', 'valor_mueble']:
            if hasattr(self, f'txt_{campo}'):
                getattr(self, f'txt_{campo}').delete(0, tk.END)

        self.txt_cantidad.delete(0, tk.END)
        self.txt_cantidad.insert(0, "1")
        self.txt_observaciones.delete(0, tk.END)  # ✅ Limpiar observaciones (Entry)
        self.tipo_doc_var.set("CC")
        self.txt_busqueda.delete(0, tk.END)
        self.cliente_seleccionado = None
        self.ruta_foto = None
        self.lbl_foto.config(text="No se ha seleccionado foto", fg="#7F8C8D")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir de la gestión de clientes?"):
            self.ventana.destroy()

    def mostrar(self):
        self.ventana.mainloop()


def main():
    app = VentanaClientes()
    app.mostrar()


if __name__ == "__main__":
    main()