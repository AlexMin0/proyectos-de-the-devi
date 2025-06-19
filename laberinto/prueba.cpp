#include <iostream>    //entrada y salida
#include <vector>      //vector de vectores
#include <queue>       // cola para BFS
#include <cstdlib>     // funciones aleatorias
#include <ctime>        // para inicializar la semilla del mundo aleatoria

using namespace std;

//variables para el laberinto
char muro = '#';     
char camino = ' ';   
char entrada = 'E';  
char salida = 'S';   
char ruta = '*';     

// tamaño del laberinto
int filas = 10;
int columnas = 10;

// movimientos arriba, abajo, izquierda, derecha
int mover_fila[4] = {-1, 1, 0, 0};
int mover_columna[4] = {0, 0, -1, 1};

// funcion que revisa si la casilla no es un muro
bool es_valido(int f, int c, vector<vector<char>>& laberinto) {   
    return laberinto[f][c] != muro;
}

// funcion que genera un camino asegurado desde la entrada hasta la salida
void generar_laberinto(vector<vector<char>>& laberinto) {
    int total_filas = filas + 2;       
    int total_columnas = columnas + 2;

    // lleno de muros el laberinto
    laberinto = vector<vector<char>>(total_filas, vector<char>(total_columnas, muro));

    // posicion de donde a donde empezar generar el laberinto
    int f = 1, c = 1;
    laberinto[f][c] = camino;

    // genera un camino aleatorio desde la entrada hasta la salida
    while (f != filas || c != columnas) {
        if (f < filas && (rand() % 2 == 0 || c == columnas)) {   
            f++; 
        } else if (c < columnas) {
            c++; 
        }
        laberinto[f][c] = camino; // marca el camino
    }



    // rellena el laberinto con caminos y muros aleatorios
    for (int i = 1; i <= filas; i++) {  // recorrer
        for (int j = 1; j <= columnas; j++) {
            if (laberinto[i][j] != camino) {
                // poner mas cainos que muros
                laberinto[i][j] = (rand() % 3 != 0) ? camino : muro; // iinveztigar ? 
            }
        }
    }

    // posicionar la slida y entrada
    laberinto[1][1] = entrada;
    laberinto[filas][columnas] = salida;
}

// busca un camino mas corto 
bool resolver_laberinto(vector<vector<char>>& laberinto) {
    int total_filas = filas + 2;
    int total_columnas = columnas + 2;  // investigar

    // marca que casillas ya se visitaron
    vector<vector<bool>> visitado(total_filas, vector<bool>(total_columnas, false));

    // guarda por donde se llego a cada casilla
    vector<vector<pair<int, int>>> anterior(total_filas, vector<pair<int, int>>(total_columnas, {-1, -1}));

    // cola para explorar
    queue<pair<int, int>> cola;

    // comienza en la entrada
    cola.push({1, 1});  // push es como un append
    visitado[1][1] = true;

    // bucle BFS para recorrer 
    while (!cola.empty()) {
        int f = cola.front().first;
        int c = cola.front().second;
        cola.pop();   // elimina de las opciones

        // termina cuando llega a la salida
        if (f == filas && c == columnas) break;

        // prueba morverse en 4 direcciones
        for (int i = 0; i < 4; i++) {
            int nueva_f = f + mover_fila[i];
            int nueva_c = c + mover_columna[i];

            // ver si es que se puede abanzar por esa casilla
            if (es_valido(nueva_f, nueva_c, laberinto) && !visitado[nueva_f][nueva_c]) {
                visitado[nueva_f][nueva_c] = true;
                anterior[nueva_f][nueva_c] = {f, c}; 
                cola.push({nueva_f, nueva_c});
            }
        }
    }

    // recorre el camino ya correcto 
    int f = filas, c = columnas;
    while (anterior[f][c].first != -1) {
        int anterior_f = anterior[f][c].first;
        int anterior_c = anterior[f][c].second;

        // marca el camino corecto
        if (laberinto[anterior_f][anterior_c] != entrada) laberinto[anterior_f][anterior_c] = ruta;

        f = anterior_f;
        c = anterior_c;
    }

    return true;
}

// imprime el laberinto completito
void mostrar_laberinto(const vector<vector<char>>& laberinto) {
    for (const auto& fila : laberinto) {   
        for (char celda : fila) cout << celda;
        cout << '\n';
    }
}

// se empieza a ejecucion del programa
int main(int argc, char* argv[]) {
    srand(time(0));
    if (argc == 3) {    
        filas = atoi(argv[1]);  // atoi y argv  scrand
        columnas = atoi(argv[2]);
    }

    vector<vector<char>> laberinto;  // dclaracion del laberinto como caracteres

    // lamo a las funciones
    generar_laberinto(laberinto);
    //resolver_laberinto(laberinto);
    mostrar_laberinto(laberinto);

    return 0; // fin del programa
}

