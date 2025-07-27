import math
from typing import Callable

def buscar_raiz_biseccion(tolerancia: float, maximas_iteraciones: int, cifras_significativas: int, 
                           criterio_paro: int, funcion: Callable, a: float, b: float) -> float:
    """
    Encuentra la raíz de una función utilizando el método de la bisección.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz.
    - maximas_iteraciones (int): El número máximo de iteraciones, default 100,000.
    - cifras_significativas (int): El número de cifras significativas para redondear la raíz, default 6.
    - criterio_paro (int): Criterio de parada (1, 2 o 3):
        1 -> abs(Pn - Pn-1) < E
        2 -> abs(Pn - Pn-1) / abs(Pn) < E
        3 -> abs(f(Pn)) < E
    - funcion (Callable): La función para la cual encontrar la raíz.
    - a (float): El límite inferior del intervalo.
    - b (float): El límite superior del intervalo.

    Retorna:
    - float: La raíz aproximada de la función dentro de la tolerancia y cifras significativas dadas.
    """

    if funcion(a) * funcion(b) > 0:
        raise ValueError("La función no cambia de signo en el intervalo dado")

    p_anterior = a  # Inicializamos el valor anterior con 'a'

    for _ in range(maximas_iteraciones):
        p_actual = (a + b) / 2  # Punto medio

        if criterio_paro == 1 and abs(p_actual - p_anterior) < tolerancia:
            return round(p_actual, cifras_significativas)
        if criterio_paro == 2 and abs(p_actual - p_anterior) / max(abs(p_actual), 1e-10) < tolerancia:
            return round(p_actual, cifras_significativas)
        if criterio_paro == 3 and abs(funcion(p_actual)) < tolerancia:
            return round(p_actual, cifras_significativas)

        # Actualizamos los extremos del intervalo
        if funcion(a) * funcion(p_actual) < 0:
            b = p_actual
        else:
            a = p_actual

        p_anterior = p_actual  # Guardamos el valor actual como el anterior para la siguiente iteración

    return round((a + b) / 2, cifras_significativas)  # Retorno si se alcanza el máximo de iteraciones


def estimar_iteraciones_biseccion(tolerancia: float, a: float, b: float) -> int:
    """
    Estima el número de iteraciones necesarias para encontrar la raíz de una función utilizando el método de la bisección.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz, default 10^-5.
    - a (float): El límite inferior del intervalo.
    - b (float): El límite superior del intervalo.

    Retorna:
    - int: El número de iteraciones necesarias para encontrar la raíz de la función dentro de la tolerancia dada.
    """
    n = -((math.log(tolerancia / (b - a))) / (math.log(2)))
    return math.ceil(n)
