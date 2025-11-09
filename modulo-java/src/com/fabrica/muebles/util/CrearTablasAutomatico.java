package com.fabrica.muebles.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.SQLException;

/**
 * Programa para crear automáticamente la base de datos y las tablas
 * Sistema de Gestión - Fábrica de Muebles
 * 
 * Tablas: clientes, produccion, proveedor
 * 
 * @author William Alonso Samaca Lopez
 * @version 2.0
 */
public class CrearTablasAutomatico {
    
    // Datos de conexión (sin base de datos específica para crearla primero)
    private static final String URL_SERVER = "jdbc:mysql://localhost:3306/?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true";
    private static final String USUARIO = "root";
    private static final String CLAVE = "Mariana28";
    
    public static void main(String[] args) {
        System.out.println("════════════════════════════════════════════════════════");
        System.out.println("  CREACIÓN AUTOMÁTICA DE BASE DE DATOS Y TABLAS        ");
        System.out.println("  Sistema: Fábrica de Muebles                          ");
        System.out.println("════════════════════════════════════════════════════════");
        System.out.println();
        
        Connection conn = null;
        Statement stmt = null;
        
        try {
            // PASO 1: Registrar el driver
            System.out.println("Paso 1: Registrando driver JDBC...");
            Class.forName("com.mysql.cj.jdbc.Driver");
            System.out.println("✅ EXITOSO: Driver registrado correctamente");
            System.out.println();
            
            // PASO 2: Conectar al servidor MySQL (sin base de datos específica)
            System.out.println("Paso 2: Conectando al servidor MySQL...");
            conn = DriverManager.getConnection(URL_SERVER, USUARIO, CLAVE);
            stmt = conn.createStatement();
            System.out.println("✅ EXITOSO: Conexión establecida");
            System.out.println();
            
            // PASO 3: Crear la base de datos
            System.out.println("Paso 3: Creando base de datos 'fabrica_muebles'...");
            stmt.executeUpdate("CREATE DATABASE IF NOT EXISTS fabrica_muebles " +
                             "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
            System.out.println("✅ EXITOSO: Base de datos creada");
            System.out.println();
            
            // PASO 4: Usar la base de datos
            stmt.executeUpdate("USE fabrica_muebles");
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 5: Crear tabla CLIENTES
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 4: Creando tabla 'clientes'...");
            stmt.executeUpdate("DROP TABLE IF EXISTS clientes");
            
            String sqlClientes = 
                "CREATE TABLE clientes (" +
                "  id_cliente INT AUTO_INCREMENT PRIMARY KEY," +
                "  nombre VARCHAR(100) NOT NULL," +
                "  telefono VARCHAR(20) NOT NULL," +
                "  direccion VARCHAR(200)," +
                "  email VARCHAR(100) NOT NULL," +
                "  fecha_registro DATE NOT NULL," +
                "  estado INT DEFAULT 1," +
                "  INDEX idx_nombre (nombre)," +
                "  INDEX idx_email (email)" +
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
            
            stmt.executeUpdate(sqlClientes);
            System.out.println("✅ EXITOSO: Tabla 'clientes' creada");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 6: Crear tabla PRODUCCION
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 5: Creando tabla 'produccion'...");
            stmt.executeUpdate("DROP TABLE IF EXISTS produccion");
            
            String sqlProduccion = 
                "CREATE TABLE produccion (" +
                "  id INT AUTO_INCREMENT PRIMARY KEY," +
                "  nombre_producto VARCHAR(100) NOT NULL," +
                "  cantidad INT NOT NULL DEFAULT 0," +
                "  fecha_inicio DATE NOT NULL," +
                "  fecha_fin DATE," +
                "  estado VARCHAR(50) NOT NULL," +
                "  INDEX idx_estado (estado)," +
                "  INDEX idx_fecha (fecha_inicio)" +
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
            
            stmt.executeUpdate(sqlProduccion);
            System.out.println("✅ EXITOSO: Tabla 'produccion' creada");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 7: Crear tabla PROVEEDOR
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 6: Creando tabla 'proveedor'...");
            stmt.executeUpdate("DROP TABLE IF EXISTS proveedor");
            
            String sqlProveedor = 
                "CREATE TABLE proveedor (" +
                "  id INT AUTO_INCREMENT PRIMARY KEY," +
                "  nombre VARCHAR(100) NOT NULL," +
                "  contacto VARCHAR(100) NOT NULL," +
                "  telefono VARCHAR(20) NOT NULL," +
                "  direccion VARCHAR(200)," +
                "  correo VARCHAR(100) NOT NULL," +
                "  INDEX idx_nombre (nombre)" +
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
            
            stmt.executeUpdate(sqlProveedor);
            System.out.println("✅ EXITOSO: Tabla 'proveedor' creada");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 8: Insertar datos de prueba en CLIENTES
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 7: Insertando datos de prueba en 'clientes'...");
            
            String[] clientesInsert = {
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES " +
                "('Juan Pérez García', '3101234567', 'Calle 10 #20-30, Tunja', 'juan.perez@email.com', CURDATE(), 1)",
                
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES " +
                "('María López Rodríguez', '3209876543', 'Carrera 15 #25-40, Tunja', 'maria.lopez@email.com', CURDATE(), 1)",
                
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES " +
                "('Carlos Martínez Silva', '3158765432', 'Avenida Norte #30-15, Tunja', 'carlos.martinez@email.com', CURDATE(), 1)",
                
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES " +
                "('Ana Gómez Torres', '3187654321', 'Calle 5 #12-25, Tunja', 'ana.gomez@email.com', CURDATE(), 1)",
                
                "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) VALUES " +
                "('Luis Hernández Castro', '3145678901', 'Carrera 8 #18-20, Tunja', 'luis.hernandez@email.com', CURDATE(), 1)"
            };
            
            for (String insert : clientesInsert) {
                stmt.executeUpdate(insert);
            }
            System.out.println("✅ EXITOSO: " + clientesInsert.length + " clientes insertados");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 9: Insertar datos de prueba en PRODUCCION
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 8: Insertando datos de prueba en 'produccion'...");
            
            String[] produccionInsert = {
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES " +
                "('Mesa de Comedor Roble', 10, '2024-11-01', '2024-11-15', 'Finalizado')",
                
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES " +
                "('Silla Ejecutiva Ergonómica', 25, '2024-11-10', NULL, 'En Proceso')",
                
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES " +
                "('Escritorio Moderno L-Shape', 8, '2024-11-05', '2024-11-20', 'Finalizado')",
                
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES " +
                "('Estantería de Pared', 15, '2024-11-12', NULL, 'En Proceso')",
                
                "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES " +
                "('Armario 3 Puertas', 5, '2024-10-25', '2024-11-08', 'Entregado')"
            };
            
            for (String insert : produccionInsert) {
                stmt.executeUpdate(insert);
            }
            System.out.println("✅ EXITOSO: " + produccionInsert.length + " registros de producción insertados");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // PASO 10: Insertar datos de prueba en PROVEEDOR
            // ═══════════════════════════════════════════════════════════════
            System.out.println("Paso 9: Insertando datos de prueba en 'proveedor'...");
            
            String[] proveedorInsert = {
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES " +
                "('Maderas del Norte S.A.S', 'Pedro Ramírez', '3201234567', 'Zona Industrial Norte, Tunja', 'ventas@maderasnorte.com')",
                
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES " +
                "('Herrajes y Accesorios Ltda', 'Sandra Castro', '3159876543', 'Calle 20 #15-30, Tunja', 'pedidos@herrajes.com')",
                
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES " +
                "('Pinturas Industriales', 'Miguel Ángel Torres', '3187654321', 'Carrera 10 #25-40, Tunja', 'contacto@pinturas.com')",
                
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES " +
                "('Tapizados El Roble', 'Laura Martínez', '3145678901', 'Avenida Sur #18-22, Tunja', 'info@tapizados.com')",
                
                "INSERT INTO proveedor (nombre, contacto, telefono, direccion, correo) VALUES " +
                "('Vidrios y Espejos S.A.', 'Roberto Díaz', '3208765432', 'Zona Comercial Este, Tunja', 'ventas@vidrios.com')"
            };
            
            for (String insert : proveedorInsert) {
                stmt.executeUpdate(insert);
            }
            System.out.println("✅ EXITOSO: " + proveedorInsert.length + " proveedores insertados");
            System.out.println();
            
            // ═══════════════════════════════════════════════════════════════
            // RESUMEN FINAL
            // ═══════════════════════════════════════════════════════════════
            System.out.println("════════════════════════════════════════════════════════");
            System.out.println("    ¡BASE DE DATOS CREADA EXITOSAMENTE!                 ");
            System.out.println("════════════════════════════════════════════════════════");
            System.out.println();
            System.out.println("📊 RESUMEN:");
            System.out.println("   ✅ Base de datos: fabrica_muebles");
            System.out.println("   ✅ Tabla 'clientes' creada con 5 registros");
            System.out.println("   ✅ Tabla 'produccion' creada con 5 registros");
            System.out.println("   ✅ Tabla 'proveedor' creada con 5 registros");
            System.out.println();
            System.out.println("🎉 Tu sistema está listo para usar");
            System.out.println();
            
        } catch (ClassNotFoundException e) {
            System.err.println();
            System.err.println("❌ ERROR: No se encontró el driver JDBC de MySQL");
            System.err.println("   Verifica que mysql-connector-j-9.4.0.jar esté en la carpeta lib/");
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println();
            System.err.println("❌ ERROR DE SQL: " + e.getMessage());
            System.err.println("   Verifica que MySQL esté ejecutándose");
            System.err.println("   Verifica usuario y contraseña");
            e.printStackTrace();
        } finally {
            // Cerrar recursos
            try {
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
                System.out.println("🔒 Conexión cerrada");
                System.out.println();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}