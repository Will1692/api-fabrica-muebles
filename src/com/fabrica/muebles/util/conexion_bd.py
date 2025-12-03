import pymysql
from pymysql import Error
import os
from pathlib import Path


class ConexionBD:
    _propiedades_cargadas = False
    _host = None
    _port = None
    _database = None
    _user = None
    _password = None
    _charset = None

    def __init__(self):
        raise RuntimeError("Esta clase no debe ser instanciada. Use los métodos estáticos.")

    @classmethod
    def _inicializar(cls):
        if cls._propiedades_cargadas:
            return

        try:
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            properties_path = project_root / "config" / "database.properties"

            if not properties_path.exists():
                print(f"No se encontró el archivo: {properties_path}")
                print("Asegúrate de que existe en: config/database.properties")
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {properties_path}")

            propiedades = {}
            with open(properties_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            propiedades[key.strip()] = value.strip()

            cls._host = propiedades.get('db.host')
            cls._port = int(propiedades.get('db.port', 3306))
            cls._database = propiedades.get('db.database')
            cls._user = propiedades.get('db.user')
            cls._password = propiedades.get('db.password')
            cls._charset = propiedades.get('db.charset', 'utf8mb4')

            if not all([cls._host, cls._database, cls._user, cls._password]):
                raise ValueError("Propiedades de base de datos incompletas en database.properties")

            print("Archivo de configuración cargado correctamente")
            print("Configuración de MySQL cargada correctamente")
            cls._propiedades_cargadas = True

        except Exception as e:
            raise RuntimeError(f"No se pudieron cargar las propiedades de conexión: {str(e)}")

    @classmethod
    def get_conexion(cls):
        if not cls._propiedades_cargadas:
            cls._inicializar()

        try:
            conexion = pymysql.connect(
                host=cls._host,
                port=cls._port,
                database=cls._database,
                user=cls._user,
                password=cls._password,
                charset=cls._charset,
                autocommit=False
            )
            return conexion
        except Error as e:
            print(f"ERROR DETALLADO: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            raise RuntimeError(f"No se pudo establecer la conexión: {str(e)}")
        except Exception as e:
            print(f"ERROR INESPERADO: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            raise RuntimeError(f"Error inesperado: {str(e)}")

    @classmethod
    def probar_conexion(cls):
        if not cls._propiedades_cargadas:
            cls._inicializar()

        conexion = None
        cursor = None

        try:
            conexion = cls.get_conexion()
            print("Conexión establecida correctamente a la base de datos")

            cursor = conexion.cursor()
            cursor.execute("SELECT DATABASE()")
            resultado = cursor.fetchone()

            if resultado:
                print(f"Base de datos: {resultado[0]}")

            print("Conexión exitosa y activa")
            return True

        except Exception as e:
            print(f"Error probando la conexión: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conexion:
                try:
                    conexion.close()
                except:
                    pass

    @classmethod
    def cerrar_conexion(cls, conexion):
        if conexion:
            try:
                conexion.close()
                print("Conexión cerrada correctamente")
            except Exception as e:
                print(f"Error al cerrar conexión: {str(e)}")
                import traceback
                traceback.print_exc()

    @classmethod
    def get_connection(cls):
        return cls.get_conexion()


def obtener_conexion():
    return ConexionBD.get_conexion()