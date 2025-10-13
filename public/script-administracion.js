// src/routes/administracion.js
import express from "express";
const router = express.Router();

// Datos simulados de administración
const administracion = [
  { id: 1, nombre: "Carlos Gómez", rol: "Gerente General", estado: "Activo" },
  { id: 2, nombre: "Laura Pérez", rol: "Contadora", estado: "Activo" },
  { id: 3, nombre: "Andrés Rojas", rol: "Supervisor de Ventas", estado: "Inactivo" },
  { id: 4, nombre: "María Torres", rol: "Jefe de Producción", estado: "Activo" },
];

// Ruta GET principal
router.get("/", (req, res) => {
  res.json(administracion);
  console.log("Ruta de Administración funcionando correctamente ✅");
});

export default router;