from com.fabrica.muebles.modelo.produccion import Produccion
from com.fabrica.muebles.util.conexion_bd import ConexionBD


class ProduccionDAO:
    """DAO para operaciones CRUD de Producción"""

    def insertar_produccion(self, produccion):
        """Inserta una nueva producción"""
        sql = "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES (%s, %s, %s, %s, %s)"
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (produccion.nombre_producto, produccion.cantidad,
                                 produccion.fecha_inicio, produccion.fecha_fin, produccion.estado))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar producción: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def consultar_todos(self):
        """Consulta todas las producciones"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM produccion ORDER BY id DESC")
            return [Produccion(*fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error al consultar producciones: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def consultar_por_id(self, id):
        """Consulta una producción por ID"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM produccion WHERE id = %s", (id,))
            fila = cursor.fetchone()
            return Produccion(*fila) if fila else None
        except Exception as e:
            print(f"Error al consultar producción: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def actualizar_produccion(self, produccion):
        """Actualiza una producción existente"""
        sql = "UPDATE produccion SET nombre_producto=%s, cantidad=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s WHERE id=%s"
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (produccion.nombre_producto, produccion.cantidad,
                                 produccion.fecha_inicio, produccion.fecha_fin,
                                 produccion.estado, produccion.id))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar producción: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def finalizar_produccion(self, id):
        """Finaliza una producción (marca como Finalizado y establece fecha fin)"""
        sql = "UPDATE produccion SET estado='Finalizado', fecha_fin=CURDATE() WHERE id=%s"
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al finalizar producción: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar_produccion(self, id):
        """Elimina una producción"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM produccion WHERE id=%s", (id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar producción: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()