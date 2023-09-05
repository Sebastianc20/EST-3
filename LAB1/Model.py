class NodoArbolB:
    def __init__(self, es_hoja=True, max_claves=3):
        self.es_hoja = es_hoja
        self.claves = []
        self.datos = []
        self.hijos = []
        self.max_claves = max_claves  # Establece el límite de claves en el nodo

    def insertar(self, clave, persona):
        if self.es_nodo_lleno():
            # Dividir el nodo si está lleno
            self.dividir_nodo()

        if self.es_hoja:
            # Insertar la clave y el dato en el nodo hoja
            indice_insercion = 0
            while indice_insercion < len(self.claves) and clave > self.claves[indice_insercion]:
                indice_insercion += 1

            self.claves.insert(indice_insercion, clave)
            self.datos.insert(indice_insercion, persona)
        else:
            # Encontrar el hijo adecuado y continuar la inserción
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1

            # Realizar búsqueda en el hijo correspondiente
            if indice_hijo < len(self.hijos):
                self.hijos[indice_hijo].insertar(clave, persona)
            else:
                # Esto podría ocurrir si la clave es mayor que todas las claves del nodo
                # En ese caso, debemos insertar en el último hijo
                self.hijos[-1].insertar(clave, persona)

    def dividir_nodo(self):
        # Dividir el nodo en dos partes aproximadamente iguales
        medio = len(self.claves) // 2

        nueva_clave = self.claves[medio]
        nueva_persona = self.datos[medio]

        nuevo_nodo = NodoArbolB(self.es_hoja, self.max_claves)

        nuevo_nodo.claves = self.claves[medio + 1:]
        nuevo_nodo.datos = self.datos[medio + 1:]
        self.claves = self.claves[:medio]
        self.datos = self.datos[:medio]

        if not self.es_hoja:
            nuevo_nodo.hijos = self.hijos[medio + 1:]
            self.hijos = self.hijos[:medio + 1]

        if self.padre is None:
            # Si no tiene un nodo padre, crea uno nuevo
            nuevo_padre = NodoArbolB(False, self.max_claves)
            nuevo_padre.claves.append(nueva_clave)
            nuevo_padre.hijos.append(self)
            nuevo_padre.hijos.append(nuevo_nodo)

            self.padre = nuevo_padre
            nuevo_nodo.padre = nuevo_padre
        else:
            # Insertar en el nodo padre existente
            self.padre.insertar(nueva_clave, nueva_persona, nuevo_nodo)
            
    
    def buscar(self, clave):
        if clave in self.claves:
            indice = self.claves.index(clave)
            return self.datos[indice]
        elif not self.es_hoja:
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1

            if indice_hijo < len(self.hijos):
                return self.hijos[indice_hijo].buscar(clave)
            else:
                return None
        else:
            return None

    # Otras funciones como  eliminar, etc.

class ArbolB:
    def __init__(self, orden):
        self.raiz = NodoArbolB(False, orden)  # Inicialmente, la raíz no es un nodo hoja
        self.orden = orden

    def insertar(self, clave, persona):
        self.raiz.insertar(clave, persona)

    def eliminar(self, clave):
        # Implementa la eliminación en el árbol B aquí
        pass

    def actualizar(self, clave, nueva_persona):
        # Implementa la actualización en el árbol B aquí
        pass

    def buscar(self, clave):
        return self.raiz.buscar(clave)

# Uso del árbol B
T = 2  # Orden del árbol B (ajusta según tus necesidades)
arbol_b = ArbolB(T)
