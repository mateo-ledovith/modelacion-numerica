import math
from typing import Callable

def buscar_raiz_punto_fijo(tolerancia: float, maximas_iteraciones: int, cifras_significativas: int, 
                            criterio_paro: int, funcion: Callable[[float], float], x0: float) -> float:
    """
    Encuentra la raíz de una función utilizando el método del punto fijo.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz (default 10^-5).
    - maximas_iteraciones (int): El número máximo de iteraciones (default 100,000).
    - cifras_significativas (int): Número de cifras significativas para redondear la raíz (default 6).
    - criterio_paro (int): Criterio de parada (1, 2 o 3):
        1 -> abs(Pn - Pn-1) < E
        2 -> abs(Pn - Pn-1) / abs(Pn) < E
        3 -> abs(f(Pn)) < E
    - funcion (Callable): La función f(x) de la cual la raíz es buscada.
    - x0 (float): La aproximación inicial.

    Retorna:
    - float: La raíz aproximada si el método converge.
    - None: Si la función no cumple con la condición de convergencia.
    """
    
    def g(x: float) -> float:
        """Función auxiliar g(x) = x + f(x)."""
        return funcion(x) + x

    def g_derivada_aprox(x: float, h: float = 1e-5) -> float:
        """Aproxima la derivada de g(x) usando diferencias finitas."""
        return (g(x + h) - g(x)) / h

    # Verificamos que |g'(x)| < 1 cerca de x0
    if abs(g_derivada_aprox(x0)) >= 1:
        raise ValueError("La función no cumple la condición de convergencia del método de punto fijo.")

    for _ in range(maximas_iteraciones):
        x1 = g(x0)  # Iteración del método del punto fijo

        if criterio_paro == 1:  # Criterio de error absoluto
            if abs(x1 - x0) < tolerancia:
                return round(x1, cifras_significativas)
        elif criterio_paro == 2:  # Criterio de error relativo (evita división por cero)
            if abs(x1 - x0) / max(abs(x1), 1e-10) < tolerancia:
                return round(x1, cifras_significativas)
        elif criterio_paro == 3:  # Criterio de error en la función
            if abs(funcion(x1)) < tolerancia:
                return round(x1, cifras_significativas)

        x0 = x1  # Actualizamos el valor de x0

    return round(x1, cifras_significativas)  # Retorno si no se alcanza el criterio de paro

def estimar_iteraciones_punto_fijo(tolerancia: float, funcion: Callable[[float], float], x0: float) -> int:
    """
    Estima el número de iteraciones necesarias para que el método del punto fijo alcance la tolerancia deseada.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz (default 10^-5).
    - funcion (Callable): La función f(x) cuya raíz queremos encontrar.
    - x0 (float): La aproximación inicial.

    Retorna:
    - int: El número de iteraciones necesarias.
    """
    
    def g(x: float) -> float:
        """Función auxiliar g(x) = x + f(x)."""
        return funcion(x) + x
    
    # Calculamos x1 = g(x0) para estimar la convergencia
    x1 = g(x0)
    
    def g_derivada_aprox(x: float, h: float = 1e-5) -> float:
        """Aproxima la derivada de g(x) usando diferencias finitas."""
        return (g(x + h) - g(x)) / h

    g_derivada = g_derivada_aprox(x0)
    
    # Verificamos que |g'(x)| < 1 cerca de x0
    if abs(g_derivada) >= 1:
        raise ValueError("La función no cumple la condición de convergencia del método de punto fijo.")
    
    # Fórmula para calcular las iteraciones necesarias
    n = math.log((tolerancia * (1 - g_derivada)) / abs(g(x0) - x0)) / math.log(g_derivada)

    return math.ceil(n)
