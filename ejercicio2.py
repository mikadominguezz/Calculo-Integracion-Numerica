"""Compara tres particiones para aproximar la integral de f en [-1, 1].

Se usan sumas superiores de Darboux para las particiones equiespaciada,
aleatoria uniforme y cosenoidal x_i = cos(i*pi/N). Aquí N es el número de
subintervalos: la partición tiene N+1 puntos, como requiere esa fórmula.
"""

import csv
import math
import random
from pathlib import Path


A = -1.0
B = 1.0
PI = math.pi
SEMILLA_ALEATORIA = 20261016
DIRECTORIO_RESULTADOS = Path(__file__).parent / "resultados_ejercicio2"

RANGOS_N = {
	"10_a_100": range(10, 101, 10),
	"100_a_1000": range(100, 1001, 100),
	"1000_a_10000": range(1000, 10001, 1000),
}


def f(x: float) -> float:
	"""Devuelve f(x) = 2*sqrt(1 - x²)."""
	return 2.0 * math.sqrt(max(0.0, 1.0 - x * x))


def particion_equiespaciada(n: int) -> list[float]:
	"""Construye N subintervalos iguales, con N+1 puntos incluyendo extremos."""
	validar_n(n)
	return [A + (B - A) * i / n for i in range(n + 1)]


def particion_aleatoria_uniforme(n: int) -> list[float]:
	"""Genera N subintervalos usando N-1 puntos Uniforme(-1, 1) ordenados.

	La semilla fija hace que los resultados puedan repetirse exactamente.
	Para un mismo N se genera la misma partición en todas las ejecuciones.
	"""
	validar_n(n)
	rng = random.Random(SEMILLA_ALEATORIA + n)
	puntos = {A, B}
	while len(puntos) < n + 1:
		puntos.add(rng.uniform(A, B))
	return sorted(puntos)


def particion_cosenoidal(n: int) -> list[float]:
	"""Construye x_i=cos(i*pi/N), i=0,...,N, en orden creciente.

	La fórmula produce los extremos en orden descendente (1 hasta -1), por lo
	que se invierte la lista para procesar subintervalos de izquierda a derecha.
	"""
	validar_n(n)
	puntos_descendentes = [math.cos(i * math.pi / n) for i in range(n + 1)]
	puntos_descendentes[0] = B
	puntos_descendentes[-1] = A
	return list(reversed(puntos_descendentes))


def validar_n(n: int) -> None:
	"""Valida que N represente al menos un subintervalo."""
	if not isinstance(n, int) or isinstance(n, bool) or n < 1:
		raise ValueError("N debe ser un entero positivo")


def suma_superior(puntos: list[float]) -> float:
	"""Calcula la suma superior de Darboux para una partición de [-1, 1].

	La función es simétrica y decrece al aumentar |x|. En cada subintervalo el
	valor máximo se da en el punto más cercano a cero, incluido x=0 si cae dentro
	del subintervalo. Se evalúa el mínimo en el extremo más alejado de cero.
	"""
	if len(puntos) < 2 or puntos[0] != A or puntos[-1] != B:
		raise ValueError("La partición debe incluir -1 y 1 y tener al menos dos puntos")
	if any(x_izq >= x_der for x_izq, x_der in zip(puntos, puntos[1:])):
		raise ValueError("Los puntos de la partición deben estar estrictamente ordenados")

	resultado = 0.0
	for x_izquierda, x_derecha in zip(puntos, puntos[1:]):
		if x_izquierda <= 0.0 <= x_derecha:
			distancia_minima = 0.0
		else:
			distancia_minima = min(abs(x_izquierda), abs(x_derecha))
		distancia_maxima = max(abs(x_izquierda), abs(x_derecha))
		maximo = f(distancia_minima)
		resultado += maximo * (x_derecha - x_izquierda)
	return resultado


def generar_registros(valores_n: list[int]) -> list[dict[str, float | int]]:
	"""Calcula suma superior y residuo firmado para cada N y tipo de partición."""
	constructores = {
		"equiespaciada": particion_equiespaciada,
		"aleatoria_uniforme": particion_aleatoria_uniforme,
		"cosenoidal": particion_cosenoidal,
	}
	registros = []
	for n in valores_n:
		registro: dict[str, float | int] = {"N": n}
		for nombre, construir in constructores.items():
			aproximacion = suma_superior(construir(n))
			registro[f"suma_{nombre}"] = aproximacion
			registro[f"residuo_{nombre}"] = aproximacion - PI
		registros.append(registro)
	return registros


def imprimir_tabla(nombre: str, registros: list[dict[str, float | int]]) -> None:
	"""Imprime las tres aproximaciones y sus residuos con signo."""
	print(f"\nRango N = {nombre}")
	print(
		f"{'N':>7} | {'Equiespaciada':>17} | {'Residuo':>13} | "
		f"{'Aleatoria':>17} | {'Residuo':>13} | "
		f"{'Cosenoidal':>17} | {'Residuo':>13}"
	)
	print("-" * 111)
	for r in registros:
		print(
			f"{r['N']:7d} | {r['suma_equiespaciada']:17.11f} | "
			f"{r['residuo_equiespaciada']:13.5e} | "
			f"{r['suma_aleatoria_uniforme']:17.11f} | "
			f"{r['residuo_aleatoria_uniforme']:13.5e} | "
			f"{r['suma_cosenoidal']:17.11f} | "
			f"{r['residuo_cosenoidal']:13.5e}"
		)


def guardar_csv(nombre: str, registros: list[dict[str, float | int]]) -> None:
	"""Guarda una tabla comparativa como CSV."""
	archivo = DIRECTORIO_RESULTADOS / f"tabla_{nombre}.csv"
	campos = [
		"N",
		"suma_equiespaciada",
		"residuo_equiespaciada",
		"suma_aleatoria_uniforme",
		"residuo_aleatoria_uniforme",
		"suma_cosenoidal",
		"residuo_cosenoidal",
	]
	with archivo.open("w", newline="", encoding="utf-8") as salida:
		escritor = csv.DictWriter(salida, fieldnames=campos)
		escritor.writeheader()
		escritor.writerows(registros)


def guardar_grafica_comparativa(
	nombre: str, registros: list[dict[str, float | int]]
) -> None:
	"""Grafica las tres sumas superiores y el valor teórico pi."""
	import matplotlib

	matplotlib.use("Agg")
	import matplotlib.pyplot as plt

	valores_n = [int(r["N"]) for r in registros]
	figura, eje = plt.subplots(figsize=(10, 6))
	for columna, etiqueta, marcador in (
		("suma_equiespaciada", "Equiespaciada", "o"),
		("suma_aleatoria_uniforme", "Aleatoria uniforme", "s"),
		("suma_cosenoidal", "Cosenoidal", "^"),
	):
		eje.plot(
			valores_n,
			[float(r[columna]) for r in registros],
			marcador + "-",
			label=etiqueta,
			markersize=4,
		)
	eje.axhline(PI, color="black", linestyle="--", label="π teórico")
	etiquetas_rango = {
		"10_a_100": "10, 20, ..., 100",
		"100_a_1000": "100, 200, ..., 1000",
		"1000_a_10000": "1000, 2000, ..., 10000",
	}
	eje.set_title(f"Influencia de la partición: N = {etiquetas_rango[nombre]}")
	eje.set_xlabel("Número de subintervalos, N")
	eje.set_ylabel("Suma superior")
	eje.set_xlim(min(valores_n), max(valores_n))
	valores_y = [PI] + [float(r[f"suma_{key}"]) for r in registros for key in (
		"equiespaciada", "aleatoria_uniforme", "cosenoidal"
	)]
	variacion = max(valores_y) - min(valores_y)
	margen = max(variacion * 0.12, 1e-12)
	eje.set_ylim(min(valores_y) - margen, max(valores_y) + margen)
	eje.grid(True, alpha=0.3)
	eje.legend()
	figura.tight_layout()
	archivo = DIRECTORIO_RESULTADOS / f"grafica_{nombre}.png"
	figura.savefig(archivo, dpi=180)
	plt.close(figura)
	print(f"Gráfica comparativa guardada: {archivo}")


def guardar_grafica_rectangulos_n100() -> None:
	"""Dibuja f y los rectángulos superiores con N=100 para los tres tipos."""
	import matplotlib

	matplotlib.use("Agg")
	import matplotlib.pyplot as plt
	from matplotlib.patches import Rectangle

	constructores = (
		("Equiespaciada", particion_equiespaciada),
		("Aleatoria uniforme", particion_aleatoria_uniforme),
		("Cosenoidal", particion_cosenoidal),
	)
	curva_x = [A + (B - A) * i / 1000 for i in range(1001)]
	curva_y = [f(x) for x in curva_x]
	figura, ejes = plt.subplots(3, 1, figsize=(12, 13), sharex=True, sharey=True)

	for eje, (etiqueta, construir) in zip(ejes, constructores):
		puntos = construir(100)
		eje.plot(curva_x, curva_y, color="black", linewidth=1.6, label="f(x)")
		for izquierda, derecha in zip(puntos, puntos[1:]):
			if izquierda <= 0.0 <= derecha:
				distancia_minima = 0.0
			else:
				distancia_minima = min(abs(izquierda), abs(derecha))
			altura = f(distancia_minima)
			rectangulo = Rectangle(
				(izquierda, 0.0),
				derecha - izquierda,
				altura,
				facecolor="tab:blue",
				edgecolor="tab:blue",
				alpha=0.22,
				linewidth=0.55,
			)
			eje.add_patch(rectangulo)
		eje.set_title(f"{etiqueta} — suma superior, N=100")
		eje.grid(True, alpha=0.25)
		eje.legend(loc="upper right")
		eje.set_ylabel("f(x)")

	ejes[-1].set_xlabel("x")
	figura.suptitle("Función y rectángulos de aproximación superior", y=0.995)
	figura.tight_layout()
	archivo = DIRECTORIO_RESULTADOS / "rectangulos_N100.png"
	figura.savefig(archivo, dpi=180)
	plt.close(figura)
	print(f"Gráfica de rectángulos guardada: {archivo}")


def main() -> None:
	DIRECTORIO_RESULTADOS.mkdir(exist_ok=True)
	print("Influencia de la partición para f(x) = 2*sqrt(1 - x²) en [-1, 1]")
	print(f"Integral exacta: pi = {PI:.15f}")
	print("Se usan sumas superiores; residuo = aproximación - pi.")
	print("N representa subintervalos; cada partición contiene N+1 puntos.")

	for nombre, rango in RANGOS_N.items():
		registros = generar_registros(list(rango))
		imprimir_tabla(nombre, registros)
		guardar_csv(nombre, registros)
		guardar_grafica_comparativa(nombre, registros)

	guardar_grafica_rectangulos_n100()

	comparacion_100 = generar_registros([100])[0]
	print("\nComparación de residuos para N=100 (menor residuo absoluto es mejor):")
	for clave, etiqueta in (
		("equiespaciada", "Equiespaciada"),
		("aleatoria_uniforme", "Aleatoria uniforme"),
		("cosenoidal", "Cosenoidal"),
	):
		residuo = float(comparacion_100[f"residuo_{clave}"])
		print(
			f"{etiqueta:22s}: suma={comparacion_100[f'suma_{clave}']:.12f}, "
			f"residuo={residuo:.6e}"
		)
	print("\nPara estas particiones, el residuo de la suma superior es no negativo.")
	print("Los CSV y PNG se guardaron en:", DIRECTORIO_RESULTADOS)


if __name__ == "__main__":
	main()
