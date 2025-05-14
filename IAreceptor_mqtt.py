import paho.mqtt.client as mqtt
import json
import pandas as pd
import os

# 📌 Configuración del Servidor MQTT
MQTT_BROKER = "100.118.148.120"  # IP Raspberry Pi (via Tailscale)
MQTT_PORT = 1883
MQTT_TOPIC = "raspberry/datos"
CSV_FILE = "datos_flores.csv"

# 📌 Callback cuando se recibe conexión
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Conectado al broker MQTT (v5)")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Escuchando en {MQTT_TOPIC}...")
    else:
        print(f"❌ Error al conectar. Código: {reason_code}")

# 📌 Callback cuando llega un mensaje
def on_message(client, userdata, msg):
    try:
        datos = json.loads(msg.payload.decode())
        print(f"📥 Datos recibidos: {datos}")

        # Convertir correctamente en DataFrame
        if isinstance(datos, list):
            df = pd.DataFrame(datos)
        else:
            df = pd.DataFrame([datos])

        # Convertir fecha_hora al formato Excel entendible (mm/dd/yyyy HH:MM)
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora']).dt.strftime('%-m/%-d/%Y %H:%M')

        # Reordenar columnas
        columnas_ordenadas = ['id', 'fecha_hora', 'lugar_id', 'temperatura', 'humedad_aire',
                              'humedad_tierra', 'uv', 'abono', 'lugar']
        df = df[columnas_ordenadas]

        # Escribir al archivo CSV
        if not os.path.isfile(CSV_FILE):
            df.to_csv(CSV_FILE, index=False)
        else:
            df.to_csv(CSV_FILE, mode='a', index=False, header=False)

    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")

def on_disconnect(client, userdata, reason_code, properties):
    print(f"⚠️ Cliente desconectado. Razón: {reason_code}")

# 📌 Inicializar Cliente MQTT
cliente = mqtt.Client(protocol=mqtt.MQTTv5)
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.on_disconnect = on_disconnect

try:
    print(f"🔄 Intentando conectar a {MQTT_BROKER}...")
    cliente.connect(MQTT_BROKER, MQTT_PORT, 60)
    cliente.loop_forever()

except ConnectionRefusedError:
    print("❌ Conexión rechazada. Verifica que el broker MQTT esté activo.")
except OSError as e:
    print(f"❌ Error de red: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
