#importando librerias necesarias para trabajar con los exceles 
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

# Función para calcular el promedio de un string de números separados por comas
def calcular_promedio_preguntas_multiple_Seleccion(val):
    if isinstance(val, str) and ',' in val:
        #1. Convertir el string a una lista de números, ignorando los valores no numéricos
        numeros = []
        for num in val.split(','):
            try:
                numeros.append(float(num))  #2. Intenta convertir a float
            except ValueError:
                continue  #3. Ignora los valores que no se pueden convertir

        #4. Calcular y retornar el promedio si hay números válidos
        if numeros:  #5. Verifica que la lista no esté vacía
            return sum(numeros) / len(numeros)

    return val  #6. Retornar el valor original si no es un string con comas

#funcion que hace limpieza del data set 
def LimpiezaDatos(DataSetLimpiar,NombreColumna):
 
    #1: se pasa la informacion original a una nueva columna
    DataSetLimpiar[f'{NombreColumna}_original'] = DataSetLimpiar[NombreColumna]
    #2: se calcula el promedio de la preguntas de multiple respuesta
    DataSetLimpiar[NombreColumna] = DataSetLimpiar[NombreColumna].apply(calcular_promedio_preguntas_multiple_Seleccion)
    #3: se procede a calcular el promedio de todas las respuestas numericas
    DataSetLimpiar[NombreColumna] = pd.to_numeric(DataSetLimpiar[NombreColumna], errors='coerce')
    #media_Respuesta = DataSetLimpiar[NombreColumna].mean()
    media_Respuesta = 0
    #4: se reemplaza todos las respuesta no numericas por el promedio para no afectar el margen del promedio 
    DataSetLimpiar[NombreColumna] = DataSetLimpiar[NombreColumna].fillna(media_Respuesta)
    #5: se convierte en float para manejar mejor el calculo cuando se hacen la agrupaciones
    DataSetLimpiar[NombreColumna] = DataSetLimpiar[NombreColumna].astype(float)
    return DataSetLimpiar #6: se regresa el data set limpio para despues hacer su analisis

# funcion que limpia todo el dataset de caracteres especiales
def limpiar_texto(texto):
    if isinstance(texto, str):
        # Eliminar saltos de línea y caracteres especiales al inicio y al final
        return re.sub(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', texto)
    return texto  # Retorna el valor original si no es una cadena

#funcion que calcula el promedio por dimesnion
def CalcularPromedioDimension(DataSet, Año, tipoExcel):
    # 1. Promedia el resultados por persona componeten y dimension
    ResultadoDimensiones = DataSet.groupby(['Dimension','Subdimension', 'Persona'])['Respuesta'].mean().reset_index()
    # 2.haciendo agrupacion de la dimesiones
    ResultadoDimensiones = ResultadoDimensiones.groupby('Dimension', as_index=False)['Respuesta'].mean().reset_index()
    # 3. Agregando la columna año
    ResultadoDimensiones['año'] = Año
    # 4. Agregando la columna tipo de Excel para saber cual excel uso para la informacion
    ResultadoDimensiones['Excel Origen'] = f"{tipoExcel} {Año}"
    return ResultadoDimensiones

#funcion que calcula el promedio de dimension por componente y persona y despues por 
def CalculosPromediosComponenteDataSet(DataSet, Año, tipoExcel):
    # 1. Promedia el resultados por persona componeten y dimension
    promedio_dimension_componente = DataSet.groupby(['Dimension','Subdimension', 'Persona'])['Respuesta'].mean().reset_index()
    
    # 2. Promedia esos resultados por dimension y componetn
    promedio_componente = promedio_dimension_componente.groupby(['Dimension','Subdimension'])['Respuesta'].mean().reset_index()
   
    # 3. Renombrar la columna para mayor claridad
    promedio_componente.rename(columns={'Respuesta': 'promedio_respuesta'}, inplace=True)

    # 4. agrega la columna de año
    promedio_componente["año"]=Año
    # 5. agrega la columan de  tipo de excel para saber cual excel uso para los calculos
    promedio_componente["Excel Origen"]=f"{tipoExcel} {Año}"

    return promedio_componente

#funcion que reemplaza valor en una columna del dataset
def ReemplazarValorDataSet(datset, Nobrecolumna, ValorBusar, ValorReemplazar):
    datset.columns = datset.columns.str.replace(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', regex=True) #para quitar salto de linea y espacios al inicio y al final en el nombre columna
    datset[Nobrecolumna] = datset[Nobrecolumna].replace(ValorBusar, ValorReemplazar) # reemplaza el valor para unificar data
    return datset



# llamado de la funcion principal que procesa la informacion
# Cargar el conjunto de datos desde un archivo CSV
df_2023 = pd.read_excel('datos_2023.xlsx',sheet_name="Data privot")
df_2025Directivo = pd.read_excel('datos_2025_directivos.xlsx',sheet_name="Hoja1")
df_2025Miembro = pd.read_excel('datos_2025_miembros.xlsx',sheet_name="Hoja1")

#cargando los datos de las preguntas que se van a tratar
df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_general_090425.xlsx',sheet_name="Hoja1",header=0)
df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_general_090425.xlsx',sheet_name="Hoja1",header=1)

# Limpiamos los datas set de cualquier caracter especial
# df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.applymap(limpiar_texto)
# df_2025PreguntasMiembro = df_2025PreguntasMiembro.applymap(limpiar_texto)
df_2023 = df_2023.applymap(limpiar_texto)
# df_2025Directivo = df_2025Directivo.applymap(limpiar_texto)
# df_2025Miembro = df_2025Miembro.applymap(limpiar_texto)

#Buscando la preguntas que tiene respuesta liker y si o no
df_2025PreguntasDirectivo = df_2025PreguntasDirectivo[df_2025PreguntasDirectivo['Tipo de Pregunta'].isin(['Sí o No', 'Likert'])]
df_2025PreguntasMiembro = df_2025PreguntasMiembro[df_2025PreguntasMiembro['Tipo'].isin(['Sí o No', 'Likert','Sí/no'])]

df_2025PreguntasMiembro.rename(columns={'Tipo': 'Tipo de Pregunta'}, inplace=True)


#haciendo el cruce de informacion para obtener los datos que nos interesa trabaja

df_2025Directivo = pd.merge(df_2025Directivo, df_2025PreguntasDirectivo, left_on='Pregunta', right_on='Pregunta', how='inner')
df_2025Miembro = pd.merge(df_2025Miembro, df_2025PreguntasMiembro, left_on='Pregunta', right_on='Pregunta', how='inner')


# Limpieza de datos

df_2023[f'Respuesta_original'] = df_2023["Respuesta"]
df_2023['año'] = "2023"
df_2023['Excel Origen'] = f"Original 2023"

df_2025Directivo[f'Respuesta_original'] = df_2025Directivo["Respuesta"]
df_2025Directivo['año'] = "2025"
df_2025Directivo['Excel Origen'] = f"Directiva 2025"


df_2025Miembro[f'Respuesta_original'] = df_2025Miembro["Respuesta"]
df_2025Miembro['año'] = "2025"
df_2025Miembro['Excel Origen'] = f"Miembro 2025"



df_2025Directivo = LimpiezaDatos(df_2025Directivo,"Respuesta")
df_2025Miembro = LimpiezaDatos(df_2025Miembro,"Respuesta")


df_2025Directivo = ReemplazarValorDataSet(df_2025Directivo
                                          ,"Subdimension"
                                          ,"1.3 Definición del Gestión del Conocimiento en la organización"
                                          ,"1.1 Definición del Gestión del Conocimiento en la organización")

df_2025Miembro =  ReemplazarValorDataSet(df_2025Miembro
                                         ,"Subdimension"
                                         ,"1.3 Definición del Gestión del Conocimiento en la organización"
                                         ,"1.1 Definición del Gestión del Conocimiento en la organización")



#calculos de los promedios por dimension
ResultadoDimensiones2023=CalcularPromedioDimension(df_2023
                                                   ,"2023"
                                                   ,"General")
ResultadoDimensionesDirectivo2025=CalcularPromedioDimension(df_2025Directivo
                                                            ,"2025"
                                                            ,"Directiva")
ResultadoDimensionesMiembro2025=CalcularPromedioDimension(df_2025Miembro
                                                          ,"2025"
                                                          ,"Miembro")

#calculo por el promedio de dimension componentes y persona
promedio_dimension_2023 = CalculosPromediosComponenteDataSet(df_2023
                                                             ,"2023"
                                                             ,"General")
promedio_dimension_directivo= CalculosPromediosComponenteDataSet(df_2025Directivo
                                                                 ,"2025"
                                                                 ,"Directivo")
promedio_dimension_Miembro= CalculosPromediosComponenteDataSet(df_2025Miembro
                                                               ,"2025"
                                                               ,"Miembro")


#uniendo los dataset en uno solo
df_unidoDimesion = pd.concat([ResultadoDimensiones2023
                              , ResultadoDimensionesDirectivo2025
                              ,ResultadoDimensionesMiembro2025]
                              , ignore_index=True)
df_Unidocomponente  = pd.concat([promedio_dimension_2023
                                 , promedio_dimension_directivo
                                 ,promedio_dimension_Miembro]
                                 , ignore_index=True)

df_limpiezaUnido = pd.concat([df_2023
                            , df_2025Directivo
                            ,df_2025Miembro]
                            , ignore_index=True)
df_limpiezaUnido = df_limpiezaUnido.drop(columns=['Texto','DateRecord','TipoPregunta','Unnamed: 0'])

# Guardar los dataset en un archivo Excel con varias hojas
with pd.ExcelWriter('Resultado.xlsx', engine='openpyxl') as writer:
    df_limpiezaUnido.to_excel(writer, sheet_name='LimpiezaDataSet', index=False)
    df_unidoDimesion.to_excel(writer, sheet_name='Promedio Dimension', index=False)
    df_Unidocomponente.to_excel(writer, sheet_name='Promedio Dimension Componente por personas', index=False)
    ResultadoDimensiones2023.to_excel(writer, sheet_name='ResultadoDimensiones2023', index=False)
    ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='ResultadoDimesionProcesoDirectivo2025', index=False)
    ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='ResultadoDimesionProcesoMiembro2025', index=False)

print("fin")
# Leer datos desde CSV
# df = pd.read_csv("ejemplo_radar_long.csv", delimiter=";")

# # Configuración del gráfico
# labels = df['Habilidad'].unique()
# num_vars = len(labels)
# angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
# angles += angles[:1]

# # Crear figura
# fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# # Función para agregar una persona al gráfico
# def add_person(nombre, color):
#     valores = df[df['Nombre'] == nombre].sort_values('Habilidad')['Puntuación'].tolist()
#     valores += valores[:1]
#     ax.plot(angles, valores, label=nombre, color=color)
#     ax.fill(angles, valores, alpha=0.25, color=color)

# # Colores y nombres
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
# nombres = df['Nombre'].unique()
# for i, nombre in enumerate(nombres):
#     add_person(nombre, colors[i % len(colors)])

# # Personalización
# ax.set_theta_offset(np.pi / 2)
# ax.set_theta_direction(-1)
# ax.set_thetagrids(np.degrees(angles[:-1]), labels)
# ax.set_title('Comparación de Habilidades', size=15)
# ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# plt.tight_layout()
# plt.show()
