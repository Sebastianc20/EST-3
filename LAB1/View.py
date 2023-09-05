import json
from Controller import RegistroPersonas

class VistaRegistroPersonas:
    def __init__(self):
        self.base_de_datos = RegistroPersonas()

    def cargar_datos_desde_jsonl(self, archivo_jsonl):
        operaciones = []  # Lista para almacenar las operaciones

        try:
            with open(archivo_jsonl, "r") as jsonl_file:
                for line in jsonl_file:
                    entrada = json.loads(line)
                    operaciones.append(entrada)  # Almacena la operación en la lista

            # Itera sobre las operaciones después de leer todo el archivo
            for entrada in operaciones:
                operacion = entrada["operacion"]
                datos_persona = entrada["datos"]

                if operacion == "INSERT":
                    nombre = datos_persona["nombre"]
                    id_persona = datos_persona["id_persona"]
                    fecha_nacimiento = datos_persona["fecha_nacimiento"]
                    # Verificar si la clave "direccion" está presente en datos_persona
                    if "direccion" in datos_persona:
                        direccion = datos_persona["direccion"]
                    else:
                        direccion = None  # O asigna un valor predeterminado si no está presente
                    self.base_de_datos.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion)
                    print(f"Persona insertada correctamente: {nombre}")

                elif operacion == "PATCH":
                    nombre = datos_persona["nombre"]
                    id_persona = datos_persona["id_persona"]
                    nueva_fecha_nacimiento = datos_persona["fecha_nacimiento"]
                    # Verificar si la clave "direccion" está presente en datos_persona
                    if "direccion" in datos_persona:
                        nueva_direccion = datos_persona["direccion"]
                    else:
                        nueva_direccion = None  # O asigna un valor predeterminado si no está presente
                    # Realizar la operación PATCH aquí
                    self.base_de_datos.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                    print(f"Fecha de nacimiento actualizada para: {nombre}")

                elif operacion == "DELETE":
                    nombre = datos_persona["nombre"]
                    id_persona = datos_persona["id_persona"]
                    # Realizar la operación DELETE aquí
                    self.base_de_datos.eliminar_persona(nombre, id_persona)
                    print(f"Persona eliminada: {nombre}")

            print("Datos cargados exitosamente desde el archivo JSONL.")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def mostrar_menu(self):
        while True:
            print("\nMenú:")
            print("1. Cargar datos desde archivo JSON")
            print("2. Insertar persona")
            print("3. Eliminar persona")
            print("4. Actualizar persona")
            print("5. Buscar registros por nombre")
            print("6. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                archivo_jsonl = input("Ingresa el nombre del archivo JSONL: ")
                self.cargar_datos_desde_jsonl(archivo_jsonl)

            elif opcion == "2":
                while True:
                    nombre = input("Nombre (o Enter para finalizar la inserción): ")
                    if not nombre:
                        break
                    id_persona = int(input("ID: "))
                    fecha_nacimiento = input("Fecha de Nacimiento: ")
                    direccion = input("Dirección: ")
                    self.base_de_datos.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion)
                    print(f"Persona insertada correctamente: {nombre}")

                print("Inserción de personas finalizada.")
                
            elif opcion == "3":
                nombre = input("Nombre de la persona a eliminar: ")
                id_persona = int(input("ID de la persona a eliminar: "))
                self.base_de_datos.eliminar_persona(nombre, id_persona)
                print("Persona eliminada correctamente.")
                
            elif opcion == "4":
                nombre = input("Nombre de la persona a actualizar: ")
                id_persona = int(input("ID de la persona a actualizar: "))
                nueva_fecha_nacimiento = input("Nueva fecha de nacimiento: ")
                nueva_direccion = input("Nueva dirección: ")
                self.base_de_datos.actualizar_persona(nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion)
                print("Persona actualizada correctamente.")
                
            elif opcion == "5":
                nombre = input("Nombre de la persona a buscar: ")
                registros = self.base_de_datos.buscar_registros_por_nombre(nombre)
                if registros:
                    print("\nRegistros encontrados:")
                    for registro in registros:
                        print(registro)
                else:
                    print("No se encontraron registros para ese nombre.")
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Introduce un número del 1 al 6.")

if __name__ == "__main__":
    # Crear una instancia de la clase RegistroPersonas
    base_de_datos = RegistroPersonas()

    # Crear una instancia de la vista y mostrar el menú
    vista = VistaRegistroPersonas()
    vista.mostrar_menu()
