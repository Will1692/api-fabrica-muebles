package com.fabrica.muebles.modelo;

import java.sql.Date;

/**
 * Clase modelo que representa un registro de Producción
 * Corresponde a la tabla: produccion
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class Produccion {
    
    // Atributos (coinciden con los campos de la tabla produccion)
    private int id;
    private String nombreProducto;
    private int cantidad;
    private Date fechaInicio;
    private Date fechaFin;
    private String estado;
    
    // Constructor vacío
    public Produccion() {
    }
    
    // Constructor para insertar (sin ID)
    public Produccion(String nombreProducto, int cantidad, Date fechaInicio, String estado) {
        this.nombreProducto = nombreProducto;
        this.cantidad = cantidad;
        this.fechaInicio = fechaInicio;
        this.estado = estado;
    }
    
    // Constructor completo (para consultas)
    public Produccion(int id, String nombreProducto, int cantidad, Date fechaInicio, 
                      Date fechaFin, String estado) {
        this.id = id;
        this.nombreProducto = nombreProducto;
        this.cantidad = cantidad;
        this.fechaInicio = fechaInicio;
        this.fechaFin = fechaFin;
        this.estado = estado;
    }
    
    // Getters y Setters
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getNombreProducto() {
        return nombreProducto;
    }
    
    public void setNombreProducto(String nombreProducto) {
        this.nombreProducto = nombreProducto;
    }
    
    public int getCantidad() {
        return cantidad;
    }
    
    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }
    
    public Date getFechaInicio() {
        return fechaInicio;
    }
    
    public void setFechaInicio(Date fechaInicio) {
        this.fechaInicio = fechaInicio;
    }
    
    public Date getFechaFin() {
        return fechaFin;
    }
    
    public void setFechaFin(Date fechaFin) {
        this.fechaFin = fechaFin;
    }
    
    public String getEstado() {
        return estado;
    }
    
    public void setEstado(String estado) {
        this.estado = estado;
    }
    
    @Override
    public String toString() {
        return "Produccion{" +
                "ID=" + id +
                ", producto='" + nombreProducto + '\'' +
                ", cantidad=" + cantidad +
                ", estado='" + estado + '\'' +
                '}';
    }
}