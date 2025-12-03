from com.fabrica.muebles.modelo.proveedor import Proveedor
from com.fabrica.muebles.util.conexion_bd import ConexionBD


class ProveedorDAO:
    """DAO para operaciones CRUD de Proveedores"""

    def buscar(self, id):
        """Busca un proveedor por ID"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM proveedor WHERE id = %s", (id,))
            fila = cursor.fetchone()
            return Proveedor(*fila) if fila else None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def listar(self):
        """Lista todos los proveedores"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM proveedor")
            return [Proveedor(*fila) for fila in cursor.fetchall()]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def agregar(self, p):
        """Agrega un nuevo proveedor"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES (%s, %s, %s, %s, %s)",
                (p.nombre, p.contacto, p.telefono, p.direccion, p.correo))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, p):
        """Actualiza un proveedor existente"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE proveedor SET nombre=%s, contacto=%s, telefono=%s, direccion=%s, correo=%s WHERE id=%s",
                (p.nombre, p.contacto, p.telefono, p.direccion, p.correo, p.id))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id):
        """Elimina un proveedor"""
        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM proveedor WHERE id=%s", (id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()