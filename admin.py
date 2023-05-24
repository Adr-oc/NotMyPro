import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('data.csv')

# Agrupar los datos por discapacidad y contar el número de personas en cada grupo
discapacidad = df.groupby('Discapacidad auditiva')['nombre'].count()

# Graficar los datos
discapacidad.plot(kind='bar')
plt.title('Personas con discapacidad auditiva')
plt.xlabel('Discapacidad auditiva')
plt.ylabel('Número de personas')
plt.show()

# Agrupar los datos por trabajo y contar el número de personas en cada grupo
trabajo = df.groupby('Trabajos')['nombre'].count()

# Graficar los datos
trabajo.plot(kind='bar')
plt.title('Personas que aplicaron a cierto trabajo')
plt.xlabel('Trabajo')
plt.ylabel('Número de personas')
plt.show()
