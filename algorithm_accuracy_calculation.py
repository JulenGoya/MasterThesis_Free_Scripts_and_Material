import pandas as pd
import os
from sklearn.metrics import rand_score, adjusted_rand_score, adjusted_mutual_info_score, normalized_mutual_info_score, homogeneity_score, completeness_score, v_measure_score, fowlkes_mallows_score, silhouette_score
from sklearn.cluster import KMeans

def calcular_precision(df_traces):
    # Extraer el identificador de persona y de cámara
    df_traces['person_id'] = df_traces.loc_id.str.extract(r'(\d+)').astype(int)
    
    # Agrupar por identificador de persona y comprobar consistencia de clúster
    grupos = df_traces.groupby('person_id')
    aciertos = 0
    errores = 0
    # Crear un conjunto para llevar el registro de los clusters ya asociados a una persona
    clusters_usados = set()
    
    for person_id, grupo in grupos:
        # Verificar que todas las trazas de una persona estén en un único cluster
        if grupo.cluster.nunique() == 1:
            cluster_asignado = grupo.cluster.iloc[0]
            
            # Verificar que el cluster no esté ya asociado a otra persona
            if cluster_asignado not in clusters_usados:
                aciertos += grupo.shape[0]
                clusters_usados.add(cluster_asignado)
            else:
                errores += grupo.shape[0]
        else:
            errores += grupo.shape[0]
    
    # Calcular la precisión
    total_trazas = aciertos + errores
    precision = aciertos / total_trazas if total_trazas else 0
    return precision, aciertos, errores, total_trazas

# Leer el archivo Excel 
ruta_archivo = 'C:/Users/julen/OneDrive/Escritorio/Uc3m/Master Habilitante/TFM/Proyectos2/OPTIMUM_VALUES/10_1/output/df_traces.xlsx'  # Reemplaza con la ruta a tu archivo
df_traces = pd.read_excel(ruta_archivo)

# Calcular la precisión
precision, aciertos, errores, total_trazas = calcular_precision(df_traces)

#------------------------------------------------------------------------------------------------------------------
#----------------------------- RAND INDEX AND ADJUSTED RAND INDEX EVALUATION --------------------------------------
#------------------------------------------------------------------------------------------------------------------


# Asumimos que 'person_id' es tu true_labels y 'cluster' tus predicted_labels
# Primero, necesitamos asegurarnos de que tenemos la misma longitud y orden de ambas
df_traces.sort_values(by='person_id', inplace=True)  # Ordenar por person_id para alineación
true_labels = df_traces['person_id'].tolist()
predicted_labels = df_traces['cluster'].tolist()

# Calcular RI y ARI
ri = rand_score(true_labels, predicted_labels)
ari = adjusted_rand_score(true_labels, predicted_labels)


#------------------------------------------------------------------------------------------------------------------
#----------------------------- RAND INDEX AND ADJUSTED RAND INDEX EVALUATION --------------------------------------
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#----------------------------- ADJUSTED MUTUAL INFO AND NORMALIZED MUTUAL INFO ------------------------------------
#------------------------------------------------------------------------------------------------------------------

# Suponiendo que 'true_labels' y 'predicted_labels' ya están definidos como antes
ami = adjusted_mutual_info_score(true_labels, predicted_labels)
nmi = normalized_mutual_info_score(true_labels, predicted_labels)

#------------------------------------------------------------------------------------------------------------------
#----------------------------- ADJUSTED MUTUAL INFO AND NORMALIZED MUTUAL INFO ------------------------------------
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#----------------------------- HOMOGENEITY, COMPLETENESS AND V-MEASURE --------------------------------------------
#------------------------------------------------------------------------------------------------------------------

# Suponiendo que 'true_labels' y 'predicted_labels' ya están definidos
homogeneity = homogeneity_score(true_labels, predicted_labels)
completeness = completeness_score(true_labels, predicted_labels)
v_measure = v_measure_score(true_labels, predicted_labels)

#------------------------------------------------------------------------------------------------------------------
#----------------------------- HOMOGENEITY, COMPLETENESS AND V-MEASURE --------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#---------------------------------------- FOWLKES-MALLOWS SCORE ---------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

# Asumiendo que 'true_labels' y 'predicted_labels' ya están definidos
fmi_score = fowlkes_mallows_score(true_labels, predicted_labels)

#------------------------------------------------------------------------------------------------------------------
#---------------------------------------- FOWLKES-MALLOWS SCORE ---------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------ SILHOUETTE SCORE ------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------

# Suponiendo que X es tu conjunto de datos y ya está definido
#kmeans_model = KMeans(n_clusters=3, random_state=1).fit(X)
#labels = kmeans_model.labels_
#silhouette_avg = silhouette_score(X, labels, metric='euclidean')

#------------------------------------------------------------------------------------------------------------------
#------------------------------------------ SILHOUETTE SCORE ------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------


# Crear un DataFrame para los resultados
df_resultados = pd.DataFrame({
    'Precisión(%)': [precision * 100],  # Porcentaje
    'Aciertos': [aciertos],
    'Errores': [errores],
    'Total Trazas': [total_trazas],
    'Rand Index(RI)': [ri],
    'Adjusted Rand Index(ARI)': [ari],
    'Adjusted mutual information (AMI)': [ami],
    'Normalized mutual information (NMI)': [nmi],
    'Homogeneity': [homogeneity],
    'Completeness': [completeness],
    'V-Measure': [v_measure],
    'Fowlkess-Mallow Score': [fmi_score]
})

# Construir la ruta del archivo de resultados en la misma carpeta que el archivo de origen
nombre_archivo_resultados = 'resultado_precision.xlsx'
ruta_carpeta_origen = os.path.dirname(ruta_archivo)
ruta_archivo_resultados = os.path.join(ruta_carpeta_origen, nombre_archivo_resultados)

# Guardar los resultados en otro archivo Excel, creado automáticamente en la misma carpeta
with pd.ExcelWriter(ruta_archivo_resultados, engine='openpyxl') as writer:
    df_resultados.to_excel(writer, index=False)

print(f'Archivo de resultados guardado en: {ruta_archivo_resultados}')

from sklearn.metrics import rand_score, adjusted_rand_score
