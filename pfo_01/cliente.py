import socket

def iniciar_cliente():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("localhost", 5000))

        print("Conectado al servidor.")

        while True:
            mensaje = input("Escribí un mensaje ('éxito' para salir): ")

            if mensaje.lower() == "éxito":
                print("Cerrando conexión...")
                break

            cliente.send(mensaje.encode())

            respuesta = cliente.recv(1024).decode()
            print("Servidor:", respuesta)

        cliente.close()

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    iniciar_cliente()