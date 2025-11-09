package com.fabrica.muebles.vista;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * Ventana Principal del Sistema de Gestión de Fábrica de Muebles
 * Menú con acceso a todos los módulos
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class MenuPrincipal extends JFrame {
    
    private JButton btnClientes;
    private JButton btnProduccion;
    private JButton btnProveedores;
    private JButton btnAdministracion;
    private JButton btnSalir;
    
    public MenuPrincipal() {
        inicializarComponentes();
    }
    
    private void inicializarComponentes() {
        // Configuración de la ventana
        setTitle("Sistema de Gestión - Fábrica de Muebles");
        setSize(600, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setResizable(false);
        
        // Panel principal con color de fondo
        JPanel panelPrincipal = new JPanel();
        panelPrincipal.setLayout(null);
        panelPrincipal.setBackground(new Color(240, 240, 240));
        
        // Título
        JLabel lblTitulo = new JLabel("FÁBRICA DE MUEBLES");
        lblTitulo.setFont(new Font("Arial", Font.BOLD, 28));
        lblTitulo.setForeground(new Color(51, 51, 51));
        lblTitulo.setBounds(120, 20, 400, 40);
        panelPrincipal.add(lblTitulo);
        
        // Subtítulo
        JLabel lblSubtitulo = new JLabel("Sistema de Control Empresarial");
        lblSubtitulo.setFont(new Font("Arial", Font.PLAIN, 16));
        lblSubtitulo.setForeground(new Color(100, 100, 100));
        lblSubtitulo.setBounds(180, 60, 300, 25);
        panelPrincipal.add(lblSubtitulo);
        
        // Botón Clientes
        btnClientes = crearBoton("CLIENTES", 50, 120, new Color(52, 152, 219));
        btnClientes.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                abrirVentanaClientes();
            }
        });
        panelPrincipal.add(btnClientes);
        
        // Botón Producción
        btnProduccion = crearBoton("PRODUCCIÓN", 320, 120, new Color(46, 204, 113));
        btnProduccion.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                abrirVentanaProduccion();
            }
        });
        panelPrincipal.add(btnProduccion);
        
        // Botón Proveedores
        btnProveedores = crearBoton("PROVEEDORES", 50, 250, new Color(155, 89, 182));
        btnProveedores.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                abrirVentanaProveedores();
            }
        });
        panelPrincipal.add(btnProveedores);
        
        // Botón Administración
        btnAdministracion = crearBoton("ADMINISTRACIÓN", 320, 250, new Color(230, 126, 34));
        btnAdministracion.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                abrirVentanaAdministracion();
            }
        });
        panelPrincipal.add(btnAdministracion);
        
        // Botón Salir
        btnSalir = new JButton("SALIR");
        btnSalir.setBounds(220, 400, 160, 40);
        btnSalir.setFont(new Font("Arial", Font.BOLD, 14));
        btnSalir.setBackground(new Color(231, 76, 60));
        btnSalir.setForeground(Color.WHITE);
        btnSalir.setFocusPainted(false);
        btnSalir.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnSalir.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                salir();
            }
        });
        panelPrincipal.add(btnSalir);
        
        // Etiqueta de pie de página
        JLabel lblFooter = new JLabel("© 2025 Sistema desarrollado para SENA");
        lblFooter.setFont(new Font("Arial", Font.PLAIN, 11));
        lblFooter.setForeground(new Color(150, 150, 150));
        lblFooter.setBounds(190, 445, 300, 20);
        panelPrincipal.add(lblFooter);
        
        add(panelPrincipal);
    }
    
    private JButton crearBoton(String texto, int x, int y, Color color) {
        JButton boton = new JButton(texto);
        boton.setBounds(x, y, 230, 100);
        boton.setFont(new Font("Arial", Font.BOLD, 18));
        boton.setBackground(color);
        boton.setForeground(Color.WHITE);
        boton.setFocusPainted(false);
        boton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        boton.setBorder(BorderFactory.createEmptyBorder());
        
        // Efecto hover
        boton.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) {
                boton.setBackground(color.darker());
            }
            public void mouseExited(MouseEvent e) {
                boton.setBackground(color);
            }
        });
        
        return boton;
    }
    
    private void abrirVentanaClientes() {
        JOptionPane.showMessageDialog(this, 
            "Módulo de Clientes\n(En desarrollo...)", 
            "Clientes", 
            JOptionPane.INFORMATION_MESSAGE);
        // VentanaClientes ventana = new VentanaClientes();
        // ventana.setVisible(true);
    }
    
    private void abrirVentanaProduccion() {
        JOptionPane.showMessageDialog(this, 
            "Módulo de Producción\n(En desarrollo...)", 
            "Producción", 
            JOptionPane.INFORMATION_MESSAGE);
        // VentanaProduccion ventana = new VentanaProduccion();
        // ventana.setVisible(true);
    }
    
    private void abrirVentanaProveedores() {
        JOptionPane.showMessageDialog(this, 
            "Módulo de Proveedores\n(En desarrollo...)", 
            "Proveedores", 
            JOptionPane.INFORMATION_MESSAGE);
        // VentanaProveedores ventana = new VentanaProveedores();
        // ventana.setVisible(true);
    }
    
    private void abrirVentanaAdministracion() {
        JOptionPane.showMessageDialog(this, 
            "Módulo de Administración\n(En desarrollo...)", 
            "Administración", 
            JOptionPane.INFORMATION_MESSAGE);
        // VentanaAdministracion ventana = new VentanaAdministracion();
        // ventana.setVisible(true);
    }
    
    private void salir() {
        int opcion = JOptionPane.showConfirmDialog(
            this,
            "¿Está seguro de que desea salir del sistema?",
            "Confirmar Salida",
            JOptionPane.YES_NO_OPTION,
            JOptionPane.QUESTION_MESSAGE
        );
        
        if (opcion == JOptionPane.YES_OPTION) {
            System.out.println("Sistema cerrado correctamente");
            System.exit(0);
        }
    }
    
    public static void main(String[] args) {
        // Usar el Look and Feel del sistema operativo
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        // Crear y mostrar la ventana
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                MenuPrincipal menu = new MenuPrincipal();
                menu.setVisible(true);
            }
        });
    }
}