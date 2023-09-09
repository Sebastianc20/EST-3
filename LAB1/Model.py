class NodoArbolAVL:
    def __init__(self, clave, persona):
        self.clave = clave
        self.persona = persona
        self.altura = 1
        self.izquierda = None
        self.derecha = None

class ArbolAVL:
    def __init__(self):
        self.raiz = None
        
    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def insertar(self, raiz, clave, persona):
        if not raiz:
            return NodoArbolAVL(clave, persona)

        if clave < raiz.clave:
            raiz.izquierda = self.insertar(raiz.izquierda, clave, persona)
        else:
            raiz.derecha = self.insertar(raiz.derecha, clave, persona)

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        # Casos de rotación
        if balance > 1:
            if clave < raiz.izquierda.clave:
                return self.rotacion_derecha(raiz)
            else:
                raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
                return self.rotacion_derecha(raiz)

        if balance < -1:
            if clave > raiz.derecha.clave:
                return self.rotacion_izquierda(raiz)
            else:
                raiz.derecha = self.rotacion_derecha(raiz.derecha)
                return self.rotacion_izquierda(raiz)

        return raiz

    def rotacion_izquierda(self, nodo_y):
        nodo_x = nodo_y.derecha
        nodo_z = nodo_x.izquierda

        nodo_x.izquierda = nodo_y
        nodo_y.derecha = nodo_z

        nodo_y.altura = 1 + max(self.altura(nodo_y.izquierda), self.altura(nodo_y.derecha))
        nodo_x.altura = 1 + max(self.altura(nodo_x.izquierda), self.altura(nodo_x.derecha))

        return nodo_x

    def rotacion_derecha(self, nodo_x):
        nodo_y = nodo_x.izquierda
        nodo_z = nodo_y.derecha

        nodo_y.derecha = nodo_x
        nodo_x.izquierda = nodo_z

        nodo_x.altura = 1 + max(self.altura(nodo_x.izquierda), self.altura(nodo_x.derecha))
        nodo_y.altura = 1 + max(self.altura(nodo_y.izquierda), self.altura(nodo_y.derecha))

        return nodo_y

    def buscar_por_nombre_y_id(self, raiz, nombre, id_persona):
        resultados = []

        if not raiz:
            return resultados

        if nombre == raiz.clave[0] and (id_persona is None or id_persona == raiz.clave[1]):
            resultados.append(raiz.persona)

        if nombre < raiz.clave[0] or (nombre == raiz.clave[0] and (id_persona is None or id_persona < raiz.clave[1])):
            resultados.extend(self.buscar_por_nombre_y_id(raiz.izquierda, nombre, id_persona))

        resultados.extend(self.buscar_por_nombre_y_id(raiz.derecha, nombre, id_persona))

        return resultados
    
    
    
    def actualizar_persona(self, raiz, clave, nuevos_datos):
        if not raiz:
            return None

        if clave < raiz.clave:
            raiz.izquierda = self.actualizar_persona(raiz.izquierda, clave, nuevos_datos)
        elif clave > raiz.clave:
            raiz.derecha = self.actualizar_persona(raiz.derecha, clave, nuevos_datos)
        else:
            # Encontramos la persona a actualizar
            persona = raiz.persona
            persona.Nombre = nuevos_datos.get("name", persona.Nombre)
            persona.Fecha_Nacimiento = nuevos_datos.get("dateBirth", persona.Fecha_Nacimiento)
            persona.Direccion = nuevos_datos.get("address", persona.Direccion)
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        # Casos de rotación
        if balance > 1:
            if clave < raiz.izquierda.clave:
                return self.rotacion_derecha(raiz)
            else:
                raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
                return self.rotacion_derecha(raiz)

        if balance < -1:
            if clave > raiz.derecha.clave:
                return self.rotacion_izquierda(raiz)
            else:
                raiz.derecha = self.rotacion_derecha(raiz.derecha)
                return self.rotacion_izquierda(raiz)

        return raiz
    
    
    
    def eliminar(self, raiz, clave):
        if not raiz:
            return raiz

        if clave < raiz.clave:
            raiz.izquierda = self.eliminar(raiz.izquierda, clave)
        elif clave > raiz.clave:
            raiz.derecha = self.eliminar(raiz.derecha, clave)
        else:
            # Encontramos el nodo a eliminar
            if not raiz.izquierda:
                return raiz.derecha
            elif not raiz.derecha:
                return raiz.izquierda
            # Nodo con dos hijos: obtenemos el sucesor in-order (el nodo más pequeño en el subárbol derecho)
            sucesor = self.get_sucesor(raiz.derecha)
            # Copiamos los datos del sucesor a este nodo
            raiz.clave = sucesor.clave
            raiz.persona = sucesor.persona
            # Eliminamos el sucesor
            raiz.derecha = self.eliminar(raiz.derecha, sucesor.clave)

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        # Casos de rotación
        if balance > 1:
            if clave < raiz.izquierda.clave:
                return self.rotacion_derecha(raiz)
            else:
                raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
                return self.rotacion_derecha(raiz)

        if balance < -1:
            if clave > raiz.derecha.clave:
                return self.rotacion_izquierda(raiz)
            else:
                raiz.derecha = self.rotacion_derecha(raiz.derecha)
                return self.rotacion_izquierda(raiz)

        return raiz

def get_sucesor(self, nodo):
    if not nodo or not nodo.izquierda:
        return nodo
    return self.get_sucesor(nodo.izquierda)
