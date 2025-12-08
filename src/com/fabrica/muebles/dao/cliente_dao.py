from com.fabrica.muebles.modelo.cliente import Cliente
from com.fabrica.muebles.util.conexion_bd import ConexionBD


class ClienteDAO:
    """DAO para operaciones CRUD de Clientes"""

    def insertar_cliente(self, cliente):
        sql = """INSERT INTO clientes 
                 (nombre, telefono, direccion, email, codigo_mueble, tipo_documento, 
                  numero_documento, tipo_mueble_vendido, cantidad, valor_mueble, 
                  ruta_foto, fecha_registro) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (
                cliente.nombre,
                cliente.telefono,
                cliente.direccion,
                cliente.email,
                cliente.codigo_mueble,
                cliente.tipo_documento,
                cliente.numero_documento,
                cliente.tipo_mueble_vendido,
                cliente.cantidad,
                cliente.valor_mueble,
                cliente.ruta_foto,
                cliente.fecha_registro
            ))
            conexion.commit()
            print("Cliente insertado correctamente")
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
        sql = """SELECT id_cliente, nombre, telefono, direccion, email, codigo_mueble, 
                        tipo_documento, numero_documento, tipo_mueble_vendido, cantidad, 
                        valor_mueble, ruta_foto, fecha_registro 
                 FROM clientes 
                 ORDER BY id_cliente DESC"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql)
            return [Cliente(*fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def consultar_por_id(self, id_cliente):
        sql = """SELECT id_cliente, nombre, telefono, direccion, email, codigo_mueble, 
                        tipo_documento, numero_documento, tipo_mueble_vendido, cantidad, 
                        valor_mueble, ruta_foto, fecha_registro 
                 FROM clientes 
                 WHERE id_cliente = %s"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (id_cliente,))
            fila = cursor.fetchone()
            return Cliente(*fila) if fila else None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def actualizar_cliente(self, cliente):
        sql = """UPDATE clientes 
                 SET nombre=%s, telefono=%s, direccion=%s, email=%s, codigo_mueble=%s, 
                     tipo_documento=%s, numero_documento=%s, tipo_mueble_vendido=%s, 
                     cantidad=%s, valor_mueble=%s, ruta_foto=%s
                 WHERE id_cliente=%s"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (
                cliente.nombre,
                cliente.telefono,
                cliente.direccion,
                cliente.email,
                cliente.codigo_mueble,
                cliente.tipo_documento,
                cliente.numero_documento,
                cliente.tipo_mueble_vendido,
                cliente.cantidad,
                cliente.valor_mueble,
                cliente.ruta_foto,
                cliente.id_cliente
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

    def eliminar_cliente(self, id_cliente):
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (id_cliente,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()