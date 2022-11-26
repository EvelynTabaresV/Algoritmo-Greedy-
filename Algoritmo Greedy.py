# ______ALGORITMO________

def greedy(costo, peso, tipo_parada, valor_parada, operador_parada, restriccion_peso, vector_restricciones,
           valores, operadores, c, s_x, solucion, tipo, orden):

    if tipo == 1: # modifica el vector con el que se trabaja dependiendo del tipo de vector elegido
        vector = costo
        tipo_vector = "COSTO"
    elif tipo == 2:
        vector = peso
        tipo_vector = "PESO"
    elif tipo == 3:
        vector = relacion_costo_peso(costo, peso)
        tipo_vector = "COSTO/PESO"
    else:
        print("El tipo de vector debe estar entre 1 y 3, intentelo de nuevo")
        return

    if orden == 2: # Modifica el orden en el que se organiza
        orden = True # argumento de la función sorted, ordena de manera descendente
        tipo_orden = "MAYOR"
    elif orden == 1:
        orden = False
        tipo_orden = "MENOR"
    else:
        print("El orden del vector debe estar entre 1 y 2, intentelo de nuevo")
        return

# ________________________________________
    # variable con vector de tipo y orden elegido
    vector_ordenado = sorted(vector, reverse=orden)
    i = 0 # recorre el vector_ordenado y sirve para el print
    print("\n   X-N       Vector C - {x}    ", "                 Vector S + {x}     ",
          "            Vector solución ", "        Costo ", "Peso")

    print(i, "|", "N", "|", c, "|", s_x, "|", solucion, "| ", suma_producto(solucion, costo),
          " |", suma_producto(solucion, peso))

    while suma_producto(peso, solucion) < restriccion_peso: # comprueba que no se supere la restricción de peso

        # cambia la posición desde donde el index busca en el vector un valor que concuerde con
        # el solicitado, evita que tome siempre el mismo producto
        # si es igual a 0 quiere decir que el producto ya fue tomado anteriormente
        posicion = 0
        while c[vector.index(vector_ordenado[i], posicion)] == 0:
            posicion = posicion + 1
        numero_producto = vector.index(vector_ordenado[i], posicion)
        c[vector.index(vector_ordenado[i], posicion)] = 0 # borra en el vector C
        s_x[vector.index(vector_ordenado[i], posicion)] = 1 # Añade en el vector S_x

# _______________________________________________
        # verifica que cumpla las condiciones antes de añadir al vector solución
        # Si cumple TODAS las restricciones añade el producto, sino lo borra
        if suma_producto(peso, solucion) < restriccion_peso \
                and verificar_restricciones(vector_restricciones, s_x, valores, operadores):

            solucion[vector.index(vector_ordenado[i], posicion)] = 1  # Añade en el vector solucion
        else:
            s_x[vector.index(vector_ordenado[i], posicion)] = 0  # Borra en el vector S_x


# _____________________________________________________

        print(i+1, "|", numero_producto+1, "|", c, "|", s_x, "|", solucion, "| ", suma_producto(solucion, costo),
              " |", suma_producto(solucion, peso))

# _____________________________________________________
        # comprueba que el vector solución actual sea una solución
        if parada(tipo_parada, valor_parada, operador_parada, solucion, peso, costo) \
                and suma_producto(peso, solucion) <= restriccion_peso \
                and verificar_restricciones(vector_restricciones, solucion, valores, operadores):
            print("______________________________________________", tipo_orden, tipo_vector,
                  "______________________________________________")
            print("¡Solución encontrada!")
            print("\nCosto:", producto(solucion, costo), "=", suma_producto(solucion, costo))
            print("Peso: ", producto(solucion, peso), " =", suma_producto(solucion, peso))
            print("______________________________________________")
            print("Peso máximo:          ", restriccion_peso)
            print("Condición de parada: >", valor_parada)

            return
# _________________________________________________

        if c[vector.index(vector_ordenado[i], posicion)] == 0:
            i = i + 1
    print("______________________________________________", tipo_orden, tipo_vector,
          "______________________________________________")
    print("\nNo se encontró una solución")

# __________FIN______________

# ____________INTERFAZ___________

def interfaz():
    print("______________________________________________METAHEURÍSTICA_GREEDY",
          "______________________________________________\n")
    opcion = int(input("Ingrese 1 para seleccionar valores manualmente, de lo contrario ingrese 0: "))

    # Vector que almacena los vectores restricción
    vector_restricciones = []

    if opcion == 1:
        cantidad_productos = int(input("Ingrese la cantidad de productos: "))
        costo = []
        peso = []

        i = 0
        while i < cantidad_productos:
            print("Ingrese el costo del producto ", i + 1, ": ")
            costo.append(int(input()))
            print("Ingrese el peso del producto ", i + 1, ": ")
            peso.append(int(input()))
            i = i + 1

        ingresar_restricciones = (int(input("¿Desea ingresar restricciones a los productos?\n1 = si, 0 = no: ")))
        valores = []
        operadores = []
        while ingresar_restricciones == 1:
            i = 0
            restriccion = []
            while i < cantidad_productos:
                print("Ingrese la restricción del producto ", i + 1, ": ")
                restriccion.append(int(input()))
                i = i + 1
            operadores.append(input("Ingrese el operador lógico de restricción: "))
            valores.append(int(input("Ingrese el valor de restricción: ")))
            vector_restricciones.append(restriccion)
            ingresar_restricciones = int(input("¿Desea ingresar más restricciones a los productos? \n 1 = si, 0 = no: "))



        restriccion_peso = int(input("Ingrese el peso maximo de la mochila: "))
        tipo_parada = int(input("Ingrese la condición de parada: 1 = peso, 2 = costo: "))
        valor_parada = int(input("Ingrese el valor de parada: "))
        operador_parada = input("Ingrese el operador lógico de la restricción de parada: ")
        tipo = int(input("Elegir por costo: 1, peso: 2, relacion costo/peso: 3\n"))
        orden = int(input("Ordenar de manera ascendente: 1, descendente: 2\n"))

        c = rellenar_vector(cantidad_productos, True) #Debe iniciar siempre con sus valores en 1
        s_x = rellenar_vector(cantidad_productos, False) #Debe iniciar siempre con sus valores en 0
        solucion = rellenar_vector(cantidad_productos, False) #Debe iniciar siempre con sus valores en 0

        greedy(costo, peso, tipo_parada, valor_parada, operador_parada, restriccion_peso, vector_restricciones,
               valores, operadores, c, s_x, solucion, tipo, orden)
    else:
        costo = [5, 6, 6, 3, 6, 14, 10, 4, 10, 9]
        peso = [8, 4, 3, 11, 3, 15, 9, 8, 6, 12]
        restriccion_peso = 40
        tipo_parada = 1
        valor_parada = 30
        operador_parada = '>'
        vector_restricciones = [[0, 0, 0, -1, 0, 1, 0, 0, 0, 0], [0, 3, 0, -1, 0, 0, 0, 0, 0, 0]]
        operadores = ['<=', '<']
        valores = [0,2]

        c = rellenar_vector(len(costo), True)
        s_x = rellenar_vector(len(costo), False)
        solucion = rellenar_vector(len(costo), False)

        tipo = 2
        orden = 2

        greedy(costo, peso, tipo_parada, valor_parada, operador_parada, restriccion_peso, vector_restricciones, valores, operadores, c, s_x, solucion, tipo, orden)

# _______________FIN_______________

# ___________FUNCIONES____________

# devuelve un vector con el producto de los elementos de
# cada posición de los vectores
def producto(lista_1,lista_2):
    resultado = []
    i = 0
    while i < len(lista_1):
        resultado.append(lista_1[i] * lista_2[i])
        i = i + 1
    return resultado

# Es una función que hace el producto punto entre el vector solución y los vectores de
# peso y costo, da como resultado la suma de los elementos que se han "guardado en la mochila"
def suma_producto(lista_1,lista_2):
    resultado = 0
    j = 0
    while j < len(lista_1):
        resultado = resultado + producto(lista_1,lista_2)[j]
        j = j + 1
    return resultado

# Rellena los vectores con 1 y 0, opcion = True para 1, opcion = False para 0
# sirve para los vectores iniciales c, s_x y solucion
def rellenar_vector(tamaño, opcion):
    vector = []
    i = 0
    if opcion:
        while i < tamaño:
            vector.append(1)
            i = i + 1
    else:
        while i < tamaño:
            vector.append(0)
            i = i + 1
    return vector

# Realiza la relación entre costo y peso
def relacion_costo_peso(costo,peso):
    relacion = []
    i = 0
    while i < len(costo):
        relacion.append(costo[i] / peso[i])
        i = i + 1
    return relacion

# Comprueba los vectores de restricción ingresados
def verificar_restricciones(vector_restricciones, vector_s, valores, operadores):
    cumple = True
    for j in operadores:
        if j == '>=':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) >= valores[operadores.index(j)]):
                    cumple = False
                    break
        elif j == '<=':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) <= valores[operadores.index(j)]):
                    cumple = False
                    break
        elif j == '=':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) == valores[operadores.index(j)]):
                    cumple = False
                    break
        elif j == '<':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) < valores[operadores.index(j)]):
                    cumple = False
                    break
        elif j == '>':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) > valores[operadores.index(j)]):
                    cumple = False
                    break
        elif j == '!=':
            for i in vector_restricciones:
                if not (suma_producto(i, vector_s) != valores[operadores.index(j)]):
                    cumple = False
                    break

    return cumple


def parada(tipo_parada, valor_parada, operador, vector_solucion, peso, costo):
    cumple = True
    if tipo_parada == 1:
        vector_parada = peso
    else:
        vector_parada = costo
    if operador == '>=':
        if not suma_producto(vector_solucion, vector_parada) >= valor_parada:
            cumple = False
    elif operador == '<=':
        if not suma_producto(vector_solucion, vector_parada) <= valor_parada:
            cumple = False
    elif operador == '>':
        if not suma_producto(vector_solucion, vector_parada) > valor_parada:
            cumple = False
    elif operador == '<':
        if not suma_producto(vector_solucion, vector_parada) < valor_parada:
            cumple = False
    elif operador == '=':
        if not suma_producto(vector_solucion, vector_parada) == valor_parada:
            cumple = False
    elif operador == '!=':
        if not suma_producto(vector_solucion, vector_parada) != valor_parada:
            cumple = False

    return cumple

# __________FIN__________

interfaz()