from Model import ArbolAVL  # Importa la clase ArbolAVL desde el módulo Model
import json  # Importa el módulo json para trabajar con datos JSON

class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion):
        # Constructor de la clase Personas
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion

class RegistroPersonas:
    def __init__(self):
        # Constructor de la clase RegistroPersonas
        self.arbol_avl = ArbolAVL()  # Crea una instancia de tu Árbol AVL

    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion):
        # Método para insertar una persona en el Árbol AVL
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion)  # Crea una instancia de Personas
        clave = (nombre, id_persona)  # Crea una clave única para la persona
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)  # Inserta la persona en el Árbol AVL

    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        # Método para eliminar una persona del Árbol AVL por nombre e ID
        clave = (nombre, str(id_persona))  # Convierte id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)  # Elimina la persona del Árbol AVL
        if self.arbol_avl.raiz:
            print(f"Persona eliminada correctamente: {nombre}")
        else:
            print(f"No se encontró la persona con nombre {nombre} e ID {id_persona}")

    def buscar_registros_por_nombre(self, nombre, id_persona):
        # Método para buscar registros en el Árbol AVL por nombre e ID
        return self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)

    def actualizar_persona_por_nombre_id(self, nombre, id_persona, nueva_fecha_nacimiento):
        # Método para actualizar la fecha de nacimiento de una persona en el Árbol AVL por nombre e ID
        clave = (nombre, id_persona)  # Crea una clave única para la persona
        nuevos_datos = {
            "dateBirth": nueva_fecha_nacimiento
        }
        self.arbol_avl.raiz = self.arbol_avl.actualizar_persona(self.arbol_avl.raiz, clave, nuevos_datos)  # Actualiza la fecha de nacimiento
        if self.arbol_avl.raiz:
            print(f"Fecha de nacimiento actualizada correctamente para: {nombre}")
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
                        self.actualizar_persona_por_nombre_id(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                        print(f"Fecha de nacimiento actualizada para: {nombre}")

                    elif operacion == "DELETE":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        self.eliminar_persona_por_nombre_id(nombre, id_persona)
                        print(f"Persona eliminada: {nombre}")

            print("Datos cargados exitosamente desde el archivo JSONL.")
        except FileNotFoundError as e:
            print(f"Error: {e}")

# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()
