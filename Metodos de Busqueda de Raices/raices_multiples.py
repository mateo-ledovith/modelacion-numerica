import math
from typing import Callable

def buscar_raiz_raices_multiples(tolerancia: float, maximas_iteraciones: int, cifras_significativas: int, criterio_paro: int,
                                 f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:
    """
    Encuentra una raíz de una función usando el método de raíces múltiples sin conocer la multiplicidad.

    Parámetros:
    - f (Callable): Función cuya raíz queremos encontrar.
    - df (Callable): Derivada de f(x).
    - ddf (Callable): Segunda derivada de f(x).
    - x0 (float): Aproximación inicial.
    - tolerancia (float): Criterio de parada para el error (default 1e-5).
    - maximas_iteraciones (int): Número máximo de iteraciones (default 1000).
    - criterio_paro (int): Tipo de criterio de parada:
        - 1: |x_n - x_{n-1}| < tolerancia
        - 2: |x_n - x_{n-1}| / |x_n| < tolerancia
    - cifras_significativas (int): Número de cifras significativas para redondear la raíz (default 6).

    Retorna:
    - float: La raíz aproximada encontrada con el número de cifras significativas dado.
    """

    for _ in range(maximas_iteraciones):
        fx = f(x0)
        dfx = df(x0)
        ddfx = ddf(x0)

        if dfx == 0:  # Evita división por cero
            raise ValueError("La derivada se anuló. El método no puede continuar.")

        # Fórmula del método de raíces múltiples (asumiendo m = 1)
        x1 = x0 - (fx * dfx) / (dfx**2 - fx * ddfx)

        # Criterios de parada
        if criterio_paro == 1 and abs(x1 - x0) < tolerancia:
            return round(x1, cifras_significativas)
        if criterio_paro == 2 and abs(x1 - x0) / abs(x1) < tolerancia:
            return round(x1, cifras_significativas)

        x0 = x1  # Actualizamos la iteración

    return round(x1, cifras_significativas)  # Retorno si se alcanza el máximo de iteraciones

def estimar_iteraciones_raices_multiples(tolerancia: float, 
                                        f: Callable[[float], float], 
                                        df: Callable[[float], float], 
                                        ddf: Callable[[float], float], 
                                        x0: float) -> int:
    """
    Estima el número de iteraciones necesarias para alcanzar una tolerancia dada con el método de raíces múltiples.

    Parámetros:
    - f (Callable): Función cuya raíz queremos encontrar.
    - df (Callable): Primera derivada de f(x).
    - ddf (Callable): Segunda derivada de f(x).
    - x0 (float): Aproximación inicial.
    - tolerancia (float): Tolerancia deseada para el error (default 1e-5).

    Retorna:
    - int: Número estimado de iteraciones necesarias.
    """

    # Aproximación inicial de la convergencia usando el método de raíces múltiples
    fx = f(x0)
    dfx = df(x0)
    ddfx = ddf(x0)

    if dfx == 0:
        raise ValueError("La derivada se anuló en x0. No se puede estimar el número de iteraciones.")

    # Orden de convergencia (al ser un método cuasi-cuadrático, asumimos r ≈ 2)
    r = 2  

    # Estimación de la constante de error
    if abs(dfx**2 - fx * ddfx) < 1e-12:  # Evita divisiones por casi 0
        raise ValueError("El denominador se aproxima a cero, lo que impide la estimación correcta.")

    C = abs((fx * dfx) / (dfx**2 - fx * ddfx))

    # Fórmula de estimación de iteraciones: n = log(tolerancia / C) / log(r)
    n = math.log(tolerancia / C) / math.log(r)

    return math.ceil(n)  # Redondeamos hacia arriba, al menos 1 iteración.
