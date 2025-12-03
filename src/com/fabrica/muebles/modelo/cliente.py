from datetime import date


class Cliente:
    """
    Clase modelo que representa un Cliente en el sistema
    Corresponde a la tabla: clientes

    Autor: William Alonso Samaca Lopez
    Sistema de Gestión Fábrica de Muebles
    """

    def __init__(self, id_cliente=None, nombre=None, telefono=None, direccion=None,
                 email=None, fecha_registro=None, estado=1):
        """
        Constructor de la clase Cliente

        Args:
            id_cliente: ID del cliente (None para nuevos clientes)
            nombre: Nombre completo del cliente
            telefono: Teléfono del cliente
            direccion: Dirección del cliente
            email: Email del cliente
            fecha_registro: Fecha de registro (None para fecha actual)
            estado: Estado del cliente (1=Activo, 0=Inactivo)
        """
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.fecha_registro = fecha_registro or date.today()
        self.estado = estado

    def get_estado_texto(self):
        """Retorna el estado como texto"""
        return "Activo" if self.estado == 1 else "Inactivo"

    def __str__(self):
        """Representación en string del objeto Cliente"""
        return (f"Cliente{{ID={self.id_cliente}, nombre='{self.nombre}', "
                f"telefono='{self.telefono}', email='{self.email}', "
                f"estado='{self.get_estado_texto()}'}}")

    def __repr__(self):
        return self.__str__()