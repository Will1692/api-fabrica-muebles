import express from "express";
const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Proveedores
 *   description: Endpoints para la gestión de proveedores
 */

/**
 * @swagger
 * /proveedores:
 *   get:
 *     summary: Obtener todos los proveedores
 *     tags: [Proveedores]
 *     responses:
 *       200:
 *         description: Lista de proveedores disponibles
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
 *                     example: Maderas del Norte
 *                   contacto:
 *                     type: string
 *                     example: Carlos Torres
 *                   telefono:
 *                     type: string
 *                     example: 3216549870
 *                   correo:
 *                     type: string
 *                     example: contacto@maderasnorte.com
 *                   direccion:
 *                     type: string
 *                     example: Calle 10 #15-25, Bogotá
 */
router.get("/", (req, res) => {
  const proveedores = [
    {
      id: 1,
      nombre: "Maderas del Norte",
      contacto: "Carlos Torres",
      telefono: "3216549870",
      correo: "contacto@maderasnorte.com",
      direccion: "Calle 10 #15-25, Bogotá",
    },
    {
      id: 2,
      nombre: "Acabados y Barnices S.A.S",
      contacto: "María Gómez",
      telefono: "3209988776",
      correo: "ventas@acabadosybarnices.com",
      direccion: "Cra 45 #20-30, Medellín",
    },
  ];
  res.json(proveedores);
});

/**
 * @swagger
 * /proveedores/{id}:
 *   get:
 *     summary: Obtener un proveedor por su ID
 *     tags: [Proveedores]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Proveedor encontrado
 *       404:
 *         description: Proveedor no encontrado
 */
router.get("/:id", (req, res) => {
  const { id } = req.params;
  const proveedores = [
    {
      id: 1,
      nombre: "Maderas del Norte",
      contacto: "Carlos Torres",
      telefono: "3216549870",
      correo: "contacto@maderasnorte.com",
      direccion: "Calle 10 #15-25, Bogotá",
    },
    {
      id: 2,
      nombre: "Acabados y Barnices S.A.S",
      contacto: "María Gómez",
      telefono: "3209988776",
      correo: "ventas@acabadosybarnices.com",
      direccion: "Cra 45 #20-30, Medellín",
    },
  ];

  const proveedor = proveedores.find((p) => p.id === parseInt(id));
  if (!proveedor) return res.status(404).json({ error: "Proveedor no encontrado" });
  res.json(proveedor);
});

/**
 * @swagger
 * /proveedores:
 *   post:
 *     summary: Registrar un nuevo proveedor
 *     tags: [Proveedores]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - nombre
 *               - contacto
 *               - telefono
 *             properties:
 *               nombre:
 *                 type: string
 *                 example: Proveedora Andina
 *               contacto:
 *                 type: string
 *                 example: Juan Rojas
 *               telefono:
 *                 type: string
 *                 example: 3101122334
 *               correo:
 *                 type: string
 *                 example: contacto@proveedoraandina.com
 *               direccion:
 *                 type: string
 *                 example: Calle 25 #10-55, Cali
 *     responses:
 *       201:
 *         description: Proveedor registrado exitosamente
 */
router.post("/", (req, res) => {
  const { nombre, contacto, telefono, correo, direccion } = req.body;
  if (!nombre || !contacto || !telefono) {
    return res.status(400).json({ error: "Nombre, contacto y teléfono son obligatorios" });
  }

  const nuevoProveedor = {
    id: 3,
    nombre,
    contacto,
    telefono,
    correo,
    direccion,
  };

  res.status(201).json({ message: "Proveedor registrado", proveedor: nuevoProveedor });
});

/**
 * @swagger
 * /proveedores/{id}:
 *   put:
 *     summary: Actualizar información de un proveedor
 *     tags: [Proveedores]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nombre:
 *                 type: string
 *               contacto:
 *                 type: string
 *               telefono:
 *                 type: string
 *               correo:
 *                 type: string
 *               direccion:
 *                 type: string
 *     responses:
 *       200:
 *         description: Proveedor actualizado correctamente
 */
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { nombre, contacto, telefono, correo, direccion } = req.body;
  res.json({
    message: `Proveedor ${id} actualizado correctamente`,
    proveedor: { id, nombre, contacto, telefono, correo, direccion },
  });
});

/**
 * @swagger
 * /proveedores/{id}:
 *   delete:
 *     summary: Eliminar un proveedor
 *     tags: [Proveedores]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Proveedor eliminado exitosamente
 */
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  res.json({ message: `Proveedor ${id} eliminado correctamente` });
});

export default router;