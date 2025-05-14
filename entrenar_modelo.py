import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

CSV_FILE = "datos_flores.csv"
MODELOS_DIR = "modelos_recomendacion"
os.makedirs(MODELOS_DIR, exist_ok=True)

# 📥 Cargar datos
df = pd.read_csv(CSV_FILE)

# 📌 Verificación básica
campos_requeridos = ['id','fecha_hora','lugar_id','temperatura','humedad_aire','humedad_tierra','uv','abono','lugar','crecimiento']
if not all(col in df.columns for col in campos_requeridos):
    raise Exception(f"❌ Faltan columnas necesarias en el archivo CSV. Se requieren: {campos_requeridos}")

# 🧹 Limpieza
df.dropna(inplace=True)

# 📊 ENTRENAMIENTO DE MODELOS INVERTIDOS (estimamos el valor óptimo de cada recurso según crecimiento)
resultados = {}

for variable_objetivo in ['abono', 'humedad_tierra', 'temperatura', 'uv']:
    print(f"🔧 Entrenando modelo para {variable_objetivo}...")

    columnas_input = ['humedad_aire', 'temperatura', 'humedad_tierra', 'uv', 'abono']
    columnas_input.remove(variable_objetivo)

    X = df[['crecimiento']]
    y = df[variable_objetivo]

    # Entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100)
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    error = np.sqrt(mean_squared_error(y_test, pred))

    # Guardar modelo
    modelo_path = os.path.join(MODELOS_DIR, f"{variable_objetivo}_modelo.pkl")
    joblib.dump(modelo, modelo_path)

    resultados[variable_objetivo] = {
        "modelo": modelo_path,
        "RMSE": round(error, 2)
    }

# ✅ Mostrar resultados
print("\n📈 Resultados del entrenamiento:")
for recurso, info in resultados.items():
    print(f"🔹 {recurso.capitalize()}: RMSE = {info['RMSE']} - Modelo guardado en {info['modelo']}")
