from Model import ArbolB
import json

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

    def buscar_registros_por_nombre(self, nombre, id_persona):
        return self.arbol_b.buscar(nombre, id_persona)

    def procesar_jsonl(self, archivo_jsonl):
        try:
            with open(archivo_jsonl, "r") as jsonl_file:
                for line in jsonl_file:
                    entrada = json.loads(line)
                    operacion = entrada["operacion"]
                    datos_persona = entrada["datos"]

                    if operacion == "INSERT":
                        nombre = datos_persona["nombre"]
                        id_persona = datos_persona["id_persona"]
                        fecha_nacimiento = datos_persona["fecha_nacimiento"]
                        direccion = datos_persona["direccion"] if "direccion" in datos_persona else None
                        self.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion)

                    elif operacion == "PATCH":
                        nombre = datos_persona["nombre"]
                        id_persona = datos_persona["id_persona"]
                        nueva_fecha_nacimiento = datos_persona["fecha_nacimiento"]
                        nueva_direccion = datos_persona["direccion"] if "direccion" in datos_persona else None
                        self.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)

                    elif operacion == "DELETE":
                        nombre = datos_persona["nombre"]
                        id_persona = datos_persona["id_persona"]
                        self.eliminar_persona(nombre, id_persona)

        except FileNotFoundError as e:
            print(f"Error: {e}")

# Crear una instancia de la clase RegistroPersonas fuera de la clase
base_de_datos = RegistroPersonas()

# Llamar a la función procesar_jsonl después de crear la instancia
base_de_datos.procesar_jsonl("Bitacora.jsonl")
