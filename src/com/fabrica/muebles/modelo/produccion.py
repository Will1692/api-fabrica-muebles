from datetime import date


class Produccion:
    """
    Clase modelo que representa un registro de Producción
    Corresponde a la tabla: produccion

    Autor: William Alonso Samaca Lopez
    Sistema de Gestión Fábrica de Muebles
    """

    def __init__(self, id=None, codigo_mueble=None, nombre_cliente=None, tipo_documento_cliente='CC',
                 numero_documento_cliente=None, nombre_producto=None, cantidad=None,
                 fecha_inicio=None, fecha_fin=None, estado=None, observaciones=None, ruta_archivo=None):
        """
        Constructor de la clase Produccion

        Args:
            id: ID de la producción (autogenerado)
            codigo_mueble: Código del mueble asignado por producción
            nombre_cliente: Nombre del cliente
            tipo_documento_cliente: Tipo de documento del cliente (CC o NIT)
            numero_documento_cliente: Número de documento del cliente
            nombre_producto: Nombre del producto a fabricar
            cantidad: Cantidad a producir
            fecha_inicio: Fecha de inicio de producción
            fecha_fin: Fecha de finalización de producción
            estado: Estado de la producción
            observaciones: Observaciones del producto
            ruta_archivo: Ruta del archivo (foto/plano)
        """
        self.id = id
        self.codigo_mueble = codigo_mueble
        self.nombre_cliente = nombre_cliente
        self.tipo_documento_cliente = tipo_documento_cliente
        self.numero_documento_cliente = numero_documento_cliente
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.fecha_inicio = fecha_inicio or date.today()
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.observaciones = observaciones
        self.ruta_archivo = ruta_archivo

    def __str__(self):
        """Representación en string del objeto Produccion"""
        return (f"Produccion{{codigo='{self.codigo_mueble}', producto='{self.nombre_producto}', "
                f"cantidad={self.cantidad}, estado='{self.estado}'}}")

    def __repr__(self):
        return self.__str__()