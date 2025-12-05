from chatexchange.client import Client
import time
import json
from datetime import datetime, timedelta

#Datos de inicio de sesión 
EMAIL = "usertest@gmail.com"
PASSWORD = "123456"
#ID de la sala
ROOM_ID = "30872"
#Usamos como constante la fecha de la partida de "Trauma"
FECHA = "27-03-2025"
#Ejecutamos el worker a las 8 de la mañana 
HORA = 8

fecha = datetime.strptime(FECHA, "%d-%m-%Y")
dias = (datetime.now()- fecha).days

def iniciar():
    try:        
        with open("cookies.json", "r") as f:
            cookie_data = json.load(f)
        client = Client("stackexchange.com")
        for c in cookie_data:
            client._br.session.cookies.set(c["name"], c["value"], domain=c["domain"], path=c["path"])
        #client.login(EMAIL, PASSWORD)        
        time.sleep(10)
        room = client.get_room(ROOM_ID)
        room.join()
        room.send_message("Dia " + str(abs(dias)) + " sin Trauma")
        print("Dia " + str(abs(dias)) + " sin Trauma")
        #client.logout()         
        return True
    except Exception as e:
        print("\nError de inicio de sesión.")
        print(e)
        return False

while True:    
    ahora = datetime.now()
    hora_objetivo_hoy = datetime(ahora.year, ahora.month, ahora.day, HORA, 0, 0)
    
    if ahora >= hora_objetivo_hoy:
    # La ejecución de hoy ya pasó -> programar mañana
        if iniciar():
            dias += 1
        proxima_ejecucion = hora_objetivo_hoy + timedelta(days=1)
    else:
        proxima_ejecucion = hora_objetivo_hoy
    tiempo_espera = (proxima_ejecucion - ahora).total_seconds()
    if tiempo_espera < 0:
        tiempo_espera = 60  # esperar 1 minuto y recalcular
        tiempo_espera = (proxima_ejecucion - ahora).total_seconds()
    
    print(f"Esperando {(tiempo_espera / 3600):.2f} horas hasta la próxima ejecución a las {proxima_ejecucion.strftime('%H:%M:%S')}")
    time.sleep(tiempo_espera)