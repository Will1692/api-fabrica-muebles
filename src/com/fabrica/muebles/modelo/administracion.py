from com.fabrica.muebles.dao.cliente_dao import ClienteDAO
from com.fabrica.muebles.dao.proveedor_dao import ProveedorDAO


class Administracion:
    """Clase que centraliza las operaciones de administración"""

    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.proveedor_dao = ProveedorDAO()

    # CLIENTES
    def agregar_cliente(self, cliente):
        return self.cliente_dao.insertar_cliente(cliente)

    def listar_clientes(self):
        return self.cliente_dao.consultar_todos()

    def buscar_cliente(self, id):
        return self.cliente_dao.consultar_por_id(id)

    def actualizar_cliente(self, cliente):
        return self.cliente_dao.actualizar_cliente(cliente)

    def eliminar_cliente(self, id):
        return self.cliente_dao.eliminar_cliente(id)

    # PROVEEDORES
    def agregar_proveedor(self, proveedor):
        return self.proveedor_dao.agregar(proveedor)

    def listar_proveedores(self):
        return self.proveedor_dao.listar()

    def buscar_proveedor(self, id):
        return self.proveedor_dao.buscar(id)

    def actualizar_proveedor(self, proveedor):
        return self.proveedor_dao.actualizar(proveedor)

    def eliminar_proveedor(self, id):
        return self.proveedor_dao.eliminar(id)