import argparse
import joblib
import os

# 📁 Ruta donde se guardaron los modelos
MODELOS_DIR = r"C:\Users\ASUS\Desktop\ECI\ICCS\modelos_recomendacion" 
#"modelos_recomendacion"

# 📌 Recursos a predecir (los modelos fueron entrenados con crecimiento como input)
RECURSOS = ['abono', 'humedad_tierra', 'temperatura', 'uv']

def cargar_modelos():
    modelos = {}
    for recurso in RECURSOS:
        modelo_path = os.path.join(MODELOS_DIR, f"{recurso}_modelo.pkl")
        if not os.path.exists(modelo_path):
            raise FileNotFoundError(f"❌ No se encontró el modelo de {recurso} en {modelo_path}")
        modelos[recurso] = joblib.load(modelo_path)
    return modelos

def generar_recomendaciones(crecimiento_deseado, modelos):
    recomendaciones = {}
    X_input = [[crecimiento_deseado]]
    for recurso, modelo in modelos.items():
        valor_recomendado = modelo.predict(X_input)[0]
        recomendaciones[recurso] = round(valor_recomendado, 2)
    return recomendaciones

def main():
    # 🎛️ Definición de argumentos
    parser = argparse.ArgumentParser(description="Recomendar condiciones óptimas para el cultivo de rosas")
    parser.add_argument('--crecimiento', type=float, required=True, help="Valor de crecimiento deseado (ej: 8.5)")
    args = parser.parse_args()

    # 📥 Cargar modelos entrenados
    print("📦 Cargando modelos...")
    modelos = cargar_modelos()

    # 🤖 Generar recomendaciones
    recomendaciones = generar_recomendaciones(args.crecimiento, modelos)

    # 📊 Mostrar resultados
    print(f"\n🌹 Recomendaciones para lograr un crecimiento de {args.crecimiento}:")
    print("-" * 45)
    print(f" Fertilizante       : {recomendaciones['abono']} ml")
    print(f" Humedad del Suelo  : {recomendaciones['humedad_tierra']} %")
    print(f" Temperatura        : {recomendaciones['temperatura']} °C")
    print(f" Radiación UV       : {recomendaciones['uv']} (índice)")
    print("-" * 45)

if __name__ == "__main__":
    main()
