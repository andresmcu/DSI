# -*- coding: utf-8 -*-

## Autores: Andrés Manrique y Fernando Gualo

import numpy
from sklearn import preprocessing 
import sklearn.neighbors
import matplotlib.pyplot as plt
from scipy import cluster
from sklearn import tree
from sklearn.externals.six import StringIO  
import pydotplus 


## Cargamos el fichero loaddata donde tenemos los métodos para importar los datos
import loaddata
# Cargamos en la variable data los datos que vamos a utilizar para hacer el custering
# Cargamos en la variable alldata los datos completos con todas las columnas para 
# más adelante obtener los resultados

FILE = "../../Datos/DATATHON_2015_Processed.csv"

data = loaddata.load_data(FILE)
alldata = numpy.asarray(loaddata.load_data(FILE))
datastr = numpy.asarray(loaddata.load_all_data(FILE))
 
## 1. Normalization of the data
# http://scikit-learn.org/stable/modules/preprocessing.html
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data) 
    
# 2. Compute the similarity matrix
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data)

# 3. Building the Dendrogram    
# http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage
clusters = cluster.hierarchy.linkage(matsim, method = 'ward')

# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.dendrogram.html
cluster.hierarchy.dendrogram(clusters, color_threshold=0)
plt.show()

# 4. Cutting the dendrogram
# Forms flat clusters from the hierarchical clustering defined by the linkage matrix clusters
# introduce the value after dendrogram visualization
cut = float(input("Threshold cut:"))

clusters = cluster.hierarchy.fcluster(clusters, cut, criterion = 'distance')
n_clusters_ = len(set(clusters)) - (1 if -1 in clusters else 0)

## Creamos una variable para cada uno de los clusters donde se introducirán los elementos 
## asignados a cada cluster
for i in range(0, n_clusters_):
    exec 'group%s = []' %(i)
    exec 'group%salldata = []' %(i)


## Insertamos cada elemento en su grupo eliminando los outliers
for index, x in numpy.ndenumerate(clusters - 1):
    exec 'group%s.append(alldata[index])' %(x)
    exec 'group%salldata.append(datastr[index])' %(x)
    
# Calculamos los diferentes indicadores que queremos analizar para cada uno de los clusters
for i in range(0, n_clusters_):
    exec 'mean%s = numpy.mean(group%s, axis=0) ' %(i, i)
 
# Obtenemos las inicadores para cada uno de los clusters que tenemos situadas en las columnas 0 y 1 respectivamente
MercadoE0 = numpy.asarray(group0alldata)[:,13].tolist().count(u'1\r\n')
MercadoE1 = numpy.asarray(group1alldata)[:,13].tolist().count(u'1\r\n')
MercadoE2 = numpy.asarray(group2alldata)[:,13].tolist().count(u'1\r\n')
T0 = numpy.asarray(group0alldata)[:,11].tolist().count(u'1')
T1 = numpy.asarray(group1alldata)[:,11].tolist().count(u'1')
T2 = numpy.asarray(group2alldata)[:,11].tolist().count(u'1')

############################## GENERAMOS LOS ÁRBOLES ##############################
############### Arbol Cluster 1 ###############
cluster_0 = tree.DecisionTreeClassifier()

productsg0 = numpy.asarray(group0alldata)[:, 12].tolist()
productsg0distinct = list(set([x.encode('utf-8') for x in productsg0]))

elementst0 = numpy.zeros((len(group0), 3))

for i in range(0, len(group0)):
    elementst0[i][0] = group0[i][2]
    elementst0[i][1] = group0[i][5]
    elementst0[i][2] = group0[i][6]
    
    
cluster_0 = cluster_0.fit(elementst0,[x.encode('utf-8') for x in productsg0])

## Extract the decision tree logic from the trained model
dot_data = StringIO() 
tree.export_graphviz(cluster_0, out_file = dot_data, feature_names = ["Gasto Dia", "Gasto Noche", "Mercado"], class_names = productsg0distinct, filled = False, rounded = True, special_characters = True)

## Convert the logics into graph
graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 

## This will plot decision tree in pdf file
graph.write_pdf(path = "Cluster_Arbol_1.pdf") 

############### Arbol Cluster 2 ###############
cluster_1 = tree.DecisionTreeClassifier()

productsg1 = numpy.asarray(group1alldata)[:, 12].tolist()
productsg1distinct = list(set([x.encode('utf-8') for x in productsg1]))

elementst1 = numpy.zeros((len(group1), 3))

for i in range(0, len(group1)):
    elementst1[i][0] = group1[i][2]
    elementst1[i][1] = group1[i][5]
    elementst1[i][2] = group1[i][6]
    
cluster_1 = cluster_1.fit(elementst1, [x.encode('utf-8') for x in productsg1])

## Extract the decision tree logic from the trained model
dot_data = StringIO() 
tree.export_graphviz(cluster_1, out_file=dot_data, feature_names=["Gasto Dia","Gasto Noche","Mercado"], class_names=productsg1distinct, filled=False, rounded=True, special_characters=True)

## Convert the logics into graph
graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 

## This will plot decision tree in pdf file
graph.write_pdf(path = "Cluster_Arbol_2.pdf") 

############### Arbol Cluster 3 ###############
cluster_2 = tree.DecisionTreeClassifier()

productsg2 = numpy.asarray(group2alldata)[:,12].tolist()
productsg2distinct = list(set([x.encode('utf-8') for x in productsg2]))

elementst2 = numpy.zeros((len(group2), 3))

for i in range(0, len(group2)):
    elementst2[i][0] = group2[i][2]
    elementst2[i][1] = group2[i][5]
    elementst2[i][2] = group2[i][6]
    

cluster_2 = cluster_2.fit(elementst2, [x.encode('utf-8') for x in productsg2])

## Extract the decision tree logic from the trained model
dot_data = StringIO() 
tree.export_graphviz(cluster_2, out_file = dot_data, feature_names = ["Gasto Dia", "Gasto Noche", "Mercado"], class_names = productsg2distinct, filled = False, rounded = True, special_characters = True)

## convert the logics into graph
graph = pydotplus.graph_from_dot_data(dot_data.getvalue()) 

## This will plot decision tree in pdf file
graph.write_pdf(path="Cluster_Arbol_3.pdf") 