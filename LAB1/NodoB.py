"""class NodoArbolB:
    def __init__(self, es_hoja=True):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.datos = []

    def dividir_nodo(self, indice_hijo):
        nuevo_nodo = NodoArbolB(self.es_hoja)

        # Mover la mitad de las claves y datos al nuevo nodo
        medio = len(self.claves) // 2
        nueva_clave = self.claves[medio]
        nueva_persona = self.datos[medio]

        nuevo_nodo.claves = self.claves[medio + 1:]
        nuevo_nodo.datos = self.datos[medio + 1:]
        self.claves = self.claves[:medio]
        self.datos = self.datos[:medio]

        # Si no es un nodo hoja, también mueve los hijos
        if not self.es_hoja:
            nuevo_nodo.hijos = self.hijos[medio + 1:]
            self.hijos = self.hijos[:medio + 1]

        # Insertar la nueva clave y el nuevo nodo en el nodo padre
        if self.padre is None:
            # Si no tiene un nodo padre, crea uno nuevo
            nuevo_padre = NodoArbolB()
            nuevo_padre.claves.append(nueva_clave)
            nuevo_padre.hijos.append(self)
            nuevo_padre.hijos.append(nuevo_nodo)

            # Establecer el nuevo padre como padre de ambos nodos
            self.padre = nuevo_padre
            nuevo_nodo.padre = nuevo_padre
        else:
            # Insertar en el nodo padre existente
            self.padre.insertar(nueva_clave, nueva_persona, nuevo_nodo)

    
    # Implementación de búsqueda
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

    # Implementación de inserción
    def insertar(self, clave, persona):
        if self.es_nodo_lleno():
            # Dividir el nodo si está lleno
            # Implementa la división del nodo aquí
            pass

        if self.es_hoja:
            # Insertar la clave y el dato en el nodo hoja
            self.claves.append(clave)
            self.datos.append(persona)
            self.claves.sort()
        else:
            # Encontrar el hijo adecuado y continuar la inserción
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1
            self.hijos[indice_hijo].insertar(clave, persona)
    
    # Implementación de eliminación
    def eliminar(self, clave):
        if not self.es_hoja:
            # Encontrar el hijo adecuado y continuar la eliminación
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1
            self.hijos[indice_hijo].eliminar(clave)
        else:
            # Eliminar la clave y el dato del nodo hoja
            if clave in self.claves:
                indice = self.claves.index(clave)
                del self.claves[indice]
                del self.datos[indice]
    
    # Implementación de actualización
    def actualizar(self, clave, nueva_persona):
        if not self.es_hoja:
            # Encontrar el hijo adecuado y continuar la actualización
            indice_hijo = 0
            while indice_hijo < len(self.claves) and clave > self.claves[indice_hijo]:
                indice_hijo += 1
            self.hijos[indice_hijo].actualizar(clave, nueva_persona)
        else:
            # Actualizar la clave y el dato en el nodo hoja
            if clave in self.claves:
                indice = self.claves.index(clave)
                self.datos[indice] = nueva_persona"""
