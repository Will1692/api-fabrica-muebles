from datetime import date


class Produccion:
    """
    Clase modelo que representa un registro de Producción
    Corresponde a la tabla: produccion

    Autor: William Alonso Samaca Lopez
    Sistema de Gestión Fábrica de Muebles
    """

    def __init__(self, id=None, nombre_producto=None, cantidad=None,
                 fecha_inicio=None, fecha_fin=None, estado=None):
        """
        Constructor de la clase Produccion

        Args:
            id: ID de la producción
            nombre_producto: Nombre del producto a fabricar
            cantidad: Cantidad a producir
            fecha_inicio: Fecha de inicio de producción
            fecha_fin: Fecha de finalización de producción
            estado: Estado de la producción (En Proceso, Completado, etc.)
        """
        self.id = id
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.fecha_inicio = fecha_inicio or date.today()
        self.fecha_fin = fecha_fin
        self.estado = estado

    def __str__(self):
        """Representación en string del objeto Produccion"""
        return (f"Produccion{{ID={self.id}, producto='{self.nombre_producto}', "
                f"cantidad={self.cantidad}, estado='{self.estado}'}}")

    def __repr__(self):
        return self.__str__()