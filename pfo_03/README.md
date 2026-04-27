# Programación sobre Redes - PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)

Ríos, Román | Comisión 3A

---

## Objetivos


Transformar el sistema en una arquitectura distribuida usando sockets.

Diseñar un diagrama que incluya:

- Clientes (móviles, web).
- Balanceador de carga (Nginx/HAProxy).
- Servidores workers (cada uno con su pool de hilos).
- Cola de mensajes (RabbitMQ) para comunicación entre servidores.
- Almacenamiento distribuido (PostgreSQL, S3).

Implementar en Python:

- Un servidor que reciba tareas por socket y las distribuya a workers.
- Un cliente que envíe tareas y reciba resultados.

Entregables:

- Diagrama del sistema.
- Código del servidor y cliente en repositorio de Github

---

Instituto de Formación Técnica Superior N° 29  

Tecnicatura Superior en Desarrollo de Software  

Año 2026
