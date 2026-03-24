# Programación sobre Redes - PFO 2: Sistema de Gestión de Tareas

Ríos, Román | Comisión 3A


## Requisitos
- Python 3
- Flask

## Instalación
pip install flask werkzeug

## Ejecución
python servidor.py

## Uso
- Abrir navegador en: http://127.0.0.1:5000/tareas
- Registrar usuario
- Iniciar sesión

## Endpoints

POST /registro  
POST /login  
GET /tareas  

## Base de datos
SQLite (database.db)

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


Instituto de Formación Técnica Superior N° 29

Tecnicatura Superior en Desarrollo de Software

Año 2026
