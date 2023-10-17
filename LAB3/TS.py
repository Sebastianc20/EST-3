class TS:
    def cifrar_transposicion(self, mensaje, clave):
        # Crear una matriz vacía con el número de columnas igual a la longitud de la clave
        columnas = len(clave)
        filas = (len(mensaje) + columnas - 1) // columnas
        matriz = [[' ' for _ in range(columnas)] for _ in range(filas)]

        # Llenar la matriz con el mensaje
        fila_actual, columna_actual = 0, 0
        for letra in mensaje:
            matriz[fila_actual][columna_actual] = letra
            columna_actual += 1
            if columna_actual == columnas:
                columna_actual = 0
                fila_actual += 1

        # Crear el mensaje cifrado leyendo la matriz por columnas en el orden de la clave
        mensaje_cifrado = ''
        orden_clave = sorted(range(columnas), key=lambda x: clave[x])
        for columna in orden_clave:
            for fila in range(filas):
                mensaje_cifrado += matriz[fila][columna]

        return mensaje_cifrado

    def descifrar_transposicion(self, mensaje_cifrado, clave):
        # Crear una matriz vacía con el número de columnas igual a la longitud de la clave
        columnas = len(clave)
        filas = (len(mensaje_cifrado) + columnas - 1) // columnas
        matriz = [[' ' for _ in range(columnas)] for _ in range(filas)]

        # Obtener el orden de las columnas de la clave
        orden_clave = sorted(range(columnas), key=lambda x: clave[x])

        # Calcular el número de letras en la última fila
        letras_ultima_fila = len(mensaje_cifrado) % filas

        # Calcular el número de filas completas
        filas_completas = filas - letras_ultima_fila

        # Llenar la matriz con el mensaje cifrado
        idx = 0
        for columna in orden_clave:
            if columna < letras_ultima_fila:
                for fila in range(filas):
                    matriz[fila][columna] = mensaje_cifrado[idx]
                    idx += 1
            else:
                for fila in range(filas_completas):
                    matriz[fila][columna] = mensaje_cifrado[idx]
                    idx += 1

        # Crear el mensaje descifrado leyendo la matriz por filas
        mensaje_descifrado = ''
        for fila in range(filas):
            for columna in range(columnas):
                mensaje_descifrado += matriz[fila][columna]

        return mensaje_descifrado
