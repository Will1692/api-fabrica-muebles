package com.fabrica.muebles.modelo;

/**
 * Clase modelo que representa un Proveedor
 * Corresponde a la tabla: proveedor
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class Proveedor {
    
    private int id;
    private String nombre;
    private String contacto;
    private String telefono;
    private String direccion;
    private String correo;

    // Constructor vacío
    public Proveedor() {
    }

    // Constructor para inserción (sin ID - se genera automáticamente)
    public Proveedor(String nombre, String contacto, String telefono, 
                     String direccion, String correo) {
        this.nombre = nombre;
        this.contacto = contacto;
        this.telefono = telefono;
        this.direccion = direccion;
        this.correo = correo;
    }

    // Constructor completo (para consultas desde BD)
    public Proveedor(int id, String nombre, String contacto, String telefono, 
                     String direccion, String correo) {
        this.id = id;
        this.nombre = nombre;
        this.contacto = contacto;
        this.telefono = telefono;
        this.direccion = direccion;
        this.correo = correo;
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getContacto() {
        return contacto;
    }

    public void setContacto(String contacto) {
        this.contacto = contacto;
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

    public String getCorreo() {
        return correo;
    }

    public void setCorreo(String correo) {
        this.correo = correo;
    }

    @Override
    public String toString() {
        return "Proveedor{" +
                "ID=" + id +
                ", nombre='" + nombre + '\'' +
                ", contacto='" + contacto + '\'' +
                ", telefono='" + telefono + '\'' +
                ", correo='" + correo + '\'' +
                '}';
    }
}