package com.fabrica.muebles.util;

import java.io.InputStream;
import java.sql.*;
import java.util.Properties;

/**
 * Utilidad de conexión JDBC (MySQL).
 * - Carga propiedades desde config/database.properties (en el classpath).
 * - Registra el driver y crea SIEMPRE una NUEVA conexión por llamada.
 * - Incluye método de prueba de conexión.
 *
 * Claves esperadas en database.properties:
 *   db.driver=com.mysql.cj.jdbc.Driver
 *   db.url=jdbc:mysql://localhost:3306/fabrica_muebles?useSSL=false&serverTimezone=UTC&characterEncoding=utf8
 *   db.usuario=root
 *   db.clave=Mariana28
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public final class ConexionBD {

    private static final String PROPERTIES_PATH = "config/database.properties";

    private static String url;
    private static String usuario;
    private static String clave;
    private static String driver;
    private static volatile boolean inicializado = false;

    private ConexionBD() {}

    /** Carga propiedades y registra el driver (se ejecuta una sola vez, thread-safe). */
    private static synchronized void inicializar() {
        if (inicializado) {
            return;
        }

        InputStream in = null;
        try {
            // Usamos el classloader para cargar el archivo desde el classpath
            in = ConexionBD.class.getClassLoader().getResourceAsStream(PROPERTIES_PATH);
            if (in == null) {
                System.err.println("❓ No se encontró el archivo: " + PROPERTIES_PATH);
                System.err.println("   Asegúrate de que existe en: src/config/database.properties");
                throw new IllegalStateException("Archivo de configuración no encontrado");
            }

            Properties p = new Properties();
            p.load(in);

            driver  = p.getProperty("db.driver");
            url     = p.getProperty("db.url");
            usuario = p.getProperty("db.usuario");
            clave   = p.getProperty("db.clave");

            if (driver == null || url == null || usuario == null || clave == null) {
                throw new IllegalStateException("Propiedades JDBC incompletas en " + PROPERTIES_PATH);
            }

            Class.forName(driver); // registra el driver
            System.out.println("✅ Archivo de configuración cargado correctamente");
            System.out.println("✅ Driver JDBC de MySQL registrado correctamente");
            inicializado = true;
        } catch (Exception e) {
            throw new RuntimeException("No se pudieron cargar las propiedades de conexión", e);
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (Exception e) {
                    // Ignorar error al cerrar
                }
            }
        }
    }

    /** Devuelve SIEMPRE una NUEVA conexión (no reutiliza conexiones cerradas). */
    public static Connection getConexion() {
        if (!inicializado) {
            inicializar();
        }
        try {
            return DriverManager.getConnection(url, usuario, clave);
        } catch (SQLException e) {
            throw new RuntimeException("No se pudo establecer la conexión", e);
        }
    }

    /** Prueba de conectividad (para tus mains de test). */
    public static boolean probarConexion() {
        if (!inicializado) {
            inicializar();
        }
        
        Connection cn = null;
        Statement st = null;
        ResultSet rs = null;
        
        try {
            cn = getConexion();
            System.out.println("✅ Conexión establecida correctamente a la base de datos");
            
            st = cn.createStatement();
            rs = st.executeQuery("SELECT DATABASE()");
            
            if (rs.next()) {
                System.out.println("✅ Base de datos: " + rs.getString(1));
            }
            System.out.println("✅ Conexión exitosa y activa");
            return true;
            
        } catch (Exception e) {
            System.err.println("❌ Error probando la conexión: " + e.getMessage());
            e.printStackTrace();
            return false;
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (st != null) {
                try {
                    st.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (cn != null) {
                try {
                    cn.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
        }
    }

    /** 
     * Cierra una conexión de forma segura.
     * Este método es útil cuando no usas try-with-resources.
     * 
     * @param conexion La conexión a cerrar
     */
    public static void cerrarConexion(Connection conexion) {
        if (conexion != null) {
            try {
                if (!conexion.isClosed()) {
                    conexion.close();
                    System.out.println("🔒 Conexión cerrada correctamente");
                }
            } catch (SQLException e) {
                System.err.println("⚠️ Error al cerrar conexión: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    /**
     * Alias de getConexion() para compatibilidad con diferentes convenciones
     */
    public static Connection getConnection() {
        return getConexion();
    }
}