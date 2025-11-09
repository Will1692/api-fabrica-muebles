package com.fabrica.muebles.vista;

import javax.swing.*;
import java.awt.*;

/**
 * Ventana principal de Administración
 * Panel de control con acceso directo a todos los módulos del sistema
 * 
 * Autor: William Alonso Samaca Lopez
 * Sistema de Gestión Fábrica de Muebles
 */
public class VentanaAdministracion extends JFrame {

    private JPanel panelPrincipal;
    private JButton btnClientes, btnProveedores, btnProduccion, btnCerrarSesion;
    private JLabel lblTitulo, lblInfo;

    public VentanaAdministracion() {
        setTitle("Administración - Fábrica de Muebles");
        setSize(800, 600);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // Cambiado de EXIT_ON_CLOSE
        setLayout(new BorderLayout());

        // Panel principal
        panelPrincipal = new JPanel(new BorderLayout());
        panelPrincipal.setBackground(new Color(240, 240, 240));

        // ═══════════════════════════════════════════════════════════════
        // TÍTULO SUPERIOR
        // ═══════════════════════════════════════════════════════════════
        JPanel panelTitulo = new JPanel();
        panelTitulo.setBackground(new Color(52, 73, 94));
        panelTitulo.setBorder(BorderFactory.createEmptyBorder(20, 0, 20, 0));
        
        lblTitulo = new JLabel("PANEL DE ADMINISTRACIÓN", JLabel.CENTER);
        lblTitulo.setFont(new Font("Segoe UI", Font.BOLD, 28));
        lblTitulo.setForeground(Color.WHITE);
        panelTitulo.add(lblTitulo);
        
        panelPrincipal.add(panelTitulo, BorderLayout.NORTH);

        // ═══════════════════════════════════════════════════════════════
        // PANEL CENTRAL - BOTONES DE MÓDULOS
        // ═══════════════════════════════════════════════════════════════
        JPanel panelBotones = new JPanel(new GridLayout(2, 2, 30, 30));
        panelBotones.setBackground(new Color(240, 240, 240));
        panelBotones.setBorder(BorderFactory.createEmptyBorder(50, 100, 50, 100));

        btnClientes = crearBotonModulo("👥 CLIENTES", new Color(52, 152, 219));
        btnProveedores = crearBotonModulo("📦 PROVEEDORES", new Color(46, 204, 113));
        btnProduccion = crearBotonModulo("🏭 PRODUCCIÓN", new Color(241, 196, 15));
        btnCerrarSesion = crearBotonModulo("🚪 CERRAR SESIÓN", new Color(231, 76, 60));

        panelBotones.add(btnClientes);
        panelBotones.add(btnProveedores);
        panelBotones.add(btnProduccion);
        panelBotones.add(btnCerrarSesion);

        panelPrincipal.add(panelBotones, BorderLayout.CENTER);

        // ═══════════════════════════════════════════════════════════════
        // INFORMACIÓN INFERIOR
        // ═══════════════════════════════════════════════════════════════
        JPanel panelInfo = new JPanel();
        panelInfo.setBackground(new Color(236, 240, 241));
        panelInfo.setBorder(BorderFactory.createEmptyBorder(15, 0, 15, 0));
        
        lblInfo = new JLabel("Seleccione un módulo para administrar el sistema", JLabel.CENTER);
        lblInfo.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        lblInfo.setForeground(new Color(100, 100, 100));
        panelInfo.add(lblInfo);
        
        panelPrincipal.add(panelInfo, BorderLayout.SOUTH);

        add(panelPrincipal);

        // Configurar eventos
        configurarEventos();
    }

    /**
     * Crea un botón de módulo con estilo personalizado
     */
    private JButton crearBotonModulo(String texto, Color color) {
        JButton boton = new JButton("<html><center>" + texto + "</center></html>");
        boton.setBackground(color);
        boton.setForeground(Color.WHITE);
        boton.setFont(new Font("Segoe UI", Font.BOLD, 18));
        boton.setFocusPainted(false);
        boton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        boton.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(color.darker(), 2),
            BorderFactory.createEmptyBorder(20, 20, 20, 20)
        ));
        
        // Efecto hover
        boton.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                boton.setBackground(color.darker());
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                boton.setBackground(color);
            }
        });
        
        return boton;
    }

    /**
     * Configura los eventos de los botones
     */
    private void configurarEventos() {
        
        // Botón Clientes - Abre VentanaClientes
        btnClientes.addActionListener(e -> {
            lblInfo.setText("Abriendo módulo de Clientes...");
            VentanaClientes ventana = new VentanaClientes();
            ventana.setVisible(true);
            lblInfo.setText("Módulo de Clientes abierto");
        });

        // Botón Proveedores - Abre VentanaProveedores
        btnProveedores.addActionListener(e -> {
            lblInfo.setText("Abriendo módulo de Proveedores...");
            VentanaProveedores ventana = new VentanaProveedores();
            ventana.setVisible(true);
            lblInfo.setText("Módulo de Proveedores abierto");
        });

        // Botón Producción - Abre VentanaProduccion
        btnProduccion.addActionListener(e -> {
            lblInfo.setText("Abriendo módulo de Producción...");
            VentanaProduccion ventana = new VentanaProduccion();
            ventana.setVisible(true);
            lblInfo.setText("Módulo de Producción abierto");
        });

        // Botón Cerrar Sesión
        btnCerrarSesion.addActionListener(e -> cerrarSesion());
    }

    /**
     * Cierra la sesión de administración
     */
    private void cerrarSesion() {
        int confirmacion = JOptionPane.showConfirmDialog(
            this,
            "¿Está seguro de que desea cerrar la sesión de administración?",
            "Confirmar Cierre de Sesión",
            JOptionPane.YES_NO_OPTION,
            JOptionPane.QUESTION_MESSAGE
        );

        if (confirmacion == JOptionPane.YES_OPTION) {
            dispose(); // Cierra solo esta ventana
            JOptionPane.showMessageDialog(
                null,
                "Sesión de administración cerrada correctamente",
                "Sesión Cerrada",
                JOptionPane.INFORMATION_MESSAGE
            );
        }
    }

    /**
     * Método main para pruebas
     */
    public static void main(String[] args) {
        // Usar Look and Feel del sistema
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        SwingUtilities.invokeLater(() -> {
            VentanaAdministracion ventana = new VentanaAdministracion();
            ventana.setVisible(true);
        });
    }
}