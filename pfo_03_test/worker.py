import argparse
import concurrent.futures
import json
import math
import socket
import threading
from typing import Optional


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000
BUFFER_SIZE = 4096


def send_json(sock: socket.socket, payload: dict, lock: Optional[threading.Lock] = None) -> None:
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
    if lock:
        with lock:
            sock.sendall(data)
    else:
        sock.sendall(data)


def recv_line(sock: socket.socket, buffer: bytearray) -> Optional[dict]:
    while True:
        newline = buffer.find(b"\n")
        if newline != -1:
            raw = buffer[:newline]
            del buffer[: newline + 1]
            if not raw.strip():
                continue
            return json.loads(raw.decode("utf-8"))
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            return None
        buffer.extend(chunk)


def compute(operation: str, value):
    if operation == "add":
        if not isinstance(value, list):
            raise ValueError("Para 'add' se espera una lista de números")
        return sum(value)

    if operation == "multiply":
        if not isinstance(value, list):
            raise ValueError("Para 'multiply' se espera una lista de números")
        result = 1
        for n in value:
            result *= n
        return result

    if operation == "factorial":
        n = int(value)
        if n < 0:
            raise ValueError("factorial no admite negativos")
        return math.factorial(n)

    if operation == "fibonacci":
        n = int(value)
        if n < 0:
            raise ValueError("fibonacci no admite negativos")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    if operation == "reverse":
        return str(value)[::-1]

    if operation == "upper":
        return str(value).upper()

    if operation == "sort":
        if not isinstance(value, list):
            raise ValueError("Para 'sort' se espera una lista")
        return sorted(value)

    raise ValueError(f"Operación no soportada: {operation}")


def handle_task(task: dict, sock: socket.socket, send_lock: threading.Lock, worker_name: str, executor: concurrent.futures.ThreadPoolExecutor) -> None:
    task_id = task.get("task_id")
    operation = task.get("operation")
    value = task.get("value")

    try:
        result = compute(operation, value)
        response = {
            "task_id": task_id,
            "ok": True,
            "worker": worker_name,
            "operation": operation,
            "result": result,
        }
    except Exception as exc:
        response = {
            "task_id": task_id,
            "ok": False,
            "worker": worker_name,
            "error": str(exc),
        }

    send_json(sock, response, send_lock)


def main() -> None:
    parser = argparse.ArgumentParser(description="Worker TCP")
    parser.add_argument("--name", required=True, help="Nombre del worker")
    parser.add_argument("--host", default=SERVER_HOST, help="Host del servidor")
    parser.add_argument("--port", type=int, default=SERVER_PORT, help="Puerto del servidor")
    parser.add_argument("--threads", type=int, default=4, help="Tamaño del pool de hilos")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    send_lock = threading.Lock()
    send_json(sock, {"type": "register", "name": args.name}, send_lock)

    buffer = bytearray()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=args.threads)

    # Confirmación de registro
    ack = recv_line(sock, buffer)
    if ack is None or ack.get("type") != "registered":
        raise RuntimeError("El servidor no confirmó el registro del worker")

    print(f"[{args.name}] Conectado a {args.host}:{args.port} con pool de {args.threads} hilos")

    try:
        while True:
            task = recv_line(sock, buffer)
            if task is None:
                print(f"[{args.name}] El servidor cerró la conexión")
                break

            executor.submit(handle_task, task, sock, send_lock, args.name, executor)

    except KeyboardInterrupt:
        print(f"[{args.name}] Cerrando por teclado")
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
