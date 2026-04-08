import socket
import json

def send_request(action, note=None, index=None):
    """Envía una solicitud al servidor."""
    request_data = {"action": action}
    if note: request_data["note"] = note
    if index is not None: request_data["index"] = index
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5000))
    client_socket.send(json.dumps(request_data).encode())
    
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return json.loads(response)

def main():
    while True:
        print("\n1. Ver notas\n2. Agregar nota\n3. Eliminar nota\n4. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            response = send_request("GET")
            if response["status"] == "success":
                print("\nNotas:", response.get("notes", []))
            else:
                print("Error:", response["message"])
        
        elif choice == "2":
            note = input("Ingrese la nota: ")
            response = send_request("POST", note=note)
            print(response["message"])
        
        elif choice == "3":
            index = int(input("Índice de la nota a eliminar: "))
            response = send_request("DELETE", index=index)
            print(response["message"])
        
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
