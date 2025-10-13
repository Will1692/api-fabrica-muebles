import express from "express";
const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Clientes
 *   description: Endpoints para la gestión de clientes
 */

/**
 * @swagger
 * /clientes:
 *   get:
 *     summary: Obtener todos los clientes
 *     tags: [Clientes]
 *     responses:
 *       200:
 *         description: Lista de todos los clientes
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
 *                   nombre:
 *                     type: string
 *                     example: Juan Pérez
 *                   correo:
 *                     type: string
 *                     example: juan@example.com
 */
router.get("/", (req, res) => {
  const clientes = [
    { id: 1, nombre: "Juan Pérez", correo: "juan@example.com" },
    { id: 2, nombre: "María López", correo: "maria@example.com" },
  ];
  res.json(clientes);
});

/**
 * @swagger
 * /clientes/{id}:
 *   get:
 *     summary: Obtener un cliente por su ID
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID del cliente a obtener
 *     responses:
 *       200:
 *         description: Cliente encontrado
 *       404:
 *         description: Cliente no encontrado
 */
router.get("/:id", (req, res) => {
  const { id } = req.params;
  const clientes = [
    { id: 1, nombre: "Juan Pérez", correo: "juan@example.com" },
    { id: 2, nombre: "María López", correo: "maria@example.com" },
  ];

  const cliente = clientes.find((c) => c.id === parseInt(id));

  if (!cliente) {
    return res.status(404).json({ error: "Cliente no encontrado" });
  }

  res.json(cliente);
});

/**
 * @swagger
 * /clientes:
 *   post:
 *     summary: Crear un nuevo cliente
 *     tags: [Clientes]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - nombre
 *               - correo
 *             properties:
 *               nombre:
 *                 type: string
 *                 example: Pedro García
 *               correo:
 *                 type: string
 *                 example: pedro@example.com
 *     responses:
 *       201:
 *         description: Cliente creado exitosamente
 */
router.post("/", (req, res) => {
  const { nombre, correo } = req.body;
  if (!nombre || !correo) {
    return res.status(400).json({ error: "Nombre y correo son obligatorios" });
  }
  res.status(201).json({
    message: `Cliente '${nombre}' creado exitosamente`,
    cliente: { id: 3, nombre, correo },
  });
});

/**
 * @swagger
 * /clientes/{id}:
 *   put:
 *     summary: Actualizar un cliente existente
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID del cliente a actualizar
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nombre:
 *                 type: string
 *                 example: Carlos Gómez
 *               correo:
 *                 type: string
 *                 example: carlos@example.com
 *     responses:
 *       200:
 *         description: Cliente actualizado correctamente
 */
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { nombre, correo } = req.body;
  res.json({
    message: `Cliente ${id} actualizado correctamente`,
    cliente: { id, nombre, correo },
  });
});

/**
 * @swagger
 * /clientes/{id}:
 *   delete:
 *     summary: Eliminar un cliente
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID del cliente a eliminar
 *     responses:
 *       200:
 *         description: Cliente eliminado exitosamente
 */
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  res.json({ message: `Cliente ${id} eliminado correctamente` });
});

export default router;