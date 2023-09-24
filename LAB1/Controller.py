from Model import ArbolAVL  # Importa la clase ArbolAVL desde el módulo Model
from LZW import LZWCompressor
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
        self.lzw_compressor = LZWCompressor()

    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion, companies):
        # Método para insertar una persona en el Árbol AVL
        empresas_comprimidas = [self.lzw_compressor.compress(empresa) for empresa in companies] 
           
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion, empresas_comprimidas)
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)
        print(f"Persona insertada correctamente:")
        print(f"Nombre: {nombre}")
        print(f"DPI Comprimido: {id_persona}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento}")
        print(f"Dirección: {direccion}")
        print(f"Empresas Comprimidas: {empresas_comprimidas}")

    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        # Método para eliminar una persona del Árbol AVL por nombre e ID
        clave = (nombre, str(id_persona))  # Convierte id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)  # Elimina la persona del Árbol AVL
        

    def buscar_registros_por_nombre(self, nombre, id_persona):
        # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)

        if registros:
            # Si se encontraron registros, descomprimir la información de empresas
            for registro in registros:
                empresas_descomprimidas = [self.lzw_compressor.decompress(empresa) for empresa in registro.companies]
                registro.companies = empresas_descomprimidas

            # Imprimir la información de la persona en formato JSON
            for registro in registros:
                persona_json = {
                    "name": registro.Nombre,
                    "dpi": registro.Id_Personas,  # Descomprimir el DPI
                    "datebirth": registro.Fecha_Nacimiento,
                    "address": registro.Direccion,
                    "companies": registro.companies
                }               
        return registros
    
    def actualizar_persona_por_nombre_id(self, nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas):
        # Método para actualizar los datos de una persona en el Árbol AVL por nombre e ID
        clave = (nombre, id_persona)  # Crea una clave única para la persona

        # Buscar la persona en el Árbol AVL
        persona = self.arbol_avl.actualizar_persona(self.arbol_avl.raiz, clave, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas)

        if persona is not None:
            # Actualizar los campos de la persona con los nuevos valores
            persona.Fecha_Nacimiento = nueva_fecha_nacimiento
            persona.Direccion = nueva_direccion
            persona.companies = nuevas_empresas

         
# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()
