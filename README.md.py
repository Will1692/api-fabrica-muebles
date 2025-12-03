# Sistema de Gestión Fábrica de Muebles

Sistema de control interno para la gestión de clientes, proveedores y producción de una fábrica de muebles.

## Autor

William Alonso Samaca Lopez

## Descripción

Este proyecto es una migración de Java a Python de un sistema de gestión empresarial que permite administrar:

- Clientes
- Proveedores
- Producción de muebles

El sistema implementa operaciones CRUD completas para cada módulo y utiliza MySQL como base de datos.

## Tecnologías Utilizadas

- Python 3.14
- PyMySQL 1.1.2
- MySQL 8.0
- PyCharm IDE
- Git para control de versiones

## Requisitos Previos

- Python 3.8 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd fabrica_muebles_python
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

### 3. Activar entorno virtual

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos

Editar el archivo `config/database.properties` con tus credenciales:
```properties
db.host=localhost
db.port=3306
db.database=fabrica_muebles
db.user=root
db.password=tu_contraseña
db.charset=utf8mb4
```

### 6. Crear la base de datos

Ejecutar en MySQL:
```sql
CREATE DATABASE fabrica_muebles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Estructura del Proyecto
```
fabrica_muebles_python/
├── src/
│   └── com/
│       └── fabrica/
│           └── muebles/
│               ├── config/
│               ├── modelo/
│               │   ├── cliente.py
│               │   ├── proveedor.py
│               │   ├── produccion.py
│               │   └── administracion.py
│               ├── dao/
│               │   ├── cliente_dao.py
│               │   ├── proveedor_dao.py
│               │   └── produccion_dao.py
│               ├── util/
│               │   └── conexion_bd.py
│               └── vista/
├── config/
│   └── database.properties
├── test_conexion.py
├── test_cliente.py
├── test_completo.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Uso

### Probar conexión a la base de datos
```bash
python test_conexion.py
```

### Ejecutar pruebas completas
```bash
python test_completo.py
```

### Ejemplo de uso en código
```python
from com.fabrica.muebles.modelo.cliente import Cliente
from com.fabrica.muebles.dao.cliente_dao import ClienteDAO

# Crear un nuevo cliente
cliente = Cliente(
    nombre="Juan Pérez",
    telefono="3001234567",
    direccion="Calle 123",
    email="juan@email.com"
)

# Insertar en la base de datos
dao = ClienteDAO()
dao.insertar_cliente(cliente)

# Consultar todos los clientes
clientes = dao.consultar_todos()
for c in clientes:
    print(c)
```

## Funcionalidades

### Módulo Clientes
- Insertar nuevo cliente
- Consultar todos los clientes
- Consultar cliente por ID
- Actualizar datos de cliente
- Eliminar cliente

### Módulo Proveedores
- Agregar nuevo proveedor
- Listar todos los proveedores
- Buscar proveedor por ID
- Actualizar datos de proveedor
- Eliminar proveedor

### Módulo Producción
- Registrar nueva producción
- Consultar todas las producciones
- Consultar producción por ID
- Actualizar datos de producción
- Finalizar producción
- Eliminar producción

## Estándares de Codificación

El proyecto sigue las convenciones de Python (PEP 8):

- Nombres de variables: `snake_case`
- Nombres de clases: `PascalCase`
- Nombres de métodos: `snake_case`
- Nombres de paquetes: `lowercase`

## Migración desde Java

Este proyecto es una migración de un sistema original desarrollado en Java. Se han mantenido las mismas funcionalidades con las siguientes mejoras:

- Reducción de código aproximadamente 45%
- Sintaxis más simple y legible
- Uso de características pythonic
- Manejo simplificado de conexiones a BD

## Control de Versiones

El proyecto utiliza Git para control de versiones. Principales comandos:
```bash
git status
git add .
git commit -m "Mensaje del commit"
git log
```

## Licencia

Proyecto educativo para SENA - Análisis y Desarrollo de Software

## Contacto

William Alonso Samaca Lopez
Email: wialsalo@hotmail.com