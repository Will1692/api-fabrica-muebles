from datetime import date


class Cliente:
    """
    Clase modelo que representa un Cliente en el sistema
    Corresponde a la tabla: clientes

    Autor: William Alonso Samaca Lopez
    Sistema de Gestión Fábrica de Muebles
    """

    def __init__(self, id_cliente=None, nombre=None, telefono=None, direccion=None,
                 email=None, codigo_mueble=None, tipo_documento='CC', numero_documento=None,
                 tipo_mueble_vendido=None, cantidad=1, valor_mueble=0, ruta_foto=None,
                 fecha_registro=None):
        """
        Constructor de la clase Cliente

        Args:
            id_cliente: ID del cliente (None para nuevos clientes)
            nombre: Nombre completo del cliente
            telefono: Teléfono del cliente
            direccion: Dirección del cliente
            email: Email del cliente
            codigo_mueble: Código del mueble vendido (asignado por producción)
            tipo_documento: Tipo de documento (CC o NIT)
            numero_documento: Número de documento
            tipo_mueble_vendido: Tipo de mueble que se le vendió
            cantidad: Cantidad de muebles vendidos
            valor_mueble: Valor/precio del mueble
            ruta_foto: Ruta de la foto del mueble
            fecha_registro: Fecha de registro (None para fecha actual)
        """
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.codigo_mueble = codigo_mueble
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.tipo_mueble_vendido = tipo_mueble_vendido
        self.cantidad = cantidad
        self.valor_mueble = valor_mueble
        self.ruta_foto = ruta_foto
        self.fecha_registro = fecha_registro or date.today()

    def __str__(self):
        """Representación en string del objeto Cliente"""
        return (f"Cliente{{codigo_mueble='{self.codigo_mueble}', nombre='{self.nombre}', "
                f"tipo_doc='{self.tipo_documento}', num_doc='{self.numero_documento}', "
                f"telefono='{self.telefono}', email='{self.email}'}}")

    def __repr__(self):
        return self.__str__()