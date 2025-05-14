import paho.mqtt.client as mqtt
import json
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

DATA_FILE = "datos_sensores.csv"
TOPIC = "raspberry/datos"

# 📌 Callback al recibir datos MQTT
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    datos = json.loads(payload)
    print(f"📥 Recibido: {datos}")

    # Guardar en CSV para entrenamiento
    df = pd.DataFrame([datos])
    if not os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)

# 📌 Entrenamiento del modelo
def entrenar_modelo():
    df = pd.read_csv(DATA_FILE)

    # Limpieza básica
    df.dropna(inplace=True)
    columnas = ['humedad_suelo', 'temperatura', 'humedad_aire', 'radiacion_uv', 'fertilizante', 'crecimiento']
    df = df[columnas]

    X = df.drop('crecimiento', axis=1)
    y = df['crecimiento']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    modelo = RandomForestRegressor()
    modelo.fit(X_train, y_train)

    pred = modelo.predict(X_test)
    error = mean_squared_error(y_test, pred, squared=False)
    print(f"🎯 Error (RMSE): {error:.2f}")

    joblib.dump(modelo, "modelo_crecimiento.pkl")

# 📌 Cliente MQTT
cliente = mqtt.Client()
cliente.on_message = on_message
cliente.connect("localhost", 1883)
cliente.subscribe(TOPIC)
cliente.loop_start()

print("🔄 Escuchando datos de sensores... Presiona Ctrl+C para detener.")
try:
    while True:
        pass
except KeyboardInterrupt:
    cliente.loop_stop()
    print("🛑 Conexión MQTT detenida.")
