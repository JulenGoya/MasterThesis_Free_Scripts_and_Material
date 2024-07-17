import csv
import os
from datetime import datetime
import glob

# Definir la carpeta de origen y la ruta del archivo CSV de salida
input_folder_path = 'C:/Users/julen/OneDrive/Escritorio/Uc3m/Master Habilitante/TFM/Log MALL/PRUEBAS FINALES/10Camaras_30Personas/Logs'
output_file_path = 'C:/Users/julen/OneDrive/Escritorio/Uc3m/Master Habilitante/TFM/Datos_ISLA/SIMULADOR2/10Camaras_30Personas.csv'

# Función para convertir fecha y hora a Unix timestamp
def to_unix_timestamp(date_str):
    # Asumiendo el formato "dd/mm/aaaa hh:mm:ss.msms" para la fecha y hora
    dt_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S.%f')
    timestamp = datetime.timestamp(dt_obj)
    return timestamp

# Iniciar el archivo de salida y escribir las cabeceras
with open(output_file_path, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['t', 'device', 'loc_id', 'plan_x', 'plan_y'])

    # Buscar todos los archivos que coinciden con el patrón en la carpeta especificada
    for input_file_path in glob.glob(f'{input_folder_path}/CameraLog_*.txt'):
        device_name = os.path.basename(input_file_path).split('.')[0]
        
        with open(input_file_path, 'r') as infile:
            csv_reader = csv.reader(infile)

            for row in csv_reader:
                # Convertir la fecha y hora a Unix timestamp
                timestamp = to_unix_timestamp(row[0])
                loc_id = row[2] + device_name
                plan_x = row[5] #La row[5] es el valor en Z (el valor Y es la altura)
                plan_y = row[3] 

                # Escribir la fila en el archivo CSV de salida
                csv_writer.writerow([timestamp, device_name, loc_id, plan_x, plan_y])

print("Archivos procesados exitosamente.")
