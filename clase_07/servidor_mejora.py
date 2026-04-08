import socket
import json
import threading
import sqlite3

# -------------------------------
# Inicializar base de datos
# -------------------------------
def init_db():
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------------------
# Procesar requests
# -------------------------------
def handle_request(request):
    try:
        data = json.loads(request)
        action = data.get("action")

        conn = sqlite3.connect("notas.db")
        cursor = conn.cursor()

        if action == "GET":
            cursor.execute("SELECT contenido FROM notas")
            notas = [row[0] for row in cursor.fetchall()]
            return json.dumps({"status": "success", "notes": notas})

        elif action == "POST":
            note = data.get("note")
            if not note:
                return json.dumps({"status": "error", "message": "Nota vacía"})
            
            cursor.execute("INSERT INTO notas (contenido) VALUES (?)", (note,))
            conn.commit()
            return json.dumps({"status": "success", "message": "Nota agregada."})

        elif action == "DELETE":
            index = data.get("index")

            # Mejora: validación de índice
            cursor.execute("SELECT id FROM notas")
            ids = [row[0] for row in cursor.fetchall()]

            if isinstance(index, int) and 0 <= index < len(ids):
                cursor.execute("DELETE FROM notas WHERE id = ?", (ids[index],))
                conn.commit()
                return json.dumps({"status": "success", "message": "Nota eliminada."})
            else:
                return json.dumps({"status": "error", "message": "Índice inválido."})

        else:
            return json.dumps({"status": "error", "message": "Acción no válida."})

    except Exception as e:
        # Mejora: manejo de errores
        return json.dumps({"status": "error", "message": str(e)})

    finally:
        conn.close()


# -------------------------------
# Manejar cliente
# -------------------------------
def manejar_cliente(client_socket, addr):
    print(f"Conectado: {addr}")
    
    try:
        request = client_socket.recv(1024).decode()
        response = handle_request(request)
        client_socket.send(response.encode())
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()
        print(f"Desconectado: {addr}")


# -------------------------------
# Servidor principal
# -------------------------------
def start_server():
    init_db()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    print("Servidor escuchando en puerto 5000...")

    while True:
        client_socket, addr = server_socket.accept()
        # Mejora: threading para múltiples clientes
        threading.Thread(target=manejar_cliente, args=(client_socket, addr)).start()


if __name__ == "__main__":
    start_server()