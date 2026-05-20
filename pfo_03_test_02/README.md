# PFO 3 - Sistema Distribuido de Gestión de Tareas

## Descripción

Rediseño distribuido del sistema de gestión de tareas del PFO 2 utilizando sockets TCP.

La arquitectura implementa:

- Cliente TCP
- Servidor principal
- Balanceo Round Robin
- Workers concurrentes
- Pool de hilos
- Persistencia SQLite
- Arquitectura distribuida

---

# Arquitectura

```mermaid
graph TD

    A[Clientes Web / Mobile / Desktop]

    B[Nginx / HAProxy]

    C[Servidor Principal TCP]

    D1[Worker 1 - Pool de Hilos]
    D2[Worker 2 - Pool de Hilos]
    D3[Worker N - Pool de Hilos]

    E[RabbitMQ]

    F[(PostgreSQL)]
    G[(Amazon S3)]

    A --> B

    B --> C

    C --> D1
    C --> D2
    C --> D3

    D1 --> E
    D2 --> E
    D3 --> E

    E --> F
    E --> G
```

---

# Estructura

```text
pfo_03/
│
├── client.py
├── server.py
├── worker.py
├── database.py
├── init_db.py
├── requirements.txt
└── README.md
```

---

# Ejecución

## 1. Inicializar base de datos

```bash
python init_db.py
```

---

## 2. Iniciar servidor principal

```bash
python server.py
```

---

## 3. Iniciar workers

```bash
python worker.py --name worker-1
```

```bash
python worker.py --name worker-2
```

---

## 4. Ejecutar cliente

```bash
python client.py
```

---

# Funcionalidades

- Registro de usuarios
- Login
- Crear tareas
- Ver tareas
- Eliminar tareas
- Distribución de requests
- Workers concurrentes
- Sistema multicliente
- Arquitectura distribuida

---

# Tecnologías

- Python 3
- socket
- threading
- concurrent.futures
- sqlite3
- json

---

# Autor

Román Ríos