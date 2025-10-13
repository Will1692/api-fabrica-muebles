// 📦 script-clientes.js
// Este script obtiene los clientes desde la API y los muestra en la tabla

const API_URL = "http://localhost:3000/clientes"; // Asegúrate que tu API corra en este puerto

// Función para cargar los clientes
async function cargarClientes() {
  try {
    const respuesta = await fetch(API_URL);
    if (!respuesta.ok) throw new Error("Error al obtener los clientes");
    const clientes = await respuesta.json();

    const tabla = document.getElementById("tabla-clientes");
    tabla.innerHTML = ""; // Limpia la tabla

    clientes.forEach((cliente) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${cliente.id}</td>
        <td>${cliente.nombre}</td>
        <td>${cliente.correo || "sin correo"}</td>
      `;
      tabla.appendChild(fila);
    });
  } catch (error) {
    console.error("❌ Error cargando clientes:", error);
  }
}

// Cargar clientes al iniciar la página
document.addEventListener("DOMContentLoaded", cargarClientes);