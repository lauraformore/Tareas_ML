#No funciono 


import warnings
warnings.filterwarnings('ignore')
import pandas as pd

# Código ORIGINAL de tu guía
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Cargar datos
df = pd.read_csv(r"C:\Users\laure\Documents\Proyectos\Heart_Predition\heart.csv")
X_train = df.sample(frac=0.8, random_state=42)
X_test = df.drop(X_train.index)

# Crear y guardar el reporte (con save_html)
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=X_train, current_data=X_test)
report.save_html("drift_report.html")

print("REPORTE GENERADO CORRECTAMENTE")