# Ejercicio 2: influencia de la partición

## Qué se compara

Se aproxima la integral

$$
\int_{-1}^{1} f(x)\,dx=\int_{-1}^{1}2\sqrt{1-x^2}\,dx=\pi
$$

con tres maneras de dividir el intervalo $[-1,1]$:

1. **Equiespaciada:** todos los subintervalos tienen el mismo ancho.
2. **Aleatoria uniforme:** los puntos interiores se eligen uniformemente en $[-1,1]$ y se ordenan.
3. **Cosenoidal:** se construye usando $x_i=\cos(i\pi/N)$, para $i=0,\ldots,N$.

El programa usa sumas superiores de Darboux. La consigna permite elegir entre sumas inferiores o superiores; se eligieron las superiores para poder comparar sistemáticamente aproximaciones desde arriba. Por eso, el residuo se define como

$$
r_N=U_N-\pi.
$$

El residuo es no negativo. Cuanto menor sea su valor absoluto, mejor es la aproximación superior.

## Convención para $N$

En este ejercicio se interpreta $N$ como el número de subintervalos o tamaño de la partición. Por ello cada partición tiene $N+1$ puntos. Esto coincide con la fórmula cosenoidal: $i=0,\ldots,N$ produce $N+1$ nodos e incluye los dos extremos, pues $x_0=1$ y $x_N=-1$. Para trabajar de izquierda a derecha se invierten esos nodos.

El primer punto de la letra menciona la cantidad de puntos, pero la fórmula cosenoidal fija la convención de tamaño $N$ con $N$ intervalos. El código hace explícita esta interpretación y la mantiene igual para los tres tipos de partición.

## Construcción de cada partición

### Equiespaciada

Con $N$ subintervalos, el ancho es

$$
h=\frac{1-(-1)}{N}=\frac{2}{N}.
$$

Los puntos son $x_i=-1+ih$, $i=0,\ldots,N$. La función `particion_equiespaciada(N)` genera esta lista.

### Aleatoria uniforme

Se generan $N-1$ puntos interiores independientes con distribución uniforme en $[-1,1]$. Se agregan los extremos $-1$ y $1$ y se ordena la lista. Al quedar $N+1$ puntos en total, se forman $N$ subintervalos. `particion_aleatoria_uniforme(N)` usa una semilla fija para que cada ejecución produzca los mismos resultados, lo que facilita comparar y verificar las tablas.

La aleatoriedad implica que la suma no necesariamente disminuye en cada fila cuando aumenta $N$: una partición aleatoria particular puede tener espacios desiguales. La tendencia se aprecia al observar el conjunto de valores y el tamaño creciente de la partición.

### Cosenoidal

Se usan los nodos de Chebyshev-Lobatto indicados en la consigna:

$$
x_i=\cos\left(\frac{i\pi}{N}\right),\quad i=0,\ldots,N.
$$

Estos puntos se acumulan cerca de los extremos $-1$ y $1$, y quedan más separados cerca del centro. Esa distribución puede ser ventajosa para esta función, cuya pendiente se hace muy grande cerca de los extremos. `particion_cosenoidal(N)` genera los nodos, asegura los extremos exactos por consideraciones numéricas y los devuelve en orden creciente.

## Cálculo de la suma superior

La función $f(x)=2\sqrt{1-x^2}$ es simétrica respecto del eje $y$. También disminuye al alejarnos de cero: su máximo es $f(0)=2$ y en los extremos vale cero.

En un subintervalo $[a_i,b_i]$, el punto más cercano a cero determina el máximo:

$$
d_i=\begin{cases}
0,&a_i\leq0\leq b_i,\\
\min(|a_i|,|b_i|),&\text{en otro caso},
\end{cases}
\qquad
M_i=2\sqrt{1-d_i^2}.
$$

La suma superior es

$$
U_N=\sum_{i=1}^{N}M_i(b_i-a_i).
$$

La función `suma_superior(puntos)` recorre los intervalos de una partición ordenada y acumula altura por ancho. No basta con evaluar solamente los extremos en el intervalo que contiene cero: el máximo real está en el punto interior cero, por eso se considera explícitamente.

## Tablas y gráficas generadas

Se calculan los rangos solicitados:

- $N=10,20,\ldots,100$;
- $N=100,200,\ldots,1000$;
- $N=1000,2000,\ldots,10000$.

Para cada $N$ y cada partición, se guarda la aproximación $U_N$ y el residuo $U_N-\pi$. Las tablas se imprimen en la terminal y se guardan en archivos CSV. Para cada rango se genera una gráfica con las tres curvas de sumas superiores y una línea horizontal en $\pi$.

Además, `rectangulos_N100.png` contiene tres paneles —uno por tipo de partición— con el gráfico de $f$ y los rectángulos de la suma superior para $N=100$. En cada subintervalo, el rectángulo llega hasta el máximo de la función en ese intervalo.

Todos los archivos se guardan en `resultados_ejercicio2/`:

- `tabla_10_a_100.csv`, `tabla_100_a_1000.csv`, `tabla_1000_a_10000.csv`;
- `grafica_10_a_100.png`, `grafica_100_a_1000.png`, `grafica_1000_a_10000.png`;
- `rectangulos_N100.png`.

## Cómo interpretar cuál partición resulta mejor

Para $N=100$, la ejecución del programa dio:

| Partición | Suma superior | Residuo $U_N-\pi$ |
|---|---:|---:|
| Equiespaciada | 3.178268511099 | 0.036675857509 |
| Aleatoria uniforme | 3.205792103892 | 0.064199450302 |
| Cosenoidal | 3.172494418460 | 0.030901764870 |

En esta comparación, la partición cosenoidal produce la suma superior más cercana a $\pi$. Su distribución concentra puntos cerca de $x=\pm1$, donde la curva cambia más abruptamente, lo que reduce la sobreestimación de los rectángulos en los bordes. La partición aleatoria depende de la ubicación de sus puntos y puede variar; por eso el código fija una semilla y hace reproducible la comparación.

No se debe concluir que la partición aleatoria es siempre peor o mejor a partir de una sola realización. La comparación para $N=100$ se refiere a la semilla escogida; otras realizaciones aleatorias podrían dar otro orden.

## Cómo está organizado el código

En [ejercicio2.py](ejercicio2.py):

- `f(x)` evalúa la función del enunciado.
- `particion_equiespaciada(N)`, `particion_aleatoria_uniforme(N)` y `particion_cosenoidal(N)` devuelven los nodos ordenados.
- `suma_superior(puntos)` calcula una suma superior válida para cada partición.
- `generar_registros()` calcula las aproximaciones y residuos.
- `imprimir_tabla()` y `guardar_csv()` presentan y conservan los datos.
- `guardar_grafica_comparativa()` grafica las tres sumas y el valor teórico.
- `guardar_grafica_rectangulos_n100()` dibuja la función y los rectángulos para las tres particiones con $N=100$.
- `main()` procesa todos los tamaños pedidos.

## Ejecución

Con el entorno virtual activado, ejecuta:

```bash
python ejercicio2.py
```

Matplotlib ya está indicado como dependencia en [requirements.txt](requirements.txt). Si el entorno aún no lo tiene instalado, se puede instalar con:

```bash
python -m pip install -r requirements.txt
```