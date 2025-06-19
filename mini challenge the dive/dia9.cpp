// // Dia 09 - Ordenamiento de un Array
// // Escribir un programa que ordene un array de enteros utilizando ¡Pero
// // hazlo en C++! :)

// #include <iostream>
// #include <algorithm> // para porder usar sort que hace que ordene d emenor a mayor
// using namespace std;

// int main() {
//     // establecer los numeros a ser ordenados
//     int numeros[] = {5, 2, 9, 1, 3};
//     int tamano = 5;

//     // Ordena el array de forma automatica
//     sort(numeros, numeros + tamano);

//     // imprimir el arrary 
//     cout << "Array ordenado: ";
//     for (int i = 0; i < tamano; i++) {
//         cout << numeros[i] << " ";
//     }
//     cout << endl;

//     return 0;
// }



// Dia 10 - Palíndromo
// Escribir un programa que determine si una cadena de caracteres ingresada
// por el usuario es un palíndromo ¡Pero hazlo en C++! :)


#include <iostream>
#include <string>

using namespace std;

int main() {
    string texto, invertido = "";
    
    cout << "Ingresa una palabra: ";
    cin >> texto;

    // Crear la versión invertida del texto
    for (int i = texto.length() - 1; i >= 0; i--) {
        invertido += texto[i];
    }

    // Comparar si es igual al original
    if (texto == invertido) {
        cout << "Es un palindromo" << endl;
    } else {
        cout << "No es un palindromo" << endl;
    }

    return 0;
}