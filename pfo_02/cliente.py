import requests

# URL base del servidor Flask
URL = "http://127.0.0.1:5000"


# -------------------------------
# Registro de usuario
# -------------------------------
def registrar():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    # Enviar datos al endpoint /registro
    res = requests.post(f"{URL}/registro", json={
        "usuario": usuario,
        "contraseña": contraseña
    })

    print("Respuesta:", res.json())


# -------------------------------
# Login de usuario
# -------------------------------
def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    # Enviar datos al endpoint /login
    res = requests.post(f"{URL}/login", json={
        "usuario": usuario,
        "contraseña": contraseña
    })

    print("Respuesta:", res.json())


# -------------------------------
# Menú principal
# -------------------------------
def menu():
    while True:
        print("\n--- CLIENTE API ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    # Cliente en consola que interactúa con la API Flask
    menu()