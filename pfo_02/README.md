# Programación sobre Redes - PFO 2: Sistema de Gestión de Tareas

Ríos, Román | Comisión 3A

---

## Descripción

API REST desarrollada con Flask que permite registrar usuarios, iniciar sesión y gestionar acceso a una vista de tareas.  
Incluye autenticación con contraseñas hasheadas, persistencia en SQLite, un cliente web simple y un cliente en consola.

---

## Requisitos

- Python 3
- Librerías:
  - flask
  - werkzeug
  - requests

---

## Instalación

```bash
pip install flask werkzeug requests
```

---

## Estructura del Proyecto

- `servidor.py`: API Flask + SQLite
- `cliente.py`: Cliente en consola para interactuar con la API
- `templates/index.html`: Interfaz web básica
- `database.db`: Base de datos SQLite

---

## Ejecución

### 1. Iniciar el servidor

```bash
python servidor.py
```

Servidor disponible en:
http://127.0.0.1:5000

---

## Formas de probar

### 🔹 Opción 1: Navegador (frontend)

1. Ir a: http://127.0.0.1:5000/
2. Acceder a "Ir a tareas"
3. Registrar usuario
4. Iniciar sesión
5. Ver respuesta en pantalla

---

### 🔹 Opción 2: Cliente en consola

```bash
python cliente.py
```

Opciones disponibles:
- Registrarse
- Iniciar sesión

Se mostrarán las respuestas de la API en consola.

---

## Endpoints

- POST `/registro` → Registro de usuario  
- POST `/login` → Inicio de sesión  
- GET `/tareas` → Vista HTML  
- GET `/` → Página de inicio  

---

## Base de datos

SQLite (`database.db`)

Tabla `usuarios`:
- id
- usuario
- contraseña (hasheada)

---

## Funcionalidades

- API REST con Flask
- Registro y login de usuarios
- Contraseñas protegidas con hash
- Persistencia en SQLite
- Cliente web (HTML + fetch)
- Cliente en consola (requests)
- Manejo básico de errores

---

## Respuestas conceptuales

### ¿Por qué hashear contraseñas?

- No se almacenan en texto plano
- Protege al usuario si roban la base de datos
- Es una práctica estándar de seguridad
- Evita accesos no autorizados

### Ventajas de SQLite

- No requiere instalación de servidor
- Fácil de usar
- Ideal para proyectos pequeños
- Portátil (un solo archivo .db)
- Integración directa con Python

---

## Capturas

![Capturas](https://romanrios.github.io/IFTS-programacion-sobre-redes/pfo_02/capturas/capturas_pfo2_01.jpg)

![Capturas](https://romanrios.github.io/IFTS-programacion-sobre-redes/pfo_02/capturas/capturas_pfo2_02.jpg)

![Capturas](https://romanrios.github.io/IFTS-programacion-sobre-redes/pfo_02/capturas/capturas_pfo2_03.jpg)

---

Instituto de Formación Técnica Superior N° 29  

Tecnicatura Superior en Desarrollo de Software  

Año 2026
