from com.fabrica.muebles.modelo.produccion import Produccion
from com.fabrica.muebles.util.conexion_bd import ConexionBD


class ProduccionDAO:
    """DAO para operaciones CRUD de Producción"""

    def insertar_produccion(self, produccion):
        sql = """INSERT INTO produccion 
                 (codigo_mueble, nombre_cliente, tipo_documento_cliente, numero_documento_cliente, 
                  nombre_producto, cantidad, fecha_inicio, fecha_fin, estado, observaciones, ruta_archivo) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (
                produccion.codigo_mueble,
                produccion.nombre_cliente,
                produccion.tipo_documento_cliente,
                produccion.numero_documento_cliente,
                produccion.nombre_producto,
                produccion.cantidad,
                produccion.fecha_inicio,
                produccion.fecha_fin,
                produccion.estado,
                produccion.observaciones,
                produccion.ruta_archivo
            ))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            if 'conexion' in locals():
                conexion.rollback()
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    def consultar_todos(self):
        sql = """SELECT id, codigo_mueble, nombre_cliente, tipo_documento_cliente, numero_documento_cliente,
                        nombre_producto, cantidad, fecha_inicio, fecha_fin, estado, observaciones, ruta_archivo 
                 FROM produccion 
                 ORDER BY id DESC"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql)
            return [Produccion(*fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def consultar_por_id(self, id):
        sql = """SELECT id, codigo_mueble, nombre_cliente, tipo_documento_cliente, numero_documento_cliente,
                        nombre_producto, cantidad, fecha_inicio, fecha_fin, estado, observaciones, ruta_archivo 
                 FROM produccion 
                 WHERE id = %s"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (id,))
            fila = cursor.fetchone()
            return Produccion(*fila) if fila else None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def actualizar_produccion(self, produccion):
        sql = """UPDATE produccion 
                 SET codigo_mueble=%s, nombre_cliente=%s, tipo_documento_cliente=%s, numero_documento_cliente=%s,
                     nombre_producto=%s, cantidad=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s, observaciones=%s, ruta_archivo=%s 
                 WHERE id=%s"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (
                produccion.codigo_mueble,
                produccion.nombre_cliente,
                produccion.tipo_documento_cliente,
                produccion.numero_documento_cliente,
                produccion.nombre_producto,
                produccion.cantidad,
                produccion.fecha_inicio,
                produccion.fecha_fin,
                produccion.estado,
                produccion.observaciones,
                produccion.ruta_archivo,
                produccion.id
            ))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            if 'conexion' in locals():
                conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def finalizar_produccion(self, id):
        sql = "UPDATE produccion SET estado='Finalizado', fecha_fin=CURDATE() WHERE id=%s"
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (id,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            if 'conexion' in locals():
                conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar_produccion(self, id):
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM produccion WHERE id=%s", (id,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            if 'conexion' in locals():
                conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()