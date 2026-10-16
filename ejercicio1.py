"""Sumas de Darboux para f(x) = 2*sqrt(1 - x**2) en [-1, 1].

El programa construye particiones equiespaciadas, calcula exactamente los
extremos de la función en cada subintervalo, compara las sumas con pi y guarda
las tablas y gráficas solicitadas en resultados_ejercicio1/.
"""

import csv
import math
from pathlib import Path


A = -1.0
B = 1.0
VALOR_EXACTO = math.pi
DIRECTORIO_RESULTADOS = Path(__file__).parent / "resultados_ejercicio1"

RANGOS_N = {
	"10_a_100": range(10, 101, 10),
	"100_a_1000": range(100, 1001, 100),
	"1000_a_10000": range(1000, 10001, 1000),
}


def f(x: float) -> float:
	"""Evalúa f(x) = 2*sqrt(1 - x²) en el dominio [-1, 1]."""
	return 2.0 * math.sqrt(max(0.0, 1.0 - x * x))


def sumas_darboux(n: int) -> tuple[float, float]:
	"""Calcula las sumas con N puntos de partición equiespaciados.

	Como f depende de |x| y decrece al aumentar |x|, el máximo en un
	subintervalo está en el punto más cercano a cero y el mínimo en el extremo
	con mayor valor absoluto. Esto también maneja correctamente un subintervalo
	que contenga x=0.
	"""
	if not isinstance(n, int) or isinstance(n, bool) or n < 2:
		raise ValueError("N debe ser un entero mayor o igual que 2")

	# N puntos generan N-1 subintervalos.
	ancho = (B - A) / (n - 1)
	suma_inferior = 0.0
	suma_superior = 0.0

	for i in range(n - 1):
		x_izquierda = A + i * ancho
		x_derecha = A + (i + 1) * ancho

		# Distancia del punto del intervalo más cercano al centro x=0.
		if x_izquierda <= 0.0 <= x_derecha:
			menor_distancia = 0.0
		else:
			menor_distancia = min(abs(x_izquierda), abs(x_derecha))

		# La distancia máxima al cero ocurre en uno de los dos extremos.
		mayor_distancia = max(abs(x_izquierda), abs(x_derecha))
		maximo = f(menor_distancia)
		minimo = f(mayor_distancia)

		suma_inferior += minimo * ancho
		suma_superior += maximo * ancho

	return suma_inferior, suma_superior


def generar_registros(valores_n: list[int]) -> list[dict[str, float | int]]:
	"""Calcula sumas y residuos con signo (aproximación menos pi)."""
	registros = []
	for n in valores_n:
		inferior, superior = sumas_darboux(n)
		registros.append(
			{
				"N": n,
				"suma_inferior": inferior,
				"residuo_inferior": inferior - VALOR_EXACTO,
				"suma_superior": superior,
				"residuo_superior": superior - VALOR_EXACTO,
			}
		)
	return registros


def imprimir_tabla(nombre: str, registros: list[dict[str, float | int]]) -> None:
	"""Imprime la tabla de aproximaciones y residuos del rango indicado."""
	print(f"\nRango N = {nombre}")
	print(
		f"{'N':>7} | {'Suma inferior':>18} | {'Residuo inferior':>18} | "
		f"{'Suma superior':>18} | {'Residuo superior':>18}"
	)
	print("-" * 91)
	for r in registros:
		print(
			f"{r['N']:7d} | {r['suma_inferior']:18.12f} | "
			f"{r['residuo_inferior']:18.12e} | "
			f"{r['suma_superior']:18.12f} | "
			f"{r['residuo_superior']:18.12e}"
		)


def guardar_csv(nombre: str, registros: list[dict[str, float | int]]) -> None:
	"""Guarda las columnas de la tabla en un archivo CSV."""
	archivo = DIRECTORIO_RESULTADOS / f"tabla_{nombre}.csv"
	with archivo.open("w", newline="", encoding="utf-8") as salida:
		campos = [
			"N",
			"suma_inferior",
			"residuo_inferior",
			"suma_superior",
			"residuo_superior",
		]
		escritor = csv.DictWriter(salida, fieldnames=campos)
		escritor.writeheader()
		escritor.writerows(registros)


def guardar_grafica(nombre: str, registros: list[dict[str, float | int]]) -> None:
	"""Grafica ambas sumas, la referencia pi y ajusta la escala vertical."""
	import matplotlib

	matplotlib.use("Agg")
	import matplotlib.pyplot as plt

	valores_n = [int(r["N"]) for r in registros]
	inferiores = [float(r["suma_inferior"]) for r in registros]
	superiores = [float(r["suma_superior"]) for r in registros]

	figura, eje = plt.subplots(figsize=(10, 6))
	eje.plot(valores_n, inferiores, "o-", label="Suma inferior", markersize=4)
	eje.plot(valores_n, superiores, "o-", label="Suma superior", markersize=4)
	eje.axhline(VALOR_EXACTO, color="black", linestyle="--", label="π teórico")
	if nombre == "todos_los_N":
		titulo = "Sumas de Darboux para todos los valores de N"
	else:
		titulo = f"Sumas de Darboux para N = {nombre.replace('_', '–')}"
	eje.set_title(titulo)
	eje.set_xlabel("Número de puntos de la partición, N")
	eje.set_ylabel("Valor de la aproximación")
	eje.set_xlim(min(valores_n), max(valores_n))
	eje.grid(True, alpha=0.3)
	eje.legend()

	# Ajustar el eje y permite distinguir las dos curvas alrededor de pi.
	valores_y = inferiores + superiores + [VALOR_EXACTO]
	variacion = max(valores_y) - min(valores_y)
	margen = max(variacion * 0.12, 1e-12)
	eje.set_ylim(min(valores_y) - margen, max(valores_y) + margen)

	figura.tight_layout()
	archivo = DIRECTORIO_RESULTADOS / f"grafica_{nombre}.png"
	figura.savefig(archivo, dpi=180)
	plt.close(figura)
	print(f"Gráfica guardada: {archivo}")


def main() -> None:
	DIRECTORIO_RESULTADOS.mkdir(exist_ok=True)
	print("Sumas de Darboux para f(x) = 2*sqrt(1 - x²), en [-1, 1]")
	print(f"Valor exacto de la integral: pi = {VALOR_EXACTO:.15f}")
	print("Residuo definido como: aproximación - pi (con signo).")

	for nombre, rango in RANGOS_N.items():
		registros = generar_registros(list(rango))
		imprimir_tabla(nombre, registros)
		guardar_csv(nombre, registros)
		guardar_grafica(nombre, registros)

	# Gráfica adicional con todos los N distintos de las tres tablas.
	todos_los_n = sorted({n for rango in RANGOS_N.values() for n in rango})
	todos_los_registros = generar_registros(todos_los_n)
	guardar_grafica("todos_los_N", todos_los_registros)

	print("\nObservación: las sumas inferiores quedan debajo de pi y las superiores")
	print("por encima; ambas se acercan a pi al aumentar N.")
	print("La función es continua en [-1, 1], por lo tanto es integrable de Riemann.")
	print(f"Tablas y gráficas guardadas en: {DIRECTORIO_RESULTADOS}")


if __name__ == "__main__":
	main()
