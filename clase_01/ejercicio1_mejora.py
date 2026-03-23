import threading
import time

def contar_numeros(nombre, inicio, cantidad, delay=1):
    """
    Función que cuenta números de forma secuencial.

    Mejoras:
    - Parámetros flexibles:
        * 'cantidad' define cuántos números contar (ya no está hardcodeado).
        * 'delay' permite controlar el tiempo entre iteraciones.
    """
    for i in range(cantidad):
        time.sleep(delay)  # Simula trabajo
        print(f"{nombre} está contando: {inicio + i}")


# ==============================
# Configuración centralizada
# ==============================
# En lugar de crear los hilos manualmente uno por uno,
# definimos toda su configuración en una estructura de datos.
# Esto permite escalar fácilmente agregando o modificando entradas.
CONFIG_HILOS = [
    {"nombre": "Hilo 1", "inicio": 1, "cantidad": 5},
    {"nombre": "Hilo 2", "inicio": 6, "cantidad": 5},
    {"nombre": "Hilo 3", "inicio": 11, "cantidad": 3},
]


# Lista para almacenar los hilos creados
hilos = []


# ==============================
# Creación dinámica de hilos
# ==============================
# Se recorren las configuraciones y se crean los hilos automáticamente.
# Esto evita repetir código y permite manejar cualquier cantidad de hilos.
for config in CONFIG_HILOS:
    hilo = threading.Thread(
        target=contar_numeros,
        args=(config["nombre"], config["inicio"], config["cantidad"])
    )
    hilos.append(hilo)  # Guardamos referencia para luego hacer join()
    hilo.start()        # Iniciamos el hilo


# ==============================
# Join dinámico de hilos
# ==============================
# En lugar de llamar hilo1.join(), hilo2.join(), etc.,
# recorremos la lista y esperamos a que todos terminen.
# Esto hace el código escalable y más limpio.
for hilo in hilos:
    hilo.join()


print("¡Contador completo!")