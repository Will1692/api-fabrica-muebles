// ===============================
// 📦 API Fábrica de Muebles
// ===============================

// Importaciones principales
import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import swaggerUi from "swagger-ui-express";
import swaggerJsdoc from "swagger-jsdoc";

// Importar rutas
import clientesRoutes from "./src/routes/clientes.js";
import proveedoresRoutes from "./src/routes/proveedores.js";
import produccionRoutes from "./src/routes/produccion.js";
import administracionRoutes from "./src/routes/administracion.js";

// Configuración inicial
dotenv.config();
const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// ===============================
// 🧭 Configuración Swagger
// ===============================
const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "API Fábrica de Muebles",
      version: "1.0.0",
      description:
        "Documentación de los servicios web del sistema de gestión de fábrica de muebles.",
      contact: {
        name: "Equipo de desarrollo",
        email: "contacto@fabricamuebles.com",
      },
    },
    servers: [
      {
        url: "http://localhost:3000",
        description: "Servidor local de desarrollo",
      },
    ],
  },
  apis: ["./src/routes/*.js"], // Documentar todos los archivos de rutas
});

// Endpoint para visualizar la documentación Swagger
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ===============================
// 🚏 Rutas principales con prefijo /api
// ===============================
app.use("/api/clientes", clientesRoutes);
app.use("/api/proveedores", proveedoresRoutes);
app.use("/api/produccion", produccionRoutes);
app.use("/api/administracion", administracionRoutes);

// ===============================
// 🧪 Ruta raíz (verificación)
// ===============================
app.get("/", (req, res) => {
  res.send("✅ API de Fábrica de Muebles funcionando correctamente");
});

// ===============================
// 🚀 Servidor
// ===============================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Servidor corriendo en el puerto ${PORT}`);
  console.log(`📄 Documentación disponible en http://localhost:${PORT}/api-docs`);
});