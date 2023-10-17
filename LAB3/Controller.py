from Model import ArbolAVL  # Importa la clase ArbolAVL desde el módulo Model
from TS import TS
import json

class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion,companies):
        # Constructor de la clase Personas
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion
        self.companies = companies
        
    
class RegistroPersonas:
    def __init__(self):
        # Constructor de la clase RegistroPersonas
        self.arbol_avl = ArbolAVL()  # Crea una instancia de tu Árbol AVL
        self.cartas_por_id = {}  # Un diccionario para mapear ID (DPI) a lista de cartas
        self.ts = TS()

     
    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion, companies):
        # Método para insertar una persona en el Árbol AVL
   
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion, companies)
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)
        print(f"Persona insertada correctamente:")
        print(f"Nombre: {nombre}")
        print(f"DPI Comprimido: {id_persona}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento}")
        print(f"Dirección: {direccion}")
        print(f"Empresas: {companies}")
        
        self.buscar_cartas_de_persona(id_persona)
         # Buscar la persona en el árbol AVL

    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        # Método para eliminar una persona del Árbol AVL por nombre e ID
        clave = (nombre, str(id_persona))  # Convierte id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)  # Elimina la persona del Árbol AVL
             
    def buscar(self, nombre, id_persona):
            # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)
        return registros

    def buscar_dpi(self, id_persona):
        # Buscar registros en el árbol AVL por el DPI original (sin descomprimir)
        registros = self.arbol_avl.buscar_por_id_persona(self.arbol_avl.raiz, id_persona)
        return registros

    def buscar_registros_por_nombre(self, nombre, id_persona):
        # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)

        if registros:
            print("\nRegistros encontrados:")
            for registro in registros:
                persona_json = {
                    "name": registro.Nombre,
                    "dpi": registro.Id_Personas,  # Descomprimir y unir el DPI
                    "datebirth": registro.Fecha_Nacimiento,
                    "address": registro.Direccion,
                    "companies": registro.companies
                }
                json_str = json.dumps(persona_json)
                print(f"INSERT;{json_str}")
                self.buscar_cartas_de_persona(id_persona)
        else:
            print(f"No se encontraron registros para el nombre: {nombre}")
        return registros

    def actualizar_persona_por_nombre_id(self, nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas):
        # Método para actualizar los datos de una persona en el Árbol AVL por nombre e ID
        clave = (nombre, id_persona)  # Crea una clave única para la persona
                        
        #Comprobar si nuevas_empresas es None y asignar una lista vacía en su lugar
        if nuevas_empresas is None:
            nuevas_empresas = []        
        
        # Buscar la persona en el Árbol AVL
        persona = self.arbol_avl.actualizar_persona(self.arbol_avl.raiz, clave, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas)

        if persona is not None:
            # Actualizar los campos de la persona con los nuevos valores
            persona.Fecha_Nacimiento = nueva_fecha_nacimiento
            persona.Direccion = nueva_direccion
            persona.companies = nuevas_empresas


    def insertar_carta(self, id_carta, contenido_carta):
        contenido_cifrado = self.ts.cifrar_transposicion(contenido_carta, id_carta)
        if id_carta in self.cartas_por_id:
            # Si el ID ya existe en el diccionario, agrega la carta cifrada a la lista existente
            self.cartas_por_id[id_carta].append(contenido_cifrado)
        else:
            # Si el ID no existe en el diccionario, crea una nueva lista de cartas con el contenido cifrado
            self.cartas_por_id[id_carta] = [contenido_cifrado]
        print(f"Carta para DPI {id_carta} insertada correctamente:")
        print(f"Contenido cifrado: {contenido_cifrado}")
        
        
    def buscar_cartas_de_persona(self, id_persona):
        if id_persona in self.cartas_por_id:
            cartas = self.cartas_por_id[id_persona]
            contenido_descifrado = [self.ts.descifrar_transposicion(carta, id_persona) for carta in cartas]
            if cartas:
                print(f"Cartas para la persona con DPI {id_persona}:")
                for i, carta in enumerate(contenido_descifrado, start=1):
                    print(f"Carta {i} (Descifrada):\n{carta}\n")
            else:
                print(f"No se encontraron cartas para la persona con DPI {id_persona}")
        else:
            print(f"No se encontraron cartas para la persona con DPI {id_persona}")

# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()