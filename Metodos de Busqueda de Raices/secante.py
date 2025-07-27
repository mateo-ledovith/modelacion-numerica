from typing import Callable
import math

def buscar_raiz_secante(tolerancia: float, maximas_iteraciones: int, cifras_significativas: int, criterio_paro: int,
                        f: Callable[[float], float], x0: float, x1: float) -> float:
    """
    Encuentra una raíz de la función `f` usando el método de la secante.

    Parámetros:
    - tolerancia (float): Criterio de parada basado en la tolerancia (default 1e-5).
    - max_iter (int): Número máximo de iteraciones (default 1000).
    - criterio_paro (int): 
        1 → |x_n+1 - x_n| < tolerancia (Diferencia entre iteraciones).
        2 → |f(x_n+1) - f(x_n)| / |f(x_n+1)| < tolerancia (Diferencia relativa entre iteraciones).
        3 → |f(x_n+1)| < tolerancia (Evaluación de la función en la raíz).
    - f (Callable[[float], float]): La función cuya raíz se busca.
    - x0 (float): Primera estimación inicial.
    - x1 (float): Segunda estimación inicial.
    - cifras_significativas (int): Cantidad de cifras significativas para redondear el resultado (default 6).

    Retorna:
    - float: La raíz aproximada de la función.
    - None: Si no converge después del número máximo de iteraciones.
    """
    for _ in range(maximas_iteraciones):
        # Evitamos división por cero
        if f(x1) - f(x0) == 0:
            raise ValueError("División por cero detectada en el método de la secante.")
        
        # Aplicamos la fórmula de la secante
        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))

        # Verificamos criterio de parada
        if criterio_paro == 1 and abs(x2 - x1) < tolerancia:
            return round(x2, cifras_significativas)

        if criterio_paro == 2 and abs(f(x2) - f(x1)) / max(abs(f(x2)), 1e-10) < tolerancia:
            return round(x2, cifras_significativas)

        if criterio_paro == 3 and abs(f(x2)) < tolerancia:
            return round(x2, cifras_significativas)

        # Actualizamos valores
        x0, x1 = x1, x2

    raise ValueError(f"El método de la secante no converge después de {maximas_iteraciones} iteraciones.")

def estimar_iteraciones_secante(tolerancia: float, f: Callable[[float], float],
                                 x0: float, x1: float) -> int:
    """
    Estima el número de iteraciones necesarias para que el método de la secante alcance la tolerancia deseada.

    Parámetros:
    - tolerancia (float): La tolerancia para la aproximación de la raíz (default 1e-5).
    - f (Callable[[float], float]): La función cuya raíz se busca.
    - x0 (float): Primera estimación inicial.
    - x1 (float): Segunda estimación inicial.

    Retorna:
    - int: Número estimado de iteraciones necesarias.
    - None: Si el método no converge.
    """
    
    for i in range(1, 1000):
        # Evitamos división por cero
        if f(x1) - f(x0) == 0:
            raise ValueError("División por cero detectada en el método de la secante.")
        
        # Aplicamos la fórmula de la secante
        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))

        # Verificamos el criterio de paro (criterio de diferencia entre iteraciones)
        if abs(x2 - x1) < tolerancia:
            return i

        # Actualizamos valores
        x0, x1 = x1, x2

    raise ValueError("No se alcanzó la convergencia en la estimación de iteraciones para la secante.")
