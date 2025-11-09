package com.fabrica.muebles.vista;

import com.fabrica.muebles.dao.ClienteDAO;
import com.fabrica.muebles.modelo.Cliente;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.util.List;

/**
 * Ventana de Gestión de Clientes
 * CRUD completo con interfaz gráfica
 * 
 * Autor: William Alonso Samaca Lopez
 */
public class VentanaClientes extends JFrame {
    
    private ClienteDAO clienteDAO;
    
    // Componentes del formulario
    private JTextField txtNombre;
    private JTextField txtTelefono;
    private JTextField txtDireccion;
    private JTextField txtEmail;
    
    // Tabla
    private JTable tabla;
    private DefaultTableModel modeloTabla;
    
    // Botones
    private JButton btnGuardar;
    private JButton btnActualizar;
    private JButton btnEliminar;
    private JButton btnLimpiar;
    private JButton btnRefrescar;
    
    private int idClienteSeleccionado = -1;
    
    public VentanaClientes() {
        clienteDAO = new ClienteDAO();
        inicializarComponentes();
        cargarDatos();
    }
    
    private void inicializarComponentes() {
        setTitle("Gestión de Clientes");
        setSize(900, 600);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(10, 10));
        
        // Panel superior - Formulario
        JPanel panelFormulario = crearPanelFormulario();
        add(panelFormulario, BorderLayout.NORTH);
        
        // Panel central - Tabla
        JPanel panelTabla = crearPanelTabla();
        add(panelTabla, BorderLayout.CENTER);
        
        // Panel inferior - Botones
        JPanel panelBotones = crearPanelBotones();
        add(panelBotones, BorderLayout.SOUTH);
    }
    
    private JPanel crearPanelFormulario() {
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(4, 2, 10, 10));
        panel.setBorder(BorderFactory.createTitledBorder("Datos del Cliente"));
        panel.setBackground(Color.WHITE);
        
        // Nombre
        panel.add(new JLabel("Nombre:"));
        txtNombre = new JTextField();
        panel.add(txtNombre);
        
        // Teléfono
        panel.add(new JLabel("Teléfono:"));
        txtTelefono = new JTextField();
        panel.add(txtTelefono);
        
        // Dirección
        panel.add(new JLabel("Dirección:"));
        txtDireccion = new JTextField();
        panel.add(txtDireccion);
        
        // Email
        panel.add(new JLabel("Email:"));
        txtEmail = new JTextField();
        panel.add(txtEmail);
        
        return panel;
    }
    
    private JPanel crearPanelTabla() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("Lista de Clientes"));
        
        // Crear modelo de tabla
        String[] columnas = {"ID", "Nombre", "Teléfono", "Dirección", "Email", "Fecha Registro", "Estado"};
        modeloTabla = new DefaultTableModel(columnas, 0) {
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        
        tabla = new JTable(modeloTabla);
        tabla.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        tabla.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                seleccionarFila();
            }
        });
        
        JScrollPane scrollPane = new JScrollPane(tabla);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel crearPanelBotones() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));
        panel.setBackground(new Color(240, 240, 240));
        
        btnGuardar = crearBoton("Guardar", new Color(46, 204, 113));
        btnGuardar.addActionListener(e -> guardarCliente());
        
        btnActualizar = crearBoton("Actualizar", new Color(52, 152, 219));
        btnActualizar.addActionListener(e -> actualizarCliente());
        btnActualizar.setEnabled(false);
        
        btnEliminar = crearBoton("Eliminar", new Color(231, 76, 60));
        btnEliminar.addActionListener(e -> eliminarCliente());
        btnEliminar.setEnabled(false);
        
        btnLimpiar = crearBoton("Limpiar", new Color(149, 165, 166));
        btnLimpiar.addActionListener(e -> limpiarFormulario());
        
        btnRefrescar = crearBoton("Refrescar", new Color(155, 89, 182));
        btnRefrescar.addActionListener(e -> cargarDatos());
        
        panel.add(btnGuardar);
        panel.add(btnActualizar);
        panel.add(btnEliminar);
        panel.add(btnLimpiar);
        panel.add(btnRefrescar);
        
        return panel;
    }
    
    private JButton crearBoton(String texto, Color color) {
        JButton boton = new JButton(texto);
        boton.setPreferredSize(new Dimension(120, 35));
        boton.setBackground(color);
        boton.setForeground(Color.WHITE);
        boton.setFont(new Font("Arial", Font.BOLD, 12));
        boton.setFocusPainted(false);
        boton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return boton;
    }
    
    private void cargarDatos() {
        modeloTabla.setRowCount(0);
        List<Cliente> listaClientes = clienteDAO.consultarTodos();
        
        for (Cliente cliente : listaClientes) {
            Object[] fila = {
                cliente.getIdCliente(),
                cliente.getNombre(),
                cliente.getTelefono(),
                cliente.getDireccion(),
                cliente.getEmail(),
                cliente.getFechaRegistro(),
                cliente.getEstadoTexto()
            };
            modeloTabla.addRow(fila);
        }
    }
    
    private void seleccionarFila() {
        int filaSeleccionada = tabla.getSelectedRow();
        if (filaSeleccionada >= 0) {
            idClienteSeleccionado = (int) tabla.getValueAt(filaSeleccionada, 0);
            txtNombre.setText(tabla.getValueAt(filaSeleccionada, 1).toString());
            txtTelefono.setText(tabla.getValueAt(filaSeleccionada, 2).toString());
            txtDireccion.setText(tabla.getValueAt(filaSeleccionada, 3).toString());
            txtEmail.setText(tabla.getValueAt(filaSeleccionada, 4).toString());
            
            btnGuardar.setEnabled(false);
            btnActualizar.setEnabled(true);
            btnEliminar.setEnabled(true);
        }
    }
    
    private void guardarCliente() {
        if (validarCampos()) {
            Cliente cliente = new Cliente(
                txtNombre.getText().trim(),
                txtTelefono.getText().trim(),
                txtDireccion.getText().trim(),
                txtEmail.getText().trim()
            );
            
            if (clienteDAO.insertarCliente(cliente)) {
                JOptionPane.showMessageDialog(this, "Cliente guardado correctamente", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                limpiarFormulario();
                cargarDatos();
            } else {
                JOptionPane.showMessageDialog(this, "Error al guardar el cliente", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    private void actualizarCliente() {
        if (idClienteSeleccionado > 0 && validarCampos()) {
            Cliente cliente = clienteDAO.consultarPorId(idClienteSeleccionado);
            
            if (cliente != null) {
                cliente.setNombre(txtNombre.getText().trim());
                cliente.setTelefono(txtTelefono.getText().trim());
                cliente.setDireccion(txtDireccion.getText().trim());
                cliente.setEmail(txtEmail.getText().trim());
                
                if (clienteDAO.actualizarCliente(cliente)) {
                    JOptionPane.showMessageDialog(this, "Cliente actualizado correctamente", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                    limpiarFormulario();
                    cargarDatos();
                } else {
                    JOptionPane.showMessageDialog(this, "Error al actualizar el cliente", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        }
    }
    
    private void eliminarCliente() {
        if (idClienteSeleccionado > 0) {
            int confirmacion = JOptionPane.showConfirmDialog(
                this,
                "¿Está seguro de eliminar este cliente?",
                "Confirmar Eliminación",
                JOptionPane.YES_NO_OPTION
            );
            
            if (confirmacion == JOptionPane.YES_OPTION) {
                if (clienteDAO.eliminarCliente(idClienteSeleccionado)) {
                    JOptionPane.showMessageDialog(this, "Cliente eliminado correctamente", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                    limpiarFormulario();
                    cargarDatos();
                } else {
                    JOptionPane.showMessageDialog(this, "Error al eliminar el cliente", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        }
    }
    
    private void limpiarFormulario() {
        txtNombre.setText("");
        txtTelefono.setText("");
        txtDireccion.setText("");
        txtEmail.setText("");
        idClienteSeleccionado = -1;
        tabla.clearSelection();
        
        btnGuardar.setEnabled(true);
        btnActualizar.setEnabled(false);
        btnEliminar.setEnabled(false);
    }
    
    private boolean validarCampos() {
        if (txtNombre.getText().trim().isEmpty()) {
            JOptionPane.showMessageDialog(this, "El nombre es obligatorio", "Validación", JOptionPane.WARNING_MESSAGE);
            txtNombre.requestFocus();
            return false;
        }
        if (txtTelefono.getText().trim().isEmpty()) {
            JOptionPane.showMessageDialog(this, "El teléfono es obligatorio", "Validación", JOptionPane.WARNING_MESSAGE);
            txtTelefono.requestFocus();
            return false;
        }
        return true;
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            VentanaClientes ventana = new VentanaClientes();
            ventana.setVisible(true);
        });
    }
}