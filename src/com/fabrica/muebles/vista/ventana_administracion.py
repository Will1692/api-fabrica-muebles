from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class VentanaAdministracion(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Administración - Fábrica de Muebles")
        self.setGeometry(200, 100, 800, 600)

        contenedor = QtWidgets.QWidget()
        layout_principal = QtWidgets.QVBoxLayout(contenedor)

        # ----- Título -----
        self.lblTitulo = QtWidgets.QLabel("Panel de Administración")
        self.lblTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitulo.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))

        layout_principal.addWidget(self.lblTitulo)

        # ----- Botones Centrales -----
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(60, 40, 60, 40)

        self.btnClientes = QtWidgets.QPushButton("Clientes")
        self.btnProveedores = QtWidgets.QPushButton("Proveedores")
        self.btnProduccion = QtWidgets.QPushButton("Producción")
        self.btnCerrarSesion = QtWidgets.QPushButton("Cerrar Sesión")

        botones = [
            self.btnClientes,
            self.btnProveedores,
            self.btnProduccion,
            self.btnCerrarSesion
        ]

        for b in botones:
            b.setFont(QtGui.QFont("Segoe UI", 16))
            b.setMinimumHeight(60)

        grid.addWidget(self.btnClientes, 0, 0)
        grid.addWidget(self.btnProveedores, 0, 1)
        grid.addWidget(self.btnProduccion, 1, 0)
        grid.addWidget(self.btnCerrarSesion, 1, 1)

        layout_principal.addLayout(grid)

        # ----- Info Inferior -----
        self.lblInfo = QtWidgets.QLabel("Seleccione un módulo")
        self.lblInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInfo.setFont(QtGui.QFont("Segoe UI", 12))

        layout_principal.addWidget(self.lblInfo)

        self.setCentralWidget(contenedor)

        self.conectarEventos()

    # ------------------------------
    # Eventos
    # ------------------------------
    def conectarEventos(self):

        self.btnClientes.clicked.connect(self.abrirClientes)
        self.btnProveedores.clicked.connect(self.abrirProveedores)
        self.btnProduccion.clicked.connect(self.abrirProduccion)
        self.btnCerrarSesion.clicked.connect(self.cerrarSesion)

    def abrirClientes(self):
        self.lblInfo.setText("Abriendo módulo Clientes...")
        # Aquí abrirías tu ventana real
        QtWidgets.QMessageBox.information(self, "Clientes", "Módulo Clientes abierto.")
        self.lblInfo.setText("Módulo Clientes abierto")

    def abrirProveedores(self):
        self.lblInfo.setText("Abriendo módulo Proveedores...")
        QtWidgets.QMessageBox.information(self, "Proveedores", "Módulo Proveedores abierto.")
        self.lblInfo.setText("Módulo Proveedores abierto")

    def abrirProduccion(self):
        self.lblInfo.setText("Abriendo módulo Producción...")
        QtWidgets.QMessageBox.information(self, "Producción", "Módulo Producción abierto.")
        self.lblInfo.setText("Módulo Producción abierto")

    def cerrarSesion(self):
        confirmación = QtWidgets.QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Desea cerrar la sesión de administración?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirmación == QtWidgets.QMessageBox.Yes:
            QtWidgets.QMessageBox.information(self, "Sesión Cerrada", "Sesión cerrada correctamente.")
            self.close()


# ------- MAIN -------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaAdministracion()
    ventana.show()
    sys.exit(app.exec_())