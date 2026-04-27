import argparse
import json
import socket
import uuid
from typing import Optional


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 4096


def send_json(sock: socket.socket, payload: dict) -> None:
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
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


def parse_value(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente TCP")
    parser.add_argument("--host", default=SERVER_HOST, help="Host del servidor")
    parser.add_argument("--port", type=int, default=SERVER_PORT, help="Puerto del servidor")
    parser.add_argument("--operation", required=True, help="Operación a ejecutar")
    parser.add_argument("--value", required=True, help="Valor de entrada. Puede ser JSON, por ejemplo '[1,2,3]'")
    args = parser.parse_args()

    task = {
        "task_id": str(uuid.uuid4()),
        "operation": args.operation,
        "value": parse_value(args.value),
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    try:
        send_json(sock, task)
        buffer = bytearray()
        response = recv_line(sock, buffer)
        print(json.dumps(response, indent=2, ensure_ascii=False))
    finally:
        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
