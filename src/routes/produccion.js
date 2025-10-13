import express from "express";
const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Producción
 *   description: Endpoints para la gestión de órdenes de producción
 */

/**
 * @swagger
 * /produccion:
 *   get:
 *     summary: Obtener todas las órdenes de producción
 *     tags: [Producción]
 *     responses:
 *       200:
 *         description: Lista de órdenes de producción
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   id:
 *                     type: integer
 *                     example: 1
 *                   producto:
 *                     type: string
 *                     example: Mesa de comedor
 *                   cantidad:
 *                     type: integer
 *                     example: 10
 *                   estado:
 *                     type: string
 *                     example: en_produccion
 *                   fechaInicio:
 *                     type: string
 *                     example: 2025-10-11
 */
router.get("/", (req, res) => {
  const ordenes = [
    {
      id: 1,
      producto: "Mesa de comedor",
      cantidad: 10,
      estado: "en_produccion",
      fechaInicio: "2025-10-01",
    },
    {
      id: 2,
      producto: "Silla moderna",
      cantidad: 20,
      estado: "pendiente",
      fechaInicio: "2025-10-10",
    },
  ];
  res.json(ordenes);
});

/**
 * @swagger
 * /produccion/{id}:
 *   get:
 *     summary: Obtener una orden de producción por ID
 *     tags: [Producción]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID de la orden a obtener
 *     responses:
 *       200:
 *         description: Orden encontrada
 *       404:
 *         description: Orden no encontrada
 */
router.get("/:id", (req, res) => {
  const { id } = req.params;
  const ordenes = [
    { id: 1, producto: "Mesa de comedor", cantidad: 10, estado: "en_produccion", fechaInicio: "2025-10-01" },
    { id: 2, producto: "Silla moderna", cantidad: 20, estado: "pendiente", fechaInicio: "2025-10-10" },
  ];

  const orden = ordenes.find((o) => o.id === parseInt(id));
  if (!orden) return res.status(404).json({ error: "Orden no encontrada" });
  res.json(orden);
});

/**
 * @swagger
 * /produccion:
 *   post:
 *     summary: Crear una nueva orden de producción
 *     tags: [Producción]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - producto
 *               - cantidad
 *             properties:
 *               producto:
 *                 type: string
 *                 example: Mesa de centro
 *               cantidad:
 *                 type: integer
 *                 example: 5
 *               estado:
 *                 type: string
 *                 example: pendiente
 *               fechaInicio:
 *                 type: string
 *                 example: 2025-10-11
 *     responses:
 *       201:
 *         description: Orden creada exitosamente
 */
router.post("/", (req, res) => {
  const { producto, cantidad, estado = "pendiente", fechaInicio = new Date().toISOString().slice(0, 10) } = req.body;
  if (!producto || !cantidad) {
    return res.status(400).json({ error: "Producto y cantidad son obligatorios" });
  }
  // Nota: aquí devolvemos un id fijo simulando creación
  const nuevaOrden = { id: 3, producto, cantidad, estado, fechaInicio };
  res.status(201).json({ message: "Orden creada", orden: nuevaOrden });
});

/**
 * @swagger
 * /produccion/{id}:
 *   put:
 *     summary: Actualizar una orden de producción
 *     tags: [Producción]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID de la orden a actualizar
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               producto:
 *                 type: string
 *               cantidad:
 *                 type: integer
 *               estado:
 *                 type: string
 *               fechaInicio:
 *                 type: string
 *     responses:
 *       200:
 *         description: Orden actualizada correctamente
 */
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { producto, cantidad, estado, fechaInicio } = req.body;
  // En una implementación real buscarías la orden y la actualizarías en BD
  res.json({
    message: `Orden ${id} actualizada correctamente`,
    orden: { id, producto, cantidad, estado, fechaInicio },
  });
});

/**
 * @swagger
 * /produccion/{id}:
 *   delete:
 *     summary: Eliminar una orden de producción
 *     tags: [Producción]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID de la orden a eliminar
 *     responses:
 *       200:
 *         description: Orden eliminada exitosamente
 */
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  // En una implementación real eliminarías de la BD
  res.json({ message: `Orden ${id} eliminada correctamente` });
});

export default router;