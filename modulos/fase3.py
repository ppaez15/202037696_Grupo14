"""Consulta segura del mapa de registros del BME680 (direcciones del datasheet).

Busca un registro por direccion hexadecimal (ej. 0x75) o por nombre/grupo
(ej. "config", "gas", "humedad") usando .get() y un numero maximo de intentos.

Nota: las direcciones y el campo "limit" provienen del datasheet de Bosch
Sensortec. "status" y "calib_val" son valores de ejemplo del modelo didactico.
"""

bme680 = {
    "0x75": {"nombre": "config",     "grupo": "filtro",  "status": True,  "calib_val": 12, "limit": 127},
    "0x71": {"nombre": "ctrl_gas_1", "grupo": "gas",     "status": True,  "calib_val": 55, "limit": 9},
    "0x72": {"nombre": "ctrl_hum",   "grupo": "humedad", "status": False, "calib_val": 88, "limit": 5},
}

MAX_INTENTOS = 5  # control numerico: limita el ciclo de busqueda


def normalizar_direccion(texto):
    """Convierte '75', '0X75' o '0x75' en la clave canonica '0x75'."""
    t = texto.strip().lower()
    if not t.startswith("0x"):
        t = "0x" + t
    return t


def buscar_registro(consulta):
    """Devuelve (direccion, datos) o (None, None) si no existe."""
    # 1) Acceso directo y seguro por direccion con .get()
    direccion = normalizar_direccion(consulta)
    datos = bme680.get(direccion)
    if datos is not None:
        return direccion, datos

    # 2) Busqueda por nombre o grupo (ciclo acotado al tamano del mapa)
    consulta_min = consulta.strip().lower()
    if not consulta_min:
        return None, None
    for direccion, datos in bme680.items():
        if (consulta_min in datos.get("nombre", "").lower()
                or consulta_min in datos.get("grupo", "").lower()):
            return direccion, datos
    return None, None


def mostrar_registro(direccion, datos):
    print(f"\n  Registro  : {direccion}")
    print(f"  Nombre    : {datos.get('nombre', 'N/D')}")
    print(f"  Grupo     : {datos.get('grupo', 'N/D')}")
    print(f"  Status    : {'Activo' if datos.get('status') else 'Inactivo'}")
    print(f"  Calib_val : {datos.get('calib_val', 'N/D')}")
    print(f"  Limit     : {datos.get('limit', 'N/D')}\n")


def main():
    print("=== Consulta de registros BME680 (I2C 0x76 / 0x77) ===")
    print(f"Registros disponibles: {', '.join(bme680)}")
    print(f"Maximo de intentos: {MAX_INTENTOS}. Escriba 'salir' para terminar.\n")

    intentos = 0
    while intentos < MAX_INTENTOS:
        consulta = input(f"[{intentos + 1}/{MAX_INTENTOS}] Direccion o nombre del registro: ")
        if consulta.strip().lower() == "salir":
            break
        intentos += 1

        direccion, datos = buscar_registro(consulta)
        if datos is None:
            print("  Registro no encontrado.\n")
        else:
            mostrar_registro(direccion, datos)

    if intentos >= MAX_INTENTOS:
        print("Se alcanzo el maximo de consultas permitidas. Fin del programa.")
    else:
        print("Programa finalizado.")


if __name__ == "__main__":
    main()
    