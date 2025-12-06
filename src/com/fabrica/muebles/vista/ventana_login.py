import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.dao.usuario_dao import UsuarioDAO
from com.fabrica.muebles.modelo.usuario import Usuario


class VentanaLogin:
    """Ventana de inicio de sesion"""

    def __init__(self):
        self.ventana = tk.Tk()
        self.dao = UsuarioDAO()
        self.usuario_autenticado = None
        self.inicializar()

    def inicializar(self):
        self.ventana.title("Inicio de Sesion - Fabrica de Muebles")
        self.ventana.geometry("400x450")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#2C3E50")

        x = (self.ventana.winfo_screenwidth() - 400) // 2
        y = (self.ventana.winfo_screenheight() - 450) // 2
        self.ventana.geometry(f"400x450+{x}+{y}")

        tk.Label(self.ventana, text="FABRICA DE MUEBLES", font=("Arial", 20, "bold"),
                 bg="#2C3E50", fg="white").pack(pady=20)

        tk.Label(self.ventana, text="Sistema de Control Empresarial", font=("Arial", 12),
                 bg="#2C3E50", fg="#BDC3C7").pack()

        frame = tk.Frame(self.ventana, bg="#34495E", padx=30, pady=30)
        frame.pack(pady=30)

        tk.Label(frame, text="Usuario:", font=("Arial", 11), bg="#34495E", fg="white").grid(row=0, column=0, sticky="w",
                                                                                            pady=10)
        self.txt_usuario = tk.Entry(frame, font=("Arial", 11), width=20)
        self.txt_usuario.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Contraseña:", font=("Arial", 11), bg="#34495E", fg="white").grid(row=1, column=0,
                                                                                               sticky="w", pady=10)
        self.txt_password = tk.Entry(frame, font=("Arial", 11), width=20, show="*")
        self.txt_password.grid(row=1, column=1, pady=10)

        tk.Button(self.ventana, text="INGRESAR", bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                  width=20, height=2, cursor="hand2", command=self.login).pack(pady=10)

        tk.Button(self.ventana, text="REGISTRARSE", bg="#3498DB", fg="white", font=("Arial", 12, "bold"),
                  width=20, height=2, cursor="hand2", command=self.registrar).pack(pady=5)

        tk.Button(self.ventana, text="OLVIDE MI CONTRASEÑA", bg="#E67E22", fg="white", font=("Arial", 10),
                  width=20, cursor="hand2", command=self.recuperar).pack(pady=5)

        tk.Label(self.ventana, text="2025 Sistema desarrollado para SENA", font=("Arial", 9),
                 bg="#2C3E50", fg="#7F8C8D").pack(side="bottom", pady=10)

        self.txt_usuario.bind("<Return>", lambda e: self.txt_password.focus())
        self.txt_password.bind("<Return>", lambda e: self.login())

    def login(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Validacion", "Ingrese usuario y contraseña")
            return

        user = self.dao.autenticar(usuario, password)

        if user:
            self.usuario_autenticado = user
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.txt_password.delete(0, tk.END)
            self.txt_password.focus()

    def registrar(self):
        ventana_registro = tk.Toplevel(self.ventana)
        ventana_registro.title("Registro de Usuario")
        ventana_registro.geometry("400x400")
        ventana_registro.resizable(False, False)
        ventana_registro.configure(bg="#34495E")

        x = (ventana_registro.winfo_screenwidth() - 400) // 2
        y = (ventana_registro.winfo_screenheight() - 400) // 2
        ventana_registro.geometry(f"400x400+{x}+{y}")

        tk.Label(ventana_registro, text="REGISTRO DE USUARIO", font=("Arial", 16, "bold"),
                 bg="#34495E", fg="white").pack(pady=20)

        frame = tk.Frame(ventana_registro, bg="#34495E", padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Usuario:", bg="#34495E", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        txt_reg_usuario = tk.Entry(frame, width=25)
        txt_reg_usuario.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Contraseña:", bg="#34495E", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        txt_reg_password = tk.Entry(frame, width=25, show="*")
        txt_reg_password.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Email:", bg="#34495E", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        txt_reg_email = tk.Entry(frame, width=25)
        txt_reg_email.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Rol:", bg="#34495E", fg="white").grid(row=3, column=0, sticky="w", pady=5)

        rol_var = tk.StringVar(value="clientes")
        roles = [("Clientes", "clientes"), ("Proveedores", "proveedores"),
                 ("Produccion", "produccion"), ("Administrador", "administrador")]

        for i, (texto, valor) in enumerate(roles):
            tk.Radiobutton(frame, text=texto, variable=rol_var, value=valor,
                           bg="#34495E", fg="white", selectcolor="#2C3E50").grid(row=4 + i, column=1, sticky="w")

        def guardar():
            if not txt_reg_usuario.get() or not txt_reg_password.get():
                messagebox.showwarning("Validacion", "Complete todos los campos")
                return

            nuevo_usuario = Usuario(
                usuario=txt_reg_usuario.get(),
                password=txt_reg_password.get(),
                rol=rol_var.get(),
                email=txt_reg_email.get()
            )

            if self.dao.registrar(nuevo_usuario):
                messagebox.showinfo("Exito", "Usuario registrado correctamente")
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")

        tk.Button(ventana_registro, text="REGISTRAR", bg="#27AE60", fg="white",
                  font=("Arial", 12, "bold"), width=15, command=guardar).pack(pady=20)

    def recuperar(self):
        email = simpledialog.askstring("Recuperar Contraseña", "Ingrese su email registrado:",
                                       parent=self.ventana)
        if email:
            user = self.dao.recuperar_password(email)
            if user:
                messagebox.showinfo("Contraseña Recuperada",
                                    f"Usuario: {user.usuario}\nContraseña: {user.password}\n\nGuardela en un lugar seguro")
            else:
                messagebox.showerror("Error", "Email no encontrado en el sistema")

    def mostrar(self):
        self.ventana.mainloop()
        return self.usuario_autenticado


if __name__ == "__main__":
    login = VentanaLogin()
    usuario = login.mostrar()
    if usuario:
        print(f"Login exitoso: {usuario}")