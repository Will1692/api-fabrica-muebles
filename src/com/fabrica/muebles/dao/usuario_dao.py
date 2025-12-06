import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from com.fabrica.muebles.modelo.usuario import Usuario
from com.fabrica.muebles.util.conexion_bd import ConexionBD


class UsuarioDAO:
    """DAO para operaciones con usuarios"""

    def autenticar(self, usuario, password):
        """Valida usuario y contraseña, retorna objeto Usuario si es correcto"""
        sql = "SELECT id_usuario, usuario, password, rol, email, fecha_registro, estado FROM usuarios WHERE usuario = %s AND password = %s AND estado = 1"
        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario, password))
            fila = cursor.fetchone()

            if fila:
                return Usuario(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])
            return None
        except Exception as e:
            print(f"Error al autenticar: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def registrar(self, usuario):
        """Registra un nuevo usuario"""
        sql = "INSERT INTO usuarios (usuario, password, rol, email, fecha_registro, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario.usuario, usuario.password, usuario.rol,
                                 usuario.email, usuario.fecha_registro, usuario.estado))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            if conexion:
                conexion.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def recuperar_password(self, email):
        """Busca usuario por email para recuperar contraseña"""
        sql = "SELECT id_usuario, usuario, password, rol, email FROM usuarios WHERE email = %s AND estado = 1"
        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql, (email,))
            fila = cursor.fetchone()

            if fila:
                return Usuario(fila[0], fila[1], fila[2], fila[3], fila[4])
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()