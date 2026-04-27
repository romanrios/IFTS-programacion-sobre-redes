import argparse
import json
import queue
import socket
import threading
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


CLIENT_HOST = "0.0.0.0"
CLIENT_PORT = 5000
WORKER_HOST = "0.0.0.0"
WORKER_PORT = 6000
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


@dataclass
class WorkerConnection:
    name: str
    sock: socket.socket
    lock: threading.Lock = field(default_factory=threading.Lock)
    buffer: bytearray = field(default_factory=bytearray)
    active_tasks: int = 0


class TaskDispatcher:
    def __init__(self) -> None:
        self.workers: List[WorkerConnection] = []
        self.workers_lock = threading.Lock()
        self.pending: Dict[str, queue.Queue] = {}
        self.pending_lock = threading.Lock()
        self.round_robin = 0

    def register_worker(self, worker: WorkerConnection) -> None:
        with self.workers_lock:
            self.workers.append(worker)
            print(f"[SERVER] Worker registrado: {worker.name}")

    def remove_worker(self, worker: WorkerConnection) -> None:
        with self.workers_lock:
            self.workers = [w for w in self.workers if w.sock.fileno() != worker.sock.fileno()]
            print(f"[SERVER] Worker desconectado: {worker.name}")

    def choose_worker(self) -> WorkerConnection:
        with self.workers_lock:
            if not self.workers:
                raise RuntimeError("No hay workers disponibles")
            worker = self.workers[self.round_robin % len(self.workers)]
            self.round_robin += 1
            return worker

    def set_pending(self, task_id: str, response_queue: queue.Queue) -> None:
        with self.pending_lock:
            self.pending[task_id] = response_queue

    def pop_pending(self, task_id: str) -> Optional[queue.Queue]:
        with self.pending_lock:
            return self.pending.pop(task_id, None)

    def worker_reader(self, worker: WorkerConnection) -> None:
        try:
            while True:
                response = recv_line(worker.sock, worker.buffer)
                if response is None:
                    break

                task_id = response.get("task_id")
                if not task_id:
                    continue

                response_queue = self.pop_pending(task_id)
                if response_queue is not None:
                    response_queue.put(response)
        except Exception as exc:
            print(f"[SERVER] Error leyendo de {worker.name}: {exc}")
        finally:
            self.remove_worker(worker)
            try:
                worker.sock.close()
            except OSError:
                pass

    def dispatch_task(self, task: dict) -> dict:
        worker = self.choose_worker()
        task_id = task["task_id"]
        response_queue: queue.Queue = queue.Queue(maxsize=1)
        self.set_pending(task_id, response_queue)

        envelope = {
            "task_id": task_id,
            "operation": task["operation"],
            "value": task["value"],
        }

        try:
            send_json(worker.sock, envelope, worker.lock)
        except OSError as exc:
            self.pop_pending(task_id)
            raise RuntimeError(f"No se pudo enviar la tarea al worker {worker.name}: {exc}") from exc

        try:
            response = response_queue.get(timeout=30)
            return response
        except queue.Empty as exc:
            self.pop_pending(task_id)
            raise TimeoutError(f"Timeout esperando respuesta del worker {worker.name}") from exc


def handle_client(client_sock: socket.socket, dispatcher: TaskDispatcher) -> None:
    buffer = bytearray()
    try:
        request = recv_line(client_sock, buffer)
        if request is None:
            return

        required = {"operation", "value"}
        if not required.issubset(request):
            send_json(client_sock, {
                "ok": False,
                "error": "Formato inválido. Debe incluir operation y value."
            })
            return

        task = {
            "task_id": request.get("task_id") or str(uuid.uuid4()),
            "operation": request["operation"],
            "value": request["value"],
        }

        try:
            result = dispatcher.dispatch_task(task)
            send_json(client_sock, result)
        except Exception as exc:
            send_json(client_sock, {
                "task_id": task["task_id"],
                "ok": False,
                "error": str(exc),
            })

    except json.JSONDecodeError:
        send_json(client_sock, {"ok": False, "error": "JSON inválido"})
    except Exception as exc:
        print(f"[SERVER] Error atendiendo cliente: {exc}")
    finally:
        try:
            client_sock.close()
        except OSError:
            pass


def client_listener(dispatcher: TaskDispatcher) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((CLIENT_HOST, CLIENT_PORT))
    server.listen()
    print(f"[SERVER] Escuchando clientes en {CLIENT_HOST}:{CLIENT_PORT}")

    while True:
        client_sock, addr = server.accept()
        print(f"[SERVER] Cliente conectado desde {addr}")
        threading.Thread(target=handle_client, args=(client_sock, dispatcher), daemon=True).start()


def worker_listener(dispatcher: TaskDispatcher) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((WORKER_HOST, WORKER_PORT))
    server.listen()
    print(f"[SERVER] Escuchando workers en {WORKER_HOST}:{WORKER_PORT}")

    while True:
        worker_sock, addr = server.accept()
        buffer = bytearray()

        try:
            hello = recv_line(worker_sock, buffer)
            if hello is None or hello.get("type") != "register":
                worker_sock.close()
                continue

            name = hello.get("name", f"worker-{addr[1]}")
            worker = WorkerConnection(name=name, sock=worker_sock)
            dispatcher.register_worker(worker)
            threading.Thread(target=dispatcher.worker_reader, args=(worker,), daemon=True).start()

            send_json(worker_sock, {"type": "registered", "message": f"OK {name}"})
            print(f"[SERVER] Worker {name} listo")

        except Exception as exc:
            print(f"[SERVER] Error registrando worker desde {addr}: {exc}")
            try:
                worker_sock.close()
            except OSError:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de tareas por socket")
    _ = parser.parse_args()

    dispatcher = TaskDispatcher()

    threading.Thread(target=worker_listener, args=(dispatcher,), daemon=True).start()
    client_listener(dispatcher)


if __name__ == "__main__":
    main()
