// src/routes/produccion.js
import express from "express";
const router = express.Router();

// Datos simulados de producción
const produccion = [
  { id: 1, producto: "Mesa de comedor", estado: "En proceso" },
  { id: 2, producto: "Silla ergonómica", estado: "Terminado" },
  { id: 3, producto: "Armario de madera", estado: "Pendiente" },
  { id: 4, producto: "Escritorio ejecutivo", estado: "En producción" },
];

// Ruta GET principal
router.get("/", (req, res) => {
  res.json(produccion);
  console.log("Ruta de Producción funcionando correctamente ✅");
});

export default router;