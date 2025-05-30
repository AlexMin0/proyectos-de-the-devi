'''====definiendo variables==='''
pared = "🧱"
camino = "⬛"
queso = "🧀"
raton = "🐭"
gato = "🐱"

# movimientos simples
arriba = 8
izquierda = 4
derecha = 6
abajo = 2 

# movimiento en diagonal
arriba_derecha = 9
arriba_izquierda = 7 
abajo_derecha = 3
abajo_izquierda = 1


# saludo de bienvenida
print("Bienvenidos a")
print("🐈‍Tom y Jerry🐁")

'''===creando tablero==='''

# crear tablero donde se pueda jugar
tablero = [
    [queso , camino, camino, pared, camino, raton],
    [camino, pared, camino, camino, camino, pared],
    [camino, camino, pared, camino, camino, camino],
    [queso,camino,camino,camino, pared, camino],
    [pared, camino, pared, queso, camino, camino],
    [gato, camino, camino, camino, pared, camino]
]

# contar cuanto por cuanto es el tablero
filas = len(tablero)
columnas = len(tablero[0])


# funcion para imprimir el campo de batalla
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))   

# buscar la posicion inicial del raton
def encontrar_raton(tablero):
     for i, fila in enumerate(tablero):   #porque use enumerate porque encontre una forma mas facil y con menos errores en vez de usar range(len())
        for j, celda in enumerate(fila):   
            if celda == raton:
                return i, j
     return None, None 

def encontrar_gato(tablero):
    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if celda == gato:
                return i, j
    return None, None

'''===definiciones del juego==='''

# 🧀 Contar cuantos quesos hay en el tablero
def contar_quesos(tablero):
    return sum(fila.count(queso) for fila in tablero)

quesos_restantes = contar_quesos(tablero)
quesos_iniciales = quesos_restantes  # guardar el numero inicial de quesos

# mover el raton si es posible
def mover_raton(tablero, direccion):
    global quesos_restantes  # usamos la variable global para modificar la cantidad de queso

    i, j = encontrar_raton(tablero)
    if i is None:
        return False
    
        # Determinar si los movimientos diagonales están habilitados
    quesos_comidos = quesos_iniciales - quesos_restantes
    movimientos_permitidos = [arriba, abajo, izquierda, derecha]
    if quesos_comidos >= 2:  # Habilitar diagonales despus de comer 2 quesos
        movimientos_permitidos.extend([arriba_derecha, arriba_izquierda, abajo_derecha, abajo_izquierda]) 
        # extend es para agregar varios movimientos a la ves y porque no append porque agrega sola de a uno

    # Validar direccion
    if direccion not in movimientos_permitidos:
        if direccion in [arriba_derecha, arriba_izquierda, abajo_derecha, abajo_izquierda]:
            print("evolucion del raton al comer 2 quesos🧀")
        else:
            print("favor solo usar las teclas establecidas")
        return False
    
#===direcciones del juego===

    ci, cj = 0, 0   #ci es cambio de fila y cj cambio de columna
    if direccion == arriba:
        ci = -1 
    elif direccion == abajo:
        ci = 1
    elif direccion == izquierda:
        cj = -1
    elif direccion == derecha:
        cj = 1
    elif direccion == arriba_derecha:
        ci, cj = -1, 1
    elif direccion == arriba_izquierda:
        ci, cj = -1, -1
    elif direccion == abajo_derecha:
        ci, cj = 1, 1
    elif direccion == abajo_izquierda:
        ci, cj = 1, -1
 
    ni, nj = i + ci, j + cj    #la n significa nuevo y la i columno aisque le aigne como nombre nueva fila = ni lo mismmo con nj nnueva columna

#===limitaciones===

    # la nada😨
        # evitar que el raton salga del tablero 
    if ni < 0 or ni >= filas or nj < 0 or nj >= columnas:
        print("no hay camino por donde ir 🚫")
        return False 
    
    #pared🧱
    if tablero[ni][nj] == pared:
        print("chocaste contra una pared😵‍💫")
        return False
    
    # gato 🐱
    if tablero[ni][nj] == gato:
        print("es el gato huye")
        return False

    #queso🧀
    if tablero[ni][nj] == queso:
        print("encontraste un queso🧀")
        quesos_restantes -= 1

        # movimientos validos
    tablero[i][j] = camino
    tablero[ni][nj] = raton
    return True  # return true sifnifica que el camino esta sibre y puede pasar entonces return false seria lo contrario

'''===movimiento del gato y minimax==='''

# funcion para mover el gato hacia el raton
def mover_gato(tablero):
    gi, gj = encontrar_gato(tablero)
    ri, rj = encontrar_raton(tablero)  # Obtener la posición actual del ratón

    estado = GameState(tablero, (gi, gj), (ri, rj))
    mejor_calculo = float('-inf')  #es para comenzar de la peor forma para luego hacer una jugada mejor
    mejor_movimiento = None
                   
    for move in estado.get_possible_moves(True):  # .get_possible_moves da el movimiento para hacer
        calculo = minimax(estado.make_move(move, True), 3, False)  # profundidad 3 es el cuanto sea la distancia a calcular  make ve las consecuencias
        if calculo > mejor_calculo:
            mejor_calculo = calculo
            mejor_movimiento = move # move para ver los posibles movimientos del gato

    if mejor_movimiento:
        ni, nj = mejor_movimiento

        global contenido_debajo_del_gato # global se usa para modificas sierto contenido
        tablero[gi][gj] = contenido_debajo_del_gato
        contenido_debajo_del_gato = tablero[ni][nj]
        tablero[ni][nj] = gato

        atrapa = (ni, nj) == (ri, rj)
        return True, atrapa

    return False, False


# minimax 

class GameState: #es el que ayuda al algoritmo a pensar
    def __init__(self, tablero, gato_pos, raton_pos, profundidad=3):
        self.tablero = tablero
        self.gato_pos = gato_pos
        self.raton_pos = raton_pos
        self.profundidad = profundidad #cuantas movimientos en adelante mirara el algoritmo

    def is_terminal(self): # ve si las posisiones son iguales
        return self.gato_pos == self.raton_pos  #self es para agregar tal cosa a tal cosa

    def evaluate(self):  # self es para ver datos
        gi, gj = self.gato_pos
        ri, rj = self.raton_pos
        return -abs(gi - ri) - abs(gj - rj)  
#abs calcula la distancia de manhattan y la multiplica por -1

    def get_possible_moves(self, is_maximizing):  # es una buleano para maximizar
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
        gi, gj = self.gato_pos if is_maximizing else self.raton_pos
        posibles = []

        for ci, cj in movimientos:
            ni, nj = gi + ci, gj + cj
            if 0 <= ni < len(self.tablero) and 0 <= nj < len(self.tablero[0]):
                if self.tablero[ni][nj] != pared:
                    posibles.append((ni, nj))
        return posibles

    def make_move(self, move, is_maximizing):
        if is_maximizing:
            return GameState(self.tablero, move, self.raton_pos)
        else:
            return GameState(self.tablero, self.gato_pos, move)

def minimax(state, depth, is_maximizing):
    if state.is_terminal() or depth == 0:
        return state.evaluate()

    if is_maximizing:
        max_eval = float('-inf')
        for move in state.get_possible_moves(True):
            eval = minimax(state.make_move(move, True), depth - 1, False)
            max_eval = max(max_eval, eval) #max es la mejor jugada que va a dar y min lo contrario
        return max_eval
    else:
        min_eval = float('inf')
        for move in state.get_possible_moves(False):  #state mira toda la informacion del juego 
            eval = minimax(state.make_move(move, False), depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

imprimir_tablero(tablero)  #imprime el tablero
contenido_debajo_del_gato = camino

'''===bucle principal del juego==='''
while True:
    try:  # sirva para cuando pasa una error no se rompa 
        prompt = "Mover raton (8=arriba, 2=abajo, 4=izquierda, 6=derecha"
        if quesos_iniciales - quesos_restantes >= 2:
            prompt += ", 9=arriba_derecha, 7=arriba_izquierda, 3=abjo_derecha, 1=abjo_izquuierda"
        prompt += "): "  # += es para agregar algo ma al texto = no funciona asi ya que ese cambia por completo
        mover = int(input(prompt)) #prompt es para imprimir asi como esta escrito 
    except ValueError:  #se usa para que el programa no se rompa cuando el usuario escriba string y no un numero
        # valueerror es para que el jugador no meta letras en vez de numero
        print("favor solo usar las teclas establecidas")
        continue

    if mover_raton(tablero, mover):
        imprimir_tablero(tablero)  #imprime los movimientos del raton


        # ver si gana el raton al comer todos los quesos
        if quesos_restantes == 0:
            print("🎉 ¡Ganaste! El raton se comio todos los quesos 🧀🐭")
            break

        # el gato gana?
        gato_moved, gato_atrapo = mover_gato(tablero)
        if gato_moved:
            print("¡El gato se mueve! 🐱")
            imprimir_tablero(tablero)
        
        #el raton pierde
        if gato_atrapo:
            print("El gato atrapo al raton",
            "game over ")
            break





