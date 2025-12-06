import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))


class MenuPrincipal:
    """
    Ventana Principal del Sistema de Gestion de Fabrica de Muebles
    Menu con acceso a todos los modulos segun el rol del usuario

    Autor: William Alonso Samaca Lopez
    Sistema de Gestion Fabrica de Muebles
    """

    def __init__(self, usuario):
        self.usuario = usuario
        self.ventana = tk.Tk()
        self.inicializar_componentes()

    def inicializar_componentes(self):
        self.ventana.title("Sistema de Gestion - Fabrica de Muebles")
        self.ventana.geometry("600x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#F0F0F0")

        ancho_ventana = 600
        alto_ventana = 500
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        titulo = tk.Label(
            self.ventana,
            text="FABRICA DE MUEBLES",
            font=("Arial", 28, "bold"),
            fg="#333333",
            bg="#F0F0F0"
        )
        titulo.place(x=120, y=20)

        subtitulo = tk.Label(
            self.ventana,
            text=f"Bienvenido: {self.usuario.usuario} ({self.usuario.rol})",
            font=("Arial", 14),
            fg="#646464",
            bg="#F0F0F0"
        )
        subtitulo.place(x=150, y=60)

        # Crear botones segun el rol
        self.crear_botones_segun_rol()

        btn_salir = tk.Button(
            self.ventana,
            text="SALIR",
            font=("Arial", 14, "bold"),
            bg="#E74C3C",
            fg="white",
            width=15,
            height=2,
            cursor="hand2",
            command=self.salir
        )
        btn_salir.place(x=220, y=400)

        footer = tk.Label(
            self.ventana,
            text="2025 Sistema desarrollado para SENA",
            font=("Arial", 11),
            fg="#969696",
            bg="#F0F0F0"
        )
        footer.place(x=190, y=445)

    def crear_botones_segun_rol(self):
        rol = self.usuario.rol.lower()

        if rol == "administrador":
            # ADMINISTRADOR: Ve todo
            self.crear_boton("CLIENTES", 50, 120, "#3498DB", self.abrir_ventana_clientes)
            self.crear_boton("PRODUCCION", 320, 120, "#2ECC71", self.abrir_ventana_produccion)
            self.crear_boton("PROVEEDORES", 50, 250, "#9B59B6", self.abrir_ventana_proveedores)
            self.crear_boton("PANEL ADMIN", 320, 250, "#E67E22", self.abrir_panel_admin)

        elif rol == "clientes":
            # CLIENTES: Solo ve Clientes
            self.crear_boton("CLIENTES", 185, 150, "#3498DB", self.abrir_ventana_clientes)
            self.mostrar_mensaje_acceso("Solo tiene acceso al modulo de CLIENTES")

        elif rol == "proveedores":
            # PROVEEDORES: Solo ve Proveedores
            self.crear_boton("PROVEEDORES", 185, 150, "#9B59B6", self.abrir_ventana_proveedores)
            self.mostrar_mensaje_acceso("Solo tiene acceso al modulo de PROVEEDORES")

        elif rol == "produccion":
            # PRODUCCION: Solo ve Producción
            self.crear_boton("PRODUCCION", 185, 150, "#2ECC71", self.abrir_ventana_produccion)
            self.mostrar_mensaje_acceso("Solo tiene acceso al modulo de PRODUCCION")

        else:
            messagebox.showerror("Error", "Rol no reconocido")
            self.ventana.destroy()

    def mostrar_mensaje_acceso(self, mensaje):
        lbl = tk.Label(
            self.ventana,
            text=mensaje,
            font=("Arial", 10, "italic"),
            fg="#7F8C8D",
            bg="#F0F0F0"
        )
        lbl.place(x=150, y=300)

    def crear_boton(self, texto, x, y, color, comando):
        boton = tk.Button(
            self.ventana,
            text=texto,
            font=("Arial", 18, "bold"),
            bg=color,
            fg="white",
            width=15,
            height=4,
            cursor="hand2",
            command=comando
        )
        boton.place(x=x, y=y)

        def on_enter(e):
            boton.config(bg=self.color_mas_oscuro(color))

        def on_leave(e):
            boton.config(bg=color)

        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

        return boton

    def color_mas_oscuro(self, color_hex):
        color_hex = color_hex.lstrip('#')
        r, g, b = tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'

    def abrir_ventana_clientes(self):
        from com.fabrica.muebles.vista.ventana_clientes import VentanaClientes
        VentanaClientes(self.ventana)

    def abrir_ventana_produccion(self):
        from com.fabrica.muebles.vista.ventana_produccion import VentanaProduccion
        VentanaProduccion(self.ventana)

    def abrir_ventana_proveedores(self):
        from com.fabrica.muebles.vista.ventana_proveedores import VentanaProveedores
        VentanaProveedores(self.ventana)

    def abrir_panel_admin(self):
        messagebox.showinfo("Panel Admin",
                            "Panel de administracion\nAqui se mostrarian reportes y estadisticas generales")

    def salir(self):
        respuesta = messagebox.askyesno(
            "Confirmar Salida",
            "Esta seguro de que desea salir del sistema?"
        )
        if respuesta:
            print("Sistema cerrado correctamente")
            self.ventana.destroy()

    def mostrar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    from com.fabrica.muebles.modelo.usuario import Usuario

    usuario_prueba = Usuario(1, "admin", "admin123", "administrador", "admin@test.com")
    menu = MenuPrincipal(usuario_prueba)
    menu.mostrar()