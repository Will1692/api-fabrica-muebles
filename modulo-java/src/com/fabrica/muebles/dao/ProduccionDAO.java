package com.fabrica.muebles.dao;

import com.fabrica.muebles.modelo.Produccion;
import com.fabrica.muebles.util.ConexionBD;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * DAO básico para operaciones CRUD de Producción
 * Autor: William Alonso Samaca Lopez
 */
public class ProduccionDAO {

    // Insertar
    public boolean insertarProduccion(Produccion produccion) {
        String sql = "INSERT INTO produccion (nombre_producto, cantidad, fecha_inicio, fecha_fin, estado) VALUES (?, ?, ?, ?, ?)";
        try (Connection con = ConexionBD.getConexion();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, produccion.getNombreProducto());
            ps.setInt(2, produccion.getCantidad());
            ps.setDate(3, produccion.getFechaInicio());
            ps.setDate(4, produccion.getFechaFin());
            ps.setString(5, produccion.getEstado());
            return ps.executeUpdate() > 0;

        } catch (SQLException e) {
            System.err.println("Error al insertar producción: " + e.getMessage());
            return false;
        }
    }

    // Consultar todos
    public List<Produccion> consultarTodos() {
        List<Produccion> lista = new ArrayList<>();
        String sql = "SELECT * FROM produccion ORDER BY id DESC";

        try (Connection con = ConexionBD.getConexion();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(sql)) {

            while (rs.next()) {
                Produccion p = new Produccion(
                    rs.getInt("id"),
                    rs.getString("nombre_producto"),
                    rs.getInt("cantidad"),
                    rs.getDate("fecha_inicio"),
                    rs.getDate("fecha_fin"),
                    rs.getString("estado")
                );
                lista.add(p);
            }

        } catch (SQLException e) {
            System.err.println("Error al consultar producciones: " + e.getMessage());
        }
        return lista;
    }

    // Consultar por ID
    public Produccion consultarPorId(int id) {
        String sql = "SELECT * FROM produccion WHERE id = ?";
        try (Connection con = ConexionBD.getConexion();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Produccion(
                        rs.getInt("id"),
                        rs.getString("nombre_producto"),
                        rs.getInt("cantidad"),
                        rs.getDate("fecha_inicio"),
                        rs.getDate("fecha_fin"),
                        rs.getString("estado")
                    );
                }
            }
        } catch (SQLException e) {
            System.err.println("Error al consultar producción: " + e.getMessage());
        }
        return null;
    }

    // Actualizar
    public boolean actualizarProduccion(Produccion produccion) {
        String sql = "UPDATE produccion SET nombre_producto=?, cantidad=?, fecha_inicio=?, fecha_fin=?, estado=? WHERE id=?";
        try (Connection con = ConexionBD.getConexion();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, produccion.getNombreProducto());
            ps.setInt(2, produccion.getCantidad());
            ps.setDate(3, produccion.getFechaInicio());
            ps.setDate(4, produccion.getFechaFin());
            ps.setString(5, produccion.getEstado());
            ps.setInt(6, produccion.getId());
            return ps.executeUpdate() > 0;

        } catch (SQLException e) {
            System.err.println("Error al actualizar producción: " + e.getMessage());
            return false;
        }
    }

    // Finalizar producción
    public boolean finalizarProduccion(int id) {
        String sql = "UPDATE produccion SET estado='Finalizado', fecha_fin=CURDATE() WHERE id=?";
        try (Connection con = ConexionBD.getConexion();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setInt(1, id);
            return ps.executeUpdate() > 0;

        } catch (SQLException e) {
            System.err.println("Error al finalizar producción: " + e.getMessage());
            return false;
        }
    }

    // Eliminar
    public boolean eliminarProduccion(int id) {
        String sql = "DELETE FROM produccion WHERE id=?";
        try (Connection con = ConexionBD.getConexion();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setInt(1, id);
            return ps.executeUpdate() > 0;

        } catch (SQLException e) {
            System.err.println("Error al eliminar producción: " + e.getMessage());
            return false;
        }
    }
}