package com.fabrica.muebles;

import com.fabrica.muebles.dao.ProveedorDAO;
import com.fabrica.muebles.modelo.Proveedor;
import java.util.List;

public class MainProveedor {

    // Cambia a true SOLO cuando quieras insertar 1 vez de prueba
    private static final boolean DO_INSERT = false;

    public static void main(String[] args) {
        System.out.println("PRUEBA DEL MÓDULO PROVEEDORES");

        ProveedorDAO dao = new ProveedorDAO();

        // 1) INSERT controlado por flag (evita duplicados en cada ejecución)
        if (DO_INSERT) {
            Proveedor nuevo = new Proveedor();
            nuevo.setNombre("Maderas del Norte");
            nuevo.setContacto("Carlos Pérez");
            nuevo.setTelefono("3124567890");
            nuevo.setDireccion("Calle 10 #23-45");
            nuevo.setCorreo("contacto@maderasnorte.com");

            if (dao.agregar(nuevo)) {
                System.out.println("Proveedor insertado correctamente.");
            } else {
                System.out.println("Error al insertar proveedor.");
            }
        }

        // 2) LISTAR
        List<Proveedor> lista = dao.listar();
        System.out.println("\nLISTA DE PROVEEDORES:");
        for (Proveedor p : lista) {
            System.out.println(p.getId() + " - " + p.getNombre() + " - " + p.getContacto());
        }

        // 3) BUSCAR (si hay registros, busca el último de la lista)
        Proveedor encontrado = null;
        if (!lista.isEmpty()) {
            int idBuscar = lista.get(lista.size() - 1).getId(); // último
            encontrado = dao.buscar(idBuscar);
            if (encontrado != null) {
                System.out.println("\nProveedor encontrado: " + encontrado.getNombre());
            } else {
                System.out.println("\nNo se encontró el proveedor con ID " + idBuscar);
            }
        } else {
            System.out.println("\nNo hay proveedores para buscar.");
        }

        // 4) ACTUALIZAR (si se encontró)
        if (encontrado != null) {
            encontrado.setTelefono("3205559999");
            if (dao.actualizar(encontrado)) {
                System.out.println("Proveedor actualizado correctamente.");
            } else {
                System.out.println("Error al actualizar proveedor.");
            }
        }

        // 5) ELIMINAR (si hay registros, elimina el más reciente para asegurar que exista)
        if (!lista.isEmpty()) {
            int idEliminar = lista.get(0).getId(); // asumiendo que listar() trae en orden natural; si no, ajusta
            System.out.println("\nIntentando eliminar ID: " + idEliminar);
            if (dao.eliminar(idEliminar)) {
                System.out.println("Proveedor eliminado correctamente.");
            } else {
                System.out.println("No se pudo eliminar (puede que no exista ese ID o hay referencias).");
            }
        } else {
            System.out.println("\nNo hay proveedores para eliminar.");
        }

        System.out.println("\nFIN DE PRUEBA");
    }
}