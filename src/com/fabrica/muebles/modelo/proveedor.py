class Proveedor:
    """
    Clase modelo que representa un Proveedor
    Corresponde a la tabla: proveedor

    Autor: William Alonso Samaca Lopez
    Sistema de Gestión Fábrica de Muebles
    """

    def __init__(self, id=None, nombre=None, contacto=None, telefono=None,
                 direccion=None, correo=None):
        """
        Constructor de la clase Proveedor

        Args:
            id: ID del proveedor (None para nuevos proveedores)
            nombre: Nombre de la empresa proveedora
            contacto: Persona de contacto
            telefono: Teléfono del proveedor
            direccion: Dirección del proveedor
            correo: Email del proveedor
        """
        self.id = id
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

    def __str__(self):
        """Representación en string del objeto Proveedor"""
        return (f"Proveedor{{ID={self.id}, nombre='{self.nombre}', "
                f"contacto='{self.contacto}', telefono='{self.telefono}', "
                f"correo='{self.correo}'}}")

    def __repr__(self):
        return self.__str__()