import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

try:
    from PIL import Image, ImageTk

    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False
    print("Pillow no está instalado. Las imágenes no se mostrarán en las tarjetas.")

from com.fabrica.muebles.dao.produccion_dao import ProduccionDAO
from com.fabrica.muebles.modelo.produccion import Produccion


class VentanaProduccion:
    def __init__(self, root=None):
        self.ventana = tk.Toplevel(root) if root else tk.Tk()
        self.dao = ProduccionDAO()
        self.produccion_seleccionada = None
        self.resultados_visible = False
        self.ruta_archivo = None
        self.inicializar()

    def inicializar(self):
        self.ventana.title("Gestión de Producción - Fábrica de Muebles")
        self.ventana.geometry("1300x520")
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
        y = (self.ventana.winfo_screenheight() - 520) // 2
        self.ventana.geometry(f'1300x520+{x}+{y}')

    def crear_panel_superior(self):
        panel = tk.Frame(self.ventana, bg="#2C3E50", height=80)
        panel.pack(fill=tk.X, side=tk.TOP)
        panel.pack_propagate(False)
        tk.Label(panel, text="GESTIÓN DE PRODUCCIÓN", font=("Arial", 20, "bold"),
                 bg="#2C3E50", fg="white").pack(pady=20)

    def crear_formulario(self):
        frame = tk.LabelFrame(self.ventana, text="Datos de Producción", font=("Arial", 12, "bold"),
                              bg="#ECF0F1", fg="#2C3E50", padx=20, pady=15)
        frame.pack(fill=tk.X, padx=20, pady=10)
        grid = tk.Frame(frame, bg="#ECF0F1")
        grid.pack(fill=tk.X)

        # Fila 1: Código Mueble, Nombre Cliente, Tipo Doc, Núm Doc
        tk.Label(grid, text="Código Mueble:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.txt_codigo = tk.Entry(grid, font=("Arial", 10), width=15)
        self.txt_codigo.grid(row=0, column=1, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Nombre Cliente:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=2, sticky="w", padx=5, pady=8)
        self.txt_nombre_cliente = tk.Entry(grid, font=("Arial", 10), width=30)
        self.txt_nombre_cliente.grid(row=0, column=3, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Tipo Doc:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=4, sticky="w", padx=5, pady=8)

        self.tipo_doc_cliente_var = tk.StringVar(value="CC")
        frame_tipo = tk.Frame(grid, bg="#ECF0F1")
        frame_tipo.grid(row=0, column=5, sticky="w", padx=5, pady=8)
        tk.Radiobutton(frame_tipo, text="C.C", variable=self.tipo_doc_cliente_var, value="CC",
                       bg="#ECF0F1", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(frame_tipo, text="NIT", variable=self.tipo_doc_cliente_var, value="NIT",
                       bg="#ECF0F1", font=("Arial", 9)).pack(side=tk.LEFT)

        tk.Label(grid, text="Núm. Doc:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=0, column=6, sticky="w", padx=5, pady=8)
        self.txt_num_doc_cliente = tk.Entry(grid, font=("Arial", 10), width=18)
        self.txt_num_doc_cliente.grid(row=0, column=7, padx=5, pady=8, sticky="ew")

        # Fila 2: Nombre Producto, Estado, Cantidad
        tk.Label(grid, text="Nombre Producto:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.txt_nombre = tk.Entry(grid, font=("Arial", 10), width=40)
        self.txt_nombre.grid(row=1, column=1, columnspan=3, padx=5, pady=8, sticky="ew")

        tk.Label(grid, text="Estado:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=1, column=4, sticky="w", padx=5, pady=8)
        self.combo_estado = ttk.Combobox(grid, font=("Arial", 10), width=15, state="readonly",
                                         values=["Ingreso", "En Fabricacion", "Finalizado", "Cancelado"])
        self.combo_estado.current(1)  # Por defecto "En Fabricacion"
        self.combo_estado.grid(row=1, column=5, padx=5, pady=8, sticky="w")

        tk.Label(grid, text="Cantidad:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=1, column=6, sticky="w", padx=5, pady=8)
        self.txt_cantidad = tk.Entry(grid, font=("Arial", 10), width=10)
        self.txt_cantidad.insert(0, "1")
        self.txt_cantidad.grid(row=1, column=7, padx=5, pady=8, sticky="w")

        # Fila 3: Foto/Plano, Fecha Inicio, Fecha Fin
        tk.Label(grid, text="Foto/Plano:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=2, column=0, sticky="w", padx=5, pady=8)

        frame_foto = tk.Frame(grid, bg="#ECF0F1")
        frame_foto.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=8)

        tk.Button(frame_foto, text="Cargar Archivo", bg="#3498DB", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=self.cargar_archivo).pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_archivo = tk.Label(frame_foto, text="No se ha seleccionado archivo",
                                    font=("Arial", 9, "italic"), bg="#ECF0F1", fg="#7F8C8D")
        self.lbl_archivo.pack(side=tk.LEFT)

        tk.Label(grid, text="Fecha Inicio:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=2, column=3, sticky="e", padx=(5, 2), pady=8)
        self.txt_fecha_inicio = tk.Entry(grid, font=("Arial", 10), width=12)
        self.txt_fecha_inicio.insert(0, date.today().strftime("%d-%m-%Y"))
        self.txt_fecha_inicio.grid(row=2, column=4, padx=(0, 5), pady=8, sticky="w")

        tk.Label(grid, text="Fecha Fin:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=2, column=5, sticky="e", padx=(5, 2), pady=8)
        self.txt_fecha_fin = tk.Entry(grid, font=("Arial", 10), width=12)
        self.txt_fecha_fin.grid(row=2, column=6, padx=(0, 5), pady=8, sticky="w")

        # Fila 4: Observaciones (2 líneas - más compacta)
        tk.Label(grid, text="Observaciones:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1", fg="#E74C3C").grid(row=3, column=0, sticky="nw", padx=5, pady=8)
        self.txt_observaciones = tk.Text(grid, font=("Arial", 10), width=95, height=2)
        self.txt_observaciones.grid(row=3, column=1, columnspan=7, padx=5, pady=8, sticky="ew")

        for i in [1, 3, 5]:
            grid.columnconfigure(i, weight=1)

    def crear_panel_busqueda(self):
        frame = tk.LabelFrame(self.ventana, text="Búsqueda de Producción",
                              font=("Arial", 11, "bold"), bg="#ECF0F1", fg="#2C3E50", padx=15, pady=10)
        frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        grid = tk.Frame(frame, bg="#ECF0F1")
        grid.pack(fill=tk.X)

        tk.Label(grid, text="Buscar por:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.criterio_busqueda = ttk.Combobox(grid, font=("Arial", 10), width=20,
                                              state="readonly",
                                              values=["Código Mueble", "Nombre Producto"])
        self.criterio_busqueda.current(0)
        self.criterio_busqueda.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(grid, text="Valor:", font=("Arial", 10, "bold"),
                 bg="#ECF0F1").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.txt_busqueda = tk.Entry(grid, font=("Arial", 10), width=30)
        self.txt_busqueda.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.txt_busqueda.bind('<Return>', lambda e: self.buscar_produccion())

        tk.Button(grid, text="BUSCAR", bg="#9B59B6", fg="white",
                  font=("Arial", 10, "bold"), width=12, cursor="hand2",
                  command=self.buscar_produccion).grid(row=0, column=4, padx=10, pady=5)
        grid.columnconfigure(3, weight=1)

    def crear_botones(self):
        frame = tk.Frame(self.ventana, bg="#ECF0F1")
        frame.pack(fill=tk.X, padx=20, pady=10)

        botones = [
            ("NUEVO", "#3498DB", self.nuevo),
            ("GUARDAR", "#27AE60", self.guardar),
            ("MODIFICAR", "#F39C12", self.modificar),
            ("ELIMINAR", "#E74C3C", self.eliminar),
            ("FINALIZAR", "#FFC107", self.finalizar),
            ("LIMPIAR", "#95A5A6", self.limpiar_formulario)
        ]

        for texto, color, comando in botones:
            tk.Button(frame, text=texto, bg=color, fg="white" if color != "#FFC107" else "black",
                      font=("Arial", 10, "bold"), width=10, height=1, cursor="hand2",
                      command=comando).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="SALIR", bg="#34495E", fg="white", font=("Arial", 10, "bold"),
                  width=10, height=1, cursor="hand2", command=self.salir).pack(side=tk.RIGHT, padx=5)

    def crear_panel_resultados(self):
        self.frame_resultados = tk.LabelFrame(self.ventana, text="Resultados de Búsqueda",
                                              font=("Arial", 12, "bold"), bg="#ECF0F1",
                                              fg="#2C3E50", padx=10, pady=10)

        canvas = tk.Canvas(self.frame_resultados, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_resultados, orient="vertical", command=canvas.yview)
        self.frame_tarjetas = tk.Frame(canvas, bg="#FFFFFF")

        self.frame_tarjetas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas_resultados = canvas

    def cargar_archivo(self):
        """Abre diálogo para seleccionar foto o plano"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar foto o plano del diseño",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                       ("PDFs", "*.pdf"),
                       ("Todos", "*.*")]
        )
        if archivo:
            self.ruta_archivo = archivo
            nombre_archivo = os.path.basename(archivo)
            self.lbl_archivo.config(text=f"📄 {nombre_archivo}", fg="#27AE60")

    def buscar_produccion(self):
        criterio = self.criterio_busqueda.get()
        valor = self.txt_busqueda.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Ingrese un valor para buscar")
            return

        producciones = self.dao.consultar_todos()
        resultados = []

        for p in producciones:
            if criterio == "Código Mueble":
                codigo = str(getattr(p, 'codigo_mueble', None) or p.id)
                if valor.lower() in codigo.lower():
                    resultados.append(p)
            elif criterio == "Nombre Producto":
                if valor.lower() in p.nombre_producto.lower():
                    resultados.append(p)

        if not resultados:
            messagebox.showinfo("Sin resultados", "No se encontraron producciones con ese criterio")
            return

        self.mostrar_resultados(resultados)
        messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} producción(es)")

    def mostrar_resultados(self, producciones):
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        for idx, prod in enumerate(producciones):
            self.crear_tarjeta_produccion(prod, idx)

        if not self.resultados_visible:
            self.frame_resultados.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
            self.ventana.geometry("1300x900")
            self.resultados_visible = True

    def crear_tarjeta_produccion(self, produccion, idx):
        tarjeta = tk.Frame(self.frame_tarjetas, bg="#FFFFFF", relief=tk.RAISED, bd=2)
        tarjeta.pack(fill=tk.X, padx=10, pady=10)

        # Frame principal con foto izquierda y datos derecha
        frame_principal = tk.Frame(tarjeta, bg="#FFFFFF")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Frame izquierdo para foto/plano (si existe y es imagen)
        mostrar_imagen = False
        if hasattr(produccion, 'ruta_archivo') and produccion.ruta_archivo and PIL_DISPONIBLE:
            extensiones_imagen = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
            if produccion.ruta_archivo.lower().endswith(extensiones_imagen):
                if os.path.exists(produccion.ruta_archivo):
                    mostrar_imagen = True
                    frame_foto = tk.Frame(frame_principal, bg="#FFFFFF", width=150, height=150)
                    frame_foto.pack(side=tk.LEFT, padx=(0, 15))
                    frame_foto.pack_propagate(False)

                    try:
                        img = Image.open(produccion.ruta_archivo)
                        img.thumbnail((140, 140))
                        photo = ImageTk.PhotoImage(img)
                        lbl_img = tk.Label(frame_foto, image=photo, bg="#FFFFFF", cursor="hand2")
                        lbl_img.image = photo  # Mantener referencia
                        lbl_img.pack(expand=True)

                        # Hacer la imagen clickeable para ampliar
                        lbl_img.bind("<Button-1>", lambda e, ruta=produccion.ruta_archivo: self.ampliar_imagen(ruta))

                        # Tooltip
                        tk.Label(frame_foto, text="Click para ampliar", font=("Arial", 7, "italic"),
                                 bg="#FFFFFF", fg="#7F8C8D").pack()
                    except Exception as e:
                        tk.Label(frame_foto, text="❌ Error\nal cargar", font=("Arial", 9),
                                 bg="#FFFFFF", fg="#E74C3C").pack(expand=True)

        # Frame derecho para información
        frame_contenido = tk.Frame(frame_principal, bg="#FFFFFF")
        frame_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Color según estado
        colores_estado = {
            "Ingreso": "#FFC107",
            "En Fabricacion": "#3498DB",
            "Finalizado": "#27AE60",
            "Cancelado": "#E74C3C"
        }
        color_estado = colores_estado.get(produccion.estado, "#95A5A6")

        # Fila 1: Código, Nombre Producto, Estado
        fila1 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila1.pack(fill=tk.X, pady=5)

        tk.Label(fila1, text="Código Mueble:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#E74C3C").pack(side=tk.LEFT, padx=(0, 5))
        codigo_mostrar = getattr(produccion, 'codigo_mueble', None) or f"ID-{produccion.id}"
        tk.Label(fila1, text=codigo_mostrar, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila1, text="Producto:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#2C3E50").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila1, text=produccion.nombre_producto, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila1, text="Estado:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg=color_estado).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila1, text=produccion.estado, font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg=color_estado).pack(side=tk.LEFT)

        # Fila 2: Cliente (si existe)
        if hasattr(produccion, 'nombre_cliente') and produccion.nombre_cliente:
            fila_cliente = tk.Frame(frame_contenido, bg="#FFFFFF")
            fila_cliente.pack(fill=tk.X, pady=5)

            tk.Label(fila_cliente, text="👤 Cliente:", font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg="#8E44AD").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(fila_cliente, text=produccion.nombre_cliente, font=("Arial", 9),
                     bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 15))

            if hasattr(produccion, 'tipo_documento_cliente') and produccion.tipo_documento_cliente:
                tk.Label(fila_cliente, text=produccion.tipo_documento_cliente + ":",
                         font=("Arial", 9, "bold"), bg="#FFFFFF", fg="#8E44AD").pack(side=tk.LEFT, padx=(0, 5))
                tk.Label(fila_cliente, text=getattr(produccion, 'numero_documento_cliente', 'N/A'),
                         font=("Arial", 9), bg="#FFFFFF").pack(side=tk.LEFT)

        # Fila 3: Cantidad, Fechas
        fila2 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila2.pack(fill=tk.X, pady=5)

        tk.Label(fila2, text="Cantidad:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#F39C12").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila2, text=produccion.cantidad, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila2, text="Inicio:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#7F8C8D").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(fila2, text=self.convertir_fecha_a_vista(produccion.fecha_inicio), font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(fila2, text="Fin:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#7F8C8D").pack(side=tk.LEFT, padx=(0, 5))
        fecha_fin_mostrar = self.convertir_fecha_a_vista(produccion.fecha_fin) if produccion.fecha_fin else "Pendiente"
        tk.Label(fila2, text=fecha_fin_mostrar, font=("Arial", 9),
                 bg="#FFFFFF").pack(side=tk.LEFT)

        # Fila 3: Observaciones
        fila3 = tk.Frame(frame_contenido, bg="#FFFFFF")
        fila3.pack(fill=tk.X, pady=5)

        tk.Label(fila3, text="Observaciones:", font=("Arial", 9, "bold"),
                 bg="#FFFFFF", fg="#9B59B6").pack(side=tk.LEFT, padx=(0, 5), anchor="nw")

        obs_text = getattr(produccion, 'observaciones', '') or 'Sin observaciones'

        tk.Label(fila3, text=obs_text, font=("Arial", 9),
                 bg="#FFFFFF", wraplength=950, justify="left").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Fila 4: Archivo (si existe y NO es imagen mostrada arriba)
        if hasattr(produccion, 'ruta_archivo') and produccion.ruta_archivo and not mostrar_imagen:
            fila4 = tk.Frame(frame_contenido, bg="#FFFFFF")
            fila4.pack(fill=tk.X, pady=5)

            tk.Label(fila4, text="📄 Archivo:", font=("Arial", 9, "bold"),
                     bg="#FFFFFF", fg="#3498DB").pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(fila4, text=os.path.basename(produccion.ruta_archivo), font=("Arial", 9),
                     bg="#FFFFFF").pack(side=tk.LEFT)

        # Botones
        btn_frame = tk.Frame(frame_contenido, bg="#FFFFFF")
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="SELECCIONAR", bg="#3498DB", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda: self.seleccionar_produccion_tarjeta(produccion)).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(btn_frame, text="❌ QUITAR DE LA LISTA", bg="#E74C3C", fg="white",
                  font=("Arial", 9, "bold"), cursor="hand2",
                  command=lambda t=tarjeta: self.ocultar_tarjeta(t)).pack(side=tk.LEFT)

    def seleccionar_produccion_tarjeta(self, produccion):
        self.produccion_seleccionada = produccion
        self.cargar_datos_formulario()
        messagebox.showinfo("✅ Producción Cargada",
                            f"Datos de {produccion.nombre_producto} cargados en el formulario.\n\n"
                            f"Revise los campos de arriba para ver los datos.")

    def ocultar_tarjeta(self, tarjeta):
        tarjeta.pack_forget()
        tarjeta.destroy()

    def ampliar_imagen(self, ruta_imagen):
        """Abre ventana modal para ver la imagen ampliada con zoom"""
        if not os.path.exists(ruta_imagen):
            messagebox.showerror("Error", "No se encuentra el archivo de imagen")
            return

        # Crear ventana modal
        ventana_img = tk.Toplevel(self.ventana)
        ventana_img.title("Vista ampliada - " + os.path.basename(ruta_imagen))
        ventana_img.configure(bg="#2C3E50")
        ventana_img.geometry("900x700")

        try:
            # Cargar imagen original
            img_original = Image.open(ruta_imagen)
            ancho_orig, alto_orig = img_original.size

            # Variables de control de zoom
            zoom_actual = {"nivel": 1.0, "img": None, "photo": None}

            # Frame superior con controles
            frame_controles = tk.Frame(ventana_img, bg="#34495E")
            frame_controles.pack(fill=tk.X, padx=20, pady=(20, 10))

            tk.Label(frame_controles, text="Zoom:", font=("Arial", 10, "bold"),
                     bg="#34495E", fg="white").pack(side=tk.LEFT, padx=(0, 10))

            # Botones de zoom
            btn_menos = tk.Button(frame_controles, text="➖ -", bg="#E74C3C", fg="white",
                                  font=("Arial", 10, "bold"), cursor="hand2", width=8)
            btn_menos.pack(side=tk.LEFT, padx=5)

            lbl_zoom = tk.Label(frame_controles, text="100%", font=("Arial", 10, "bold"),
                                bg="#34495E", fg="#3498DB", width=8)
            lbl_zoom.pack(side=tk.LEFT, padx=5)

            btn_mas = tk.Button(frame_controles, text="➕ +", bg="#27AE60", fg="white",
                                font=("Arial", 10, "bold"), cursor="hand2", width=8)
            btn_mas.pack(side=tk.LEFT, padx=5)

            btn_reset = tk.Button(frame_controles, text="🔄 Reset", bg="#95A5A6", fg="white",
                                  font=("Arial", 10, "bold"), cursor="hand2", width=10)
            btn_reset.pack(side=tk.LEFT, padx=5)

            # Frame contenedor con scroll
            frame_scroll = tk.Frame(ventana_img, bg="#2C3E50")
            frame_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Canvas con scrollbars
            canvas = tk.Canvas(frame_scroll, bg="#2C3E50", highlightthickness=0)
            scrollbar_v = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
            scrollbar_h = tk.Scrollbar(frame_scroll, orient="horizontal", command=canvas.xview)

            canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

            scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
            scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Label para la imagen
            lbl_img = tk.Label(canvas, bg="#2C3E50")
            canvas_window = canvas.create_window(0, 0, window=lbl_img, anchor="nw")

            # Variables para arrastrar
            drag_data = {"x": 0, "y": 0, "dragging": False}

            def on_mouse_press(event):
                """Inicia el arrastre"""
                canvas.scan_mark(event.x, event.y)
                drag_data["dragging"] = True
                canvas.config(cursor="fleur")  # Cursor de movimiento

            def on_mouse_drag(event):
                """Arrastra la imagen"""
                if drag_data["dragging"]:
                    canvas.scan_dragto(event.x, event.y, gain=1)

            def on_mouse_release(event):
                """Termina el arrastre"""
                drag_data["dragging"] = False
                canvas.config(cursor="")

            # Bind eventos de arrastre al canvas
            canvas.bind("<ButtonPress-1>", on_mouse_press)
            canvas.bind("<B1-Motion>", on_mouse_drag)
            canvas.bind("<ButtonRelease-1>", on_mouse_release)

            # También en el label de la imagen
            lbl_img.bind("<ButtonPress-1>", on_mouse_press)
            lbl_img.bind("<B1-Motion>", on_mouse_drag)
            lbl_img.bind("<ButtonRelease-1>", on_mouse_release)

            def actualizar_imagen(nivel_zoom):
                """Actualiza la imagen con el nivel de zoom especificado"""
                try:
                    # Calcular nuevo tamaño
                    nuevo_ancho = int(ancho_orig * nivel_zoom)
                    nuevo_alto = int(alto_orig * nivel_zoom)

                    # Redimensionar
                    img_zoom = img_original.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_zoom)

                    # Actualizar imagen
                    lbl_img.configure(image=photo)
                    lbl_img.image = photo  # Mantener referencia

                    # Actualizar área de scroll
                    canvas.configure(scrollregion=canvas.bbox("all"))

                    # Actualizar label de zoom
                    lbl_zoom.config(text=f"{int(nivel_zoom * 100)}%")

                    zoom_actual["nivel"] = nivel_zoom

                except Exception as e:
                    print(f"Error al actualizar zoom: {e}")

            def zoom_in():
                nuevo_nivel = zoom_actual["nivel"] * 1.2
                if nuevo_nivel <= 5.0:  # Máximo 500%
                    actualizar_imagen(nuevo_nivel)

            def zoom_out():
                nuevo_nivel = zoom_actual["nivel"] / 1.2
                if nuevo_nivel >= 0.1:  # Mínimo 10%
                    actualizar_imagen(nuevo_nivel)

            def reset_zoom():
                # Calcular zoom para ajustar a ventana (max 800x600)
                max_ancho, max_alto = 800, 600
                if ancho_orig > max_ancho or alto_orig > max_alto:
                    ratio = min(max_ancho / ancho_orig, max_alto / alto_orig)
                else:
                    ratio = 1.0
                actualizar_imagen(ratio)

            # Asignar comandos a botones
            btn_mas.config(command=zoom_in)
            btn_menos.config(command=zoom_out)
            btn_reset.config(command=reset_zoom)

            # Atajos de teclado
            ventana_img.bind("<plus>", lambda e: zoom_in())
            ventana_img.bind("<equal>", lambda e: zoom_in())  # + sin shift
            ventana_img.bind("<minus>", lambda e: zoom_out())
            ventana_img.bind("<r>", lambda e: reset_zoom())
            ventana_img.bind("<R>", lambda e: reset_zoom())

            # Información
            info_frame = tk.Frame(ventana_img, bg="#2C3E50")
            info_frame.pack(pady=10)

            tk.Label(info_frame, text=f"📄 {os.path.basename(ruta_imagen)}",
                     font=("Arial", 10, "bold"), bg="#2C3E50", fg="white").pack()
            tk.Label(info_frame, text=f"Tamaño original: {ancho_orig}x{alto_orig} px",
                     font=("Arial", 9), bg="#2C3E50", fg="#BDC3C7").pack()
            tk.Label(info_frame, text="Atajos: [+] Ampliar  [-] Reducir  [R] Reset  |  🖱️ Click y arrastra para mover",
                     font=("Arial", 8, "italic"), bg="#2C3E50", fg="#95A5A6").pack()

            # Botón cerrar
            tk.Button(ventana_img, text="CERRAR", bg="#E74C3C", fg="white",
                      font=("Arial", 10, "bold"), cursor="hand2", width=15,
                      command=ventana_img.destroy).pack(pady=(0, 20))

            # Cargar imagen inicial (ajustada)
            reset_zoom()

            # Centrar ventana
            ventana_img.update_idletasks()
            x = (ventana_img.winfo_screenwidth() - ventana_img.winfo_width()) // 2
            y = (ventana_img.winfo_screenheight() - ventana_img.winfo_height()) // 2
            ventana_img.geometry(f"900x700+{x}+{y}")

            # Modal
            ventana_img.transient(self.ventana)
            ventana_img.grab_set()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
            ventana_img.destroy()

    def cargar_datos_formulario(self):
        if not self.produccion_seleccionada:
            return

        prod = self.produccion_seleccionada

        # Limpiar campos
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre_cliente.delete(0, tk.END)
        self.txt_num_doc_cliente.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_cantidad.delete(0, tk.END)
        self.txt_fecha_inicio.delete(0, tk.END)
        self.txt_fecha_fin.delete(0, tk.END)
        self.txt_observaciones.delete("1.0", tk.END)

        # Cargar datos
        self.txt_codigo.insert(0, str(getattr(prod, 'codigo_mueble', None) or prod.id))

        if hasattr(prod, 'nombre_cliente') and prod.nombre_cliente:
            self.txt_nombre_cliente.insert(0, prod.nombre_cliente)

        if hasattr(prod, 'tipo_documento_cliente') and prod.tipo_documento_cliente:
            self.tipo_doc_cliente_var.set(prod.tipo_documento_cliente)

        if hasattr(prod, 'numero_documento_cliente') and prod.numero_documento_cliente:
            self.txt_num_doc_cliente.insert(0, prod.numero_documento_cliente)

        self.txt_nombre.insert(0, prod.nombre_producto)
        self.txt_cantidad.insert(0, str(prod.cantidad))
        self.txt_fecha_inicio.insert(0, self.convertir_fecha_a_vista(prod.fecha_inicio))

        if prod.fecha_fin:
            self.txt_fecha_fin.insert(0, self.convertir_fecha_a_vista(prod.fecha_fin))

        if hasattr(prod, 'observaciones') and prod.observaciones:
            self.txt_observaciones.insert("1.0", prod.observaciones)

        if hasattr(prod, 'ruta_archivo') and prod.ruta_archivo:
            self.ruta_archivo = prod.ruta_archivo
            self.lbl_archivo.config(text=f"📄 {os.path.basename(prod.ruta_archivo)}", fg="#27AE60")

        # Establecer estado en combo
        estados = ["Ingreso", "En Fabricacion", "Finalizado", "Cancelado"]
        if prod.estado in estados:
            self.combo_estado.current(estados.index(prod.estado))

    def nuevo(self):
        self.limpiar_formulario()
        self.txt_codigo.focus()
        messagebox.showinfo("Nueva Producción", "Ingrese los datos de la nueva producción")

    def guardar(self):
        if not self.validar_formulario():
            return
        if not messagebox.askyesno("Confirmar", "¿Desea guardar esta producción?"):
            return

        produccion = Produccion(
            codigo_mueble=self.txt_codigo.get().strip(),
            nombre_cliente=self.txt_nombre_cliente.get().strip(),
            tipo_documento_cliente=self.tipo_doc_cliente_var.get(),
            numero_documento_cliente=self.txt_num_doc_cliente.get().strip(),
            nombre_producto=self.txt_nombre.get().strip(),
            cantidad=int(self.txt_cantidad.get().strip()),
            fecha_inicio=self.convertir_fecha_a_bd(self.txt_fecha_inicio.get().strip()),
            fecha_fin=self.convertir_fecha_a_bd(self.txt_fecha_fin.get().strip()),
            estado=self.combo_estado.get(),
            observaciones=self.txt_observaciones.get("1.0", tk.END).strip(),
            ruta_archivo=self.ruta_archivo
        )

        if self.dao.insertar_produccion(produccion):
            messagebox.showinfo("Éxito", "Producción guardada correctamente")
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo guardar la producción")

    def modificar(self):
        if not self.produccion_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una producción")
            return
        if not self.validar_formulario():
            return
        if not messagebox.askyesno("Confirmar", "¿Desea modificar esta producción?"):
            return

        self.produccion_seleccionada.codigo_mueble = self.txt_codigo.get().strip()
        self.produccion_seleccionada.nombre_cliente = self.txt_nombre_cliente.get().strip()
        self.produccion_seleccionada.tipo_documento_cliente = self.tipo_doc_cliente_var.get()
        self.produccion_seleccionada.numero_documento_cliente = self.txt_num_doc_cliente.get().strip()
        self.produccion_seleccionada.nombre_producto = self.txt_nombre.get().strip()
        self.produccion_seleccionada.cantidad = int(self.txt_cantidad.get().strip())
        self.produccion_seleccionada.fecha_inicio = self.convertir_fecha_a_bd(self.txt_fecha_inicio.get().strip())
        self.produccion_seleccionada.fecha_fin = self.convertir_fecha_a_bd(self.txt_fecha_fin.get().strip())
        self.produccion_seleccionada.estado = self.combo_estado.get()
        self.produccion_seleccionada.observaciones = self.txt_observaciones.get("1.0", tk.END).strip()
        self.produccion_seleccionada.ruta_archivo = self.ruta_archivo

        if self.dao.actualizar_produccion(self.produccion_seleccionada):
            messagebox.showinfo("Éxito", "Producción modificada correctamente")
            if self.resultados_visible:
                self.buscar_produccion()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo modificar la producción")

    def eliminar(self):
        if not self.produccion_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una producción")
            return

        if messagebox.askyesno("Confirmar",
                               f"¿Eliminar la producción:\n\n{self.produccion_seleccionada.nombre_producto}?\n\nEsta acción no se puede deshacer."):
            if self.dao.eliminar_produccion(self.produccion_seleccionada.id):
                messagebox.showinfo("Éxito", "Producción eliminada correctamente")
                if self.resultados_visible:
                    self.buscar_produccion()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la producción")

    def finalizar(self):
        if not self.produccion_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una producción para finalizar")
            return

        if messagebox.askyesno("Confirmar",
                               f"¿Finalizar la producción:\n\n{self.produccion_seleccionada.nombre_producto}?\n\n"
                               f"Se marcará como 'Finalizado' y se establecerá la fecha fin como hoy."):
            if self.dao.finalizar_produccion(self.produccion_seleccionada.id):
                messagebox.showinfo("Éxito", "Producción finalizada correctamente")
                if self.resultados_visible:
                    self.buscar_produccion()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "No se pudo finalizar la producción")

    def validar_formulario(self):
        campos = [
            (self.txt_codigo, "código del mueble"),
            (self.txt_nombre, "nombre del producto"),
            (self.txt_cantidad, "cantidad"),
            (self.txt_fecha_inicio, "fecha de inicio")
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

        return True

    def limpiar_formulario(self):
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre_cliente.delete(0, tk.END)
        self.txt_num_doc_cliente.delete(0, tk.END)
        self.tipo_doc_cliente_var.set("CC")
        self.txt_nombre.delete(0, tk.END)
        self.txt_cantidad.delete(0, tk.END)
        self.txt_cantidad.insert(0, "1")
        self.txt_fecha_inicio.delete(0, tk.END)
        self.txt_fecha_inicio.insert(0, date.today().strftime("%d-%m-%Y"))
        self.txt_fecha_fin.delete(0, tk.END)
        self.txt_observaciones.delete("1.0", tk.END)
        self.combo_estado.current(1)
        self.txt_busqueda.delete(0, tk.END)
        self.produccion_seleccionada = None
        self.ruta_archivo = None
        self.lbl_archivo.config(text="No se ha seleccionado archivo", fg="#7F8C8D")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir de la gestión de producción?"):
            self.ventana.destroy()

    def convertir_fecha_a_bd(self, fecha_str):
        """Convierte fecha de DD-MM-YYYY a YYYY-MM-DD para la BD"""
        if not fecha_str or fecha_str.strip() == "":
            return None
        try:
            # Si viene en formato DD-MM-YYYY
            if '-' in fecha_str and len(fecha_str.split('-')[0]) <= 2:
                partes = fecha_str.split('-')
                return f"{partes[2]}-{partes[1]}-{partes[0]}"  # YYYY-MM-DD
            return fecha_str  # Ya está en formato correcto
        except:
            return fecha_str

    def convertir_fecha_a_vista(self, fecha_str):
        """Convierte fecha de YYYY-MM-DD a DD-MM-YYYY para mostrar"""
        if not fecha_str or fecha_str == "None":
            return ""
        try:
            fecha_str = str(fecha_str)
            # Si viene en formato YYYY-MM-DD
            if '-' in fecha_str and len(fecha_str.split('-')[0]) == 4:
                partes = fecha_str.split('-')
                return f"{partes[2]}-{partes[1]}-{partes[0]}"  # DD-MM-YYYY
            return fecha_str  # Ya está en formato correcto
        except:
            return fecha_str

    def mostrar(self):
        self.ventana.mainloop()


def main():
    app = VentanaProduccion()
    app.mostrar()


if __name__ == "__main__":
    main()