import threading

# Variable de condición para sincronización
condicion = threading.Condition()

# Variables globales
resultados = []

def sumar_numeros(nombre):
    total = 0
    for i in range(1, 6):
        total += i
    with condicion:
        resultados.append(f"{nombre} sumó: {total}")
        condicion.notify_all()  # Notificar que se ha terminado la suma

def imprimir_resultados():
    with condicion:
        while len(resultados) < 2:
            condicion.wait()  # Esperar hasta que ambos hilos hayan terminado
        for resultado in resultados:
            print(resultado)

hilo1 = threading.Thread(target=sumar_numeros, args=("Hilo 1",))
hilo2 = threading.Thread(target=sumar_numeros, args=("Hilo 2",))

hilo1.start()
hilo2.start()

# Imprimir los resultados una vez que ambos hilos hayan terminado
imprimir_resultados()