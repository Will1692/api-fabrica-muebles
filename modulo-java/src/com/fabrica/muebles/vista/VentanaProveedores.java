package com.fabrica.muebles.vista;

import com.fabrica.muebles.dao.ProveedorDAO;
import com.fabrica.muebles.modelo.Proveedor;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.util.List;

public class VentanaProveedores extends JFrame {

    private JTextField txtId, txtNombre, txtContacto, txtTelefono, txtDireccion, txtCorreo;
    private JTable tabla;
    private DefaultTableModel modelo;
    private ProveedorDAO dao = new ProveedorDAO();

    public VentanaProveedores() {
        setTitle("Gestión de Proveedores");
        setSize(900, 600);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        // PANEL SUPERIOR - FORMULARIO
        JPanel panelForm = new JPanel(new GridLayout(6, 2, 5, 5));
        panelForm.setBorder(BorderFactory.createTitledBorder("Datos del Proveedor"));

        panelForm.add(new JLabel("ID:"));
        txtId = new JTextField();
        txtId.setEnabled(false);
        panelForm.add(txtId);

        panelForm.add(new JLabel("Nombre:"));
        txtNombre = new JTextField();
        panelForm.add(txtNombre);

        panelForm.add(new JLabel("Contacto:"));
        txtContacto = new JTextField();
        panelForm.add(txtContacto);

        panelForm.add(new JLabel("Teléfono:"));
        txtTelefono = new JTextField();
        panelForm.add(txtTelefono);

        panelForm.add(new JLabel("Dirección:"));
        txtDireccion = new JTextField();
        panelForm.add(txtDireccion);

        panelForm.add(new JLabel("Correo:"));
        txtCorreo = new JTextField();
        panelForm.add(txtCorreo);

        add(panelForm, BorderLayout.NORTH);

        // PANEL CENTRAL - TABLA
        modelo = new DefaultTableModel(new String[]{"ID", "Nombre", "Contacto", "Teléfono", "Dirección", "Correo"}, 0);
        tabla = new JTable(modelo);
        JScrollPane scroll = new JScrollPane(tabla);
        scroll.setBorder(BorderFactory.createTitledBorder("Lista de Proveedores"));
        add(scroll, BorderLayout.CENTER);

        // PANEL INFERIOR - BOTONES
        JPanel panelBotones = new JPanel();

        JButton btnAgregar = new JButton("Guardar");
        JButton btnActualizar = new JButton("Actualizar");
        JButton btnEliminar = new JButton("Eliminar");
        JButton btnLimpiar = new JButton("Limpiar");
        JButton btnListar = new JButton("Refrescar");

        // Colores de los botones (igual que VentanaClientes)
        btnAgregar.setBackground(new Color(76, 175, 80));   // Verde
        btnActualizar.setBackground(new Color(33, 150, 243)); // Azul
        btnEliminar.setBackground(new Color(244, 67, 54));   // Rojo
        btnLimpiar.setBackground(new Color(158, 158, 158));  // Gris
        btnListar.setBackground(new Color(156, 39, 176));    // Morado

        btnAgregar.setForeground(Color.WHITE);
        btnActualizar.setForeground(Color.WHITE);
        btnEliminar.setForeground(Color.WHITE);
        btnLimpiar.setForeground(Color.WHITE);
        btnListar.setForeground(Color.WHITE);

        panelBotones.add(btnAgregar);
        panelBotones.add(btnActualizar);
        panelBotones.add(btnEliminar);
        panelBotones.add(btnLimpiar);
        panelBotones.add(btnListar);

        add(panelBotones, BorderLayout.SOUTH);

        // ACCIONES DE BOTONES
        btnAgregar.addActionListener(e -> agregar());
        btnActualizar.addActionListener(e -> actualizar());
        btnEliminar.addActionListener(e -> eliminar());
        btnLimpiar.addActionListener(e -> limpiar());
        btnListar.addActionListener(e -> listar());

        tabla.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int fila = tabla.getSelectedRow();
                if (fila != -1) {
                    txtId.setText(modelo.getValueAt(fila, 0).toString());
                    txtNombre.setText(modelo.getValueAt(fila, 1).toString());
                    txtContacto.setText(modelo.getValueAt(fila, 2).toString());
                    txtTelefono.setText(modelo.getValueAt(fila, 3).toString());
                    txtDireccion.setText(modelo.getValueAt(fila, 4).toString());
                    txtCorreo.setText(modelo.getValueAt(fila, 5).toString());
                }
            }
        });

        listar();
    }

    // MÉTODOS CRUD

    private void listar() {
        modelo.setRowCount(0);
        List<Proveedor> lista = dao.listar();
        for (Proveedor p : lista) {
            modelo.addRow(new Object[]{
                p.getId(), p.getNombre(), p.getContacto(),
                p.getTelefono(), p.getDireccion(), p.getCorreo()
            });
        }
    }

    private void agregar() {
        Proveedor p = new Proveedor();
        p.setNombre(txtNombre.getText());
        p.setContacto(txtContacto.getText());
        p.setTelefono(txtTelefono.getText());
        p.setDireccion(txtDireccion.getText());
        p.setCorreo(txtCorreo.getText());

        if (dao.agregar(p)) {
            JOptionPane.showMessageDialog(this, "Proveedor agregado correctamente.");
            listar();
            limpiar();
        } else {
            JOptionPane.showMessageDialog(this, "Error al agregar el proveedor.");
        }
    }

    private void actualizar() {
        if (txtId.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Seleccione un proveedor de la tabla.");
            return;
        }
        Proveedor p = new Proveedor();
        p.setId(Integer.parseInt(txtId.getText()));
        p.setNombre(txtNombre.getText());
        p.setContacto(txtContacto.getText());
        p.setTelefono(txtTelefono.getText());
        p.setDireccion(txtDireccion.getText());
        p.setCorreo(txtCorreo.getText());

        if (dao.actualizar(p)) {
            JOptionPane.showMessageDialog(this, "Proveedor actualizado correctamente.");
            listar();
            limpiar();
        } else {
            JOptionPane.showMessageDialog(this, "Error al actualizar el proveedor.");
        }
    }

    private void eliminar() {
        if (txtId.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Seleccione un proveedor para eliminar.");
            return;
        }
        int confirm = JOptionPane.showConfirmDialog(this, "¿Eliminar este proveedor?", "Confirmar", JOptionPane.YES_NO_OPTION);
        if (confirm == JOptionPane.YES_OPTION) {
            int id = Integer.parseInt(txtId.getText());
            if (dao.eliminar(id)) {
                JOptionPane.showMessageDialog(this, "Proveedor eliminado correctamente.");
                listar();
                limpiar();
            } else {
                JOptionPane.showMessageDialog(this, "Error al eliminar el proveedor.");
            }
        }
    }

    private void limpiar() {
        txtId.setText("");
        txtNombre.setText("");
        txtContacto.setText("");
        txtTelefono.setText("");
        txtDireccion.setText("");
        txtCorreo.setText("");
    }

    // MAIN DE PRUEBA
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new VentanaProveedores().setVisible(true));
    }
}