package com.fabrica.muebles;

import com.fabrica.muebles.modelo.Proveedor;
import com.fabrica.muebles.modelo.Administracion;
import java.util.List;

/**
 * Clase Main para probar el patrón Facade (Administracion)
 * Demuestra cómo la capa de lógica de negocio centraliza el acceso a los DAOs
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class AdministracionMain {
    
    public static void main(String[] args) {
        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("  PRUEBA DEL MÓDULO ADMINISTRACIÓN (Facade Pattern)   ");
        System.out.println("═══════════════════════════════════════════════════════\n");
        
        Administracion admin = new Administracion();
        
        // ═══════════════════════════════════════════════════════════════
        // 1) AGREGAR UN PROVEEDOR
        // ═══════════════════════════════════════════════════════════════
        System.out.println("1. AGREGANDO PROVEEDOR...");
        Proveedor proveedor = new Proveedor();
        proveedor.setNombre("Proveedor Ejemplo");
        proveedor.setContacto("Juan Pérez");
        proveedor.setTelefono("123456789");
        proveedor.setDireccion("Calle Ficticia 123");
        proveedor.setCorreo("proveedor@example.com");
        
        if (admin.agregarProveedor(proveedor)) {
            System.out.println("✅ Proveedor agregado correctamente.\n");
        } else {
            System.out.println("❌ Error al agregar proveedor.\n");
        }
        
        // ═══════════════════════════════════════════════════════════════
        // 2) LISTAR TODOS LOS PROVEEDORES
        // ═══════════════════════════════════════════════════════════════
        System.out.println("2. LISTANDO PROVEEDORES...");
        List<Proveedor> lista = admin.listarProveedores();
        
        if (lista.isEmpty()) {
            System.out.println("⚠️  No hay proveedores registrados.\n");
        } else {
            System.out.println("📋 LISTA DE PROVEEDORES:");
            lista.forEach(p -> 
                System.out.println("   ID: " + p.getId() + " - Nombre: " + p.getNombre() + 
                                 " - Contacto: " + p.getContacto())
            );
            System.out.println("   Total: " + lista.size() + " proveedores\n");
        }
        
        // ═══════════════════════════════════════════════════════════════
        // 3) BUSCAR UN PROVEEDOR POR ID
        // ═══════════════════════════════════════════════════════════════
        if (!lista.isEmpty()) {
            System.out.println("3. BUSCANDO PROVEEDOR POR ID...");
            int idBuscar = lista.get(0).getId();
            Proveedor encontrado = admin.buscarProveedor(idBuscar);
            
            if (encontrado != null) {
                System.out.println("✅ Proveedor encontrado:");
                System.out.println("   ID: " + encontrado.getId());
                System.out.println("   Nombre: " + encontrado.getNombre());
                System.out.println("   Contacto: " + encontrado.getContacto());
                System.out.println("   Teléfono: " + encontrado.getTelefono());
                System.out.println("   Correo: " + encontrado.getCorreo() + "\n");
            } else {
                System.out.println("❌ No se encontró el proveedor.\n");
            }
        }
        
        // ═══════════════════════════════════════════════════════════════
        // 4) ACTUALIZAR UN PROVEEDOR
        // ═══════════════════════════════════════════════════════════════
        if (!lista.isEmpty()) {
            System.out.println("4. ACTUALIZANDO PROVEEDOR...");
            Proveedor proveedorActualizar = lista.get(0); // Tomamos el primero
            proveedorActualizar.setNombre("Proveedor Actualizado");
            proveedorActualizar.setTelefono("987654321");
            
            if (admin.actualizarProveedor(proveedorActualizar)) {
                System.out.println("✅ Proveedor actualizado correctamente.\n");
            } else {
                System.out.println("❌ Error al actualizar proveedor.\n");
            }
        }
        
        // ═══════════════════════════════════════════════════════════════
        // 5) ELIMINAR UN PROVEEDOR (solo si hay suficientes)
        // ═══════════════════════════════════════════════════════════════
        System.out.println("5. PRUEBA DE ELIMINACIÓN...");
        if (lista.size() > 3) {
            int idEliminar = lista.get(0).getId();
            System.out.println("   Intentando eliminar ID: " + idEliminar);
            
            if (admin.eliminarProveedor(idEliminar)) {
                System.out.println("✅ Proveedor eliminado correctamente.\n");
            } else {
                System.out.println("❌ Error al eliminar proveedor.\n");
            }
        } else {
            System.out.println("⚠️  Hay pocos proveedores, no se eliminará ninguno.");
            System.out.println("   (Se requieren más de 3 para probar eliminación)\n");
        }
        
        // ═══════════════════════════════════════════════════════════════
        // RESUMEN
        // ═══════════════════════════════════════════════════════════════
        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("  ✅ PRUEBA COMPLETADA                                 ");
        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("\n💡 Nota: El patrón Facade (Administracion.java) centraliza");
        System.out.println("   el acceso a múltiples DAOs simplificando el código.\n");
    }
}