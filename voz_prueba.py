import edge_tts
import asyncio
import os
from pydub import AudioSegment

# Texto original
texto = """Mejora significativamente la respuesta y eficiencia de tu motocicleta con este completo kit de alto rendimiento de Bunker Biker, conformado por tres componentes esenciales: una Bujía Iridium , una Bobina de encendido NIBBI de tercera generación y un Cable de alta NGK Racing.

La Bujía Iridium CDT Fabricada con materiales de última generación, esta bujía ofrece una chispa más fuerte, mayor durabilidad y mejor combustión, optimizando el rendimiento del motor.

BOBINA DE ENCENDIDO NIBBI

Desarrollada por NIBBI, esta bobina está diseñada para ofrecer una chispa estable, potente y rápida, incluso en condiciones extremas.

CABLE DE ALTA NGK RACING

Diseñado para complementar la bobina NIBBI, este cable garantiza una transmisión de energía eficiente y sin pérdidas.

En Bunker Biker, trabajamos para que tu motocicleta alcance su máximo potencial. Este kit es la elección ideal para motociclistas que buscan un encendido más eficiente, mayor durabilidad y mejor rendimiento en cada viaje."""

# Función para dividir texto en partes seguras
def dividir_texto(texto, max_caracteres=400):
    partes = []
    while len(texto) > max_caracteres:
        punto = texto.rfind(".", 0, max_caracteres)
        if punto == -1:
            punto = max_caracteres
        partes.append(texto[:punto+1].strip())
        texto = texto[punto+1:].strip()
    partes.append(texto)
    return partes

# Crear los audios en partes
async def generar_audio_partes(texto):
    partes = dividir_texto(texto)
    archivos = []

    for i, parte in enumerate(partes):
        archivo = f"parte_{i}.mp3"
        comunicador = edge_tts.Communicate(parte, voice="es-CO-GonzaloNeural")
        await comunicador.save(archivo)
        archivos.append(archivo)

    return archivos

# Unir audios en uno solo
def unir_audios(archivos, salida="voz_mejorada.mp3"):
    combinado = AudioSegment.empty()
    for archivo in archivos:
        combinado += AudioSegment.from_file(archivo)
    combinado.export(salida, format="mp3")
    # Limpiar
    for archivo in archivos:
        os.remove(archivo)

# Ejecutar todo
async def main():
    archivos = await generar_audio_partes(texto)
    unir_audios(archivos)

asyncio.run(main())
