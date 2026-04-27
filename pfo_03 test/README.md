# Arquitectura distribuida con sockets

## 1) Diagrama del sistema

```mermaid
flowchart LR
    subgraph Clients[Clientes]
        M[Móvil]
        W[Web]
    end

    subgraph LB[Balanceador de carga]
        N[Nginx / HAProxy]
    end

    subgraph App[Servidores de aplicación]
        S1[Servidor A]
        S2[Servidor B]
        S3[Servidor C]
    end

    subgraph Workers[Workers]
        WK1[Worker 1\nPool de hilos]
        WK2[Worker 2\nPool de hilos]
        WK3[Worker 3\nPool de hilos]
    end

    subgraph MQ[Mensajería]
        R[RabbitMQ]
    end

    subgraph Data[Persistencia]
        P[(PostgreSQL)]
        S[(S3)]
    end

    M --> N
    W --> N
    N --> S1
    N --> S2
    N --> S3

    S1 <--> R
    S2 <--> R
    S3 <--> R

    S1 --> WK1
    S1 --> WK2
    S2 --> WK2
    S2 --> WK3
    S3 --> WK1
    S3 --> WK3

    S1 --> P
    S2 --> P
    S3 --> P

    S1 --> S
    S2 --> S
    S3 --> S
```

### Qué representa
- **Clientes**: entran por HTTP/WebSocket o por socket según el caso.
- **Balanceador**: reparte peticiones entre varios servidores de aplicación.
- **Servidores**: reciben tareas, las enrutan y coordinan el trabajo.
- **RabbitMQ**: desacopla servidores y workers cuando se necesita comunicación asíncrona.
- **Workers**: ejecutan las tareas usando un **pool de hilos**.
- **PostgreSQL / S3**: guardan datos estructurados y archivos.

## 2) Ejecución del ejemplo

Este ejemplo implementa:
- un **servidor TCP** que recibe tareas por socket,
- un **worker TCP** que procesa tareas,
- un **cliente TCP** que envía tareas y recibe resultados.

### Levantar el sistema
1. Abrir una terminal y ejecutar el servidor:
   ```bash
   python server.py
   ```

2. Abrir una o más terminales y ejecutar workers:
   ```bash
   python worker.py --name worker-1
   python worker.py --name worker-2
   ```

3. En otra terminal, enviar una tarea:
   ```bash
   python client.py --operation factorial --value 5
   ```

## 3) Formato del mensaje

El protocolo usa JSON sobre TCP con una línea por mensaje.

Ejemplo de tarea:
```json
{
  "task_id": "uuid",
  "operation": "factorial",
  "value": 5
}
```

Ejemplo de respuesta:
```json
{
  "task_id": "uuid",
  "ok": true,
  "worker": "worker-1",
  "result": 120
}
```

## 4) Para subir a GitHub

Estructura sugerida del repositorio:

```text
arquitectura-distribuida-sockets/
├── README.md
├── server.py
├── worker.py
├── client.py
└── requirements.txt
```

## 5) Nota importante para tu entrega

La parte de **RabbitMQ, PostgreSQL y S3** está reflejada en el diseño de arquitectura.
El código incluido resuelve la parte pedida de **socket server + distribución a workers + cliente**.
