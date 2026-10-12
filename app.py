"""
app.py
------
Interfaz de la calculadora de matrices 3x3 módulo n, hecha con Streamlit.

Esta parte SOLO se encarga de:
  1. Pedir los datos (n, matriz A y, si hace falta, matriz B).
  2. Llamar a las funciones de matrices_mod.py.
  3. Mostrar el resultado o el mensaje de error.

Para ejecutarla en la computadora:
    streamlit run app.py
"""

import pandas as pd
import streamlit as st

from matrices_mod import inversa, multiplicar


# ---------------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------------

# layout="centered" se ve bien tanto en computadora como en el iPhone
st.set_page_config(page_title="Calculadora de matrices mod n", page_icon="🔢",
                   layout="centered")

st.title("Calculadora de matrices 3×3 mod n")
st.caption("Puedes escribir números negativos o mayores que n: "
           "el resultado siempre se reduce al rango 0 … n−1.")


# ---------------------------------------------------------------------------
# Funciones de apoyo para la interfaz
# ---------------------------------------------------------------------------

def matriz_vacia():
    """Tabla 3x3 llena de ceros con encabezados de columna 1, 2, 3.
    Se usa como valor inicial de cada editor de matriz."""
    return pd.DataFrame([[0, 0, 0]] * 3, columns=["1", "2", "3"])


def editor_matriz(nombre, clave):
    """Muestra una cuadrícula editable de 3x3 y devuelve lo que escribió
    el usuario. Se usa st.data_editor (y no 9 cajitas en columnas) porque
    en el celular las columnas de Streamlit se apilan una debajo de otra,
    mientras que el editor conserva la forma de la matriz."""
    st.markdown(f"**Matriz {nombre}**")
    columnas = {
        c: st.column_config.NumberColumn(c, step=1, format="%d")
        for c in ["1", "2", "3"]
    }
    return st.data_editor(
        matriz_vacia(),
        key=clave,                 # identifica el editor para que conserve los datos
        column_config=columnas,
        hide_index=True,
        num_rows="fixed",          # no se pueden agregar ni borrar filas
        width="stretch",
    )


def tabla_a_lista(tabla, nombre):
    """Convierte la tabla del editor a una lista de listas de enteros,
    que es el formato que usan las funciones de matrices_mod.py.
    Si alguna casilla quedó vacía, lanza un error con mensaje claro."""
    if tabla.isnull().values.any():
        raise ValueError(f"Llena todas las casillas de la matriz {nombre}.")
    return [[int(valor) for valor in fila] for fila in tabla.values.tolist()]


def mostrar_matriz(M, titulo):
    """Muestra una matriz de resultado como tabla sin índices."""
    st.markdown(f"**{titulo}**")
    st.dataframe(pd.DataFrame(M, columns=["1", "2", "3"]),
                 hide_index=True, width="stretch")


# ---------------------------------------------------------------------------
# Entradas del usuario
# ---------------------------------------------------------------------------

# Módulo n: entero, mínimo 2
n = st.number_input("Módulo n", min_value=2, value=26, step=1)

# Operación a realizar; horizontal=True ahorra espacio en el celular
operacion = st.radio("Operación", ["A⁻¹ mod n", "A · B mod n"], horizontal=True)

tabla_A = editor_matriz("A", "matriz_A")

# La matriz B solo se pide cuando se va a multiplicar
tabla_B = None
if operacion == "A · B mod n":
    tabla_B = editor_matriz("B", "matriz_B")


# ---------------------------------------------------------------------------
# Cálculo y resultado
# ---------------------------------------------------------------------------

if st.button("Calcular", type="primary", width="stretch"):
    try:
        A = tabla_a_lista(tabla_A, "A")

        if operacion == "A⁻¹ mod n":
            resultado = inversa(A, int(n))
            mostrar_matriz(resultado, f"A⁻¹ mod {int(n)}")
        else:
            B = tabla_a_lista(tabla_B, "B")
            resultado = multiplicar(A, B, int(n))
            mostrar_matriz(resultado, f"A · B mod {int(n)}")

    except ValueError as error:
        # Aquí llegan los errores de matrices_mod.py (por ejemplo, cuando
        # det(A) y n no son coprimos) y los de casillas vacías.
        st.error(str(error))
