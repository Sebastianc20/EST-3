import json
from Controller import RegistroPersonas

class VistaRegistroPersonas:
    def __init__(self):
        self.base_de_datos = RegistroPersonas()

    def cargar_datos_desde_jsonl(self, archivo_jsonl):
        try:
            with open(archivo_jsonl, "r") as jsonl_file:
                for line in jsonl_file:
                    partes = line.strip().split(";")  # Divide la línea en dos partes: operación y datos
                    operacion = partes[0]
                    print(operacion)
                    datos_json = partes[1]  # Datos en formato JSON
                    print(datos_json)

                    datos_persona = json.loads(datos_json)  # Convierte los datos JSON en un diccionario Python

                    if operacion == "INSERT":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        fecha_nacimiento = datos_persona["dateBirth"]
                        direccion = datos_persona["address"]
                        self.base_de_datos.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion)
                        print(f"Persona insertada correctamente: {nombre}")

                    elif operacion == "PATCH":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        nueva_fecha_nacimiento = datos_persona["dateBirth"]
                        nueva_direccion = datos_persona["address"]
                        self.base_de_datos.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                        print(f"Fecha de nacimiento actualizada para: {nombre}")

                    elif operacion == "DELETE":
                        nombre = datos_persona["name"]
                        id_persona = datos_persona["dpi"]
                        self.base_de_datos.eliminar_persona(nombre, id_persona)
                        print(f"Persona eliminada: {nombre}")

                        print("Datos cargados exitosamente desde el archivo JSONL.")
        except FileNotFoundError as e:
            print(f"Error: {e}")


    def mostrar_menu(self):
        while True:
            print("\nMenú:")
            print("1. Cargar datos desde archivo JSONL")
            print("2. Eliminar persona")
            print("3. Actualizar persona")
            print("4. Buscar registros por nombre y ID")
            print("5. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                archivo_jsonl = input("Ingresa el nombre del archivo JSONL: ")
                self.cargar_datos_desde_jsonl(archivo_jsonl)

                
            elif opcion == "2":
                nombre = input("Nombre de la persona a eliminar: ")
                id_persona = int(input("ID de la persona a eliminar: "))
                self.base_de_datos.eliminar_persona(nombre, id_persona)
                print("Persona eliminada correctamente.")
                
            elif opcion == "3":
                nombre = input("Nombre de la persona a actualizar: ")
                id_persona = int(input("ID de la persona a actualizar: "))
                nueva_fecha_nacimiento = input("Nueva fecha de nacimiento: ")
                nueva_direccion = input("Nueva dirección: ")
                self.base_de_datos.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                print("Persona actualizada correctamente.")
                
            elif opcion == "4":
                nombre = input("Nombre de la persona a buscar: ")
                id_persona = input("ID de la persona a buscar: ")
                registros = self.base_de_datos.buscar_registros_por_nombre(nombre, id_persona)
                if registros:
                    print("\nRegistros encontrados:")
                    for registro in registros:
                        json_data = {
                            "name": registro.Nombre,
                            "dpi": registro.Id_Personas,
                            "dateBirth": registro.Fecha_Nacimiento,
                            "address": registro.Direccion
                        }
                        json_str = json.dumps(json_data)
                        print(f"INSERT;{json_str}")
                else:
                        print(f"No se encontraron registros para el nombre: {nombre}")

            elif opcion == "5":
                break
            else:
                print("Opción no válida. Introduce un número del 1 al 5.")

if __name__ == "__main__":
    # Crear una instancia de la clase RegistroPersonas
    base_de_datos = RegistroPersonas()

    # Crear una instancia de la vista y mostrar el menú
    vista = VistaRegistroPersonas()
    vista.mostrar_menu()
