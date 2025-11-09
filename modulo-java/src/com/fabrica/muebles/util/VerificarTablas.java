package com.fabrica.muebles.util;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Clase de utilidad para verificar la existencia de tablas en la base de datos
 * y crear un diagnóstico completo del estado de la base de datos
 * 
 * Tablas verificadas: clientes, produccion, proveedor
 * 
 * @author William Alonso Samaca Lopez
 * @version 2.0
 */
public class VerificarTablas {
    
    public static void main(String[] args) {
        System.out.println("╔════════════════════════════════════════════════════════╗");
        System.out.println("║   DIAGNÓSTICO DE BASE DE DATOS - FÁBRICA DE MUEBLES   ║");
        System.out.println("╚════════════════════════════════════════════════════════╝\n");
        
        // Paso 1: Probar conexión
        if (!probarConexion()) {
            System.err.println("\n❌ No se pudo conectar a la base de datos.");
            System.err.println("   Verifica que MySQL esté ejecutándose");
            System.err.println("   y que los datos en database.properties sean correctos.\n");
            return;
        }
        
        // Paso 2: Verificar si existe la base de datos
        verificarBaseDatos();
        
        // Paso 3: Verificar tablas del sistema
        System.out.println("\n📋 VERIFICANDO TABLAS DEL SISTEMA...\n");
        boolean clientesExiste = verificarTabla("clientes");
        boolean produccionExiste = verificarTabla("produccion");
        boolean proveedorExiste = verificarTabla("proveedor");
        
        // Paso 4: Mostrar resumen
        System.out.println("\n" + repetirCaracter('═', 60));
        System.out.println("RESUMEN DEL DIAGNÓSTICO");
        System.out.println(repetirCaracter('═', 60));
        
        System.out.println("\n🔹 Base de datos: fabrica_muebles");
        System.out.println("🔹 Tabla 'clientes': " + (clientesExiste ? "✅ EXISTE" : "❌ NO EXISTE"));
        System.out.println("🔹 Tabla 'produccion': " + (produccionExiste ? "✅ EXISTE" : "❌ NO EXISTE"));
        System.out.println("🔹 Tabla 'proveedor': " + (proveedorExiste ? "✅ EXISTE" : "❌ NO EXISTE"));
        
        // Paso 5: Mostrar estructura si existen
        if (clientesExiste) {
            mostrarEstructuraTabla("clientes");
        }
        
        if (produccionExiste) {
            mostrarEstructuraTabla("produccion");
        }
        
        if (proveedorExiste) {
            mostrarEstructuraTabla("proveedor");
        }
        
        // Paso 6: Recomendaciones
        System.out.println("\n" + repetirCaracter('═', 60));
        System.out.println("RECOMENDACIONES");
        System.out.println(repetirCaracter('═', 60) + "\n");
        
        if (!clientesExiste || !produccionExiste || !proveedorExiste) {
            System.out.println("⚠️  ACCIÓN REQUERIDA:");
            System.out.println("   Necesitas crear las tablas faltantes.");
            System.out.println("   Ejecuta: CrearTablasAutomatico.java\n");
        } else {
            System.out.println("✅ Tu base de datos está completa y lista para usar.");
            System.out.println("   Puedes continuar con el desarrollo.\n");
        }
    }
    
    /**
     * Método auxiliar para repetir un carácter N veces
     * Reemplaza el método repeat() de Java 11+
     */
    private static String repetirCaracter(char c, int veces) {
        StringBuilder sb = new StringBuilder(veces);
        for (int i = 0; i < veces; i++) {
            sb.append(c);
        }
        return sb.toString();
    }
    
    /**
     * Prueba la conexión a la base de datos
     * @return true si la conexión es exitosa
     */
    private static boolean probarConexion() {
        System.out.println("🔌 Probando conexión a MySQL...\n");
        
        Connection conn = null;
        try {
            conn = ConexionBD.getConexion();
            
            if (conn != null && !conn.isClosed()) {
                System.out.println("✅ Conexión exitosa");
                System.out.println("   Host: localhost:3306");
                System.out.println("   Usuario: root");
                System.out.println("   Base de datos: fabrica_muebles");
                return true;
            }
        } catch (SQLException e) {
            System.err.println("❌ Error al verificar conexión: " + e.getMessage());
        } finally {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    // Ignorar error al cerrar
                }
            }
        }
        return false;
    }
    
    /**
     * Verifica si existe la base de datos
     */
    private static void verificarBaseDatos() {
        System.out.println("\n🗄️  Verificando base de datos...");
        
        Connection conn = null;
        try {
            conn = ConexionBD.getConexion();
            if (conn != null) {
                DatabaseMetaData metaData = conn.getMetaData();
                System.out.println("   Base de datos: " + conn.getCatalog());
                System.out.println("   Motor: " + metaData.getDatabaseProductName());
                System.out.println("   Versión: " + metaData.getDatabaseProductVersion());
            }
        } catch (SQLException e) {
            System.err.println("❌ Error al verificar base de datos: " + e.getMessage());
        } finally {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    // Ignorar error al cerrar
                }
            }
        }
    }
    
    /**
     * Verifica si existe una tabla específica
     * @param nombreTabla Nombre de la tabla a verificar
     * @return true si la tabla existe
     */
    private static boolean verificarTabla(String nombreTabla) {
        Connection conn = null;
        ResultSet rs = null;
        
        try {
            conn = ConexionBD.getConexion();
            if (conn != null) {
                DatabaseMetaData metaData = conn.getMetaData();
                rs = metaData.getTables(null, null, nombreTabla, new String[]{"TABLE"});
                
                if (rs.next()) {
                    System.out.println("✅ Tabla '" + nombreTabla + "' encontrada");
                    contarRegistros(nombreTabla);
                    return true;
                } else {
                    System.out.println("❌ Tabla '" + nombreTabla + "' NO existe");
                    return false;
                }
            }
        } catch (SQLException e) {
            System.err.println("❌ Error al verificar tabla '" + nombreTabla + "': " + e.getMessage());
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
        }
        return false;
    }
    
    /**
     * Cuenta los registros en una tabla
     * @param nombreTabla Nombre de la tabla
     */
    private static void contarRegistros(String nombreTabla) {
        String sql = "SELECT COUNT(*) as total FROM " + nombreTabla;
        
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        
        try {
            conn = ConexionBD.getConexion();
            stmt = conn.createStatement();
            rs = stmt.executeQuery(sql);
            
            if (rs.next()) {
                int total = rs.getInt("total");
                System.out.println("   📊 Registros: " + total);
            }
            
        } catch (SQLException e) {
            System.err.println("   ⚠️  No se pudo contar registros: " + e.getMessage());
        } finally {
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
        }
    }
    
    /**
     * Muestra la estructura de una tabla
     * @param nombreTabla Nombre de la tabla
     */
    private static void mostrarEstructuraTabla(String nombreTabla) {
        System.out.println("\n" + repetirCaracter('─', 60));
        System.out.println("📋 ESTRUCTURA DE LA TABLA: " + nombreTabla.toUpperCase());
        System.out.println(repetirCaracter('─', 60));
        
        Connection conn = null;
        ResultSet columnas = null;
        ResultSet pk = null;
        
        try {
            conn = ConexionBD.getConexion();
            if (conn != null) {
                DatabaseMetaData metaData = conn.getMetaData();
                columnas = metaData.getColumns(null, null, nombreTabla, null);
                
                System.out.printf("%-20s %-15s %-10s %-10s%n", "COLUMNA", "TIPO", "NULO", "CLAVE");
                System.out.println(repetirCaracter('─', 60));
                
                while (columnas.next()) {
                    String nombreColumna = columnas.getString("COLUMN_NAME");
                    String tipoColumna = columnas.getString("TYPE_NAME");
                    String nulo = columnas.getString("IS_NULLABLE").equals("YES") ? "Sí" : "No";
                    
                    // Verificar si es clave primaria
                    pk = metaData.getPrimaryKeys(null, null, nombreTabla);
                    String esClave = "";
                    while (pk.next()) {
                        if (pk.getString("COLUMN_NAME").equals(nombreColumna)) {
                            esClave = "PK";
                            break;
                        }
                    }
                    
                    System.out.printf("%-20s %-15s %-10s %-10s%n", 
                                    nombreColumna, tipoColumna, nulo, esClave);
                    
                    if (pk != null) {
                        try {
                            pk.close();
                        } catch (SQLException e) {
                            // Ignorar
                        }
                    }
                }
            }
        } catch (SQLException e) {
            System.err.println("❌ Error al mostrar estructura: " + e.getMessage());
        } finally {
            if (columnas != null) {
                try {
                    columnas.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (pk != null) {
                try {
                    pk.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    // Ignorar
                }
            }
        }
    }
}