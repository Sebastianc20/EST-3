class NodoArbolB:
    def __init__(self, es_hoja=True, max_claves=3):
        self.es_hoja = es_hoja
        self.claves = []
        self.datos = []
        self.hijos = []
        self.padre = None
        self.max_claves = max_claves

    def insertar(self, clave, persona):
        if self.es_nodo_lleno():
            # Dividir el nodo si está lleno
            self.dividir_nodo()

        if self.es_hoja:
            indice_insercion = 0
            while indice_insercion < len(self.claves) and clave > self.claves[indice_insercion]:
                indice_insercion += 1

            self.claves.insert(indice_insercion, clave)
            self.datos.insert(indice_insercion, persona)
        else:
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1

            if indice_hijo < len(self.hijos):
                self.hijos[indice_hijo].insertar(clave, persona)
            else:
                nuevo_hijo = NodoArbolB(self.es_hoja, self.max_claves)
                nuevo_hijo.insertar(clave, persona)
                self.hijos.append(nuevo_hijo)
                nuevo_hijo.padre = self

    def dividir_nodo(self):
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
            nuevo_padre = NodoArbolB(False, self.max_claves)
            nuevo_padre.claves.append(nueva_clave)
            nuevo_padre.hijos.append(self)
            nuevo_padre.hijos.append(nuevo_nodo)

            self.padre = nuevo_padre
            nuevo_nodo.padre = nuevo_padre
        else:
            self.padre.insertar(nueva_clave, nueva_persona)

    def es_nodo_lleno(self):
        return len(self.claves) >= self.max_claves


class ArbolB:
    def __init__(self, orden):
        self.raiz = NodoArbolB(True, orden)
        self.orden = orden

    def insertar(self, clave, persona):
        self.raiz.insertar(clave, persona)

    def eliminar(self, clave):
        pass

    def actualizar(self, clave, nueva_persona):
        pass

    def buscar(self, clave):
        pass


# Uso del árbol B
T = 2
arbol_b = ArbolB(T)
