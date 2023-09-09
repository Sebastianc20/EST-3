from Model import ArbolAVL
import json

class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion):
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion

class RegistroPersonas:
    def __init__(self):
        self.arbol_avl = ArbolAVL()  # Crea una instancia de tu Árbol AVL

    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion):
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion)
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)  # Inserta la persona en el Árbol AVL

    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        clave = (nombre, str(id_persona))  # Convertir id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)
        if self.arbol_avl.raiz:
            print(f"Persona eliminada correctamente: {nombre}")
        else:
            print(f"No se encontró la persona con nombre {nombre} e ID {id_persona}")

    def buscar_registros_por_nombre(self, nombre, id_persona):
        return self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)
    
    def actualizar_persona_por_nombre_id(self, nombre, id_persona, nuevos_datos):
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.actualizar_persona(self.arbol_avl.raiz, clave, nuevos_datos)
        if self.arbol_avl.raiz:
            print(f"Persona actualizada correctamente: {nombre}")
        else:
            print(f"No se encontró la persona con nombre {nombre} e ID {id_persona}")
            
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
                        print(f"Persona insertada correctamente: {nombre}")

                    elif operacion == "PATCH":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        nueva_fecha_nacimiento = datos_persona["dateBirth"]
                        nueva_direccion = datos_persona["address"]
                        self.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                        print(f"Fecha de nacimiento actualizada para: {nombre}")

                    elif operacion == "DELETE":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        self.eliminar_persona(nombre, id_persona)
                        print(f"Persona eliminada: {nombre}")

            print("Datos cargados exitosamente desde el archivo JSONL.")
        except FileNotFoundError as e:
            print(f"Error: {e}")


# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()