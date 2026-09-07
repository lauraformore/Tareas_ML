import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usamos el backend 'Agg' para que no se abra una ventana, sino que guarde la imagen
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv(r"C:\Users\laure\Documents\Proyectos\Heart_Predition\heart.csv")

# Separar en entrenamiento y prueba (simulando)
X_train = df.sample(frac=0.8, random_state=42)
X_test = df.drop(X_train.index)

# Escoger una columna para visualizar la deriva (por ejemplo, 'Age')
columna = 'Age'

# Crear la figura
plt.figure(figsize=(10, 6))

# Dibujar histogramas comparando X_train y X_test
plt.hist(X_train[columna], bins=20, alpha=0.6, label='Datos de Entrenamiento (Reference)', color='blue')
plt.hist(X_test[columna], bins=20, alpha=0.6, label='Datos de Prueba (Current)', color='red')

# Configurar el gráfico
plt.title(f'Monitoreo de Deriva de Datos (Data Drift) - Columna: {columna}')
plt.xlabel(columna)
plt.ylabel('Frecuencia')
plt.legend()

# Guardar el reporte como imagen
plt.savefig("drift_report.png")
print("REPORTE DE DERIVA GENERADO CORRECTAMENTE (revisa 'drift_report.png')")