import socket
import threading

HOST = "localhost"
PORT = 1234

# Diccionario con respuestas (normalizadas en minúsculas)
respuestas = {
    "capital de francia": "París",
    "cuantos lados tiene un cuadrado": "4",
    "que lenguaje usamos": "Python",
}

def manejar_cliente(conn, addr):
    print(f"Conectado: {addr}")
    
    try:
        # Mejora: mensaje de bienvenida al cliente
        conn.sendall("Bienvenido. Escribí 'salir' para terminar.\n".encode())

        while True:
            # Mejora: normalización del texto para evitar coincidencias exactas
            data = conn.recv(1024).decode().strip().lower()

            if not data:
                break

            # Mejora: comando de salida controlado
            if data == "salir":
                conn.sendall("Conexión cerrada.\n".encode())
                break

            print(f"[{addr}] {data}")

            respuesta = respuestas.get(data, "No sé la respuesta")
            conn.sendall((respuesta + "\n").encode())

    except Exception as e:
        # Mejora: manejo de errores para evitar caídas del servidor
        print(f"Error con {addr}:", e)
    
    finally:
        conn.close()
        print(f"Desconectado: {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        # Mejora: threading para múltiples clientes simultáneos
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()