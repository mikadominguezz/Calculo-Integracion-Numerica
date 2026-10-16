Respuestas a las preguntas analíticas (Punto 4)
   
¿Qué método dio mejores resultados? ¿Hay métodos mejores que otros?
El método del Punto Medio ofrece ampliamente los mejores resultados, seguido por el método del Trapecio. El método de Rectángulos estándar es el que presenta mayor error y converge de manera más lenta.
Justifique geométricamente por qué pasa esto:
Método de Rectángulos: Asume que la función es constante en cada subintervalo (aproximando mediante crestas horizontales). Al tratarse de una curva suave (la semicircunferencia), dejar la parte superior plana genera un error lineal importante dependiente de la pendiente en los extremos.
Método del Trapecio: Conecta los puntos extremos mediante una línea recta inclinada. Dado que la semicircunferencia es una función estrictamente cóncava (f 
′′
 (x)<0), las cuerdas de los trapecios quedan siempre por debajo de la curva real, subestimando ligeramente el área real.
Método del Punto Medio: Utiliza un rectángulo cuya altura es el valor de la función en la mitad del subintervalo. Geométricamente, la línea tangente trazada en el punto medio corta a la cuerda del trapecio de tal forma que el área del triángulo que sobra por encima de la curva compensa casi exactamente al área del triángulo que falta por debajo. Esto cancela los errores de primer orden, otorgándole al método del punto medio un orden de convergencia superior (similar al de la regla de Simpson en términos de precisión local por intervalo).
