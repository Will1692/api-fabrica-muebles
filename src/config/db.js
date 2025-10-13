// src/config/db.js
import mysql from "mysql2";
import dotenv from "dotenv";

dotenv.config(); // Cargar variables de entorno

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
});

// Probar la conexión
db.connect((err) => {
  if (err) {
    console.error("❌ Error de conexión a la base de datos:", err);
  } else {
    console.log("✅ Conexión a la base de datos exitosa!");
  }
});

export default db;