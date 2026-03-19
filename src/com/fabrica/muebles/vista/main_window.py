import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys
import os

_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
if _src not in sys.path:
    sys.path.insert(0, _src)

from com.fabrica.muebles.util.conexion_bd import ConexionBD

COLOR_PRIMARIO   = "#1a237e"
COLOR_SECUNDARIO = "#283593"
COLOR_ACENTO     = "#e8eaf6"
COLOR_BOTON_ADD  = "#2e7d32"
COLOR_BOTON_EDT  = "#1565c0"
COLOR_BOTON_DEL  = "#c62828"
COLOR_BOTON_LMP  = "#6a1b9a"
COLOR_TEXTO      = "#ffffff"
FONT_TITULO      = ("Segoe UI", 13, "bold")
FONT_LABEL       = ("Segoe UI", 10)
FONT_BOTON       = ("Segoe UI", 10, "bold")


def boton(parent, texto, color, comando):
    return tk.Button(parent, text=texto, bg=color, fg=COLOR_TEXTO,
                     font=FONT_BOTON, relief="flat", padx=12, pady=6,
                     cursor="hand2", command=comando)


def tabla_widget(parent, columnas, anchos, alto=10):
    frame = tk.Frame(parent, bg=COLOR_ACENTO)
    frame.pack(fill="both", expand=True, padx=15, pady=8)
    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=alto)
    for col, ancho in zip(columnas, anchos):
        tree.heading(col, text=col)
        tree.column(col, width=ancho, anchor="center")
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return tree


def entrada(parent, label, row, col_ini=0, width=25):
    tk.Label(parent, text=label, font=FONT_LABEL,
             bg=COLOR_ACENTO).grid(row=row, column=col_ini, sticky="e", padx=5, pady=4)
    e = tk.Entry(parent, font=FONT_LABEL, width=width, relief="solid", bd=1)
    e.grid(row=row, column=col_ini+1, padx=5, pady=4, sticky="w")
    return e


class ModuloClientes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_ACENTO)
        self._id        = None
        self._ruta_foto = None
        self._build()

    def _build(self):
        tk.Label(self, text="👥  Gestión de Clientes", font=FONT_TITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, pady=12).pack(fill="x")

        ff = tk.LabelFrame(self, text="Datos del Cliente", font=FONT_LABEL,
                           bg=COLOR_ACENTO, padx=10, pady=4)
        ff.pack(fill="x", padx=15, pady=4)

        self.e = {}
        self.e["nombre"]             = entrada(ff, "Nombre:",         0, 0)
        self.e["telefono"]           = entrada(ff, "Teléfono:",        0, 2)
        self.e["email"]              = entrada(ff, "Email:",           1, 0)
        self.e["direccion"]          = entrada(ff, "Dirección:",       1, 2)
        self.e["codigo_mueble"]      = entrada(ff, "Cód. Mueble:",     2, 0)
        self.e["numero_documento"]   = entrada(ff, "Nº Documento:",    2, 2)
        self.e["tipo_mueble_vendido"]= entrada(ff, "Tipo Mueble:",     3, 0)
        self.e["cantidad"]           = entrada(ff, "Cantidad:",        3, 2, 10)
        self.e["valor_mueble"]       = entrada(ff, "Valor Mueble:",    4, 0, 15)

        tk.Label(ff, text="Tipo Doc:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=5, column=0, sticky="e", padx=5, pady=4)
        self.tipo_doc = tk.StringVar(value="CC")
        fr = tk.Frame(ff, bg=COLOR_ACENTO)
        fr.grid(row=5, column=1, sticky="w")
        for v in ("CC", "NIT"):
            tk.Radiobutton(fr, text=v, variable=self.tipo_doc,
                           value=v, bg=COLOR_ACENTO, font=FONT_LABEL).pack(side="left")

        tk.Label(ff, text="Foto Mueble:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=5, column=2, sticky="e", padx=5, pady=4)
        fr_foto = tk.Frame(ff, bg=COLOR_ACENTO)
        fr_foto.grid(row=5, column=3, sticky="w", padx=5)

        self.btn_foto = tk.Button(fr_foto, text="📷 Seleccionar foto",
                                  bg="#37474f", fg=COLOR_TEXTO, font=FONT_LABEL,
                                  relief="flat", padx=8, pady=4, cursor="hand2",
                                  command=self.seleccionar_foto)
        self.btn_foto.pack(side="left")

        self.lbl_foto = tk.Label(fr_foto, text="Sin foto", font=("Segoe UI", 9),
                                 bg=COLOR_ACENTO, fg="#555", width=20, anchor="w")
        self.lbl_foto.pack(side="left", padx=6)

        self.panel_foto = tk.Label(ff, bg="#cfd8dc", width=12, height=6,
                                   text="Sin\nfoto", font=("Segoe UI", 9),
                                   relief="groove", cursor="hand2")
        self.panel_foto.grid(row=0, column=4, rowspan=6, padx=15, pady=4, sticky="n")
        self.panel_foto.bind("<Button-1>", self.abrir_foto_zoom)

        fb_busq = tk.Frame(self, bg=COLOR_ACENTO)
        fb_busq.pack(fill="x", padx=15, pady=(0, 2))
        tk.Label(fb_busq, text="🔍 Buscar:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).pack(side="left")
        self.buscar_entry = tk.Entry(fb_busq, font=FONT_LABEL, width=30,
                                     relief="solid", bd=1)
        self.buscar_entry.pack(side="left", padx=6)
        boton(fb_busq, "Buscar", COLOR_BOTON_EDT, self.buscar).pack(side="left", padx=4)

        fb = tk.Frame(self, bg=COLOR_ACENTO)
        fb.pack(pady=2)
        boton(fb, "➕ Agregar",    COLOR_BOTON_ADD, self.agregar).pack(side="left", padx=4)
        boton(fb, "✏️ Actualizar", COLOR_BOTON_EDT, self.actualizar).pack(side="left", padx=4)
        boton(fb, "🗑️ Eliminar",  COLOR_BOTON_DEL, self.eliminar).pack(side="left", padx=4)
        boton(fb, "🧹 Limpiar",   COLOR_BOTON_LMP, self.limpiar).pack(side="left", padx=4)

        cols   = ("ID","Nombre","Teléfono","Email","Dirección","Cód.Mueble","Tipo Doc","Nº Doc","Tipo Mueble","Cant","Valor","Fecha Reg")
        anchos = (40, 130, 90, 130, 100, 80, 70, 90, 100, 50, 80, 90)
        self.tabla = tabla_widget(self, cols, anchos, alto=3)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def abrir_foto_zoom(self, _=None):
        if not self._ruta_foto:
            return
        try:
            from PIL import Image, ImageTk
            img = Image.open(self._ruta_foto)
            win = tk.Toplevel(self)
            win.title("Vista de foto")
            win.configure(bg="#263238")
            sw = win.winfo_screenwidth()
            sh = win.winfo_screenheight()
            max_w = int(sw * 0.90)
            max_h = int(sh * 0.90)
            # Escalar manteniendo proporción pero siempre al máximo posible
            orig_w, orig_h = img.size
            ratio = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * ratio)
            new_h = int(orig_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=photo, bg="#263238")
            lbl.image = photo
            lbl.pack(padx=10, pady=10)
            win.update_idletasks()
            x = (sw - win.winfo_width()) // 2
            y = (sh - win.winfo_height()) // 2
            win.geometry(f"+{x}+{y}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen:\n{e}")

    def seleccionar_foto(self):
        from tkinter import filedialog
        from PIL import Image, ImageTk
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto del mueble",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if ruta:
            self._ruta_foto = ruta
            nombre = os.path.basename(ruta)
            self.lbl_foto.config(text=nombre[:25] + "..." if len(nombre) > 25 else nombre)
            try:
                img = Image.open(ruta).resize((200, 180), Image.LANCZOS)
                self._img_tk = ImageTk.PhotoImage(img)
                self.panel_foto.config(image=self._img_tk, text="", width=200, height=180)
            except Exception:
                self.panel_foto.config(text="Vista\nprevia\nnodisponible")

    def _cargar_fila(self, filas):
        for r in self.tabla.get_children():
            self.tabla.delete(r)
        for f in filas:
            self.tabla.insert("", "end", values=f)

    def cargar_ultimo(self):
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id_cliente, nombre, telefono, email, direccion,
                                  codigo_mueble, tipo_documento, numero_documento,
                                  tipo_mueble_vendido, cantidad, valor_mueble,
                                  fecha_registro
                           FROM clientes ORDER BY id_cliente DESC LIMIT 1""")
            self._cargar_fila(cur.fetchall())
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def ver_todos(self):
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id_cliente, nombre, telefono, email, direccion,
                                  codigo_mueble, tipo_documento, numero_documento,
                                  tipo_mueble_vendido, cantidad, valor_mueble,
                                  fecha_registro
                           FROM clientes ORDER BY id_cliente DESC""")
            self._cargar_fila(cur.fetchall())
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def buscar(self):
        termino = self.buscar_entry.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Escribe un nombre o número de documento.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id_cliente, nombre, telefono, email, direccion,
                                  codigo_mueble, tipo_documento, numero_documento,
                                  tipo_mueble_vendido, cantidad, valor_mueble,
                                  fecha_registro
                           FROM clientes
                           WHERE nombre LIKE %s OR numero_documento LIKE %s
                           ORDER BY id_cliente DESC""",
                        (f"%{termino}%", f"%{termino}%"))
            filas = cur.fetchall()
            self._cargar_fila(filas)
            if not filas:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def seleccionar(self, _):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]
        self.limpiar()
        self._id = v[0]
        keys = ["nombre","telefono","email","direccion","codigo_mueble",
                "numero_documento","tipo_mueble_vendido","cantidad","valor_mueble"]
        vals = [v[1],v[2],v[3],v[4],v[5],v[7],v[8],v[9],v[10]]
        for k, val in zip(keys, vals):
            self.e[k].insert(0, val if val else "")
        self.tipo_doc.set(v[6] if v[6] else "CC")
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("SELECT ruta_foto FROM clientes WHERE id_cliente=%s", (self._id,))
            fila = cur.fetchone()
            if fila and fila[0]:
                self._ruta_foto = fila[0]
                self.lbl_foto.config(text=os.path.basename(fila[0]))
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(fila[0]).resize((200, 180), Image.LANCZOS)
                    self._img_tk = ImageTk.PhotoImage(img)
                    self.panel_foto.config(image=self._img_tk, text="", width=200, height=180)
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            cur.close(); con.close()

    def _datos(self):
        return (
            self.e["nombre"].get(),
            self.e["telefono"].get(),
            self.e["direccion"].get(),
            self.e["email"].get(),
            self.e["codigo_mueble"].get(),
            self.tipo_doc.get(),
            self.e["numero_documento"].get(),
            self.e["tipo_mueble_vendido"].get(),
            self.e["cantidad"].get() or 1,
            self.e["valor_mueble"].get() or 0,
            self._ruta_foto,
            None,
            str(date.today())
        )

    def agregar(self):
        if not self.e["nombre"].get():
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""INSERT INTO clientes
                (nombre,telefono,direccion,email,codigo_mueble,tipo_documento,
                 numero_documento,tipo_mueble_vendido,cantidad,valor_mueble,
                 ruta_foto,observaciones,fecha_registro)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", self._datos())
            con.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            self.limpiar()
            self.cargar_ultimo()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def actualizar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente de la tabla.")
            return
        try:
            d = self._datos()
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""UPDATE clientes SET
                nombre=%s, telefono=%s, direccion=%s, email=%s,
                codigo_mueble=%s, tipo_documento=%s, numero_documento=%s,
                tipo_mueble_vendido=%s, cantidad=%s, valor_mueble=%s,
                ruta_foto=%s, observaciones=%s, fecha_registro=%s
                WHERE id_cliente=%s""", d + (self._id,))
            con.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self.limpiar()
            self.cargar_ultimo()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def eliminar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            try:
                con = ConexionBD.get_conexion()
                cur = con.cursor()
                cur.execute("DELETE FROM clientes WHERE id_cliente=%s", (self._id,))
                con.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado.")
                self.limpiar()
                for r in self.tabla.get_children():
                    self.tabla.delete(r)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cur.close(); con.close()

    def limpiar(self):
        for e in self.e.values():
            e.delete(0, "end")
        self.tipo_doc.set("CC")
        self._id        = None
        self._ruta_foto = None
        self.lbl_foto.config(text="Sin foto")
        self.panel_foto.config(image="", text="Sin\nfoto", width=12, height=6)
        if hasattr(self, '_img_tk'):
            del self._img_tk


class ModuloProveedores(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_ACENTO)
        self._id = None
        self._build()

    def _build(self):
        tk.Label(self, text="🏭  Gestión de Proveedores", font=FONT_TITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, pady=12).pack(fill="x")

        ff = tk.LabelFrame(self, text="Datos del Proveedor", font=FONT_LABEL,
                           bg=COLOR_ACENTO, padx=10, pady=8)
        ff.pack(fill="x", padx=15, pady=8)

        self.e = {}
        self.e["nombre"]   = entrada(ff, "Nombre:",    0, 0)
        self.e["contacto"] = entrada(ff, "Contacto:",  0, 2)
        self.e["telefono"] = entrada(ff, "Teléfono:",  1, 0)
        self.e["direccion"]= entrada(ff, "Dirección:", 1, 2)
        self.e["correo"]   = entrada(ff, "Correo:",    2, 0)

        fb_busq = tk.Frame(self, bg=COLOR_ACENTO)
        fb_busq.pack(fill="x", padx=15, pady=(0, 2))
        tk.Label(fb_busq, text="🔍 Buscar:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).pack(side="left")
        self.buscar_entry = tk.Entry(fb_busq, font=FONT_LABEL, width=30,
                                     relief="solid", bd=1)
        self.buscar_entry.pack(side="left", padx=6)
        boton(fb_busq, "Buscar", COLOR_BOTON_EDT, self.buscar).pack(side="left", padx=4)

        fb = tk.Frame(self, bg=COLOR_ACENTO)
        fb.pack(pady=5)
        boton(fb, "➕ Agregar",    COLOR_BOTON_ADD, self.agregar).pack(side="left", padx=4)
        boton(fb, "✏️ Actualizar", COLOR_BOTON_EDT, self.actualizar).pack(side="left", padx=4)
        boton(fb, "🗑️ Eliminar",  COLOR_BOTON_DEL, self.eliminar).pack(side="left", padx=4)
        boton(fb, "🧹 Limpiar",   COLOR_BOTON_LMP, self.limpiar).pack(side="left", padx=4)

        cols   = ("ID", "Nombre", "Contacto", "Teléfono", "Dirección", "Correo")
        anchos = (50, 160, 140, 110, 160, 170)
        self.tabla = tabla_widget(self, cols, anchos, alto=3)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar(self):
        for r in self.tabla.get_children():
            self.tabla.delete(r)
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("SELECT id, nombre, contacto, telefono, direccion, correo FROM proveedor")
            for f in cur.fetchall():
                self.tabla.insert("", "end", values=f)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def buscar(self):
        termino = self.buscar_entry.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Escribe un nombre o teléfono.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id, nombre, contacto, telefono, direccion, correo
                           FROM proveedor
                           WHERE nombre LIKE %s OR telefono LIKE %s
                           ORDER BY id DESC""",
                        (f"%{termino}%", f"%{termino}%"))
            filas = cur.fetchall()
            for r in self.tabla.get_children():
                self.tabla.delete(r)
            for f in filas:
                self.tabla.insert("", "end", values=f)
            if not filas:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def seleccionar(self, _):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]
        self.limpiar()
        self._id = v[0]
        for k, val in zip(["nombre","contacto","telefono","direccion","correo"], v[1:]):
            self.e[k].insert(0, val if val else "")

    def _datos(self):
        return tuple(self.e[k].get() for k in ["nombre","contacto","telefono","direccion","correo"])

    def agregar(self):
        if not self.e["nombre"].get():
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""INSERT INTO proveedor (nombre,contacto,telefono,direccion,correo)
                           VALUES (%s,%s,%s,%s,%s)""", self._datos())
            con.commit()
            messagebox.showinfo("Éxito", "Proveedor agregado.")
            self.limpiar(); self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def actualizar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un proveedor.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""UPDATE proveedor SET nombre=%s,contacto=%s,
                           telefono=%s,direccion=%s,correo=%s WHERE id=%s""",
                        self._datos() + (self._id,))
            con.commit()
            messagebox.showinfo("Éxito", "Proveedor actualizado.")
            self.limpiar(); self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def eliminar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un proveedor.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
            try:
                con = ConexionBD.get_conexion()
                cur = con.cursor()
                cur.execute("DELETE FROM proveedor WHERE id=%s", (self._id,))
                con.commit()
                messagebox.showinfo("Éxito", "Proveedor eliminado.")
                self.limpiar(); self.cargar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cur.close(); con.close()

    def limpiar(self):
        for e in self.e.values():
            e.delete(0, "end")
        self._id = None


class ModuloProduccion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_ACENTO)
        self._id = None
        self._ruta_plano = None
        self._build()

    def _build(self):
        tk.Label(self, text="🪑  Gestión de Producción", font=FONT_TITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, pady=12).pack(fill="x")

        ff = tk.LabelFrame(self, text="Datos de Producción", font=FONT_LABEL,
                           bg=COLOR_ACENTO, padx=10, pady=8)
        ff.pack(fill="x", padx=15, pady=8)

        self.e = {}
        self.e["codigo_mueble"]            = entrada(ff, "Cód. Mueble:",      0, 0)
        self.e["nombre_cliente"]           = entrada(ff, "Cliente:",           0, 2)
        self.e["numero_documento_cliente"] = entrada(ff, "Nº Doc. Cliente:",  1, 0)
        self.e["nombre_producto"]          = entrada(ff, "Producto:",          1, 2)
        self.e["cantidad"]                 = entrada(ff, "Cantidad:",          2, 0, 10)
        self.e["fecha_inicio"]             = entrada(ff, "Fecha Inicio:",      2, 2, 15)
        self.e["fecha_fin"]                = entrada(ff, "Fecha Fin:",         3, 0, 15)

        # Observaciones más ancha ocupando columnas 2-3
        tk.Label(ff, text="Observaciones:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=3, column=2, sticky="e", padx=5, pady=4)
        self.e["observaciones"] = tk.Entry(ff, font=FONT_LABEL, width=50, relief="solid", bd=1)
        self.e["observaciones"].grid(row=3, column=3, columnspan=2, padx=5, pady=4, sticky="w")

        tk.Label(ff, text="Tipo Doc:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=4, column=0, sticky="e", padx=5, pady=4)
        self.tipo_doc = tk.StringVar(value="CC")
        fr = tk.Frame(ff, bg=COLOR_ACENTO)
        fr.grid(row=4, column=1, sticky="w")
        for v in ("CC", "NIT"):
            tk.Radiobutton(fr, text=v, variable=self.tipo_doc,
                           value=v, bg=COLOR_ACENTO, font=FONT_LABEL).pack(side="left")

        tk.Label(ff, text="Estado:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=4, column=2, sticky="e", padx=5, pady=4)
        self.estado_var = tk.StringVar(value="En Proceso")
        ttk.Combobox(ff, textvariable=self.estado_var,
                     values=["En Proceso", "Finalizado", "Cancelado"],
                     state="readonly", width=16,
                     font=FONT_LABEL).grid(row=4, column=3, padx=5, pady=4, sticky="w")

        # Plano/diseño
        tk.Label(ff, text="Plano/Diseño:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).grid(row=5, column=0, sticky="e", padx=5, pady=4)
        fr_plano = tk.Frame(ff, bg=COLOR_ACENTO)
        fr_plano.grid(row=5, column=1, columnspan=3, sticky="w", padx=5)

        self.btn_plano = tk.Button(fr_plano, text="📐 Seleccionar plano",
                                   bg="#37474f", fg=COLOR_TEXTO, font=FONT_LABEL,
                                   relief="flat", padx=8, pady=4, cursor="hand2",
                                   command=self.seleccionar_plano)
        self.btn_plano.pack(side="left")

        self.lbl_plano = tk.Label(fr_plano, text="Sin plano", font=("Segoe UI", 9),
                                  bg=COLOR_ACENTO, fg="#555", width=20, anchor="w")
        self.lbl_plano.pack(side="left", padx=6)

        self.panel_plano = tk.Label(ff, bg="#cfd8dc", width=12, height=6,
                                    text="Sin\nplano", font=("Segoe UI", 9),
                                    relief="groove", cursor="hand2")
        self.panel_plano.grid(row=0, column=4, rowspan=6, padx=(300, 15), pady=4, sticky="n")
        self.panel_plano.bind("<Button-1>", self.abrir_plano_zoom)

        fb_busq = tk.Frame(self, bg=COLOR_ACENTO)
        fb_busq.pack(fill="x", padx=15, pady=(0, 2))
        tk.Label(fb_busq, text="🔍 Buscar:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).pack(side="left")
        self.buscar_entry = tk.Entry(fb_busq, font=FONT_LABEL, width=30,
                                     relief="solid", bd=1)
        self.buscar_entry.pack(side="left", padx=6)
        boton(fb_busq, "Buscar", COLOR_BOTON_EDT, self.buscar).pack(side="left", padx=4)

        fb = tk.Frame(self, bg=COLOR_ACENTO)
        fb.pack(pady=5)
        boton(fb, "➕ Agregar",    COLOR_BOTON_ADD, self.agregar).pack(side="left", padx=4)
        boton(fb, "✏️ Actualizar", COLOR_BOTON_EDT, self.actualizar).pack(side="left", padx=4)
        boton(fb, "🗑️ Eliminar",  COLOR_BOTON_DEL, self.eliminar).pack(side="left", padx=4)
        boton(fb, "🧹 Limpiar",   COLOR_BOTON_LMP, self.limpiar).pack(side="left", padx=4)

        cols   = ("ID","Cód.Mueble","Cliente","Tipo Doc","Nº Doc","Producto","Cant","F.Inicio","F.Fin","Estado")
        anchos = (40, 90, 130, 70, 100, 130, 50, 90, 90, 90)
        self.tabla = tabla_widget(self, cols, anchos, alto=3)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

        # Área de observaciones debajo de la tabla
        fo = tk.Frame(self, bg=COLOR_ACENTO)
        fo.pack(fill="x", padx=15, pady=(0, 8))
        tk.Label(fo, text="Observaciones:", font=FONT_LABEL,
                 bg=COLOR_ACENTO).pack(side="left", anchor="n", pady=4)
        self.txt_obs = tk.Text(fo, font=FONT_LABEL, width=70, height=4,
                               wrap="word", relief="solid", bd=1,
                               padx=6, pady=6, state="disabled", bg="#f9f9f9")
        self.txt_obs.pack(side="left", padx=8, pady=4)

    def seleccionar_plano(self):
        from tkinter import filedialog
        from PIL import Image, ImageTk
        ruta = filedialog.askopenfilename(
            title="Seleccionar plano o diseño",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if ruta:
            self._ruta_plano = ruta
            nombre = os.path.basename(ruta)
            self.lbl_plano.config(text=nombre[:25] + "..." if len(nombre) > 25 else nombre)
            try:
                img = Image.open(ruta).resize((200, 180), Image.LANCZOS)
                self._img_plano_tk = ImageTk.PhotoImage(img)
                self.panel_plano.config(image=self._img_plano_tk, text="", width=200, height=180)
            except Exception:
                self.panel_plano.config(text="Vista\nprevia\nnodisponible")

    def abrir_plano_zoom(self, _=None):
        if not self._ruta_plano:
            return
        try:
            from PIL import Image, ImageTk
            img = Image.open(self._ruta_plano)
            win = tk.Toplevel(self)
            win.title("Vista de plano/diseño")
            win.configure(bg="#263238")
            sw = win.winfo_screenwidth()
            sh = win.winfo_screenheight()
            max_w = int(sw * 0.90)
            max_h = int(sh * 0.90)
            orig_w, orig_h = img.size
            ratio = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * ratio)
            new_h = int(orig_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=photo, bg="#263238")
            lbl.image = photo
            lbl.pack(padx=10, pady=10)
            win.update_idletasks()
            x = (sw - win.winfo_width()) // 2
            y = (sh - win.winfo_height()) // 2
            win.geometry(f"+{x}+{y}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el plano:\n{e}")

    def cargar(self):
        for r in self.tabla.get_children():
            self.tabla.delete(r)
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id, codigo_mueble, nombre_cliente,
                                  tipo_documento_cliente, numero_documento_cliente,
                                  nombre_producto, cantidad, fecha_inicio,
                                  fecha_fin, estado, observaciones
                           FROM produccion ORDER BY id DESC LIMIT 1""")
            for f in cur.fetchall():
                self.tabla.insert("", "end", values=f)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def buscar(self):
        termino = self.buscar_entry.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Escribe un nombre o código de mueble.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""SELECT id, codigo_mueble, nombre_cliente,
                                  tipo_documento_cliente, numero_documento_cliente,
                                  nombre_producto, cantidad, fecha_inicio,
                                  fecha_fin, estado, observaciones
                           FROM produccion
                           WHERE nombre_cliente LIKE %s OR codigo_mueble LIKE %s
                           ORDER BY id DESC""",
                        (f"%{termino}%", f"%{termino}%"))
            filas = cur.fetchall()
            for r in self.tabla.get_children():
                self.tabla.delete(r)
            for f in filas:
                self.tabla.insert("", "end", values=f)
            if not filas:
                messagebox.showinfo("Búsqueda", "No se encontraron resultados.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def seleccionar(self, _):
        sel = self.tabla.selection()
        if not sel:
            return
        v = self.tabla.item(sel[0])["values"]
        self.limpiar()
        self._id = v[0]
        keys = ["codigo_mueble","nombre_cliente","numero_documento_cliente",
                "nombre_producto","cantidad","fecha_inicio","fecha_fin"]
        vals = [v[1],v[2],v[4],v[5],v[6],v[7],v[8]]
        for k, val in zip(keys, vals):
            self.e[k].insert(0, val if val else "")
        self.tipo_doc.set(v[3] if v[3] else "CC")
        self.estado_var.set(v[9] if v[9] else "En Proceso")
        # Mostrar observaciones
        obs = v[10] if len(v) > 10 else ""
        self.txt_obs.config(state="normal")
        self.txt_obs.delete("1.0", "end")
        self.txt_obs.insert("1.0", str(obs) if obs and str(obs) != "None" else "")
        self.txt_obs.config(state="disabled")
        # Cargar plano si existe
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("SELECT ruta_archivo FROM produccion WHERE id=%s", (self._id,))
            fila = cur.fetchone()
            if fila and fila[0]:
                self._ruta_plano = fila[0]
                self.lbl_plano.config(text=os.path.basename(fila[0]))
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(fila[0]).resize((200, 180), Image.LANCZOS)
                    self._img_plano_tk = ImageTk.PhotoImage(img)
                    self.panel_plano.config(image=self._img_plano_tk, text="", width=200, height=180)
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            cur.close(); con.close()

    def _datos(self):
        fecha_fin = self.e["fecha_fin"].get().strip()
        fecha_fin = None if not fecha_fin or fecha_fin.lower() == "none" else fecha_fin
        return (
            self.e["codigo_mueble"].get(),
            self.e["nombre_cliente"].get(),
            self.tipo_doc.get(),
            self.e["numero_documento_cliente"].get(),
            self.e["nombre_producto"].get(),
            self.e["cantidad"].get() or 0,
            self.e["fecha_inicio"].get() or str(date.today()),
            fecha_fin,
            self.estado_var.get(),
            self.e["observaciones"].get(),
            self._ruta_plano
        )

    def agregar(self):
        if not self.e["nombre_producto"].get():
            messagebox.showwarning("Advertencia", "El nombre del producto es obligatorio.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""INSERT INTO produccion
                (codigo_mueble, nombre_cliente, tipo_documento_cliente,
                 numero_documento_cliente, nombre_producto, cantidad,
                 fecha_inicio, fecha_fin, estado, observaciones, ruta_archivo)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", self._datos())
            con.commit()
            messagebox.showinfo("Éxito", "Producción agregada.")
            self.limpiar(); self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def actualizar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un registro.")
            return
        try:
            con = ConexionBD.get_conexion()
            cur = con.cursor()
            cur.execute("""UPDATE produccion SET
                codigo_mueble=%s, nombre_cliente=%s, tipo_documento_cliente=%s,
                numero_documento_cliente=%s, nombre_producto=%s, cantidad=%s,
                fecha_inicio=%s, fecha_fin=%s, estado=%s,
                observaciones=%s, ruta_archivo=%s
                WHERE id=%s""", self._datos() + (self._id,))
            con.commit()
            messagebox.showinfo("Éxito", "Producción actualizada.")
            self.limpiar(); self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close(); con.close()

    def finalizar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un registro.")
            return
        if messagebox.askyesno("Confirmar", "¿Marcar como Finalizado?"):
            try:
                con = ConexionBD.get_conexion()
                cur = con.cursor()
                cur.execute("""UPDATE produccion SET estado='Finalizado',
                               fecha_fin=CURDATE() WHERE id=%s""", (self._id,))
                con.commit()
                messagebox.showinfo("Éxito", "Producción finalizada.")
                self.limpiar(); self.cargar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cur.close(); con.close()

    def eliminar(self):
        if not self._id:
            messagebox.showwarning("Advertencia", "Selecciona un registro.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
            try:
                con = ConexionBD.get_conexion()
                cur = con.cursor()
                cur.execute("DELETE FROM produccion WHERE id=%s", (self._id,))
                con.commit()
                messagebox.showinfo("Éxito", "Producción eliminada.")
                self.limpiar(); self.cargar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cur.close(); con.close()

    def limpiar(self):
        for e in self.e.values():
            e.delete(0, "end")
        self.tipo_doc.set("CC")
        self.estado_var.set("En Proceso")
        self._id = None
        self._ruta_plano = None
        self.lbl_plano.config(text="Sin plano")
        self.panel_plano.config(image="", text="Sin\nplano", width=12, height=6)
        if hasattr(self, '_img_plano_tk'):
            del self._img_plano_tk
        self.txt_obs.config(state="normal")
        self.txt_obs.delete("1.0", "end")
        self.txt_obs.config(state="disabled")


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Fábrica de Muebles")
        self.geometry("1050x720")
        self.resizable(True, True)
        self.configure(bg=COLOR_PRIMARIO)
        self._build()

    def _build(self):
        tk.Label(self, text="🪑  Sistema de Gestión - Fábrica de Muebles",
                 font=("Segoe UI", 15, "bold"), bg=COLOR_PRIMARIO,
                 fg=COLOR_TEXTO, pady=15).pack()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COLOR_PRIMARIO, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"),
                        padding=[20, 8], background=COLOR_SECUNDARIO,
                        foreground=COLOR_TEXTO)
        style.map("TNotebook.Tab",
                  background=[("selected", COLOR_ACENTO)],
                  foreground=[("selected", COLOR_PRIMARIO)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        nb.add(ModuloClientes(nb),    text="👥 Clientes")
        nb.add(ModuloProveedores(nb), text="🏭 Proveedores")
        nb.add(ModuloProduccion(nb),  text="🪑 Producción")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()