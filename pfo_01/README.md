# Programación sobre Redes - PFO 1: Chat Cliente-Servidor con Sockets

Ríos, Román | Comisión 3A

---

## Descripción

Este proyecto consiste en la implementación de un sistema básico de comunicación cliente-servidor utilizando sockets en Python.  
El servidor recibe mensajes de múltiples clientes, los almacena en una base de datos SQLite y responde con una confirmación que incluye la fecha y hora de recepción.

---

## Requisitos

- Python 3
- Librerías estándar:
  - socket
  - sqlite3
  - datetime

(No se requiere instalación adicional)

---

## Estructura del Proyecto

- `servidor.py`: Implementa el servidor de sockets y la persistencia en base de datos.
- `cliente.py`: Permite conectarse al servidor y enviar mensajes.
- `mensajes.db`: Base de datos SQLite generada automáticamente.

---

## Ejecución

### 1. Iniciar el servidor

```bash
python servidor.py
```

El servidor quedará escuchando en:

localhost:5000

---

### 2. Ejecutar el cliente (en otra terminal)

```bash
python cliente.py
```

---

## Uso

- El cliente se conecta al servidor.
- Permite enviar múltiples mensajes.
- Para finalizar, escribir:

éxito

- El servidor responde a cada mensaje con:

Mensaje recibido: <timestamp>

---

## Base de Datos

Se utiliza SQLite con una tabla llamada `mensajes`:

- `id`: Identificador único
- `contenido`: Mensaje enviado por el cliente
- `fecha_envio`: Fecha y hora del mensaje
- `ip_cliente`: Dirección IP del cliente

---

## Funcionalidades Implementadas

- Servidor TCP en `localhost:5000`
- Recepción de mensajes desde múltiples clientes
- Persistencia en base de datos SQLite
- Manejo de errores:
  - Puerto ocupado
  - Problemas con la base de datos
- Respuesta automática al cliente
- Cliente interactivo en consola

---

## Pruebas

1. Ejecutar el servidor.
2. Ejecutar uno o más clientes en distintas terminales.
3. Enviar mensajes.
4. Verificar:
   - Respuesta del servidor
   - Almacenamiento en `mensajes.db`

---

Instituto de Formación Técnica Superior N° 29  

Tecnicatura Superior en Desarrollo de Software  

Año 2026
