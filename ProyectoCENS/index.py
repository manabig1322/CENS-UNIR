import pandas as pd
import re
import unicodedata
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import pi
import seaborn as sns
#import os

def LimpiezaDatos(df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro):
    
    
    df_2025Directivos = QuitarEspaciosCeldasAcentosColumnas(df_2025Directivos)
    df_2025Miembros = QuitarEspaciosCeldasAcentosColumnas(df_2025Miembros)
    df_2025PreguntasDirectivo = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasDirectivo)
    df_2025PreguntasMiembro = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasMiembro)

    #renombrando las columnas para unificar nombres
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Componente': 'Subdimension'})

    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Dimensión': 'Dimension'})


    #Quitando los espacios en blanco y quitando acentos de los nombres de las columnas
    # df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"Dimension")
    # df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"Dimension")
    # df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"Dimension")
    # df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"Dimension")
    
    # df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"Subdimension")
    # df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"Subdimension")
    # df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"Subdimension")
    # df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"Subdimension")

    # df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"TipoPregunta")
    # df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"TipoPregunta")
    # df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"TipoPregunta")
    # df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"TipoPregunta")

    
    #quitando los numeros y puntos
    df_2025Miembros = limpiar_columna_numeros(df_2025Miembros,"Dimension")
    df_2025Directivos = limpiar_columna_numeros(df_2025Directivos,"Dimension")
    df_2025PreguntasDirectivo = limpiar_columna_numeros(df_2025PreguntasDirectivo,"Dimension")
    df_2025PreguntasMiembro = limpiar_columna_numeros(df_2025PreguntasMiembro,"Dimension")
    
    df_2025Miembros = limpiar_columna_numeros(df_2025Miembros,"Subdimension")
    df_2025Directivos = limpiar_columna_numeros(df_2025Directivos,"Subdimension")
    df_2025PreguntasDirectivo = limpiar_columna_numeros(df_2025PreguntasDirectivo,"Subdimension")
    df_2025PreguntasMiembro = limpiar_columna_numeros(df_2025PreguntasMiembro,"Subdimension")
    

       #creando diccionario para reemplazar los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
       
    diccionario_dimension = {
        'Dimension de Indicadores':'Indicadores',
        'Dimensión de los Procesos de Gestión del Conocimiento':'Procesos',
        'Dimensión de la Tecnología':'Tecnologia',
        'Dimensión Humana':'Humana',
        'Dimensión de Indicadores':'Indicadores',
        'Dimensión de la Estrategía y Dirección':'Estrategia y direccion',
        'Estrategia y dirección':'Estrategia y direccion',
        'Tecnología':'Tecnologia',
        'Ciclos de conversión': 'Ciclos de conversion',
        'Tipo de tecnología':'Tipo de tecnologia',
        'Uso de tecnología':'Uso de tecnologia'    }


    #creando diccionario para reemplazar los nombres de las componente por su nombre corto de componente en el dataset
    diccionario_componente = {
        'Definición del Gestión del Conocimiento en la organización':'Definicion de gestion del conocimiento',
        'Definición de gestión del conocimiento':'Definicion de gestion del conocimiento',
        'Motivación e incentivos':'Motivacion',
        'Matriz de conocimiento estratégico': 'Matriz de conocimiento',
        'Procesos de gestión del conocimiento' :'Procesos',
        'Plan estratégico':'Plan estrategico',
        'Tipo de tecnología':'Tipo de tecnologia',
        'Indicadores de generación de valor':'Indicadores de generacion de valor',
        'Ciclos de conversión':'Ciclos de conversion',
        'Ciclos de Conversión':'Ciclos de conversion',
        'Uso de tecnología':'Uso de tecnologia',
        'Ciclos de conversión': 'Ciclos de conversion',
        'Plan estratégico':'Plan estrategico',
        'Tipo de tecnología':'Tipo de tecnologia',
        'Uso de tecnología':'Uso de tecnologia',
        'Comunidades de Conocimiento':'Comunidades de conocimiento',
        'Motivación':'Motivacion',
        'Redes de Conocimiento':'Red de conocimiento'

    }
    
    diccionario_tipo_pregunta ={
        "Opción única":"Opcion unica",
        "Selección múltiple con texto":"Seleccion multiple con texto"
        }
       #reemplazando los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
    for llave, valor in diccionario_dimension.items():
           df_2025Directivos = ReemplazarValorDataSet(df_2025Directivos
                                               ,"Dimension"
                                               ,llave
                                               ,valor)
           df_2025Miembros = ReemplazarValorDataSet(df_2025Miembros
                                               ,"Dimension"
                                               ,llave
                                               ,valor)
           df_2025PreguntasDirectivo= ReemplazarValorDataSet(df_2025PreguntasDirectivo
                                               ,"Dimension"
                                               ,llave
                                               ,valor)
           df_2025PreguntasMiembro= ReemplazarValorDataSet(df_2025PreguntasMiembro
                                               ,"Dimension"
                                               ,llave
                                               ,valor)

       #reemplazando los nombres de las componente por su nombre corto de componente en el dataset
    for llave, valor in diccionario_componente.items():
           df_2025Directivos = ReemplazarValorDataSet(df_2025Directivos
                                               ,"Subdimension"
                                               ,llave
                                               ,valor)
           df_2025Miembros = ReemplazarValorDataSet(df_2025Miembros
                                               ,"Subdimension"
                                               ,llave
                                               ,valor)
           df_2025PreguntasDirectivo= ReemplazarValorDataSet(df_2025PreguntasDirectivo
                                               ,"Subdimension"
                                               ,llave
                                               ,valor)
           df_2025PreguntasMiembro= ReemplazarValorDataSet(df_2025PreguntasMiembro
                                               ,"Subdimension"
                                               ,llave
                                               ,valor)
           
    for llave, valor in diccionario_tipo_pregunta.items():
        df_2025Directivos = ReemplazarValorDataSet(df_2025Directivos
                                                      ,"TipoPregunta"
                                                      ,llave
                                                      ,valor)
        df_2025Miembros = ReemplazarValorDataSet(df_2025Miembros
                                                      ,"TipoPregunta"
                                                      ,llave
                                                      ,valor)



    # quitando filas en Minusculas
    df_2025Miembros =  QuitarFilaConMinusculas(df_2025Miembros, "Persona")
    df_2025Directivos =  QuitarFilaConMinusculas(df_2025Directivos, "Persona")
    
    return df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro

#funcion que valida si hay coma en la cadena
def contiene_coma(cadena):
    if pd.isna(cadena):
        return False
    return ',' in cadena
def limpiar_texto(texto):
     
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'[0-9.]', '',texto)
    return texto.strip()

#funcion que quita los numeros y puntos
def limpiar_columna_numeros(df,columna):
    
    if columna not in df.columns:
        return df
    # Limpiar dejando solo dígitos (y opcionalmente punto decimal)
    df[columna] = df[columna].astype(str).apply(limpiar_texto)
    return df
#funcion que quitas los campos que tiene minusculas
def QuitarFilaConMinusculas(df, columna):
    # Filtrar el DataFrame para mantener solo las filas donde 'columna1' está en mayúsculas
    return df[df[columna].str.isupper()]
#fucnion que quitas los acentos para evitar errores
def QuitarEspaciosCeldasAcentosColumnas(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df.columns = [quitar_acentos(col) for col in df.columns]
    return df
#funcion que reemplaza valor en una columna del dataset
def ReemplazarValorDataSet(datset, Nobrecolumna, ValorBusar, ValorReemplazar):
    datset.columns = datset.columns.str.replace(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', regex=True) #para quitar salto de linea y espacios al inicio y al final en el nombre columna
    datset[Nobrecolumna] = datset[Nobrecolumna].replace(ValorBusar, ValorReemplazar) # reemplaza el valor para unificar data
    return datset
def quitar_acentos(texto):
    if isinstance(texto, str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
        return texto_sin_acentos
    return texto
def calcularPromedioTotalDimension(df,columna,valor):
    # Agrupar por 'dimension' y calcular el promedio de 'valor' para cada grupo
    df_promedio = df.groupby(columna)[valor].mean().reset_index()

    # Devolver el nuevo dataset con 'dimension' y 'valor'
    return df_promedio
def calcularPromedioTotalComponente(df,columna1,columna2,valor):
    # Agrupar por 'dimension' y calcular el promedio de 'valor' para cada grupo
    df_promedio = df.groupby([columna1,columna2])[valor].mean().reset_index()

    # Devolver el nuevo dataset con 'dimension' y 'valor'
    return df_promedio
# funcion que calcula el promedio de dimension por componente y persona y despues por dimension
def CalcularPromedioDimension(DataSet, columnaValor, Año, tipoExcel):
    # 1. Convertir 'valor' a numérico, forzando ignorar los valores no numericas
    DataSet[columnaValor] = pd.to_numeric(DataSet[columnaValor], errors='coerce')
    # 2. Promedia el resultados por persona componeten y dimension
    promedio_dimension_componente = DataSet.groupby(['Dimension','Subdimension', 'Persona'])[columnaValor].mean().reset_index()
    # 3. haciendo agrupacion de la dimesiones
    ResultadoDimensiones = promedio_dimension_componente.groupby('Dimension', as_index=False)[columnaValor].mean()
    # 4. Agregando la columna año
    ResultadoDimensiones['año'] = Año
    # 5. Agregando la columna tipo de Excel para saber cual excel uso para la informacion
    ResultadoDimensiones['Excel Origen'] = f"{tipoExcel} {Año}"
    return ResultadoDimensiones
#funcion que calcula el promedio de dimension por componente y persona y despues por componente
def CalculosPromediosComponenteDataSet(DataSet, ColumnaValor, Año, tipoExcel):
    
    # 1. Convertir 'valor' a numérico, forzando ignorar los valores no numericas
    DataSet[ColumnaValor] = pd.to_numeric(DataSet[ColumnaValor], errors='coerce')
    # 2. Promedia el resultados por persona componeten y dimension
    promedio_dimension_componente = DataSet.groupby(['Dimension','Subdimension', 'Persona'])[ColumnaValor].mean().reset_index()
    
    # 3. Promedia esos resultados por dimension y componetn
    promedio_componente = promedio_dimension_componente.groupby(['Dimension','Subdimension'])[ColumnaValor].mean().reset_index()
   
    # 4. Renombrar la columna para mayor claridad
    promedio_componente.rename(columns={'Respuesta': 'promedio_respuesta'}, inplace=True)

    # 5. agrega la columna de año
    promedio_componente["año"]=Año
    # 6. agrega la columan de  tipo de excel para saber cual excel uso para los calculos
    promedio_componente["Excel Origen"]=f"{tipoExcel} {Año}"

    return promedio_componente
#funcion que agrega los componente faltantes
def AgregarComponenteFaltantes(df1, df2,columnaDimension, columnaComponente, ColumnaValor):
     
    # Obtener listado único de Dimension
    listadoDimensionDataSetPreguntas = set(df1[columnaDimension].dropna().unique())

    for valDimension in listadoDimensionDataSetPreguntas:
      
        # Obtener listado único de Componente
        listadoComponenteDataSetRespuesta = df2[df2[columnaDimension] == valDimension][columnaComponente].dropna().unique()

        if len(listadoComponenteDataSetRespuesta) == 0:
            # Si no hay coincidencias, crear una nueva fila con el valor de df2
            listado_componente = df1[df1[columnaDimension] == valDimension][columnaComponente].dropna().unique()
           
            # Crear nuevas filas con los valores faltantes
            # Rellenamos el resto de columnas con NaN
            nueva_filas = pd.DataFrame(columns=df2.columns)
            nueva_filas[columnaComponente] = listado_componente
            nueva_filas[columnaDimension] = valDimension
            nueva_filas[ColumnaValor]= 1
            nueva_filas["Persona"]=" " #<-- importante para la agrupacion
      
            df2 = pd.concat([df2, nueva_filas], ignore_index=True)
        else:

            #busca el listado de componente del dataset de preguntas            
            listado_componente1 = set(df1[df1[columnaDimension] == valDimension][columnaComponente].dropna().unique())
           
            #busca el lista de componente del dataset de respuesta
            listadoComponenteDataSetRespuesta = set(listadoComponenteDataSetRespuesta)
            
            #devuelviendo la diferencia faltante
            faltantes = list(listado_componente1 - listadoComponenteDataSetRespuesta)

            # Crear nuevas filas con los valores faltantes
            # Rellenamos el resto de columnas con NaN
            nueva_filas = pd.DataFrame(columns=df2.columns)
            nueva_filas[columnaComponente]= list(faltantes)
            nueva_filas[columnaDimension] = valDimension
            nueva_filas[ColumnaValor]= 1
            nueva_filas["Persona"]=" " #<-- importante para la agrupacion
         
            df2 = pd.concat([df2, nueva_filas], ignore_index=True)
              
    #regresando el dataset actualizado con los componentes faltante agregados
    return df2

def procesar_valores(valor):
    if pd.isna(valor):
        return []
    valores = [v.strip().lower() for v in str(valor).split(',')]
    numeros = [int(v) for v in valores if v.isdigit()]
    otros = any('otro' in v for v in valores)
    return numeros, otros  
def AgregarConteoPreguntasSeleccionMultiple(df2,columnaDimension, columnaComponente,ColumnaPregunta,ColumnaTipoPregunta, ColumnaValor):

  
    # Filtrar registros donde TipoPregunta = "Seleccion multiple con texto"
    df_filtrado = df2[df2['TipoPregunta'] == "Seleccion multiple con texto"].copy()
    
# Procesar todos los registros para encontrar el mínimo y máximo global
    todos_numeros = []
    otros_flag = False
    
    for valor in df_filtrado['Valor']:
        numeros, tiene_otros = procesar_valores(valor)
        todos_numeros.extend(numeros)
        if tiene_otros:
            otros_flag = True
    
    valor_min = min(todos_numeros)
    valor_max = max(todos_numeros)
    
    
    # Crear nuevas columnas dinámicamente
    columnas_nuevas = [f'respuesta{n}' for n in range(valor_min, valor_max+1)]
    if otros_flag:
        columnas_nuevas.append('respuesta_otros')
    
    columnas_dimension = [f'dimension{n}' for n in range(valor_min, valor_max+1)]
    columnas_subdimension = [f'subdimension{n}' for n in range(valor_min, valor_max+1)]
    columnas_pregunta = [f'pregunta{n}' for n in range(valor_min, valor_max+1)]
    
    nuevas_columnas = columnas_nuevas + columnas_dimension + columnas_subdimension + columnas_pregunta
    
    # Crear un DataFrame vacío con las nuevas columnas
    df_expandido = pd.DataFrame(columns=nuevas_columnas)
    
    # Recorrer los registros para llenar el nuevo DataFrame
    for idx, row in df_filtrado.iterrows():
        numeros, tiene_otros = procesar_valores(row['Valor'])
        nueva_fila = {col: np.nan for col in nuevas_columnas}
    
        for numero in numeros:
            col_name = f'respuesta{numero}'
            if col_name in nueva_fila:
                nueva_fila[col_name] = numero
                nueva_fila[f'dimension{numero}'] = row['Dimension']
                nueva_fila[f'subdimension{numero}'] = row['Subdimension']
                nueva_fila[f'pregunta{numero}'] = row['Pregunta']
    
        if tiene_otros:
            nueva_fila['respuesta_otros'] = 1
            nueva_fila['dimension1'] = row['Dimension']
            nueva_fila['subdimension1'] = row['Subdimension']
            nueva_fila['pregunta1'] = row['Pregunta']
    
        df_expandido = pd.concat([df_expandido, pd.DataFrame([nueva_fila])], ignore_index=True)
    
    # Ahora agrupar y contar la cantidad de registros por columna, agrupando por Dimension, Subdimension y Pregunta
    # Preparamos un DataFrame auxiliar para contar
    lista_resultados = []
    
    for numero in range(valor_min, valor_max+1):
        col = f'respuesta{numero}'
        dim_col = f'dimension{numero}'
        subdim_col = f'subdimension{numero}'
        preg_col = f'pregunta{numero}'
    
        temp_df = df_expandido[[col, dim_col, subdim_col, preg_col]].dropna()
        temp_df = temp_df.rename(columns={
            dim_col: 'Dimension',
            subdim_col: 'Subdimension',
            preg_col: 'Pregunta'
        })
        temp_df['Respuesta'] = col
        lista_resultados.append(temp_df)
    
    # Para respuesta_otros
    if 'respuesta_otros' in df_expandido.columns:
        temp_df = df_expandido[['respuesta_otros', 'dimension1', 'subdimension1', 'pregunta1']].dropna()
        temp_df = temp_df.rename(columns={
            'dimension1': 'Dimension',
            'subdimension1': 'Subdimension',
            'pregunta1': 'Pregunta'
        })
        temp_df['Respuesta'] = 'respuesta_otros'
        lista_resultados.append(temp_df)
    
    # Concatenamos todos
    df_resultado = pd.concat(lista_resultados, ignore_index=True)
    
    # Contar por Dimension, Subdimension, Pregunta y Respuesta
    conteo_final = df_resultado.groupby(['Dimension', 'Subdimension', 'Pregunta', 'Respuesta']).size().reset_index(name='Cantidad')
    
   
    return conteo_final

def AgregarConteoPreguntasLikert(df):

 
        # Filtrar solo filas con TipoPregunta igual a 'Likert'
    df_filtrado = df[df['TipoPregunta'] == 'Likert']
    
    # Agrupar por Dimension, Subdimension, Pregunta y Valor (incluyendo NaN)
    conteo = df_filtrado.groupby(['Dimension', 'Subdimension', 'Pregunta', 'Valor'], dropna=False) \
                        .size().reset_index(name='Cantidad')
    
    # Convertir valores numéricos (ignorar NaN)
    valores_numericos = pd.to_numeric(conteo['Valor'], errors='coerce')
    valor_maximo = int(valores_numericos.max(skipna=True))
    
    # Obtener combinaciones únicas de grupo
    grupos = conteo[['Dimension', 'Subdimension', 'Pregunta']].drop_duplicates()
    
    # Crear lista con todos los valores esperados (1 al max)
    valores_completos = list(range(1, valor_maximo + 1))
    
    # Crear combinaciones para valor_1 hasta valor_n
    grilla = pd.DataFrame([
        (dim, sub, preg, val) 
        for _, (dim, sub, preg) in grupos.iterrows()
        for val in valores_completos
    ], columns=['Dimension', 'Subdimension', 'Pregunta', 'Valor'])
    
    # Combinar con los datos reales (sin NaN)
    conteo_sin_nan = conteo[conteo['Valor'].notna()].copy()
    conteo_sin_nan['Valor'] = conteo_sin_nan['Valor'].astype(int)
    
    conteo_completo = pd.merge(grilla, conteo_sin_nan, 
                               on=['Dimension', 'Subdimension', 'Pregunta', 'Valor'], 
                               how='left').fillna({'Cantidad': 0})
    
    # Crear columna Valor_Nombre como valor_1, valor_2, etc.
    conteo_completo['Valor_Nombre'] = conteo_completo['Valor'].apply(lambda x: f'valor_{int(x)}')
    conteo_completo['Cantidad'] = conteo_completo['Cantidad'].astype(int)
    
    # ---- AÑADIR valor_nan con cantidad = 0 si no existe ----
    # Identificar grupos que NO tienen valor_nan
    grupos_con_nan = conteo[conteo['Valor'].isna()][['Dimension', 'Subdimension', 'Pregunta']]
    grupos_faltantes_nan = pd.merge(grupos, grupos_con_nan, 
                                    on=['Dimension', 'Subdimension', 'Pregunta'], 
                                    how='left', indicator=True)
    grupos_sin_nan = grupos_faltantes_nan[grupos_faltantes_nan['_merge'] == 'left_only'] \
                        .drop(columns='_merge')
    
    # Crear registros valor_nan = 0 para esos grupos
    faltantes_nan = grupos_sin_nan.copy()
    faltantes_nan['Valor_Nombre'] = 'valor_nan'
    faltantes_nan['Cantidad'] = 0
    
    # Tomar registros valor_nan existentes
    conteo_nan = conteo[conteo['Valor'].isna()].copy()
    conteo_nan['Valor_Nombre'] = 'valor_nan'
    conteo_nan = conteo_nan[['Dimension', 'Subdimension', 'Pregunta', 'Valor_Nombre', 'Cantidad']]
    
    # Unir los existentes con los faltantes
    valor_nan_final = pd.concat([
        conteo_nan,
        faltantes_nan[['Dimension', 'Subdimension', 'Pregunta', 'Valor_Nombre', 'Cantidad']]
    ], ignore_index=True)
    
    # Juntar todo: valores del 1 al n + valor_nan
    conteo_resultado = pd.concat([
        conteo_completo[['Dimension', 'Subdimension', 'Pregunta', 'Valor_Nombre', 'Cantidad']],
        valor_nan_final
    ], ignore_index=True)
    
    # Ordenar: valor_1 ... valor_n, luego valor_nan
    def extraer_orden(valor_nombre):
        if valor_nombre == 'valor_nan':
            return np.inf
        try:
            return int(valor_nombre.split('_')[1])
        except:
            return np.inf
    
    conteo_resultado['Orden'] = conteo_resultado['Valor_Nombre'].apply(extraer_orden)
    
    # Orden final
    conteo_final = conteo_resultado.sort_values(by=['Dimension', 'Subdimension', 'Pregunta', 'Orden']) \
                                    .drop(columns='Orden')
    
    # Mostrar o guardar
    # conteo_final.to_csv('conteo_likert_completo_con_nan.csv', index=False)
    #print(conteo_final)
    return conteo_final
        
# Preparar título manejando largo de la pregunta
def dividir_titulo(texto, max_caracteres=80):
    palabras = texto.split()
    lineas = []
    linea_actual = ''
    for palabra in palabras:
        if len(linea_actual) + len(palabra) + 1 <= max_caracteres:
            linea_actual += ' ' + palabra if linea_actual else palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return '\n'.join(lineas)

def GenerarGraficaPorPregunta(df, ExcelOrgien):
 
    # Diccionario para traducir Respuesta a significado
    if ExcelOrgien == "Miembros":
        significados = {
            'respuesta1': 'Nada efectivas',
            'respuesta2': 'Poco efectivas',
            'respuesta3': 'Moderadamente efectivas',
            'respuesta4': 'Efectivas',
            'respuesta5': 'Muy efectivas',
            'respuesta6': '',
            'respuesta_otros': 'Otros'
        }
    else:
        significados = {
            'respuesta1': 'La falta de confianza entre los miembros',
            'respuesta2': 'El tiempo escaso para compartir información',
            'respuesta3': 'Moderadamente efectivas',
            'respuesta4': 'La escasa practicidad de las plataformas digitales',
            'respuesta5': 'Los bajos incentivos para compartir conocimiento',
            'respuesta6': 'La actitud de las personas',
            'respuesta_otros': 'Otros (especificar)'
        }

    mostrar_otros = False
    if not mostrar_otros:
        df = df[df['Respuesta'] != 'respuesta_otros']

    grupos = df.groupby(['Dimension', 'Subdimension', 'Pregunta'])

    for (dimension, subdimension, pregunta), datos in grupos:
        plt.figure(figsize=(10, 6))

        datos['Orden'] = datos['Respuesta'].apply(lambda x: int(x.replace('respuesta', '').replace('_otros', '99')))
        datos = datos.sort_values('Orden')

        respuestas = list(datos['Respuesta'])
        etiquetas_numericas = list(range(1, len(respuestas) + 1))
        etiquetas_texto = [significados.get(resp, resp) for resp in respuestas]
        cantidades = datos['Cantidad']
        total_respuestas = cantidades.sum()

        # Crear colores degradados en azul (oscuro a claro)
        cmap = cm.get_cmap('Blues')
        degradado = cmap(np.linspace(0.9, 0.4, len(respuestas)))

        barras = plt.bar(etiquetas_numericas, cantidades, color=degradado)

        # Mostrar conteo y porcentaje encima de cada barra
        for barra, cantidad in zip(barras, cantidades):
            porcentaje = (cantidad / total_respuestas) * 100
            texto = f"{int(cantidad)} ({porcentaje:.1f}%)"
            plt.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + (max(cantidades) * 0.00),
                texto,
                ha='center',
                va='bottom',
                fontsize=10
            )

        titulo_formateado = f"{dimension} - {subdimension}\n{dividir_titulo(pregunta)}"
        plt.title(titulo_formateado, fontsize=14)
        plt.xlabel('Respuestas (número)')
        plt.ylabel('Cantidad')
        plt.xticks(etiquetas_numericas, [str(n) for n in etiquetas_numericas], fontsize=12)

        # Leyenda con degradado y descripción
        handles = [plt.Rectangle((0, 0), 1, 1, color=degradado[i]) for i in range(len(respuestas))]
        labels = [f"{i + 1}: {etiquetas_texto[i]}" for i in range(len(etiquetas_texto))]
        plt.legend(
            handles, labels, title="Respuestas",
            loc='upper center', bbox_to_anchor=(0.5, -0.18),
            ncol=2, fancybox=True, shadow=True, frameon=True
        )

        plt.subplots_adjust(top=0.85)
        plt.tight_layout()
        plt.show()
        plt.close()








def GenerarGraficaRadarDimensiones(df_promedio_dimension):
    col_dim    = 'Dimension'
    col_origen = 'Excel Origen'
    col_valor  = 'Valor'

    df_pivot = df_promedio_dimension.pivot(
        index=col_dim, columns=col_origen, values=col_valor
    ).fillna(0)

    labels_real = df_pivot.index.tolist()
    num_vars    = len(labels_real)
    labels_num  = [str(i+1) for i in range(num_vars)]

    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))

    colores = {
        'Miembro 2025':   '#0000FF',
        'Directiva 2025': '#228B22'
    }

    for origen in df_pivot.columns:
        vals = df_pivot[origen].tolist()
        vals += vals[:1]
        ax.plot(angles, vals, label=origen, color=colores.get(origen,'#999999'))
        ax.fill(angles, vals, alpha=0.1, color=colores.get(origen,'#999999'))

    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels_num)

    fig.suptitle(
        "Prom. Directivos vs Miembros por Dimensión",
        fontsize=14, y=0.97, ha='center'
    )

    fig.subplots_adjust(left=0.05, right=0.7, top=0.9, bottom=0.2)

    lines = []
    for i, dim in enumerate(labels_real):
        prom = df_pivot.loc[dim].mean()
        lines.append(f"{i+1}: {dim}  valor {prom:.2f}")
    texto_dim = "\n".join(lines)

    plt.figtext(
        0.75, 0.5, texto_dim,
        ha='left', va='center',
        fontsize=10, fontfamily='monospace'
    )

    ax.legend(
        loc='lower center',
        bbox_to_anchor=(0.5, -0.05),
        ncol=2,
        frameon=False
    )

    plt.show()



def generar_grafica_radar_total(df_promedio, Columna, Valor):
    # Asignar números a las dimensiones
    dimensiones = df_promedio[Columna].unique()
    dimension_dict = {dim: i+1 for i, dim in enumerate(dimensiones)}  # Asigna un número a cada dimensión

    # Reemplazar las dimensiones por números
    df_promedio['dimension_num'] = df_promedio[Columna].map(dimension_dict)
    
    # Definir los colores personalizados para las dimensiones
    colores_personalizados = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Número de variables (dimensiones)
    num_vars = len(dimensiones)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Cerrar el círculo

    # Valores para la gráfica (promedio por dimensión)
    valores = df_promedio['Valor'].tolist()
    valores += valores[:1]  # Cerrar el círculo

    # Determinar el valor máximo y ajustar la escala
    max_valor = max(valores)
    scale_max = np.ceil(max_valor)  # Redondear hacia el siguiente entero
    scale_max = int(scale_max + 2)  # Asegurarse de que el valor máximo sea el valor más alto + 2
    ticks = np.arange(0, scale_max, 1)  # Establecer las marcas de la escala solo con enteros

    # Crear la figura de radar
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

    # Dibujar cada dimensión con su color respectivo
    for i, dim in enumerate(dimensiones):
        color = colores_personalizados[i % len(colores_personalizados)]  # Asegurar que se asignen colores de forma cíclica
        valores_dim = [df_promedio[df_promedio[Columna] == dim][Valor].values[0]] * (num_vars + 1)  # Repetir el valor para cerrar el círculo
        ax.plot(angles, valores_dim, linewidth=2, linestyle='solid', label=f'{dimension_dict[dim]}: {dim}', color=color)
        ax.fill(angles, valores_dim, alpha=0.1, color=color)

        # Agregar el valor en la punta de la gráfica
        valor_promedio = df_promedio[df_promedio[Columna] == dim][Valor].values[0]
        ax.text(angles[i], valores[i], f'{valor_promedio:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=10, color=color)

    # Ajustar los ejes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Etiquetas con números en lugar de nombres de dimensiones
    ax.set_thetagrids(np.degrees(angles[:-1]), [str(dimension_dict[dim]) for dim in dimensiones])

    # Establecer la escala en los ejes radiales
    ax.set_rlabel_position(0)  # Mover las etiquetas radiales
    ax.set_rticks(ticks)  # Establecer las marcas de la escala solo con enteros

    # Título
    ax.set_title('Prom. Total Dimensión', size=16, pad=20)

    # Leyenda con los números, dimensiones y valores asociados, movida a la derecha y centrada
    leyenda_dimensiones = [f"{i+1}: {dim}" for i, dim in enumerate(dimensiones)]
    ax.legend(leyenda_dimensiones, loc='center left', bbox_to_anchor=(1.1, 0.5), fontsize=10, title="Dimensiones")

    # Ajustar el layout para evitar que la leyenda se sobreponga
    plt.tight_layout()
    plt.show()




def generar_graficas_componentes_total(df):
    
    dimensiones = df['Dimension'].unique()

    # Colores personalizables para subdimensiones
    colores_subdimensiones = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    for dimension in dimensiones:
        subset = df[df['Dimension'] == dimension]
        subdimensiones = subset['Subdimension'].tolist()
        valores = subset['Valor'].tolist()

        if len(subdimensiones) > 2:
            # Gráfica de Radar
            num_vars = len(subdimensiones)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]  # Cerrar círculo

            valores_cerrado = valores + valores[:1]

            fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

            # Dibujar los valores
            ax.plot(angles, valores_cerrado, linewidth=2, linestyle='solid', color='#1f77b4')
            ax.fill(angles, valores_cerrado, alpha=0.1, color='#1f77b4')

            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)

            # Números en lugar de nombres
            numeros = list(range(1, num_vars + 1))
            ax.set_thetagrids(np.degrees(angles[:-1]), labels=[str(n) for n in numeros])

            # Mostrar los valores en cada punta
            for angle, valor in zip(angles[:-1], valores):
                ax.text(angle, valor + 0.1, f"{valor:.2f}", ha='center', va='bottom', fontsize=9, color='black')

            # Ajustar escala con enteros
            max_val = max(valores)
            ax.set_rgrids(range(1, int(np.ceil(max_val)) + 1))

            # Título
            plt.suptitle(f'Dimensión: {dimension}', fontsize=16, y=0.95)

            # Construir la leyenda manualmente
            leyenda_texto = ""
            for idx, (sub, val) in enumerate(zip(subdimensiones, valores)):
                color = colores_subdimensiones[idx % len(colores_subdimensiones)]
                leyenda_texto += f"{idx+1}: {sub} ({val:.2f})\n"

            # Agregar la leyenda como texto a la derecha
            plt.text(1.2, 0.5, leyenda_texto, transform=ax.transAxes,
                     fontsize=10, va='center', ha='left', linespacing=1.5,
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray'))

            plt.subplots_adjust(right=0.75, top=0.9, bottom=0.1)
            plt.show()

        else:
            # Gráfica de Barras
            fig, ax = plt.subplots(figsize=(7, 6))

            sns.barplot(
                data=subset,
                x='Subdimension',
                y='Valor',
                palette='pastel',
                ax=ax
            )

            # Mostrar el valor encima de cada barra
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', label_type='edge', padding=8)

            # Ajustar espacio para los valores
            ax.margins(y=0.2)
            ax.set_title(f'Dimensión: {dimension}', size=16, pad=20)
            plt.subplots_adjust(top=0.85, bottom=0.2)
            plt.show()


def crear_grafica_radar_componente(data, dimension, colores_excel_origen):
    etiquetas_real = list(data['Subdimension'].unique())
    num_vars = len(etiquetas_real)
    labels_num = [str(i+1) for i in range(num_vars)]

    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

    # Pivot para promedio por subdimension
    df_sub_pivot = data.pivot(
        index='Subdimension',
        columns='Excel Origen',
        values='Valor'
    ).fillna(0)

    origenes = data['Excel Origen'].unique()
    for origen in origenes:
        subset = data[data['Excel Origen'] == origen]
        valores = subset.set_index('Subdimension') \
                        .reindex(etiquetas_real)['Valor'] \
                        .fillna(0).tolist()
        valores += valores[:1]
        ax.plot(angles, valores,
                linewidth=2, linestyle='solid',
                label=origen,
                color=colores_excel_origen.get(origen, '#333333'))
        ax.fill(angles, valores,
                alpha=0.1,
                color=colores_excel_origen.get(origen, '#333333'))

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels_num)

    fig.suptitle(f"Dimensión: {dimension}", fontsize=14, y=0.98, ha='center')
    fig.subplots_adjust(left=0.05, right=0.75, top=0.85, bottom=0.25)

    # Leyenda de subdimensiones a la derecha con valor promedio
    líneas = []
    for i, sub in enumerate(etiquetas_real):
        prom = df_sub_pivot.loc[sub].mean()
        líneas.append(f"{i+1}: {sub}  valor {prom:.2f}")
    texto_sub = "\n".join(líneas)

    plt.figtext(0.78, 0.5, texto_sub,
                ha='left', va='center',
                fontsize=10, fontfamily='monospace')

    # Leyenda de orígenes abajo, ajustada más abajo
    ax.legend(loc='lower center',
              bbox_to_anchor=(0.5, -0.2),
              ncol=len(origenes),
              frameon=False)

    plt.show()




# Función que genera la gráfica de barras por componente

def crear_grafica_barras_componente(data, dimension, colores_excel_origen):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Crear el gráfico de barras
    sns.barplot(
        data=data,
        x='Subdimension',
        y='Valor',
        hue='Excel Origen',
        palette=colores_excel_origen,
        ax=ax
    )
    
    # Añadir los valores encima de cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height + 0.05, f'{height:.2f}', 
                ha='center', va='center', fontsize=10, color='black')

    # Título y leyenda
    ax.set_title(f'Dimensión: {dimension} (Gráfico de Barras)', fontsize=14)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)

    # Ajuste del diseño para evitar solapamientos
    plt.tight_layout()
    plt.show()

#funcion que genera la grafia de compponente de radar o de barras
def GenerarGraficaComponente(df_promedio_componente):
        # Colores personalizados
    colores_excel_origen = {
        'Miembro 2025': '#00bf74',     # Verde
        'Directivo 2025': '#007bd2'    # Azul
}
    for dimension, grupo in df_promedio_componente.groupby('Dimension'):
        subdimensiones_unicas = grupo['Subdimension'].unique()
        if len(subdimensiones_unicas) <= 2:
            crear_grafica_barras_componente(grupo, dimension,colores_excel_origen)
        else:
            crear_grafica_radar_componente(grupo, dimension,colores_excel_origen)       
#funcion Principal que inicia el programa
def main():
    

    #cargando los dataset de los miembros y directivos de la encuesta 2025 y las preguntas de la encuesta
    df_2025Miembros = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Miembros")
    df_2025Directivos = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Directivos")
    df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_general_090425.xlsx',sheet_name="Hoja1",header=0)
    df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_general_090425.xlsx',sheet_name="Hoja1",header=1)

    df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro = LimpiezaDatos(df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro)


    #agregando los componente que faltan en el dataset de los miembros y directivos 
    df_2025Directivos = AgregarComponenteFaltantes(df_2025PreguntasDirectivo, df_2025Directivos,"Dimension","Subdimension","Valor")
    df_2025Miembros = AgregarComponenteFaltantes(df_2025PreguntasMiembro, df_2025Miembros,"Dimension","Subdimension","Valor")
    
   
    df_ListadoPreguntasEstructuradaDirectiva2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Directivos,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")
    df_ListadoPreguntasEstructuradaMiembro2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Miembros,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")
    
    AgregarConteoPreguntasLikert(df_2025Directivos)
    
    GenerarGraficaPorPregunta(df_ListadoPreguntasEstructuradaDirectiva2025,"Directiva")
    GenerarGraficaPorPregunta(df_ListadoPreguntasEstructuradaMiembro2025,"Miembros")

    df_2025DirectivosImpresion = df_2025Directivos.copy()
    df_2025MiembrosImpresion = df_2025Miembros.copy()

    #calculos de los promedios por dimension
    ResultadoDimensionesDirectivo2025=CalcularPromedioDimension(df_2025Directivos
                                                                ,"Valor"
                                                                ,"2025"
                                                                ,"Directiva")
    ResultadoDimensionesMiembro2025=CalcularPromedioDimension(df_2025Miembros
                                                            ,"Valor"
                                                            ,"2025"
                                                            ,"Miembro")
    

    #calculo por el promedio de dimension componentes y persona
    promedio_dimension_directivo= CalculosPromediosComponenteDataSet(df_2025Directivos
                                                                    ,"Valor"
                                                                    ,"2025"
                                                                    ,"Directivo")
    promedio_dimension_Miembro= CalculosPromediosComponenteDataSet(df_2025Miembros
                                                                    ,"Valor"
                                                                ,"2025"
                                                                ,"Miembro")
    #calculo de promedio total de dimension

    df_promedio_dimension = pd.concat([ResultadoDimensionesDirectivo2025, ResultadoDimensionesMiembro2025], ignore_index=True)
    df_promedio_total_dimension = calcularPromedioTotalDimension(df_promedio_dimension,'Dimension','Valor')
    generar_grafica_radar_total(df_promedio_total_dimension,'Dimension','Valor')
    GenerarGraficaRadarDimensiones(df_promedio_dimension)


    df_promedio_componente = pd.concat([promedio_dimension_directivo, promedio_dimension_Miembro], ignore_index=True)
    df_promedio_total_componente = calcularPromedioTotalComponente(df_promedio_componente,'Dimension','Subdimension','Valor')
    generar_graficas_componentes_total(df_promedio_total_componente)
    GenerarGraficaComponente(df_promedio_componente)

    with pd.ExcelWriter('Respuestas.xlsx', engine='openpyxl') as writer:
        df_2025MiembrosImpresion.to_excel(writer, sheet_name='Miembros', index=False)
        df_2025DirectivosImpresion.to_excel(writer, sheet_name='Directivos', index=False)
        ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='PromedioDirectivosDimension', index=False)
        ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='PromedioMiembroDimension', index=False)
        promedio_dimension_directivo.to_excel(writer, sheet_name='PromedioDirectivoComponente', index=False)
        promedio_dimension_Miembro.to_excel(writer, sheet_name='PromedioMiembroComponente', index=False)
        df_ListadoPreguntasEstructuradaDirectiva2025.to_excel(writer, sheet_name='ListadoPreguntasEstructuradaDirector2025', index=False)
    
    
    
    print("fin de ejecucion")


# llamando de la funcion principal
if __name__ == "__main__":
    main()
