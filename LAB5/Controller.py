from Model import ArbolAVL  # Importa la clase ArbolAVL desde el módulo Model
from TS import TS
import json
import hashlib

class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion,companies, reclutador):
        # Constructor de la clase Personas
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion
        self.companies = companies
        self.reclutador = reclutador
        
    
class RegistroPersonas:
    def __init__(self):
        # Constructor de la clase RegistroPersonas
        self.arbol_avl = ArbolAVL()  # Crea una instancia de tu Árbol AVL
        self.cartas_por_id = {}  # Un diccionario para mapear ID (DPI) a lista de cartas
        self.claves_rsa_por_id = {}  # Diccionario para almacenar claves RSA por ID de persona
        # Diccionario para almacenar claves RSA por usuario (reclutador)
        self.claves_rsa = {}
        # Diccionario para almacenar contraseñas cifradas por usuario (reclutador)
        self.contrasenas_cifradas = {}
        self.ts = TS()

    def extendido_euclidiano(self, a, b):
        # Algoritmo extendido de Euclides
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = self.extendido_euclidiano(b % a, a)
            return g, y - (b // a) * x, x

    def inverso_modulo(self, a, m):
        # Calcula el inverso multiplicativo de 'a' modulo 'm' usando el Algoritmo Extendido de Euclides
        g, x, y = self.extendido_euclidiano(a, m)
        if g != 1:
            raise ValueError("El inverso multiplicativo no existe")
        return x % m

    def generar_clave_privada_rsa(self):
        # Genera una clave privada RSA con dos números primos pequeños, solo para demostración
        p = 61
        q = 53
        n = p * q
        totient = (p - 1) * (q - 1)
        e = 17  # Este es un exponente público comúnmente usado
        d = self.inverso_modulo(e, totient)
        return d, n
    
    def generar_clave_publica_rsa(self, clave_privada):
        # Calcula la clave pública RSA a partir de una clave privada
        d, n = clave_privada
        p = 61
        q = 53
        totient = (p - 1) * (q - 1)
        e = 17
        return (e, n)
    
    def firmar_carta(self, contenido_carta):
        # Firmar digitalmente la carta
        private_key = self.generar_clave_privada_rsa()
        hash_carta = hashlib.sha256(contenido_carta.encode('utf-8')).hexdigest()
        firma = pow(int(hash_carta, 16), private_key[0], private_key[1])
        return hash_carta, firma
    
    def cifrar_con_rsa(self, mensaje, clave_publica):
        # Convertir el mensaje en un número (por ejemplo, utilizando el valor ASCII de cada caracter)
        mensaje_numerico = sum([ord(char) << (8 * i) for i, char in enumerate(mensaje)])

        # Extraer el exponente público y n de la clave pública
        e, n = clave_publica

        # Realizar el cifrado RSA: (mensaje^e) % n
        mensaje_cifrado = pow(mensaje_numerico, e, n)

        return mensaje_cifrado
    
    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion, companies, reclutador):
        # Método para insertar una persona en el Árbol AVL
        # Generar clave privada RSA
        clave_privada = self.generar_clave_privada_rsa()
        # Generar clave pública RSA basada en la clave privada
        clave_publica = self.generar_clave_publica_rsa(clave_privada)
        # Almacenar el par de claves en el diccionario
        self.claves_rsa_por_id[id_persona] = (clave_publica, clave_privada)
        
        contrasena_cifrada = self.cifrar_con_rsa(reclutador + "123", clave_publica)

        # Almacenar la contraseña cifrada y las claves RSA
        self.contrasenas_cifradas[reclutador] = contrasena_cifrada
        self.claves_rsa[reclutador] = (clave_publica, clave_privada)
        
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion, companies, reclutador)
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)
        print(f"Persona insertada correctamente:")
        print(f"Nombre: {nombre}")
        print(f"DPI Comprimido: {id_persona}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento}")
        print(f"Dirección: {direccion}")
        print(f"Empresas: {companies}")
        print(f"Reclutador: {reclutador}")
        print("\n")
        
        
    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        # Método para eliminar una persona del Árbol AVL por nombre e ID
        clave = (nombre, str(id_persona))  # Convierte id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)  # Elimina la persona del Árbol AVL
             
    def buscar(self, nombre, id_persona):
            # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)
        return registros

    def buscar_por_reclutador(self, nombre_reclutador):
        # Llamada directa al método del árbol AVL con el nombre del reclutador
        registros_coincidentes = self.arbol_avl.buscar_por_reclutador(self.arbol_avl.raiz, nombre_reclutador)
        return registros_coincidentes

    
    def buscar_registros_por_nombre(self,nombre, id_persona, nombre_reclutador):
        # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz,nombre, id_persona)

        # Filtrar los registros por el reclutador autenticado
        registros_filtrados = [reg for reg in registros if reg.reclutador == nombre_reclutador]

        if registros_filtrados:
            print("\nRegistros encontrados:")
            for registro in registros_filtrados:
                persona_json = {
                    "name": registro.Nombre,
                    "dpi": registro.Id_Personas,
                    "datebirth": registro.Fecha_Nacimiento,
                    "address": registro.Direccion,
                    "companies": registro.companies,
                    "recluiter": registro.reclutador
                }
                json_str = json.dumps(persona_json)
                print(f"INSERT;{json_str}")
                print("\n")
                # Suponiendo que tienes un método para buscar cartas de una persona
                self.buscar_cartas_de_persona(id_persona)
        else:
            print(f"No se encontraron registros para el nombre: {nombre}")

        return registros_filtrados


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


    def insertar_carta(self, id_persona, contenido_carta):
        # Calcular el hash del contenido original
        hash_carta = hashlib.sha256(contenido_carta.encode('utf-8')).hexdigest()       
        # Cifrar el contenido de la carta utilizando transposición simple
        contenido_cifrado = self.ts.cifrar_transposicion(contenido_carta, id_persona)        
        # Firmar el hash de la carta
        firma = self.firmar_carta(hash_carta)       
        if id_persona not in self.cartas_por_id:
            self.cartas_por_id[id_persona] = []     
            self.cartas_por_id[id_persona].append((contenido_cifrado, hash_carta, firma))
             
        print("Se ha agregado una Conversacion para la persona con ID:", id_persona)
        print("Contenido de la Conversacion cifrada:", contenido_cifrado)
        print("Firma generada:", firma)
        print("\n")

    def buscar_cartas_de_persona(self, id_persona):
        # Buscar una persona por su ID (DPI)
            if id_persona in self.cartas_por_id:
                cartas = self.cartas_por_id[id_persona]
                for i, carta in enumerate(cartas, start=1):
                    contenido_cifrado, hash_carta, firma = carta
                    contenido_descifrado = self.ts.descifrar_transposicion(contenido_cifrado, id_persona)
                    hash_actual = hashlib.sha256(contenido_descifrado.encode('utf-8')).hexdigest()
                    if hash_actual == hash_carta:
                        print("Conversacion número:", i)
                        print("La Conversacion para la persona con ID:", id_persona, "es válida.")
                        print("Contenido de la Conversacion descifrada:", contenido_descifrado)
                        print("\n")
                    else:
                        print("Conversacion número:", i)
                        print("La conversacion para la persona con ID:", id_persona, "ha sido modificada.")
                        print("Hash actual:", hash_actual)
                        print("Hash almacenado en la carta:", hash_carta)
                        print("\n")  # Imprimir una línea en blanco para separar cada carta
            else:
                print("No se encontró una persona con el ID (DPI) especificado.")


# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()