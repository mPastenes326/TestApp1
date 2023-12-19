import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
#import seaborn as sns


def generate_table(rows, columns):
    table = np.random.randn(rows, columns)
    return table


def create_dataframe(rows, columns):
    dataframe = pd.DataFrame(
        generate_table(rows, columns),
        columns=('info %d' % i for i in range(columns)))
    return dataframe



# Cargar datos
def cargar_datos(ruta_archivo):
    datos = pd.read_csv(ruta_archivo)
    return datos

# Procesar datos (ejemplo simple)
def procesar_datos(datos):
    datos_procesados = datos.dropna()  # Eliminar filas con valores faltantes
    return datos_procesados

# Crear una visualización (ejemplo simple)
def crear_visualizacion(datos,columna):
    plt.figure(figsize=(10, 6))
    sns.histplot(datos[columna], kde=True)
    st.pyplot(plt)
    
    
def convierte_timedela(data):
    ''''
    
    '''
    # Convertir la columna 'Tiempo' a un objeto timedelta
    data['Tiempo'] = pd.to_timedelta(data['Tiempo'])

    # Convertir las columnas 'Hora_Inicio' y 'Hora_Fin' al formato de tiempo
    data['Hora_Inicio'] = pd.to_datetime(data['Hora_Inicio'], format='%H:%M:%S').dt.time
    data['Hora_Fin'] = pd.to_datetime(data['Hora_Fin'], format='%H:%M:%S').dt.time

    # Crear una nueva columna 'Hora_Inicio_Minutos' que contiene solo la hora y minutos de 'Hora_Inicio'
    data['Hora_Inicio_Minutos'] = data['Hora_Inicio'].apply(lambda x: x.hour * 60 + x.minute)

    # Crear una nueva columna 'Hora_Fin_Minutos' que contiene solo la hora y minutos de 'Hora_Fin'
    data['Hora_Fin_Minutos'] = data['Hora_Fin'].apply(lambda x: x.hour * 60 + x.minute)

    '''
    # Definir los intervalos de media hora
    intervals = [(8, 0, 9, 0), (9, 0, 10, 0), (10, 0, 11, 0), (11, 0, 12, 0), (12, 0, 13, 0), (13, 0, 14, 0),
                (14, 0, 15, 0), (15, 0, 16, 0), (16, 0, 17, 0), (17, 0, 18, 0), (19, 0, 20, 0), (20, 0, 21, 0),
                (22, 0, 23, 0)]

    '''
    intervals = [(8,0, 8, 30), (8,30, 9,0), (9,0 , 9, 30), (9, 30, 10,0), (10,0, 10, 30), (10, 30, 11,0), (11,0, 11, 30),
             (11, 30, 12,0), (12,0, 12, 30), (12, 30, 13,0), (13,0, 13, 30), (13, 30, 14,0), (14,0, 14, 30), (14, 30, 15,0),
             (15,0 , 15, 30), (15, 30, 16,0), (16,0, 16, 30), (16, 30, 17,0), (17,0, 17, 30), (17, 30, 18,0), (18,0, 18, 30),
             (18, 30, 19,0), (19,0, 19, 30), (19, 30, 20,0), (20,0, 20, 30), (20, 30, 21,0), (21,0, 21, 30), (21, 30, 22,0),
             (22,0, 22, 30), (22, 30, 23,0), (23,0, 23, 30), (23, 30, 0, 0)]

    # Crear columnas para cada intervalo
    for interval_start_hour, interval_start_minute, interval_end_hour, interval_end_minute in intervals:
        column_name = f'Intervalo_{interval_start_hour}:{interval_start_minute}-{interval_end_hour}:{interval_end_minute}'
        data[column_name] = 0

    # Llenar las columnas de intervalo con el tiempo acumulado
    for interval_start_hour, interval_start_minute, interval_end_hour, interval_end_minute in intervals:
        interval_start_minutes = interval_start_hour * 60 + interval_start_minute
        interval_end_minutes = interval_end_hour * 60 + interval_end_minute
        
        for index, row in data.iterrows():
            overlap_start = max(row['Hora_Inicio_Minutos'], interval_start_minutes)
            overlap_end = min(row['Hora_Fin_Minutos'], interval_end_minutes)
            
            if overlap_start < overlap_end:
                data.at[index, f'Intervalo_{interval_start_hour}:{interval_start_minute}-{interval_end_hour}:{interval_end_minute}'] = overlap_end - overlap_start

    # Agrupar por día y sumar los valores de las columnas de intervalo
    result = data.groupby(['Fecha']).agg({f'Intervalo_{interval_start_hour}:{interval_start_minute}-{interval_end_hour}:{interval_end_minute}': 'sum' for interval_start_hour, interval_start_minute, interval_end_hour, interval_end_minute in intervals}).reset_index()

    # Convertir los valores de minutos a formato [hh]:mm:ss
    for interval_start_hour, interval_start_minute, interval_end_hour, interval_end_minute in intervals:
        column_name = f'Intervalo_{interval_start_hour}:{interval_start_minute}-{interval_end_hour}:{interval_end_minute}'
        result[column_name] = pd.to_timedelta(result[column_name], unit='m').apply(lambda x: str(x).split()[-1])

    # Muestra el resultado con los valores de intervalo en el formato [hh]:mm:ss
    (result)
    return result


st.title("Primer Prototipo Operaciona con Python :sunglasses:")
st.header("Equiopo de Operaciones de Canales remotos")


st.title("API SAMU")

archivo_subido = st.file_uploader("Sube tu archivo de datos", type=["csv"])

if archivo_subido is not None:
    datos = cargar_datos(archivo_subido)
    st.write("Columnas disponibles en el archivo:", datos.columns.tolist())

        # Convierte a intervalo 
    columna_seleccionada = st.selectbox("Generar Intervalo", datos.columns)

        # Selector de columnas
    columna_seleccionada = st.selectbox("Selecciona la columna que quieres visualizar", datos.columns)

    if st.button("Mostrar Visualización"):
        crear_visualizacion(datos, columna_seleccionada)
#data = create_dataframe(50, 15)
#st.subheader("Data Table")
#st.dataframe(data)
#st.subheader("Data Line Chart")
#st.line_chart(data)
#st.subheader("Data Bar Chart")
#st.bar_chart(data)#
