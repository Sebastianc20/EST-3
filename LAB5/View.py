import json
import os
import re
from Controller import RegistroPersonas

class VistaRegistroPersonas:
    def __init__(self):
        self.base_de_datos = RegistroPersonas()
        self.reclutador_autenticado = None  # Nuevo atributo para almacenar el reclutador autenticado

    def cargar_datos_desde_jsonl(self, archivo_jsonl):
        try:
            with open(archivo_jsonl, "r") as jsonl_file:
                for line in jsonl_file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(";")
                    if len(parts) != 2 or parts[0] not in ["INSERT", "PATCH", "DELETE"]:
                        print(f"Error: Formato de línea incorrecto en el archivo JSONL.")
                        continue

                    datos_json = {}
                    try:
                        datos_json = json.loads(parts[1])
                    except json.JSONDecodeError as e:
                        print(f"Error al procesar la línea JSONL: {e}")
                        continue

                    if parts[0]== "INSERT":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        fecha_nacimiento = datos_json.get("datebirth", "")
                        direccion = datos_json.get("address", "")
                        empresas = datos_json.get("companies", [])
                        recultador = datos_json.get("recluiter", "")
                                                               
                        self.base_de_datos.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion, empresas,recultador)                     
                            
                    elif parts[0]== "PATCH":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        nueva_fecha_nacimiento = datos_json.get("datebirth")
                        nueva_direccion = datos_json.get("address")
                        nuevas_empresas = datos_json.get("companies")
                                               
                        # Actualizar la persona con el DPI y las empresas comprimidas
                        self.base_de_datos.actualizar_persona_por_nombre_id(
                            nombre,
                            id_persona,  # Utiliza el DPI comprimido
                            nueva_fecha_nacimiento,
                            nueva_direccion,
                            nuevas_empresas
                        )
                                                
                        # Buscar la persona en el árbol AVL
                        persona = self.base_de_datos.buscar(nombre, id_persona)
                        
                        if persona:
                            # La persona se encontró en el árbol, ahora puedes eliminarla
                            print(f"Persona Actualizada correctamente: {nombre}")
                        else:
                            print(f"No se encontró la persona con nombre {nombre}")


                    elif parts[0]== "DELETE":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        
                        # Buscar la persona en el árbol AVL
                        persona = self.base_de_datos.buscar(nombre, id_persona)
                        
                        if persona:
                            # La persona se encontró en el árbol, ahora puedes eliminarla
                            self.base_de_datos.eliminar_persona_por_nombre_id(nombre, id_persona)
                            print(f"Persona eliminada correctamente: {nombre}")
                        else:
                            print(f"No se encontró la persona con nombre {nombre}")

        except FileNotFoundError:
            print(f"Error: El archivo {archivo_jsonl} no existe.")
        except Exception as e:
            print(f"Error al cargar los datos desde el archivo JSONL: {e}")
            
            
    def cargar_cartas_desde_carpeta(self, carpeta):
        try:
            archivos = os.listdir(carpeta)

            for archivo in archivos:
                match_conv = re.match(r'CONV-(\d+)-(\d+)\.txt', archivo)
                match_rec = re.match(r'REC-(\d+)-(\d+)\.txt', archivo)        
                        
                if match_conv:
                    id_carta = match_conv.group(1)  # Obtener el ID de la carta
                    contenido_carta = None

                    with open(os.path.join(carpeta, archivo), "r") as carta_file:
                        contenido_carta = carta_file.read()
                            
                    # Almacena la conversación cifrada y firmada en el diccionario
                    self.base_de_datos.insertar_carta(id_carta, contenido_carta)
                
                elif match_rec:
                    id_carta = match_rec.group(1)  # Obtener el ID de la carta
                    contenido_carta = None

                    with open(os.path.join(carpeta, archivo), "r") as carta_file:
                        contenido_carta = carta_file.read()
                            
                    # Almacena la conversación cifrada y firmada en el diccionario
                    self.base_de_datos.insertar_carta(id_carta, contenido_carta)
                    
        except FileNotFoundError:
            print(f"Error: La carpeta {carpeta} no existe.")
        except Exception as e:
            print(f"Error al cargar las cartas desde la carpeta: {e}")


    def iniciar_sesion(self):
        # Cargar datos desde archivo JSONL
        archivo_jsonl = input("Ingresa el nombre del archivo JSONL para cargar datos: ")
        self.cargar_datos_desde_jsonl(archivo_jsonl)

        # Cargar cartas desde carpeta
        nombre_carpeta = input("Ingresa el nombre de la carpeta para cargar cartas: ")
        carpeta = os.path.join(os.getcwd(), nombre_carpeta)
        self.cargar_cartas_desde_carpeta(carpeta)

        intentos = 3
        while intentos > 0:
            input_usuario = input("Ingresa tu usuario: ")
            input_contrasena = input("Ingresa tu contraseña: ")

            # Obtener la clave pública para el usuario
            clave_publica, _ = self.base_de_datos.claves_rsa.get(input_usuario, (None, None))

            if clave_publica:
                # Cifrar la contraseña ingresada
                contrasena_cifrada_ingresada = self.base_de_datos.cifrar_con_rsa(input_contrasena, clave_publica)

                # Comparar con la contraseña almacenada
                if self.base_de_datos.contrasenas_cifradas.get(input_usuario) == contrasena_cifrada_ingresada:
                    print("Inicio de sesión exitoso.")
                    self.reclutador_autenticado = input_usuario  # Guardar el nombre del reclutador autenticado
                    return True

            intentos -= 1
            print(f"Usuario o contraseña incorrectos. Te quedan {intentos} intentos.")

        print("Se han agotado los intentos. Inténtalo de nuevo más tarde.")
        return False



    def mostrar_menu(self):
        while True:
            print("\nMenú:")
            print("1. Eliminar persona")
            print("2. Buscar registros con archivos por nombre y dpi")
            print("3. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                nombre = input("Nombre de la persona a eliminar: ")
                id_persona = int(input("ID de la persona a eliminar: "))
                self.base_de_datos.eliminar_persona_por_nombre_id(nombre, id_persona)

            elif opcion == "2":
                nombre = input("Ingrese el nombre de la persona a buscar: ")
                id_persona = input("ID de la persona a buscar: ")
                self.base_de_datos.buscar_registros_por_nombre(nombre, id_persona, self.reclutador_autenticado)
            
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Introduce un número del 1 al 4.")


if __name__ == "__main__":
    vista = VistaRegistroPersonas()
    if vista.iniciar_sesion():
        vista.mostrar_menu()
