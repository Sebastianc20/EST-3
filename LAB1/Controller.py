from Model import ArbolB

class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion):
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion

class RegistroPersonas:
    def __init__(self):
        self.arbol_b = ArbolB(3)  # Ajusta el valor de "orden" según tus necesidades

    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion):
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion)
        clave = (nombre, id_persona)
        self.arbol_b.insertar(clave, persona)

    def eliminar_persona(self, nombre, id_persona):
        clave = (nombre, id_persona)
        self.arbol_b.eliminar(clave)

    def actualizar_persona(self, nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion):
        clave = (nombre, id_persona)
        nueva_persona = Personas(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
        self.arbol_b.actualizar(clave, nueva_persona)

    def buscar_registros_por_nombre(self, nombre):
        resultados = self.arbol_b.buscar(nombre)

        if resultados is not None:
            registros = [resultado[1] for resultado in resultados]
            return registros
        else:
            return []

 
    
    # Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()
