package com.fabrica.muebles.modelo;

import com.fabrica.muebles.dao.ClienteDAO;
import com.fabrica.muebles.dao.ProveedorDAO;
import java.util.List;

public class Administracion {

    private final ClienteDAO clienteDAO = new ClienteDAO();
    private final ProveedorDAO proveedorDAO = new ProveedorDAO();

    // ============ CLIENTES ============
    public boolean agregarCliente(Cliente c) { 
        return clienteDAO.insertarCliente(c); 
    }

    public List<Cliente> listarClientes() { 
        return clienteDAO.consultarTodos(); 
    }

    public Cliente buscarCliente(int id) { 
        return clienteDAO.consultarPorId(id); 
    }

    public boolean actualizarCliente(Cliente c) { 
        return clienteDAO.actualizarCliente(c); 
    }

    public boolean eliminarCliente(int id) { 
        return clienteDAO.eliminarCliente(id); 
    }

    // ============ PROVEEDORES ============
    public boolean agregarProveedor(Proveedor p) { 
        return proveedorDAO.agregar(p); 
    }

    public List<Proveedor> listarProveedores() { 
        return proveedorDAO.listar(); 
    }

    public Proveedor buscarProveedor(int id) { 
        return proveedorDAO.buscar(id); 
    }

    public boolean actualizarProveedor(Proveedor p) { 
        return proveedorDAO.actualizar(p); 
    }

    public boolean eliminarProveedor(int id) { 
        return proveedorDAO.eliminar(id); 
    }
}