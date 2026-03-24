import socket
import sqlite3
from datetime import datetime

# -------------------------------
# Configuración de la base de datos
# -------------------------------
def inicializar_db():
    try:
        conn = sqlite3.connect("mensajes.db")
        cursor = conn.cursor()

        # Crear tabla si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT,
            fecha_envio TEXT,
            ip_cliente TEXT
        )
        """)

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error al inicializar DB:", e)


# -------------------------------
# Guardar mensaje en la DB
# -------------------------------
def guardar_mensaje(contenido, ip):
    try:
        conn = sqlite3.connect("mensajes.db")
        cursor = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
        VALUES (?, ?, ?)
        """, (contenido, fecha, ip))

        conn.commit()
        conn.close()

        return fecha
    except Exception as e:
        print("Error al guardar mensaje:", e)
        return None


# -------------------------------
# Inicializar socket servidor
# -------------------------------
def inicializar_socket():
    try:
        # Configuración del socket TCP/IP
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", 5000))
        servidor.listen(5)

        print("Servidor escuchando en localhost:5000")
        return servidor
    except OSError:
        print("Error: el puerto 5000 ya está en uso.")
        return None


# -------------------------------
# Manejar conexiones
# -------------------------------
def manejar_conexiones(servidor):
    while True:
        try:
            cliente, direccion = servidor.accept()
            ip_cliente = direccion[0]

            print(f"Conexión desde {ip_cliente}")

            while True:
                mensaje = cliente.recv(1024).decode()

                if not mensaje:
                    break

                print(f"Mensaje recibido: {mensaje}")

                fecha = guardar_mensaje(mensaje, ip_cliente)

                if fecha:
                    respuesta = f"Mensaje recibido: {fecha}"
                else:
                    respuesta = "Error al guardar mensaje"

                cliente.send(respuesta.encode())

        except Exception as e:
            print("Error en conexión:", e)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()

    if servidor:
        manejar_conexiones(servidor)