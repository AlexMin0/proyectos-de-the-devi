# visualizacion del juego
pared = "🧱"
camino = "⬛"
queso = "🧀"
raton = "🐭"
gato = "🐱"

# Direcciones
arriba = 8
izquierda = 4
derecha = 6
abajo = 2

print("Bienvenidos")
print("A")
print("Tom y Jerry")

# Crear el tablero vacio
def crear_tablero(filas, columnas, valor):
    tablero = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(valor)
        tablero.append(fila)
    return tablero

tablero = crear_tablero(6, 6, camino)

# Poner personajes y objetos
tablero[5][0] = gato
tablero[0][5] = raton
tablero[0][0] = queso
tablero[3][0] = queso
tablero[4][3] = queso

# Poner paredes
tablero[0][3] = pared
tablero[1][1] = pared
tablero[1][5] = pared
tablero[2][2] = pared
tablero[3][4] = pared
tablero[4][0] = pared
tablero[4][2] = pared
tablero[5][4] = pared

filas = len(tablero)
columnas = len(tablero)                                 #quitar el 0

# Mostrar tablero
def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila)) 
    print()

# Encontrar raton
def buscar_raton(tablero):
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == raton:
                return i, j
    return None, None

# Encontrar gato
def buscar_gato(tablero):
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == gato:
                return i, j
    return None, None 

# Contar quesos
def contar_quesos(tablero):
    total = 0
    for fila in tablero:
        total += fila.count(queso)
    return total

quesos_restantes = contar_quesos(tablero)

# Mover el raton
def mover_raton(tablero, direccion):
    global quesos_restantes

    i, j = buscar_raton(tablero)
    if i is None:
        return False

    if direccion == arriba:
        df, dc = -1, 0
    elif direccion == abajo:
        df, dc = 1, 0
    elif direccion == izquierda:
        df, dc = 0, -1
    elif direccion == derecha:
        df, dc = 0, 1
    else:
        print("solo puedes usar 8, 2, 4 o 6")
        return False

    nueva_fila = i + df
    nueva_col = j + dc

    if not (0 <= nueva_fila < filas and 0 <= nueva_col < columnas):
        print("no puedes salirte del tablero")
        return False

    destino = tablero[nueva_fila][nueva_col]

    if destino == pared:
        print("no puedes pasar por la pared")
        return False
    if destino == gato:
        print("el gato esta ahi")
        return False
    if destino == queso:
        print("comiste un queso")
        quesos_restantes -= 1

    tablero[i][j] = camino
    tablero[nueva_fila][nueva_col] = raton
    return True

# Copiar el tablero
def copiar_tablero(tablero):
    copia = []
    for fila in tablero:        #necesita calcular que pasaria
        copia.append(fila[:])
    return copia

# Movimientos validos del gato
def movimientos_gato(tablero):
    fila, col = buscar_gato(tablero)
    movimientos = []
    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nf = fila + df
        nc = col + dc
        if 0 <= nf < filas and 0 <= nc < columnas:
            if tablero[nf][nc] not in [pared, queso]:
                movimientos.append((nf, nc))
    return movimientos

# Movimientos validos del raton
def movimientos_raton(tablero):
    fila, col = buscar_raton(tablero)
    #gato_fila, gato_col = buscar_gato(tablero)

    movimientos = []
    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nf = fila + df
        nc = col + dc
        if 0 <= nf < filas and 0 <= nc < columnas:
            if tablero[nf][nc] not in [pared, gato] and (nf, nc):
                movimientos.append((nf, nc))
    return movimientos

# da un puntaje a cada jugada
def evaluar_tablero(tablero):
    fg, cg = buscar_gato(tablero)
    fr, cr = buscar_raton(tablero)

    if fg is None or fr is None:
        return -9999

    distancia = abs(fg - fr) + abs(cg - cr)

    if distancia == 0:
        return 9999

    return 100 - distancia

# Movimiento del gato con minimax
def mover_gato_minimax(tablero, profundidad):
    def minimo_maximo(tablero_actual, profundidad, turno_gato):
        puntos = evaluar_tablero(tablero_actual)
        if profundidad == 0 or abs(puntos) >= 9000:
            return puntos, None

        if turno_gato:
            mejor = -float('inf')
            mejor_mov = None
            for mov in movimientos_gato(tablero_actual):
                copia = copiar_tablero(tablero_actual)
                fg, cg = buscar_gato(copia)
                if mov == buscar_raton(copia):
                    return 9999, mov
                copia[fg][cg] = camino
                copia[mov[0]][mov[1]] = gato
                evaluacion, _ = minimo_maximo(copia, profundidad - 1, False)
                if evaluacion > mejor:
                    mejor = evaluacion
                    mejor_mov = mov
            return mejor, mejor_mov
        else:
            peor = float('inf')
            for mov in movimientos_raton(tablero_actual):
                copia = copiar_tablero(tablero_actual)
                fr, cr = buscar_raton(copia)
                copia[fr][cr] = camino
                copia[mov[0]][mov[1]] = raton
                evaluacion, _ = minimo_maximo(copia, profundidad - 1, True)
                if evaluacion < peor:
                    peor = evaluacion
            return peor, None

    _, mejor_movimiento = minimo_maximo(tablero, profundidad, True)

    if mejor_movimiento is None:
        return False, False

    fg, cg = buscar_gato(tablero)
    nf, nc = mejor_movimiento

    atrapado = tablero[nf][nc] == raton

    tablero[fg][cg] = camino
    tablero[nf][nc] = gato

    return True, atrapado

# Inprimir el juego
mostrar_tablero(tablero)

# bucle principal del juego
while True:
    try:
        mov = int(input("mover raton (8=arriba, 2=abajo, 4=izquierda, 6=derecha): "))
    except:
        print("solo puedes poner 8, 2, 4 o 6")
        continue

    if mover_raton(tablero, mov):
        # mostrar_tablero(tablero)
        if quesos_restantes == 0:
            print("¡ganaste! 🎉 el raton comio todos los quesos")
            break

        se_movio, atrapado = mover_gato_minimax(tablero, 3)
        if se_movio:
            print("el gato se movio 🐱")
            mostrar_tablero(tablero)
        if atrapado:
            print("el gato atrapo al raton 😿 game over")
            break


 