package com.fabrica.muebles;

import com.fabrica.muebles.dao.ClienteDAO;
import com.fabrica.muebles.modelo.Cliente;
import com.fabrica.muebles.util.ConexionBD;

import java.util.List;

public class Main {
    
    public static void main(String[] args) {
        
        // 1. PROBAR CONEXIÓN
        System.out.println("1. PROBANDO CONEXION A LA BASE DE DATOS...");
        boolean conexionOk = ConexionBD.probarConexion();
        
        if (!conexionOk) {
            System.err.println("ERROR: No se pudo conectar a la base de datos");
            System.err.println("Verifica tu archivo config/database.properties");
            return;
        }
        
        // Crear instancia del DAO
        ClienteDAO clienteDAO = new ClienteDAO();
        
        // 2. INSERTAR UN NUEVO CLIENTE
        System.out.println("2. INSERTANDO UN NUEVO CLIENTE...");
        Cliente nuevoCliente = new Cliente(
            "Carlos Rodriguez",
            "3158889999",
            "Calle 25 #10-15",
            "carlos@email.com"
        );
        
        boolean insertado = clienteDAO.insertarCliente(nuevoCliente);
        
        if (insertado) {
            System.out.println("   Cliente insertado exitosamente\n");
        } else {
            System.out.println("   Error al insertar cliente\n");
        }
        
        // 3. CONSULTAR TODOS LOS CLIENTES
        System.out.println("3. CONSULTANDO TODOS LOS CLIENTES...\n");
        List<Cliente> listaClientes = clienteDAO.consultarTodos();
        
        if (listaClientes.isEmpty()) {
            System.out.println("   No hay clientes registrados\n");
        } else {
            System.out.println("   LISTA DE CLIENTES:");
            System.out.printf("   %-5s %-25s %-15s %-30s %-10s%n", 
                "ID", "NOMBRE", "TELEFONO", "EMAIL", "ESTADO");
            for (Cliente c : listaClientes) {
                System.out.printf("   %-5d %-25s %-15s %-30s %-10s%n",
                    c.getIdCliente(),
                    c.getNombre(),
                    c.getTelefono(),
                    c.getEmail(),
                    c.getEstadoTexto()
                );
            }
            System.out.println("   Total: " + listaClientes.size() + " clientes\n");
        }
        
        // 4. CONSULTAR UN CLIENTE POR ID
        System.out.println("4. CONSULTANDO CLIENTE POR ID...");
        
        if (!listaClientes.isEmpty()) {
            int idBuscar = listaClientes.get(0).getIdCliente();
            Cliente clienteEncontrado = clienteDAO.consultarPorId(idBuscar);
            
            if (clienteEncontrado != null) {
                System.out.println("\n   DATOS DEL CLIENTE:");
                System.out.println("   ID: " + clienteEncontrado.getIdCliente());
                System.out.println("   Nombre: " + clienteEncontrado.getNombre());
                System.out.println("   Telefono: " + clienteEncontrado.getTelefono());
                System.out.println("   Direccion: " + clienteEncontrado.getDireccion());
                System.out.println("   Email: " + clienteEncontrado.getEmail());
                System.out.println("   Estado: " + clienteEncontrado.getEstado());
                System.out.println();
            }
        } else {
            System.out.println("   No hay clientes para buscar\n");
        }
        
        // 5. ACTUALIZAR UN CLIENTE
        System.out.println("5. ACTUALIZANDO UN CLIENTE...");
        
        if (!listaClientes.isEmpty()) {
            Cliente clienteActualizar = listaClientes.get(0);
            clienteActualizar.setTelefono("3009998888");
            clienteActualizar.setEmail("nuevo_email@email.com");
            
            boolean actualizado = clienteDAO.actualizarCliente(clienteActualizar);
            
            if (actualizado) {
                System.out.println("   Datos actualizados correctamente\n");
            } else {
                System.out.println("   Error al actualizar\n");
            }
        } else {
            System.out.println("   No hay clientes para actualizar\n");
        }
        
        // 6. ELIMINAR UN CLIENTE (OPCIONAL - COMENTADO POR SEGURIDAD)
        System.out.println("6. PRUEBA DE ELIMINACION (Comentada por seguridad)");
        System.out.println("   Para probar eliminar, descomenta el codigo en Main.java\n");
        
        // DESCOMENTA ESTO SOLO SI QUIERES PROBAR ELIMINAR
        /*
        if (!listaClientes.isEmpty() && listaClientes.size() > 2) {
            int idEliminar = listaClientes.get(listaClientes.size() - 1).getIdCliente();
            boolean eliminado = clienteDAO.eliminarCliente(idEliminar);
            if (eliminado) {
                System.out.println("   Cliente eliminado correctamente\n");
            } else {
                System.out.println("   Error al eliminar\n");
            }
        }
        */
        
        System.out.println("    PRUEBAS COMPLETADAS");
    }
}