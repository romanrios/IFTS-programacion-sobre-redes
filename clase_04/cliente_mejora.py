import socket

HOST = "localhost"
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print("Conectado al servidor")

        # Mejora: recepción de mensaje de bienvenida
        print(s.recv(1024).decode())

        while True:
            # Mejora: interacción continua con el usuario
            mensaje = input("Pregunta: ")

            s.sendall(mensaje.encode())

            # Mejora: salida controlada desde el cliente
            if mensaje.lower() == "salir":
                print("Cerrando conexión...")
                break

            respuesta = s.recv(1024).decode()
            print("Servidor:", respuesta)

    except Exception as e:
        # Mejora: manejo de errores del cliente
        print("Error:", e)