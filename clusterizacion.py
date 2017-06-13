# -*- coding: utf-8 -*-

## Autores: Andrés Manrique y Fernando Gualo


import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

def drawDiagram(kmeans):
	labels = kmeans.labels_
	centroids = kmeans.cluster_centers_
	for i in range(kmeans.n_clusters):
		# Seleccionamos solo los datos que vamos a mostrar
	    ds = data[np.where(labels == i)]
	    # Lo dibujamos
	    plt.plot(ds[: ,0], ds[: ,1], 'o')
	    # Dibujamos los centroides
	    lines = plt.plot(centroids[i, 0], centroids[i, 1], 'kx')
	    plt.setp(lines, ms = 15.0)
	    plt.setp(lines, mew = 2.0)
	plt.show()


# Cargamos el fichero procesado. Elegimos las variables significativas para la clusterización, en nuestro caso, el gasto 
# de cada cliente: gasto durante el día y gasto durante la noche.
# Combinamos las variables en una matriz que después pasaremos como argumento al algoritmo.

df = pd.read_csv('../Datos/DATATHON_2015_Processed.csv')

# Eje X
f1 = df['Producto'].values

# Eje Y
f2 = df['Gasto_total'].values
# f3 = df['Producto'].values

K = 2

data = np.matrix(zip(f1, f2))
kmeans = KMeans(n_clusters = K).fit(data)

drawDiagram(kmeans)