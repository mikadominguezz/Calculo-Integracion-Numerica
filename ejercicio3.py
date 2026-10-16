"""Comparación de métodos de integración numérica (Rectángulos, Trapecio, Punto Medio)
sobre una partición equiespaciada para f(x) = 2*sqrt(1 - x**2) en [-1, 1].
"""

import csv
import math
from pathlib import Path
import matplotlib
from matplotlib.ticker import ScalarFormatter
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = -1.0
B = 1.0
PI = math.pi
DIRECTORIO_RESULTADOS = Path(__file__).parent / "resultados_ejercicio3"

RANGOS_N = {
    "10_a_100": range(10, 101, 10),
    "100_a_1000": range(100, 1001, 100),
    "1000_a_10000": range(1000, 10001, 1000),
}


def f(x: float) -> float:
    """Devuelve f(x) = 2*sqrt(1 - x²)."""
    return 2.0 * math.sqrt(max(0.0, 1.0 - x * x))


def particion_equiespaciada(n: int) -> list[float]:
    """Construye N puntos equiespaciados, incluyendo -1 y 1.

    N puntos consecutivos forman N-1 subintervalos.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("N debe ser un entero de al menos 2 puntos")
    return [A + (B - A) * i / (n - 1) for i in range(n)]


def metodo_rectangulos(puntos: list[float]) -> float:
    """Método de rectángulos usando el extremo izquierdo de cada subintervalo."""
    suma = 0.0
    for x_izq, x_der in zip(puntos, puntos[1:]):
        ancho = x_der - x_izq
        suma += f(x_izq) * ancho
    return suma


def metodo_trapecio(puntos: list[float]) -> float:
    """Método del trapecio usando los extremos de cada subintervalo."""
    suma = 0.0
    for x_izq, x_der in zip(puntos, puntos[1:]):
        ancho = x_der - x_izq
        area_trapecio = (f(x_izq) + f(x_der)) * ancho / 2.0
        suma += area_trapecio
    return suma


def metodo_punto_medio(puntos: list[float]) -> float:
    """Método del punto medio evaluando en el centro de cada subintervalo."""
    suma = 0.0
    for x_izq, x_der in zip(puntos, puntos[1:]):
        ancho = x_der - x_izq
        punto_medio = (x_izq + x_der) / 2.0
        suma += f(punto_medio) * ancho
    return suma


def generar_registros(valores_n: list[int]) -> list[dict[str, float | int]]:
    """Calcula aproximaciones y residuos firmados para los tres métodos."""
    metodos = {
        "rectangulos": metodo_rectangulos,
        "trapecio": metodo_trapecio,
        "punto_medio": metodo_punto_medio,
    }
    registros = []
    for n in valores_n:
        puntos = particion_equiespaciada(n)
        registro: dict[str, float | int] = {"N": n}
        for nombre, funcion_metodo in metodos.items():
            aprox = funcion_metodo(puntos)
            registro[f"aprox_{nombre}"] = aprox
            registro[f"residuo_{nombre}"] = aprox - PI
        registros.append(registro)
    return registros


def imprimir_tabla(nombre: str, registros: list[dict[str, float | int]]) -> None:
    """Imprime la tabla comparativa de los tres métodos en consola."""
    print(f"\nRango N = {nombre}")
    print(
        f"{'N':>7} | {'Rectángulos':>15} | {'Residuo':>12} | "
        f"{'Trapecio':>15} | {'Residuo':>12} | "
        f"{'Punto Medio':>15} | {'Residuo':>12}"
    )
    print("-" * 105)
    for r in registros:
        print(
            f"{r['N']:7d} | {r['aprox_rectangulos']:15.10f} | "
            f"{r['residuo_rectangulos']:12.4e} | {r['aprox_trapecio']:15.10f} | "
            f"{r['residuo_trapecio']:12.4e} | {r['aprox_punto_medio']:15.10f} | "
            f"{r['residuo_punto_medio']:12.4e}"
        )


def guardar_csv(nombre: str, registros: list[dict[str, float | int]]) -> None:
    """Guarda la tabla comparativa de métodos en formato CSV."""
    archivo = DIRECTORIO_RESULTADOS / f"tabla_metodos_{nombre}.csv"
    campos = [
        "N",
        "aprox_rectangulos",
        "residuo_rectangulos",
        "aprox_trapecio",
        "residuo_trapecio",
        "aprox_punto_medio",
        "residuo_punto_medio",
    ]
    with archivo.open("w", newline="", encoding="utf-8") as salida:
        escritor = csv.DictWriter(salida, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)


def guardar_grafica_comparativa(nombre: str, registros: list[dict[str, float | int]]) -> None:
    """Grafica las tres curvas de aproximación frente a N junto con el valor pi teórico."""
    valores_n = [int(r["N"]) for r in registros]
    figura, eje = plt.subplots(figsize=(10, 6))

    for columna, etiqueta, marcador, estilo, orden in (
        ("aprox_rectangulos", "Rectángulos", "o", "--", 4),
        ("aprox_trapecio", "Trapecio", "s", "-", 3),
        ("aprox_punto_medio", "Punto Medio", "^", "-", 2),
    ):
        eje.plot(
            valores_n,
            [float(r[columna]) for r in registros],
            marcador + estilo,
            label=etiqueta,
            markersize=4,
            markerfacecolor="none" if columna == "aprox_rectangulos" else None,
            zorder=orden,
        )

    eje.axhline(PI, color="black", linestyle="--", label="π teórico")
    etiquetas_rango = {
        "10_a_100": "N = 10, 20, ..., 100",
        "100_a_1000": "N = 100, 200, ..., 1000",
        "1000_a_10000": "N = 1000, 2000, ..., 10000",
    }
    eje.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    eje.set_title(f"Comparación de métodos numéricos ({etiquetas_rango[nombre]})")
    eje.set_xlabel("Número de puntos de la partición (N)")
    eje.set_ylabel("Valor de la aproximación")
    eje.set_xlim(min(valores_n), max(valores_n))
    
    valores_y = [PI] + [float(r[f"aprox_{key}"]) for r in registros for key in (
        "rectangulos", "trapecio", "punto_medio"
    )]
    variacion = max(valores_y) - min(valores_y)
    margen = max(variacion * 0.12, 1e-12)
    eje.set_ylim(min(valores_y) - margen, max(valores_y) + margen)
    
    eje.grid(True, alpha=0.3)
    eje.legend()
    figura.tight_layout()

    archivo = DIRECTORIO_RESULTADOS / f"grafica_metodos_{nombre}.png"
    figura.savefig(archivo, dpi=180)
    plt.close(figura)
    print(f"Gráfica guardada: {archivo}")


def main() -> None:
    DIRECTORIO_RESULTADOS.mkdir(exist_ok=True)
    print("Comparación de Métodos de Integración Numérica para f(x) = 2*sqrt(1 - x²)")
    print(f"Valor exacto: pi = {PI:.15f}")
    print("N representa puntos de la partición; se forman N-1 subintervalos.")

    for nombre, rango in RANGOS_N.items():
        registros = generar_registros(list(rango))
        imprimir_tabla(nombre, registros)
        guardar_csv(nombre, registros)
        guardar_grafica_comparativa(nombre, registros)

    print(f"\n¡Resultados de la Sección 3 guardados exitosamente en: {DIRECTORIO_RESULTADOS}!")


if __name__ == "__main__":
    main()
