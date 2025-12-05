import pymysql
from pymysql import Error


class CrearTablasAutomatico:
    """
    Programa para crear automaticamente la base de datos y las tablas
    Sistema de Gestion - Fabrica de Muebles

    Tablas: clientes, produccion, proveedor

    Autor: William Alonso Samaca Lopez
    Version: 2.0
    """

    URL_SERVER = "localhost"
    PORT = 3306
    USUARIO = "root"
    CLAVE = "Mariana28"

    @staticmethod
    def ejecutar():
        print("============================================================")
        print("  CREACION AUTOMATICA DE BASE DE DATOS Y TABLAS")
        print("  Sistema: Fabrica de Muebles")
        print("============================================================\n")

        conexion = None
        cursor = None

        try:
            print("Paso 1: Conectando al servidor MySQL...")
            conexion = pymysql.connect(
                host=CrearTablasAutomatico.URL_SERVER,
                port=CrearTablasAutomatico.PORT,
                user=CrearTablasAutomatico.USUARIO,
                password=CrearTablasAutomatico.CLAVE,
                charset='utf8mb4'
            )
            cursor = conexion.cursor()
            print("EXITOSO: Conexion establecida\n")

            print("Paso 2: Creando base de datos 'fabrica_muebles'...")
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS fabrica_muebles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("EXITOSO: Base de datos creada\n")

            cursor.execute("USE fabrica_muebles")

            print("Paso 3: Creando tabla 'clientes'...")
            cursor.execute("DROP TABLE IF EXISTS clientes")
            sql_clientes = """
                CREATE TABLE clientes (
                    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    direccion VARCHAR(200),
                    email VARCHAR(100) NOT NULL,
                    fecha_registro DATE NOT NULL,
                    estado INT DEFAULT 1,
                    INDEX idx_nombre (nombre),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(sql_clientes)
            print("EXITOSO: Tabla 'clientes' creada\n")

            print("Paso 4: Creando tabla 'produccion'...")
            cursor.execute("DROP TABLE IF EXISTS produccion")
            sql_produccion = """
                CREATE TABLE produccion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_producto VARCHAR(100) NOT NULL,
                    cantidad INT NOT NULL DEFAULT 0,
                    fecha_inicio DATE NOT NULL,
                    fecha_fin DATE,
                    estado VARCHAR(50) NOT NULL,
                    INDEX idx_estado (estado),
                    INDEX idx_fecha (fecha_inicio)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(sql_produccion)
            print("EXITOSO: Tabla 'produccion' creada\n")

            print("Paso 5: Creando tabla 'proveedor'...")
            cursor.execute("DROP TABLE IF EXISTS proveedor")
            sql_proveedor = """
                CREATE TABLE proveedor (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    contacto VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    direccion VARCHAR(200),
                    correo VARCHAR(100) NOT NULL,
                    INDEX idx_nombre (nombre)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(sql_proveedor)
            print("EXITOSO: Tabla 'proveedor' creada\n")

            print("Paso 6: Insertando datos de prueba en 'clientes'...")
            clientes_insert = [
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES ('Juan Perez Garcia', '3101234567', 'Calle 10 #20-30, Tunja', 'juan.perez@email.com', CURDATE(), 1)",
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES ('Maria Lopez Rodriguez', '3209876543', 'Carrera 15 #25-40, Tunja', 'maria.lopez@email.com', CURDATE(), 1)",
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES ('Carlos Martinez Silva', '3158765432', 'Avenida Norte #30-15, Tunja', 'carlos.martinez@email.com', CURDATE(), 1)",
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES ('Ana Gomez Torres', '3187654321', 'Calle 5 #12-25, Tunja', 'ana.gomez@email.com', CURDATE(), 1)",
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES ('Luis Hernandez Castro', '3145678901', 'Carrera 8 #18-20, Tunja', 'luis.hernandez@email.com', CURDATE(), 1)"
            ]
            for insert in clientes_insert:
                cursor.execute(insert)
            print(f"EXITOSO: {len(clientes_insert)} clientes insertados\n")

            print("Paso 7: Insertando datos de prueba en 'produccion'...")
            produccion_insert = [
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES ('Mesa de Comedor Roble', 10, '2024-11-01', '2024-11-15', 'Finalizado')",
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES ('Silla Ejecutiva Ergonomica', 25, '2024-11-10', NULL, 'En Proceso')",
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES ('Escritorio Moderno L-Shape', 8, '2024-11-05', '2024-11-20', 'Finalizado')",
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES ('Estanteria de Pared', 15, '2024-11-12', NULL, 'En Proceso')",
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES ('Armario 3 Puertas', 5, '2024-10-25', '2024-11-08', 'Entregado')"
            ]
            for insert in produccion_insert:
                cursor.execute(insert)
            print(f"EXITOSO: {len(produccion_insert)} registros de produccion insertados\n")

            print("Paso 8: Insertando datos de prueba en 'proveedor'...")
            proveedor_insert = [
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES ('Maderas del Norte S.A.S', 'Pedro Ramirez', '3201234567', 'Zona Industrial Norte, Tunja', 'ventas@maderasnorte.com')",
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES ('Herrajes y Accesorios Ltda', 'Sandra Castro', '3159876543', 'Calle 20 #15-30, Tunja', 'pedidos@herrajes.com')",
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES ('Pinturas Industriales', 'Miguel Angel Torres', '3187654321', 'Carrera 10 #25-40, Tunja', 'contacto@pinturas.com')",
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES ('Tapizados El Roble', 'Laura Martinez', '3145678901', 'Avenida Sur #18-22, Tunja', 'info@tapizados.com')",
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES ('Vidrios y Espejos S.A.', 'Roberto Diaz', '3208765432', 'Zona Comercial Este, Tunja', 'ventas@vidrios.com')"
            ]
            for insert in proveedor_insert:
                cursor.execute(insert)
            print(f"EXITOSO: {len(proveedor_insert)} proveedores insertados\n")

            conexion.commit()

            print("============================================================")
            print("    BASE DE DATOS CREADA EXITOSAMENTE!")
            print("============================================================\n")
            print("RESUMEN:")
            print("   Base de datos: fabrica_muebles")
            print("   Tabla 'clientes' creada con 5 registros")
            print("   Tabla 'produccion' creada con 5 registros")
            print("   Tabla 'proveedor' creada con 5 registros\n")
            print("Tu sistema esta listo para usar\n")

        except Error as e:
            print(f"\nERROR DE SQL: {e}")
            print("Verifica que MySQL este ejecutandose")
            print("Verifica usuario y contrasena")
            if conexion:
                conexion.rollback()
        except Exception as e:
            print(f"\nERROR: {e}")
            if conexion:
                conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
                print("Conexion cerrada\n")


if __name__ == "__main__":
    CrearTablasAutomatico.ejecutar()