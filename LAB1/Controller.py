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
                    partes = line.strip().split(";")  # Divide la línea en dos partes: operación y datos
                    operacion = partes[0]
                    datos_json = partes[1]  # Datos en formato JSON

                    datos_persona = json.loads(datos_json)  # Convierte los datos JSON en un diccionario Python

                    if operacion == "INSERT":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        fecha_nacimiento = datos_persona["dateBirth"]
                        direccion = datos_persona["address"]
                        self.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion)

                    elif operacion == "PATCH":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        nueva_fecha_nacimiento = datos_persona["dateBirth"]
                        nueva_direccion = datos_persona["address"]
                        self.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)

                    elif operacion == "DELETE":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        self.eliminar_persona(nombre, id_persona)

        except FileNotFoundError as e:
            print(f"Error: {e}")

# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()

# Llamar a la función procesar_jsonl después de crear la instancia
base_de_datos.procesar_jsonl("Bitacora.jsonl")
