# Programación sobre Redes - PFO 1: Chat Cliente-Servidor con Sockets

Ríos, Román | Comisión 3A

---

## Descripción

Sistema cliente-servidor en Python usando sockets.  
El servidor recibe mensajes de múltiples clientes, los guarda en SQLite y responde con un timestamp.  
Se implementa un modelo **multicliente concurrente** mediante threading.

---

## Requisitos

- Python 3
- Librerías estándar:
  - socket
  - sqlite3
  - datetime
  - threading

---

## Estructura

- `servidor.py`: Servidor TCP + SQLite + threading
- `cliente.py`: Cliente interactivo por consola
- `mensajes.db`: Base de datos

---

## Ejecución

### Servidor
```bash
python servidor.py
```

Escucha en: `localhost:5000`

### Cliente
```bash
python cliente.py
```

---

## Uso

- Enviar mensajes desde el cliente
- Escribir `éxito` para salir
- Respuesta del servidor:

`Mensaje recibido: <timestamp>`

---

## Base de Datos

Tabla `mensajes`:
- id
- contenido
- fecha_envio
- ip_cliente

---

## Funcionalidades

- Servidor TCP en localhost:5000
- Manejo concurrente de múltiples clientes (threading)
- Persistencia en SQLite
- Manejo de errores (socket y DB)
- Respuesta automática al cliente

---

## Pruebas

1. Ejecutar servidor
2. Abrir varios clientes
3. Enviar mensajes simultáneamente
4. Verificar respuestas y DB

---

## Capturas

![Capturas](https://romanrios.github.io/IFTS-programacion-sobre-redes/pfo_01/capturas/capturas_pfo1.jpg)


---

Instituto de Formación Técnica Superior N° 29  

Tecnicatura Superior en Desarrollo de Software  

Año 2026
