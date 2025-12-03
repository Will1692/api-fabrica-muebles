package com.fabrica.muebles.modelo;

import java.sql.Date;

/**
 * Clase modelo que representa un Cliente en el sistema
 * Corresponde a la tabla: clientes
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class Cliente {
    
    private int idCliente;
    private String nombre;
    private String telefono;
    private String direccion;
    private String email;
    private Date fechaRegistro;
    private int estado;  // 1 = Activo, 0 = Inactivo
    
    public Cliente() {
    }
    
    public Cliente(String nombre, String telefono, String direccion, String email) {
        this.nombre = nombre;
        this.telefono = telefono;
        this.direccion = direccion;
        this.email = email;
        this.fechaRegistro = new Date(System.currentTimeMillis());
        this.estado = 1;
    }
    
    public Cliente(int idCliente, String nombre, String telefono, String direccion, 
                   String email, Date fechaRegistro, int estado) {
        this.idCliente = idCliente;
        this.nombre = nombre;
        this.telefono = telefono;
        this.direccion = direccion;
        this.email = email;
        this.fechaRegistro = fechaRegistro;
        this.estado = estado;
    }
    
    public int getIdCliente() {
        return idCliente;
    }
    
    public void setIdCliente(int idCliente) {
        this.idCliente = idCliente;
    }
    
    public String getNombre() {
        return nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    public String getTelefono() {
        return telefono;
    }
    
    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }
    
    public String getDireccion() {
        return direccion;
    }
    
    public void setDireccion(String direccion) {
        this.direccion = direccion;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public Date getFechaRegistro() {
        return fechaRegistro;
    }
    
    public void setFechaRegistro(Date fechaRegistro) {
        this.fechaRegistro = fechaRegistro;
    }
    
    public int getEstado() {
        return estado;
    }
    
    public void setEstado(int estado) {
        this.estado = estado;
    }
    
    public String getEstadoTexto() {
        return (estado == 1) ? "Activo" : "Inactivo";
    }
    
    @Override
    public String toString() {
        return "Cliente{" +
                "ID=" + idCliente +
                ", nombre='" + nombre + '\'' +
                ", telefono='" + telefono + '\'' +
                ", email='" + email + '\'' +
                ", estado='" + getEstadoTexto() + '\'' +
                '}';
    }
}