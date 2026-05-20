import json
import queue
import socket
import threading
import uuid
from dataclasses import dataclass

CLIENT_HOST = "0.0.0.0"
CLIENT_PORT = 5000

WORKER_HOST = "0.0.0.0"
WORKER_PORT = 6000

BUFFER_SIZE = 4096


# ----------------------------------
# Worker
# ----------------------------------
@dataclass
class Worker:
    name: str
    sock: socket.socket
    lock: threading.Lock
    buffer: bytearray


workers = []
workers_lock = threading.Lock()
round_robin = 0

pending_requests = {}
pending_lock = threading.Lock()


# ----------------------------------
# Utils
# ----------------------------------
def send_json(sock, payload, lock=None):
    data = (json.dumps(payload) + "\n").encode()

    if lock:
        with lock:
            sock.sendall(data)
    else:
        sock.sendall(data)



def recv_json(sock, buffer):
    while True:

        if b"\n" in buffer:
            raw, _, rest = buffer.partition(b"\n")
            buffer[:] = rest

            return json.loads(raw.decode())

        chunk = sock.recv(BUFFER_SIZE)

        if not chunk:
            return None

        buffer.extend(chunk)


# ----------------------------------
# Workers
# ----------------------------------
def register_worker(worker):
    with workers_lock:
        workers.append(worker)

        print(f"[SERVER] Worker registrado: {worker.name}")



def choose_worker():
    global round_robin

    with workers_lock:

        if not workers:
            raise RuntimeError("No hay workers disponibles")

        worker = workers[round_robin % len(workers)]

        round_robin += 1

        return worker



def worker_reader(worker):
    try:
        while True:
            response = recv_json(worker.sock, worker.buffer)

            if response is None:
                break

            request_id = response.get("request_id")

            with pending_lock:
                if request_id in pending_requests:
                    pending_requests[request_id].put(response)

    except Exception as e:
        print(e)



def worker_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((WORKER_HOST, WORKER_PORT))
    server.listen()

    print(f"[SERVER] Workers en {WORKER_HOST}:{WORKER_PORT}")

    while True:
        worker_sock, addr = server.accept()

        buffer = bytearray()

        hello = recv_json(worker_sock, buffer)

        worker = Worker(
            name=hello["name"],
            sock=worker_sock,
            lock=threading.Lock(),
            buffer=buffer
        )

        register_worker(worker)

        send_json(worker_sock, {
            "type": "registered"
        })

        threading.Thread(
            target=worker_reader,
            args=(worker,),
            daemon=True
        ).start()


# ----------------------------------
# Clientes
# ----------------------------------
def dispatch_request(payload):
    worker = choose_worker()

    response_queue = queue.Queue(maxsize=1)

    request_id = str(uuid.uuid4())

    payload["request_id"] = request_id

    with pending_lock:
        pending_requests[request_id] = response_queue

    send_json(worker.sock, payload, worker.lock)

    response = response_queue.get(timeout=30)

    with pending_lock:
        pending_requests.pop(request_id, None)

    return response



def handle_client(client_sock):
    buffer = bytearray()

    try:
        request = recv_json(client_sock, buffer)

        if request is None:
            return

        response = dispatch_request(request)

        send_json(client_sock, response)

    except Exception as e:
        send_json(client_sock, {
            "ok": False,
            "message": str(e)
        })

    finally:
        client_sock.close()



def client_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((CLIENT_HOST, CLIENT_PORT))
    server.listen()

    print(f"[SERVER] Clientes en {CLIENT_HOST}:{CLIENT_PORT}")

    while True:
        client_sock, addr = server.accept()

        print(f"[SERVER] Cliente conectado: {addr}")

        threading.Thread(
            target=handle_client,
            args=(client_sock,),
            daemon=True
        ).start()


# ----------------------------------
# Main
# ----------------------------------
threading.Thread(target=worker_listener, daemon=True).start()

client_listener()