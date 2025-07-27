import math
from typing import Callable

def buscar_raiz_newton_raphson(tolerancia: float, maximas_iteraciones: int, cifras_significativas: int, criterio_paro: int,
                                f: Callable[[float], float], df: Callable[[float], float], x0: float) -> float:
    """
    Encuentra la raíz de una función utilizando el método de Newton-Raphson con diferentes criterios de paro.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz (default 10^-5).
    - max_iter (int): Número máximo de iteraciones (default 100).
    - criterio_paro (int): Criterio de parada (1, 2 o 3):
        1 -> abs(Pn - Pn-1) < E
        2 -> abs(Pn - Pn-1) / abs(Pn) < E
        3 -> abs(f(Pn)) < E
    - f (Callable): La función f(x) cuya raíz queremos encontrar.
    - df (Callable): La derivada f'(x) de la función.
    - x0 (float): Aproximación inicial.

    Retorna:
    - float: La raíz aproximada de la función.
    - None: Si el método no converge después del número máximo de iteraciones.
    """
    
    for _ in range(maximas_iteraciones):
        fx = f(x0)
        dfx = df(x0)

        # Evitar división por cero en la derivada
        if dfx == 0:
            raise ValueError("La derivada se anuló. El método no puede continuar.")
        # Aplicar la fórmula de Newton-Raphson
        x1 = x0 - fx / dfx

        # Criterio de paro 1: abs(Pn - Pn-1) < E
        if criterio_paro == 1 and abs(x1 - x0) < tolerancia:
            return round(x1, cifras_significativas)

        # Criterio de paro 2: abs(Pn - Pn-1) / abs(Pn) < E
        if criterio_paro == 2 and abs(x1 - x0) / abs(x1) < tolerancia:
            return round(x1, cifras_significativas)

        # Criterio de paro 3: abs(f(Pn)) < E
        if criterio_paro == 3 and abs(fx) < tolerancia:
            return round(x1, cifras_significativas)

        x0 = x1  # Actualizamos x0 para la siguiente iteración

    raise ValueError(f"El método no converge después de {maximas_iteraciones} iteraciones.")

def estimar_iteraciones_newton_raphson(tolerancia: float, f: Callable[[float], float],
                                        df: Callable[[float], float], x0: float) -> int:
    """
    Calcula el número de iteraciones necesarias para que el método de Newton-Raphson alcance la tolerancia deseada.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz (default 10^-5).
    - f (Callable): La función f(x) cuya raíz queremos encontrar.
    - df (Callable): La derivada f'(x) de la función.
    - x0 (float): La aproximación inicial.

    Retorna:
    - int: El número de iteraciones necesarias.
    - None: Si el método no converge.
    """
    
    for i in range(1, 1000):
        fx = f(x0)
        dfx = df(x0)

        x1 = x0 - fx / dfx

        # Criterio de paro 1: abs(Pn - Pn-1) < E
        if abs(x1 - x0) < tolerancia:
            return i

        x0 = x1  # Actualizamos x0 para la siguiente iteración
    
    raise ValueError("No se alcanzó la convergencia en la estimación de iteraciones para Newton-Raphson.")
