from com.fabrica.muebles.util.conexion_bd import ConexionBD


class VerificarTablas:
    """
    Clase de utilidad para verificar la existencia de tablas en la base de datos
    y crear un diagnostico completo del estado de la base de datos

    Tablas verificadas: clientes, produccion, proveedor

    Autor: William Alonso Samaca Lopez
    Version: 2.0
    """

    @staticmethod
    def ejecutar():
        print("============================================================")
        print("   DIAGNOSTICO DE BASE DE DATOS - FABRICA DE MUEBLES")
        print("============================================================\n")

        if not VerificarTablas.probar_conexion():
            print("\nNo se pudo conectar a la base de datos.")
            print("Verifica que MySQL este ejecutandose")
            print("y que los datos en database.properties sean correctos.\n")
            return

        VerificarTablas.verificar_base_datos()

        print("\nVERIFICANDO TABLAS DEL SISTEMA...\n")
        clientes_existe = VerificarTablas.verificar_tabla("clientes")
        produccion_existe = VerificarTablas.verificar_tabla("produccion")
        proveedor_existe = VerificarTablas.verificar_tabla("proveedor")

        print("\n" + "=" * 60)
        print("RESUMEN DEL DIAGNOSTICO")
        print("=" * 60)

        print("\nBase de datos: fabrica_muebles")
        print(f"Tabla 'clientes': {'EXISTE' if clientes_existe else 'NO EXISTE'}")
        print(f"Tabla 'produccion': {'EXISTE' if produccion_existe else 'NO EXISTE'}")
        print(f"Tabla 'proveedor': {'EXISTE' if proveedor_existe else 'NO EXISTE'}")

        if clientes_existe:
            VerificarTablas.mostrar_estructura_tabla("clientes")

        if produccion_existe:
            VerificarTablas.mostrar_estructura_tabla("produccion")

        if proveedor_existe:
            VerificarTablas.mostrar_estructura_tabla("proveedor")

        print("\n" + "=" * 60)
        print("RECOMENDACIONES")
        print("=" * 60 + "\n")

        if not clientes_existe or not produccion_existe or not proveedor_existe:
            print("ACCION REQUERIDA:")
            print("Necesitas crear las tablas faltantes.")
            print("Ejecuta: python src/com/fabrica/muebles/util/crear_tablas_automatico.py\n")
        else:
            print("Tu base de datos esta completa y lista para usar.")
            print("Puedes continuar con el desarrollo.\n")

    @staticmethod
    def probar_conexion():
        print("Probando conexion a MySQL...\n")

        conexion = None
        try:
            conexion = ConexionBD.get_conexion()

            if conexion and conexion.open:
                print("Conexion exitosa")
                print("Host: localhost:3306")
                print("Usuario: root")
                print("Base de datos: fabrica_muebles")
                return True
        except Exception as e:
            print(f"Error al verificar conexion: {e}")
        finally:
            if conexion:
                try:
                    conexion.close()
                except:
                    pass
        return False

    @staticmethod
    def verificar_base_datos():
        print("\nVerificando base de datos...")

        conexion = None
        cursor = None
        try:
            conexion = ConexionBD.get_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT DATABASE()")
                bd = cursor.fetchone()

                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()

                print(f"Base de datos: {bd[0]}")
                print(f"Motor: MySQL")
                print(f"Version: {version[0]}")
        except Exception as e:
            print(f"Error al verificar base de datos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    @staticmethod
    def verificar_tabla(nombre_tabla):
        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(f"SHOW TABLES LIKE '{nombre_tabla}'")
                resultado = cursor.fetchone()

                if resultado:
                    print(f"Tabla '{nombre_tabla}' encontrada")
                    VerificarTablas.contar_registros(nombre_tabla)
                    return True
                else:
                    print(f"Tabla '{nombre_tabla}' NO existe")
                    return False
        except Exception as e:
            print(f"Error al verificar tabla '{nombre_tabla}': {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return False

    @staticmethod
    def contar_registros(nombre_tabla):
        sql = f"SELECT COUNT(*) as total FROM {nombre_tabla}"

        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchone()

            if resultado:
                print(f"   Registros: {resultado[0]}")
        except Exception as e:
            print(f"   No se pudo contar registros: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    @staticmethod
    def mostrar_estructura_tabla(nombre_tabla):
        print("\n" + "-" * 60)
        print(f"ESTRUCTURA DE LA TABLA: {nombre_tabla.upper()}")
        print("-" * 60)

        conexion = None
        cursor = None

        try:
            conexion = ConexionBD.get_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(f"DESCRIBE {nombre_tabla}")
                columnas = cursor.fetchall()

                print(f"{'COLUMNA':<20} {'TIPO':<15} {'NULO':<10} {'CLAVE':<10}")
                print("-" * 60)

                for columna in columnas:
                    nombre = columna[0]
                    tipo = columna[1]
                    nulo = "Si" if columna[2] == "YES" else "No"
                    clave = columna[3] if columna[3] else ""

                    print(f"{nombre:<20} {tipo:<15} {nulo:<10} {clave:<10}")
        except Exception as e:
            print(f"Error al mostrar estructura: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()


if __name__ == "__main__":
    VerificarTablas.ejecutar()