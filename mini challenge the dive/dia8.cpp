// Dia 8 - Suma de numeros en C++
// Escribir un programa que pida al usuario dos números y los sume. ¡Pero
// esta vez hazlo en C++! :)


#include <iostream>
using namespace std;

int main() {
    // que los numeros sean enteros
    int numero1, numero2, suma;

    // preguntar que se va asumar
    cout << "primer sumero a sumar";
    cin >> numero1;

    cout << "segundo numero a ser sumado";
    cin >> numero2;

    // sumar los numeros dados
    suma = numero1 + numero2;

    // imprimer el resultado
    cout << "el total es " << suma << endl;

    return 0;
}

