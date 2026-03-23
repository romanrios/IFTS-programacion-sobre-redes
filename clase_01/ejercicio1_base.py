import threading
import time

def contar_numeros(nombre, inicio):
    for i in range(5):
        time.sleep(1)  # Simula un trabajo que toma tiempo (1 segundo por número)
        print(f"{nombre} está contando: {inicio + i}")

hilo1 = threading.Thread(target=contar_numeros, args=("Hilo 1", 1))
hilo2 = threading.Thread(target=contar_numeros, args=("Hilo 2", 6))

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("¡Contador completo!")