import socket
import json

# Almacenamiento de notas (simulado en memoria)
notes = []

def handle_request(request):
    """Procesa las solicitudes del cliente."""
    global notes
    try:
        data = json.loads(request)
        action = data.get("action")
        
        if action == "GET":
            return json.dumps({"status": "success", "notes": notes})
        
        elif action == "POST":
            new_note = data.get("note")
            notes.append(new_note)
            return json.dumps({"status": "success", "message": "Nota agregada."})
        
        elif action == "DELETE":
            note_index = data.get("index")
            if 0 <= note_index < len(notes):
                deleted_note = notes.pop(note_index)
                return json.dumps({"status": "success", "message": f"Nota '{deleted_note}' eliminada."})
            else:
                return json.dumps({"status": "error", "message": "Índice inválido."})
        
        else:
            return json.dumps({"status": "error", "message": "Acción no válida."})
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def start_server():
    """Inicia el servidor en localhost:5000."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen(1)
    print("Servidor escuchando en puerto 5000...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión aceptada desde {addr}")
        
        request = client_socket.recv(1024).decode()
        response = handle_request(request)
        client_socket.send(response.encode())
        
        client_socket.close()

if __name__ == "__main__":
    start_server()