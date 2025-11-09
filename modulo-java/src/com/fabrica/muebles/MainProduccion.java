package com.fabrica.muebles;

import com.fabrica.muebles.dao.ProduccionDAO;
import com.fabrica.muebles.modelo.Produccion;
import com.fabrica.muebles.util.ConexionBD;

import java.sql.Date;
import java.util.List;

/**
 * Clase Main para probar las operaciones CRUD de ProduccionDAO
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class MainProduccion {

    public static void main(String[] args) {

        // Probar conexión
        if (!ConexionBD.probarConexion()) {
            System.err.println("No se pudo conectar a la base de datos");
            return;
        }

        ProduccionDAO produccionDAO = new ProduccionDAO();

        // Insertar nuevo registro
        Date fechaInicio = new Date(System.currentTimeMillis());
        Produccion nuevaProduccion = new Produccion(
            "Mesa de Centro Moderna", 5, fechaInicio, "En proceso"
        );

        boolean insertado = produccionDAO.insertarProduccion(nuevaProduccion);
        System.out.println(insertado ? "Producción insertada correctamente." : "Error al insertar producción.");

        // Consultar todos los registros
        List<Produccion> listaProduccion = produccionDAO.consultarTodos();
        for (Produccion p : listaProduccion) {
            System.out.println(p.getId() + " - " + p.getNombreProducto() + " - " + p.getCantidad() + " - " + p.getEstado());
        }

        // Consultar por ID (si hay registros)
        if (!listaProduccion.isEmpty()) {
            int idBuscar = listaProduccion.get(0).getId();
            Produccion produccionEncontrada = produccionDAO.consultarPorId(idBuscar);
            if (produccionEncontrada != null) {
                System.out.println("Producción encontrada: " + produccionEncontrada.getNombreProducto());
            }
        }

        // Actualizar una producción (si hay registros)
        if (!listaProduccion.isEmpty()) {
            Produccion produccionActualizar = listaProduccion.get(0);
            produccionActualizar.setCantidad(8);
            produccionActualizar.setEstado("Finalizado");
            boolean actualizado = produccionDAO.actualizarProduccion(produccionActualizar);
            System.out.println(actualizado ? "Producción actualizada." : "Error al actualizar.");
        }

        // Eliminar (opcional)
        /*
        if (!listaProduccion.isEmpty()) {
            int idEliminar = listaProduccion.get(0).getId();
            boolean eliminado = produccionDAO.eliminarProduccion(idEliminar);
            System.out.println(eliminado ? "Producción eliminada." : "Error al eliminar.");
        }
        */
    }
}