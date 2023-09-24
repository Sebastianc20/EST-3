import json
from Controller import RegistroPersonas

class VistaRegistroPersonas:
    def __init__(self):
        self.base_de_datos = RegistroPersonas()

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

                    if parts[0] == "INSERT":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        fecha_nacimiento = datos_json.get("datebirth", "")
                        direccion = datos_json.get("address", "")
                        empresas = datos_json.get("companies", [])
                                              
                        self.base_de_datos.insertar_persona(nombre, id_persona, fecha_nacimiento, direccion, empresas)
                        nuevos_datos = {
                            "datebirth": fecha_nacimiento,
                            "address": direccion,
                            "companies": empresas
                        }                       

                    elif parts[0] == "PATCH":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        nuevos_datos = datos_json.get("new_data", {})
                        nueva_fecha_nacimiento = nuevos_datos.get("datebirth")
                        nueva_direccion = nuevos_datos.get("address")
                        nuevas_empresas = nuevos_datos.get("companies")

                        self.base_de_datos.actualizar_persona_por_nombre_id(
                            nombre,
                            id_persona,
                            nueva_fecha_nacimiento,
                            nueva_direccion,
                            nuevas_empresas
                        )

                        persona = self.base_de_datos.buscar_registros_por_nombre(nombre, id_persona)
                        if persona is None:
                            print(f"No se encontró la persona: {nombre}")
                            continue
                        print(f"Se ha actualizado la persona correctamente: {nombre}")

                    elif parts[0] == "DELETE":
                        nombre = datos_json.get("name", "")
                        id_persona = datos_json.get("dpi", "")
                        
                        # Buscar la persona en el árbol AVL
                        persona = self.base_de_datos.buscar_registros_por_nombre(nombre, id_persona)
                        
                        if persona:
                            # La persona se encontró en el árbol, ahora puedes eliminarla
                            self.base_de_datos.eliminar_persona_por_nombre_id(nombre, id_persona)
                            print(f"Persona eliminada correctamente: {nombre}")
                        else:
                            print(f"No se encontró la persona con nombre {nombre} e ID {id_persona}")


        except FileNotFoundError:
            print(f"Error: El archivo {archivo_jsonl} no existe.")
        except Exception as e:
            print(f"Error al cargar los datos desde el archivo JSONL: {e}")


    def mostrar_menu(self):
        while True:
            print("\nMenú:")
            print("1. Cargar datos desde archivo JSONL")
            print("2. Eliminar persona")
            print("3. Buscar registros por nombre y ID")
            print("4. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                archivo_jsonl = input("Ingresa el nombre del archivo JSONL: ")
                self.cargar_datos_desde_jsonl(archivo_jsonl)

            elif opcion == "2":
                nombre = input("Nombre de la persona a eliminar: ")
                id_persona = int(input("ID de la persona a eliminar: "))
                self.base_de_datos.eliminar_persona_por_nombre_id(nombre, id_persona)


            elif opcion == "3":
                nombre = input("Nombre de la persona a buscar: ")
                id_persona = input("ID de la persona a buscar: ")
                registros = self.base_de_datos.buscar_registros_por_nombre(nombre, id_persona)
                if registros:
                    print("\nRegistros encontrados:")
                    for registro in registros:
                        json_data = {
                            "name": registro.Nombre,
                            "dpi": registro.Id_Personas,
                            "datebirth": registro.Fecha_Nacimiento,
                            "address": registro.Direccion,
                            "companies": registro.companies
                        }
                        json_str = json.dumps(json_data)
                        print(f"INSERT;{json_str}")
                else:
                    print(f"No se encontraron registros para el nombre: {nombre}")

            elif opcion == "4":
                break
            else:
                print("Opción no válida. Introduce un número del 1 al 4.")

if __name__ == "__main__":
    vista = VistaRegistroPersonas()
    vista.mostrar_menu()
