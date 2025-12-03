package com.fabrica.muebles;

import com.fabrica.muebles.dao.ClienteDAO;
import com.fabrica.muebles.modelo.Cliente;
import java.util.List;

public class MainCliente {

    // Cambia a true SOLO cuando quieras insertar 1 vez de prueba
    private static final boolean DO_INSERT = false;

    public static void main(String[] args) {
        System.out.println("PRUEBA DEL MÓDULO CLIENTES");

        ClienteDAO dao = new ClienteDAO();

        // 1) INSERT (controlado por flag para no duplicar registros en cada ejecución)
        if (DO_INSERT) {
            Cliente nuevo = new Cliente();
            nuevo.setNombre("Juan Pérez");
            nuevo.setTelefono("3125551234");
            nuevo.setDireccion("Avenida Siempre Viva 742");
            nuevo.setEmail("juanperez@email.com");

            if (dao.insertarCliente(nuevo)) {
                System.out.println("Cliente insertado correctamente.");
            } else {
                System.out.println("Error al insertar cliente.");
            }
        }

        // 2) LISTAR
        List<Cliente> lista = dao.consultarTodos();
        System.out.println("\nLISTA DE CLIENTES:");
        for (Cliente c : lista) {
            System.out.println(c.getIdCliente() + " - " + c.getNombre() + " - " + c.getTelefono());
        }

        // 3) BUSCAR (si hay registros, busca el último de la lista)
        Cliente encontrado = null;
        if (!lista.isEmpty()) {
            int idBuscar = lista.get(lista.size() - 1).getIdCliente();
            encontrado = dao.consultarPorId(idBuscar);
            if (encontrado != null) {
                System.out.println("\nCliente encontrado: " + encontrado.getNombre());
            } else {
                System.out.println("\nNo se encontró el cliente con ID " + idBuscar);
            }
        } else {
            System.out.println("\nNo hay clientes para buscar.");
        }

        // 4) ACTUALIZAR (si se encontró)
        if (encontrado != null) {
            encontrado.setTelefono("3009998888");
            if (dao.actualizarCliente(encontrado)) {
                System.out.println("Cliente actualizado correctamente.");
            } else {
                System.out.println("Error al actualizar cliente.");
            }
        }

        // 5) ELIMINAR (si hay registros, elimina el más reciente para asegurar que exista)
        if (!lista.isEmpty()) {
            int idEliminar = lista.get(0).getIdCliente(); // asumiendo ORDER BY id DESC en consultarTodos()
            System.out.println("\nIntentando eliminar ID: " + idEliminar);
            if (dao.eliminarCliente(idEliminar)) {
                System.out.println("Cliente eliminado correctamente.");
            } else {
                System.out.println("No se pudo eliminar (puede que no exista ese ID o hay referencias).");
            }
        } else {
            System.out.println("\nNo hay clientes para eliminar.");
        }

        System.out.println("\nFIN DE PRUEBA");
    }
}