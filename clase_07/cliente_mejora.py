import socket
import json

def send_request(action, note=None, index=None):
    """Envía una solicitud al servidor."""
    try:
        request_data = {"action": action}
        if note:
            request_data["note"] = note
        if index is not None:
            request_data["index"] = index

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5000))

        client_socket.send(json.dumps(request_data).encode())

        response = client_socket.recv(1024).decode()
        client_socket.close()

        return json.loads(response)

    except Exception as e:
        # Mejora: manejo de errores en cliente
        return {"status": "error", "message": str(e)}


def main():
    while True:
        print("\n1. Ver notas\n2. Agregar nota\n3. Eliminar nota\n4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            response = send_request("GET")
            print("Notas:", response.get("notes", []))

        elif choice == "2":
            note = input("Ingrese la nota: ")
            response = send_request("POST", note=note)
            print(response["message"])

        elif choice == "3":
            try:
                index = int(input("Índice de la nota a eliminar: "))
                response = send_request("DELETE", index=index)
                print(response["message"])
            except ValueError:
                # Mejora: validación de entrada
                print("Índice inválido.")

        elif choice == "4":
            break


if __name__ == "__main__":
    main()