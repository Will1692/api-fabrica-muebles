package com.fabrica.muebles.vista;

import com.fabrica.muebles.dao.ProduccionDAO;
import com.fabrica.muebles.modelo.Produccion;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.Date;
import java.util.List;

public class VentanaProduccion extends JFrame {

    private JTextField txtId, txtNombreProducto, txtCantidad, txtFechaInicio, txtFechaFin, txtEstado;
    private JTable tablaProduccion;
    private DefaultTableModel modelo;
    private ProduccionDAO produccionDAO;

    public VentanaProduccion() {
        produccionDAO = new ProduccionDAO();
        setTitle("Gestión de Producción - Fábrica de Muebles");
        setSize(800, 600);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        // Panel de formulario
        JPanel panelFormulario = new JPanel(new GridLayout(6, 2, 10, 10));
        panelFormulario.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        panelFormulario.add(new JLabel("ID:"));
        txtId = new JTextField();
        txtId.setEditable(false);
        panelFormulario.add(txtId);

        panelFormulario.add(new JLabel("Nombre Producto:"));
        txtNombreProducto = new JTextField();
        panelFormulario.add(txtNombreProducto);

        panelFormulario.add(new JLabel("Cantidad:"));
        txtCantidad = new JTextField();
        panelFormulario.add(txtCantidad);

        panelFormulario.add(new JLabel("Fecha Inicio (YYYY-MM-DD):"));
        txtFechaInicio = new JTextField();
        panelFormulario.add(txtFechaInicio);

        panelFormulario.add(new JLabel("Fecha Fin (YYYY-MM-DD):"));
        txtFechaFin = new JTextField();
        panelFormulario.add(txtFechaFin);

        panelFormulario.add(new JLabel("Estado:"));
        txtEstado = new JTextField();
        panelFormulario.add(txtEstado);

        add(panelFormulario, BorderLayout.NORTH);

        // Tabla
        modelo = new DefaultTableModel(new String[]{"ID", "Producto", "Cantidad", "Inicio", "Fin", "Estado"}, 0);
        tablaProduccion = new JTable(modelo);
        JScrollPane scroll = new JScrollPane(tablaProduccion);
        add(scroll, BorderLayout.CENTER);

        // Panel de botones
        JPanel panelBotones = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));

        JButton btnAgregar = new JButton("Agregar");
        JButton btnActualizar = new JButton("Actualizar");
        JButton btnEliminar = new JButton("Eliminar");
        JButton btnFinalizar = new JButton("Finalizar");
        JButton btnLimpiar = new JButton("Limpiar");

        // Colores de botones (como en VentanaClientes)
        btnAgregar.setBackground(new Color(76, 175, 80));
        btnAgregar.setForeground(Color.WHITE);

        btnActualizar.setBackground(new Color(33, 150, 243));
        btnActualizar.setForeground(Color.WHITE);

        btnEliminar.setBackground(new Color(244, 67, 54));
        btnEliminar.setForeground(Color.WHITE);

        btnFinalizar.setBackground(new Color(255, 193, 7));
        btnFinalizar.setForeground(Color.BLACK);

        btnLimpiar.setBackground(new Color(158, 158, 158));
        btnLimpiar.setForeground(Color.WHITE);

        panelBotones.add(btnAgregar);
        panelBotones.add(btnActualizar);
        panelBotones.add(btnEliminar);
        panelBotones.add(btnFinalizar);
        panelBotones.add(btnLimpiar);
        add(panelBotones, BorderLayout.SOUTH);

        // Eventos
        btnAgregar.addActionListener(e -> agregarProduccion());
        btnActualizar.addActionListener(e -> actualizarProduccion());
        btnEliminar.addActionListener(e -> eliminarProduccion());
        btnFinalizar.addActionListener(e -> finalizarProduccion());
        btnLimpiar.addActionListener(e -> limpiarCampos());

        tablaProduccion.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent evt) {
                int fila = tablaProduccion.getSelectedRow();
                if (fila >= 0) {
                    txtId.setText(modelo.getValueAt(fila, 0).toString());
                    txtNombreProducto.setText(modelo.getValueAt(fila, 1).toString());
                    txtCantidad.setText(modelo.getValueAt(fila, 2).toString());
                    txtFechaInicio.setText(modelo.getValueAt(fila, 3).toString());
                    txtFechaFin.setText(modelo.getValueAt(fila, 4) != null ? modelo.getValueAt(fila, 4).toString() : "");
                    txtEstado.setText(modelo.getValueAt(fila, 5).toString());
                }
            }
        });

        listarProduccion();
        setVisible(true);
    }

    private void listarProduccion() {
        modelo.setRowCount(0);
        List<Produccion> lista = produccionDAO.consultarTodos();
        for (Produccion p : lista) {
            modelo.addRow(new Object[]{
                p.getId(),
                p.getNombreProducto(),
                p.getCantidad(),
                p.getFechaInicio(),
                p.getFechaFin(),
                p.getEstado()
            });
        }
    }

    private void agregarProduccion() {
        try {
            String nombre = txtNombreProducto.getText();
            int cantidad = Integer.parseInt(txtCantidad.getText());
            Date fechaInicio = Date.valueOf(txtFechaInicio.getText());
            Date fechaFin = txtFechaFin.getText().isEmpty() ? null : Date.valueOf(txtFechaFin.getText());
            String estado = txtEstado.getText();

            Produccion p = new Produccion(nombre, cantidad, fechaInicio, estado);
            p.setFechaFin(fechaFin);

            if (produccionDAO.insertarProduccion(p)) {
                JOptionPane.showMessageDialog(this, "Producción agregada correctamente.");
                listarProduccion();
                limpiarCampos();
            } else {
                JOptionPane.showMessageDialog(this, "Error al agregar producción.");
            }
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Datos inválidos: " + e.getMessage());
        }
    }

    private void actualizarProduccion() {
        if (txtId.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Seleccione un registro para actualizar.");
            return;
        }
        try {
            int id = Integer.parseInt(txtId.getText());
            String nombre = txtNombreProducto.getText();
            int cantidad = Integer.parseInt(txtCantidad.getText());
            Date fechaInicio = Date.valueOf(txtFechaInicio.getText());
            Date fechaFin = txtFechaFin.getText().isEmpty() ? null : Date.valueOf(txtFechaFin.getText());
            String estado = txtEstado.getText();

            Produccion p = new Produccion(id, nombre, cantidad, fechaInicio, fechaFin, estado);
            if (produccionDAO.actualizarProduccion(p)) {
                JOptionPane.showMessageDialog(this, "Producción actualizada correctamente.");
                listarProduccion();
                limpiarCampos();
            } else {
                JOptionPane.showMessageDialog(this, "Error al actualizar producción.");
            }
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Datos inválidos: " + e.getMessage());
        }
    }

    private void eliminarProduccion() {
        if (txtId.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Seleccione una producción para eliminar.");
            return;
        }
        int id = Integer.parseInt(txtId.getText());
        int confirm = JOptionPane.showConfirmDialog(this, "¿Desea eliminar esta producción?", "Confirmar", JOptionPane.YES_NO_OPTION);
        if (confirm == JOptionPane.YES_OPTION) {
            if (produccionDAO.eliminarProduccion(id)) {
                JOptionPane.showMessageDialog(this, "Producción eliminada correctamente.");
                listarProduccion();
                limpiarCampos();
            } else {
                JOptionPane.showMessageDialog(this, "Error al eliminar producción.");
            }
        }
    }

    private void finalizarProduccion() {
        if (txtId.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Seleccione una producción para finalizar.");
            return;
        }
        int id = Integer.parseInt(txtId.getText());
        if (produccionDAO.finalizarProduccion(id)) {
            JOptionPane.showMessageDialog(this, "Producción finalizada exitosamente.");
            listarProduccion();
            limpiarCampos();
        } else {
            JOptionPane.showMessageDialog(this, "Error al finalizar producción.");
        }
    }

    private void limpiarCampos() {
        txtId.setText("");
        txtNombreProducto.setText("");
        txtCantidad.setText("");
        txtFechaInicio.setText("");
        txtFechaFin.setText("");
        txtEstado.setText("");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(VentanaProduccion::new);
    }
}