import sys
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog

sys.path.insert(0, str(Path(__file__).parent / "src"))

from com.fabrica.muebles.vista.ventana_login import VentanaLogin
from com.fabrica.muebles.vista.menu_principal import MenuPrincipal

if __name__ == "__main__":
    login = VentanaLogin()
    usuario = login.mostrar()

    if usuario:
        print(f"Bienvenido: {usuario.usuario} - Rol: {usuario.rol}")
        menu = MenuPrincipal(usuario)
        menu.mostrar()
    else:
        print("Login cancelado")