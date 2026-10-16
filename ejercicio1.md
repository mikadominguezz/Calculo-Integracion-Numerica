# Ejercicio 1: convergencia de las sumas inferior y superior

## Qué pide la consigna

La función y el intervalo son

$$
f(x)=2\sqrt{1-x^2},\qquad x\in[-1,1].
$$

La consigna pide implementar una función que reciba el número $N$ de puntos de la partición equiespaciada, calcular suma inferior y superior, repetirlo para tres rangos de $N$, tabular aproximaciones y residuos respecto de $\pi$, graficar ambas sumas junto con $\pi$ y decidir si la función es integrable de Riemann.

El código corregido está en [ejercicio1.py](ejercicio1.py). Produce tres tablas CSV y cuatro gráficas (una por rango y otra con todos los $N$) bajo `resultados_ejercicio1/`.

## Interpretación geométrica y valor exacto

La ecuación $x^2+y^2=1$ describe el círculo unitario. Su semicircunferencia superior es $y=\sqrt{1-x^2}$. La función del ejercicio es el doble de esa altura, $f(x)=2y$. El área de esa semicircunferencia es $\pi/2$; al duplicar las alturas, el área bajo $f$ es $\pi$:

$$
\int_{-1}^{1}2\sqrt{1-x^2}\,dx=\pi.
$$

Este $\pi$ es el valor exacto usado como referencia al calcular los residuos.

## Cómo se forman las sumas

Para un $N$ dado, la partición tiene $N$ puntos equiespaciados. Esos puntos forman $N-1$ subintervalos de igual ancho:

$$
\Delta x=\frac{1-(-1)}{N-1}=\frac{2}{N-1}.
$$

Los puntos de la partición son $x_i=-1+i\Delta x$, para $i=0,1,\ldots,N-1$. En cada subintervalo $[x_{i-1},x_i]$, llamamos $m_i$ al mínimo de la función y $M_i$ a su máximo. Las sumas de Darboux son

$$
L_N=\sum_{i=1}^{N-1}m_i\Delta x,
\qquad
U_N=\sum_{i=1}^{N-1}M_i\Delta x.
$$

Como $f(x)$ depende de $|x|$, es simétrica respecto del eje $y$. Al aumentar $|x|$ desde cero hacia los extremos $-1$ o $1$, la función disminuye desde $2$ hasta $0$. Por eso, dentro de cada subintervalo:

- el máximo está en el punto del intervalo más cercano a cero;
- el mínimo está en el extremo más alejado de cero.

Todos los $N$ que pide la consigna son múltiplos de 10, por lo que $N$ es par y hay $N-1$ subintervalos, una cantidad impar. En consecuencia, el punto $0$ cae dentro del subintervalo central, no en un punto de la partición. Allí la función alcanza el máximo interior $f(0)=2$. El código contempla este caso: si el intervalo contiene a cero, usa cero como la distancia más corta al origen. En los demás subintervalos, los extremos determinan máximo y mínimo porque la función es monótona a cada lado de cero.

Por tanto, si $d_{\min}$ es la menor distancia a cero dentro del subintervalo y $d_{\max}$ la mayor distancia a cero de sus extremos, las alturas se calculan como

$$
M_i=2\sqrt{1-d_{\min}^2},
\qquad
m_i=2\sqrt{1-d_{\max}^2}.
$$

Multiplicamos cada altura por $\Delta x$ y sumamos. Esto calcula los extremos exactos de la función en cada subintervalo, no una aproximación basada en tomar muestras arbitrarias.

## Rangos de $N$, tablas y residuos

El programa usa exactamente los tres grupos solicitados:

1. $N=10,20,\ldots,100$ (incremento de 10).
2. $N=100,200,\ldots,1000$ (incremento de 100).
3. $N=1000,2000,\ldots,10000$ (incremento de 1000).

Los extremos 100 y 1000 aparecen en dos grupos, tal como resulta de aplicar literalmente los rangos indicados. En cada fila aparecen las dos aproximaciones y sus residuos. El programa define el residuo con signo como

$$
r_L=L_N-\pi,
\qquad
r_U=U_N-\pi.
$$

Así, se espera que $r_L\leq0$ y $r_U\geq0$. Si se quisiera el error absoluto, sería $|r_L|$ o $|r_U|$; la tabla informa el residuo firmado para distinguir si la aproximación quedó por debajo o por encima de $\pi$.

Al aumentar $N$, cada rectángulo se hace más angosto. La suma inferior se aproxima a $\pi$ desde abajo y la superior desde arriba. Las tablas completas se guardan como `tabla_10_a_100.csv`, `tabla_100_a_1000.csv` y `tabla_1000_a_10000.csv` dentro de `resultados_ejercicio1/`.

## Gráficas

Se generan cuatro imágenes PNG:

- `grafica_10_a_100.png`
- `grafica_100_a_1000.png`
- `grafica_1000_a_10000.png`
- `grafica_todos_los_N.png`

Cada una dibuja la suma inferior, la suma superior y una línea horizontal discontinua en $y=\pi$. Las tres primeras enfocan los rangos individuales para ver mejor la separación; la última reúne todos los $N$ distintos en una sola gráfica. En cada gráfico se ajusta el rango vertical a los datos para que el comportamiento se aprecie, sin cambiar los valores representados.

## ¿Es integrable de Riemann?

Sí. La expresión $1-x^2$ es no negativa en $[-1,1]$, la raíz cuadrada es continua allí y multiplicar por 2 conserva la continuidad. Por tanto, $f$ es continua en el intervalo cerrado y acotado $[-1,1]$. Toda función continua en un intervalo cerrado y acotado es integrable de Riemann.

En términos de las sumas de Darboux, al refinar la partición la diferencia $U_N-L_N$ tiende a cero; las dos sumas encierran el valor de la integral y convergen a $\pi$:

$$
L_N\leq \pi\leq U_N,
\qquad
\lim_{N\to\infty}L_N=\lim_{N\to\infty}U_N=\pi.
$$

## Cómo está implementado el código

### Función `f(x)`

Calcula la fórmula pedida. `max(0.0, 1.0 - x*x)` evita que un pequeño error de redondeo de punto flotante produzca una raíz cuadrada de un número negativo en los extremos.

### Función `sumas_darboux(N)`

1. Valida que $N$ sea un entero de al menos 2 (hacen falta al menos dos puntos para formar un intervalo).
2. Calcula $\Delta x=2/(N-1)$, porque $N$ puntos forman $N-1$ subintervalos.
3. Recorre los $N-1$ subintervalos y calcula sus dos extremos.
4. Determina qué punto está más cerca y cuál más lejos de cero.
5. Evalúa en esas distancias el máximo y mínimo de $f$.
6. Acumula altura por ancho en la suma inferior y superior.

Se usa la simetría y el comportamiento monótono de cada mitad de la función para localizar los máximos y mínimos reales de cada subintervalo.

### Tablas y residuos

`generar_registros()` llama a `sumas_darboux()` para cada $N$ y calcula $L_N-\pi$ y $U_N-\pi$. `imprimir_tabla()` presenta esos valores en la terminal y `guardar_csv()` los conserva en archivos CSV para poder abrirlos, por ejemplo, con una hoja de cálculo.

### Gráficas

`guardar_grafica()` dibuja las dos secuencias y el valor teórico $\pi$. Se usa Matplotlib; el archivo [requirements.txt](requirements.txt) declara esa dependencia.

### Función principal

`main()` crea la carpeta de resultados, procesa los tres rangos que pide la consigna, imprime y guarda las tablas, y produce una gráfica por rango más la gráfica conjunta. La instrucción final `if __name__ == "__main__":` ejecuta `main()` al correr el archivo directamente.

## Cómo ejecutarlo

Con el entorno virtual del proyecto activado, ejecuta:

```bash
python ejercicio1.py
```

Si todavía no está instalada la dependencia, instálala con:

```bash
python -m pip install -r requirements.txt
```

Al terminar, la terminal muestra las tres tablas y la carpeta `resultados_ejercicio1/` contiene los CSV y PNG generados.
