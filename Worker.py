import asyncio
import sys
import time

import zendriver as zd

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

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
async def enviar_mensaje():
    try:
        browser = await zd.start(headless=True)
        page = await browser.get("https://chat.stackexchange.com/rooms/30872/stack-overflow-en-espanol")
        checkbox = await page.wait_for("input#agree-to-code")
        await checkbox.click()

        await asyncio.sleep(0.5)

        button = await page.wait_for("button#general-rules-button")
        await button.click()

        await asyncio.sleep(0.5)

        login = await page.wait_for("#bubble > a:nth-child(1)")
        await login.click()

        await asyncio.sleep(1)

        accept_cookies = await page.wait_for("#onetrust-reject-all-handler")
        await accept_cookies.click()

        await asyncio.sleep(0.5)
        
        email_input = await page.wait_for("#email")
        await email_input.send_keys(EMAIL)

        await asyncio.sleep(0.5)

        password_input = await page.wait_for("#password")
        await password_input.send_keys(PASSWORD)

        await asyncio.sleep(0.5)

        submit_button = await page.wait_for("#submit-button")
        await submit_button.click()

        await asyncio.sleep(5)

        textarea = await page.wait_for("#input")
        await textarea.send_keys(f"Dia {abs(dias)} sin Trauma")

        await asyncio.sleep(1)

        send_button = await page.wait_for("#sayit-button")
        await send_button.click()

        await asyncio.sleep(1)

        return True
    except Exception as e:
        print("\nError de inicio de sesión.")
        print(e)
        return False
    finally:
        # 1. CIERRE EXPLÍCITO: Garantiza que el navegador se cierre y sus recursos 
        # se liberen mientras el bucle de eventos sigue activo.
        if browser:
            print("Cerrando la sesión del navegador...")
            try:
                await browser.close()
                print("Cierre de browser completado.")
            except Exception as e_close:
                # Manejar posibles errores al cerrar, aunque el objetivo es evitar la excepción principal.
                print(f"Error al cerrar el navegador: {e_close}")

while True:    
    ahora = datetime.now()
    hora_objetivo_hoy = datetime(ahora.year, ahora.month, ahora.day, HORA, 0, 0)
    
    if ahora >= hora_objetivo_hoy:
    # La ejecución de hoy ya pasó -> programar mañana
        asyncio.run(enviar_mensaje())
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