sistema_activo = True
temperatura = 100
ciclo = 0
LIMITE_MUESTREO = 40   # frecuencia de muestreo del sensor, según datasheet

while sistema_activo:
    ciclo += 1

    if temperatura > 130:
        print(f"[Ciclo {ciclo}] ALERTA CRÍTICA: Parada de emergencia ({temperatura}°C)")
        sistema_activo = False
    elif temperatura < 115:
        print(f"[Ciclo {ciclo}] Estado: Calentando autoclave ({temperatura}°C)")
        temperatura += 2
    elif temperatura >= 115 and temperatura <= 121:
        print(f"[Ciclo {ciclo}] Estado: Fase estable de esterilización ({temperatura}°C)")
    else:
        print(f"[Ciclo {ciclo}] Estado: Enfriamiento activo ({temperatura}°C)")
        temperatura -= 3

    if ciclo >= LIMITE_MUESTREO:
        print(f"[Ciclo {ciclo}] Fin de la simulación: límite de muestreo alcanzado.")
        sistema_activo = False