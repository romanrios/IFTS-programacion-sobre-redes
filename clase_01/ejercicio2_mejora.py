import threading

def sumar_numeros(nombre, rango, condicion, resultados):
    """
    Función que calcula la suma de un rango de números.

    Mejoras:
    - Eliminación de variables globales:
        * 'condicion' y 'resultados' se pasan como parámetros.
        * Esto hace el código más modular, testeable y seguro en concurrencia.

    - Uso de sum(range()):
        * Se reemplaza el bucle manual por una solución más eficiente.
    """
    total = sum(rango)

    # Sección crítica protegida por la condición
    with condicion:
        resultados.append(f"{nombre} sumó: {total}")
        condicion.notify_all()  # Notifica que un hilo terminó


def imprimir_resultados(condicion, resultados, total_hilos):
    """
    Espera hasta que todos los hilos hayan terminado y luego imprime resultados.

    Mejoras:
    - Uso de wait_for():
        * Reemplaza el while + wait().
        * Más limpio y evita errores.
    """
    with condicion:
        condicion.wait_for(lambda: len(resultados) == total_hilos)

        for resultado in resultados:
            print(resultado)


# ==============================
# Configuración centralizada
# ==============================
# Define dinámicamente los hilos a crear
CONFIG_HILOS = [
    {"nombre": "Hilo 1", "rango": range(1, 6)},
    {"nombre": "Hilo 2", "rango": range(1, 6)},
]


# ==============================
# Recursos compartidos (ya no globales)
# ==============================
condicion = threading.Condition()
resultados = []

hilos = []


# ==============================
# Generación dinámica de hilos
# ==============================
# Se crean los hilos a partir de la configuración
for config in CONFIG_HILOS:
    hilo = threading.Thread(
        target=sumar_numeros,
        args=(config["nombre"], config["rango"], condicion, resultados)
    )
    hilos.append(hilo)
    hilo.start()


# ==============================
# Espera e impresión sincronizada
# ==============================
# Se pasa también la cantidad de hilos esperados
imprimir_resultados(condicion, resultados, total_hilos=len(CONFIG_HILOS))


# ==============================
# Join dinámico (buena práctica adicional)
# ==============================
# Asegura que todos los hilos realmente finalicen antes de terminar el programa
for hilo in hilos:
    hilo.join()