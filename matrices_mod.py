"""
matrices_mod.py
---------------
Parte matemática de la calculadora de matrices 3x3 módulo n.

Todo se calcula con números enteros de Python (sin NumPy) para:
  1. Evitar errores de redondeo (NumPy trabaja con decimales).
  2. Mostrar el procedimiento real de la aritmética modular.

Funciones principales que usará la interfaz:
  - multiplicar(A, B, n)  ->  A·B mod n
  - inversa(A, n)         ->  A⁻¹ mod n (o error si no existe)
"""


# ---------------------------------------------------------------------------
# Validaciones y utilidades
# ---------------------------------------------------------------------------

def validar_modulo(n):
    """Verifica que el módulo sea un entero mayor o igual a 2.
    Módulo 0 no existe y módulo 1 haría que todo valga 0."""
    if not isinstance(n, int) or n < 2:
        raise ValueError("El módulo n debe ser un número entero mayor o igual a 2.")


def reducir_matriz(M, n):
    """Lleva cada elemento de la matriz al rango 0..n-1.
    En Python, el operador % ya convierte negativos correctamente:
    por ejemplo, -3 % 26 = 23."""
    return [[x % n for x in fila] for fila in M]


# ---------------------------------------------------------------------------
# Operación 1: multiplicación A·B mod n
# ---------------------------------------------------------------------------

def multiplicar(A, B, n):
    """Calcula C = A·B mod n.
    Cada elemento C[i][j] es la suma de multiplicar la fila i de A
    por la columna j de B, y al final se reduce módulo n."""
    validar_modulo(n)
    C = [[0, 0, 0] for _ in range(3)]
    for i in range(3):          # recorre las filas de A
        for j in range(3):      # recorre las columnas de B
            suma = 0
            for k in range(3):  # producto punto fila i · columna j
                suma += A[i][k] * B[k][j]
            C[i][j] = suma % n
    return C


# ---------------------------------------------------------------------------
# Herramientas para la inversa
# ---------------------------------------------------------------------------

def determinante(A):
    """Determinante de una matriz 3x3 por expansión de cofactores
    sobre la primera fila. Devuelve el entero SIN reducir módulo n."""
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def euclides_extendido(a, b):
    """Algoritmo de Euclides extendido.
    Devuelve (mcd, x, y) tales que:  a·x + b·y = mcd(a, b).
    Si mcd(a, n) = 1, entonces x es el inverso de a módulo n,
    porque a·x + n·y = 1  implica  a·x ≡ 1 (mod n)."""
    if b == 0:
        return a, 1, 0
    mcd, x1, y1 = euclides_extendido(b, a % b)
    # Se reconstruyen los coeficientes del paso anterior
    return mcd, y1, x1 - (a // b) * y1


def inverso_modular(a, n):
    """Inverso multiplicativo de a módulo n.
    Devuelve (inverso, mcd). Si a y n no son coprimos, inverso es None."""
    a = a % n
    mcd, x, _ = euclides_extendido(a, n)
    if mcd != 1:
        return None, mcd
    return x % n, mcd  # x puede salir negativo; % n lo deja en 0..n-1


def adjunta(A):
    """Matriz adjunta = transpuesta de la matriz de cofactores.
    Cofactor C[i][j] = (-1)^(i+j) · determinante del menor 2x2
    que queda al quitar la fila i y la columna j."""
    cofactores = [[0, 0, 0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            # Menor: la submatriz 2x2 sin la fila i ni la columna j
            menor = [[A[r][c] for c in range(3) if c != j]
                     for r in range(3) if r != i]
            det_menor = menor[0][0] * menor[1][1] - menor[0][1] * menor[1][0]
            signo = (-1) ** (i + j)
            cofactores[i][j] = signo * det_menor
    # Transponer: la fila i pasa a ser la columna i
    return [[cofactores[j][i] for j in range(3)] for i in range(3)]


# ---------------------------------------------------------------------------
# Operación 2: inversa A⁻¹ mod n
# ---------------------------------------------------------------------------

def inversa(A, n):
    """Calcula A⁻¹ mod n con la fórmula  A⁻¹ ≡ det(A)⁻¹ · adj(A) (mod n).
    Si mcd(det(A), n) ≠ 1, la inversa no existe y se lanza ValueError
    con un mensaje que explica por qué."""
    validar_modulo(n)

    # Paso 1: determinante reducido módulo n
    det = determinante(A) % n

    # Paso 2: condición de existencia (coprimos) e inverso del determinante
    det_inv, mcd = inverso_modular(det, n)
    if det_inv is None:
        raise ValueError(
            f"A no es invertible módulo {n}: det(A) ≡ {det} (mod {n}) "
            f"y mcd({det}, {n}) = {mcd}, no son coprimos."
        )

    # Paso 3: multiplicar la adjunta por el inverso del determinante, mod n
    adj = adjunta(A)
    return [[(det_inv * adj[i][j]) % n for j in range(3)] for i in range(3)]


# ---------------------------------------------------------------------------
# Pruebas rápidas: se ejecutan solo con  python matrices_mod.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    n = 26

    # Ejemplo invertible (clave clásica del cifrado de Hill)
    A = [[6, 24, 1],
         [13, 16, 10],
         [20, 17, 15]]
    A_inv = inversa(A, n)
    print("A⁻¹ mod 26 =", A_inv)
    print("A·A⁻¹ mod 26 =", multiplicar(A, A_inv, n), "(debe ser la identidad)")

    # Entrada con negativos y números mayores que n
    B = [[-1, 30, 0],
         [2, -27, 5],
         [100, 1, -3]]
    print("A·B mod 26 =", multiplicar(A, B, n))

    # Ejemplo NO invertible: det = 4, mcd(4, 26) = 2
    M = [[2, 4, 6],
         [1, 3, 5],
         [0, 0, 2]]
    try:
        inversa(M, n)
    except ValueError as e:
        print("Error esperado:", e)
