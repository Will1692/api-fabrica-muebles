package com.fabrica.muebles.dao;

import com.fabrica.muebles.modelo.Cliente;
import com.fabrica.muebles.util.ConexionBD;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Clase DAO para operaciones CRUD de Clientes
 * Implementa: Insertar, Consultar, Actualizar y Eliminar
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class ClienteDAO {
    
    public boolean insertarCliente(Cliente cliente) {
        String sql = "INSERT INTO clientes (nombre, telefono, direccion, email, fecha_registro, estado) " +
                     "VALUES (?, ?, ?, ?, ?, ?)";
        
        Connection conexion = null;
        PreparedStatement ps = null;
        
        try {
            conexion = ConexionBD.getConexion();
            ps = conexion.prepareStatement(sql);
            
            ps.setString(1, cliente.getNombre());
            ps.setString(2, cliente.getTelefono());
            ps.setString(3, cliente.getDireccion());
            ps.setString(4, cliente.getEmail());
            ps.setDate(5, cliente.getFechaRegistro());
            ps.setInt(6, cliente.getEstado());
            
            int filasAfectadas = ps.executeUpdate();
            
            if (filasAfectadas > 0) {
                System.out.println("Cliente insertado correctamente");
                return true;
            }
            
        } catch (SQLException e) {
            System.err.println("Error al insertar cliente: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cerrarRecursos(conexion, ps, null);
        }
        
        return false;
    }
    
    public List<Cliente> consultarTodos() {
        List<Cliente> listaClientes = new ArrayList<Cliente>();
        String sql = "SELECT id_cliente, nombre, telefono, direccion, email, fecha_registro, estado " +
                     "FROM clientes ORDER BY id_cliente DESC";
        
        Connection conexion = null;
        Statement st = null;
        ResultSet rs = null;
        
        try {
            conexion = ConexionBD.getConexion();
            st = conexion.createStatement();
            rs = st.executeQuery(sql);
            
            while (rs.next()) {
                Cliente cliente = new Cliente();
                cliente.setIdCliente(rs.getInt("id_cliente"));
                cliente.setNombre(rs.getString("nombre"));
                cliente.setTelefono(rs.getString("telefono"));
                cliente.setDireccion(rs.getString("direccion"));
                cliente.setEmail(rs.getString("email"));
                cliente.setFechaRegistro(rs.getDate("fecha_registro"));
                cliente.setEstado(rs.getInt("estado"));
                
                listaClientes.add(cliente);
            }
            
            System.out.println("Se consultaron " + listaClientes.size() + " clientes");
            
        } catch (SQLException e) {
            System.err.println("Error al consultar clientes: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cerrarRecursos(conexion, st, rs);
        }
        
        return listaClientes;
    }
    
    public Cliente consultarPorId(int idCliente) {
        String sql = "SELECT id_cliente, nombre, telefono, direccion, email, fecha_registro, estado " +
                     "FROM clientes WHERE id_cliente = ?";
        
        Connection conexion = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        Cliente cliente = null;
        
        try {
            conexion = ConexionBD.getConexion();
            ps = conexion.prepareStatement(sql);
            ps.setInt(1, idCliente);
            
            rs = ps.executeQuery();
            
            if (rs.next()) {
                cliente = new Cliente();
                cliente.setIdCliente(rs.getInt("id_cliente"));
                cliente.setNombre(rs.getString("nombre"));
                cliente.setTelefono(rs.getString("telefono"));
                cliente.setDireccion(rs.getString("direccion"));
                cliente.setEmail(rs.getString("email"));
                cliente.setFechaRegistro(rs.getDate("fecha_registro"));
                cliente.setEstado(rs.getInt("estado"));
                
                System.out.println("Cliente encontrado: " + cliente.getNombre());
            } else {
                System.out.println("No se encontro cliente con ID: " + idCliente);
            }
            
        } catch (SQLException e) {
            System.err.println("Error al consultar cliente por ID: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cerrarRecursos(conexion, ps, rs);
        }
        
        return cliente;
    }
    
    public boolean actualizarCliente(Cliente cliente) {
        String sql = "UPDATE clientes SET nombre = ?, telefono = ?, direccion = ?, " +
                     "email = ?, estado = ? WHERE id_cliente = ?";
        
        Connection conexion = null;
        PreparedStatement ps = null;
        
        try {
            conexion = ConexionBD.getConexion();
            ps = conexion.prepareStatement(sql);
            
            ps.setString(1, cliente.getNombre());
            ps.setString(2, cliente.getTelefono());
            ps.setString(3, cliente.getDireccion());
            ps.setString(4, cliente.getEmail());
            ps.setInt(5, cliente.getEstado());
            ps.setInt(6, cliente.getIdCliente());
            
            int filasAfectadas = ps.executeUpdate();
            
            if (filasAfectadas > 0) {
                System.out.println("Cliente actualizado correctamente");
                return true;
            } else {
                System.out.println("No se encontro el cliente a actualizar");
            }
            
        } catch (SQLException e) {
            System.err.println("Error al actualizar cliente: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cerrarRecursos(conexion, ps, null);
        }
        
        return false;
    }
    
    public boolean eliminarCliente(int idCliente) {
        String sql = "DELETE FROM clientes WHERE id_cliente = ?";
        
        Connection conexion = null;
        PreparedStatement ps = null;
        
        try {
            conexion = ConexionBD.getConexion();
            ps = conexion.prepareStatement(sql);
            ps.setInt(1, idCliente);
            
            int filasAfectadas = ps.executeUpdate();
            
            if (filasAfectadas > 0) {
                System.out.println("Cliente eliminado correctamente");
                return true;
            } else {
                System.out.println("No se encontro el cliente a eliminar");
            }
            
        } catch (SQLException e) {
            System.err.println("Error al eliminar cliente: " + e.getMessage());
            e.printStackTrace();
        } finally {
            cerrarRecursos(conexion, ps, null);
        }
        
        return false;
    }
    
    private void cerrarRecursos(Connection conexion, Statement statement, ResultSet resultSet) {
        try {
            if (resultSet != null) resultSet.close();
            if (statement != null) statement.close();
            if (conexion != null) conexion.close();
        } catch (SQLException e) {
            System.err.println("Error al cerrar recursos: " + e.getMessage());
        }
    }
}