import express from "express";
const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Administración
 *   description: Endpoints para la gestión de usuarios del sistema
 */

/**
 * @swagger
 * /administracion:
 *   get:
 *     summary: Obtener todos los usuarios del sistema
 *     tags: [Administración]
 *     responses:
 *       200:
 *         description: Lista de usuarios disponibles
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
 *                     example: Admin Principal
 *                   rol:
 *                     type: string
 *                     example: Administrador
 *                   correo:
 *                     type: string
 *                     example: admin@fabrica.com
 *                   estado:
 *                     type: string
 *                     example: Activo
 */
router.get("/", (req, res) => {
  const usuarios = [
    {
      id: 1,
      nombre: "Admin Principal",
      rol: "Administrador",
      correo: "admin@fabrica.com",
      estado: "Activo",
    },
    {
      id: 2,
      nombre: "María López",
      rol: "Operario",
      correo: "maria@fabrica.com",
      estado: "Activo",
    },
  ];
  res.json(usuarios);
});

/**
 * @swagger
 * /administracion/{id}:
 *   get:
 *     summary: Obtener un usuario por su ID
 *     tags: [Administración]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Usuario encontrado
 *       404:
 *         description: Usuario no encontrado
 */
router.get("/:id", (req, res) => {
  const { id } = req.params;
  const usuarios = [
    {
      id: 1,
      nombre: "Admin Principal",
      rol: "Administrador",
      correo: "admin@fabrica.com",
      estado: "Activo",
    },
    {
      id: 2,
      nombre: "María López",
      rol: "Operario",
      correo: "maria@fabrica.com",
      estado: "Activo",
    },
  ];

  const usuario = usuarios.find((u) => u.id === parseInt(id));
  if (!usuario) return res.status(404).json({ error: "Usuario no encontrado" });
  res.json(usuario);
});

/**
 * @swagger
 * /administracion:
 *   post:
 *     summary: Registrar un nuevo usuario
 *     tags: [Administración]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - nombre
 *               - rol
 *               - correo
 *             properties:
 *               nombre:
 *                 type: string
 *                 example: Carlos Pérez
 *               rol:
 *                 type: string
 *                 example: Supervisor
 *               correo:
 *                 type: string
 *                 example: carlos@fabrica.com
 *               estado:
 *                 type: string
 *                 example: Activo
 *     responses:
 *       201:
 *         description: Usuario creado exitosamente
 */
router.post("/", (req, res) => {
  const { nombre, rol, correo, estado } = req.body;
  if (!nombre || !rol || !correo) {
    return res.status(400).json({ error: "Nombre, rol y correo son obligatorios" });
  }

  const nuevoUsuario = {
    id: 3,
    nombre,
    rol,
    correo,
    estado: estado || "Activo",
  };

  res.status(201).json({ message: "Usuario registrado correctamente", usuario: nuevoUsuario });
});

/**
 * @swagger
 * /administracion/{id}:
 *   put:
 *     summary: Actualizar información de un usuario
 *     tags: [Administración]
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
 *               rol:
 *                 type: string
 *               correo:
 *                 type: string
 *               estado:
 *                 type: string
 *     responses:
 *       200:
 *         description: Usuario actualizado correctamente
 */
router.put("/:id", (req, res) => {
  const { id } = req.params;
  const { nombre, rol, correo, estado } = req.body;
  res.json({
    message: `Usuario ${id} actualizado correctamente`,
    usuario: { id, nombre, rol, correo, estado },
  });
});

/**
 * @swagger
 * /administracion/{id}:
 *   delete:
 *     summary: Eliminar un usuario del sistema
 *     tags: [Administración]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Usuario eliminado exitosamente
 */
router.delete("/:id", (req, res) => {
  const { id } = req.params;
  res.json({ message: `Usuario ${id} eliminado correctamente` });
});

export default router;