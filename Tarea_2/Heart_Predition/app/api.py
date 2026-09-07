# app/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os
import pathlib

# 1. Inicializar la app
app = FastAPI(title="API Predicción Cardíaca")

# 2. Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Cargar el modelo
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(directorio_actual, "model.joblib")

try:
    modelo = joblib.load(ruta_modelo)
except FileNotFoundError:
    print(f"⚠️ ADVERTENCIA: No se encontró el modelo en {ruta_modelo}. Asegúrate de haberlo generado en el notebook.")
    modelo = None

# 4. Definir la estructura de los datos con VALIDACIONES
class DatosPaciente(BaseModel):
    Age: int = Field(..., ge=0, le=120, description="Edad del paciente (0-120)")
    Sex: str = Field(..., pattern="^(M|F)$", description="Sexo: 'M' o 'F'")
    ChestPainType: str = Field(..., pattern="^(ASY|NAP|ATA|TA)$", description="Tipo de dolor: ASY, NAP, ATA, TA")
    RestingBP: int = Field(..., ge=0, le=250, description="Presión arterial en reposo")
    Cholesterol: int = Field(..., ge=0, le=600, description="Nivel de colesterol")
    FastingBS: int = Field(..., ge=0, le=1, description="Ayuno de azúcar (0 o 1)")
    RestingECG: str = Field(..., pattern="^(Normal|ST|LVH)$", description="ECG en reposo: Normal, ST, LVH")
    MaxHR: int = Field(..., ge=0, le=250, description="Frecuencia cardíaca máxima")
    ExerciseAngina: str = Field(..., pattern="^(Y|N)$", description="Angina inducida: 'Y' o 'N'")
    Oldpeak: float = Field(..., description="Depresión del segmento ST")
    ST_Slope: str = Field(..., pattern="^(Up|Flat|Down)$", description="Pendiente ST: Up, Flat, Down")

# 5. Rutas de la API

@app.get("/health")
def salud():
    if modelo is None:
        return {"estado": "error", "detalle": "Modelo no cargado"}
    return {"estado": "ok"}

@app.post("/predict")
def predecir_enfermedad(datos: DatosPaciente):
    if modelo is None:
        raise HTTPException(status_code=503, detail="El modelo no está cargado. Revisa el servidor.")
    
    df = pd.DataFrame([datos.dict()])
    prediccion_clase = modelo.predict(df)[0]
    
    try:
        proba = modelo.predict_proba(df)[0]
        probabilidad_enfermedad = round(float(proba[1]), 4)
    except:
        probabilidad_enfermedad = None

    return {
        "prediccion": int(prediccion_clase),
        "probabilidad_riesgo": probabilidad_enfermedad,
        "mensaje": "⚠️ Alto riesgo de enfermedad cardíaca detectado" if prediccion_clase == 1 else "✅ Sin riesgo de enfermedad cardíaca"
    }

# 6. Servir el Frontend (HTML)
frontend_path = pathlib.Path(__file__).parent.parent / "frontend"

# Servir archivos estáticos si los hubiera
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Ruta raíz que carga el index.html
@app.get("/")
def frontend():
    return FileResponse(frontend_path / "index.html")