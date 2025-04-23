import pandas as pd
import re
import unicodedata

def limpiar_texto(texto):
    if isinstance(texto, str):
        # Eliminar saltos de línea y caracteres especiales al inicio y al final
        texto = re.sub(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', texto)
        return texto
    return texto  # Retorna el valor original si no es una cadena
def limpiar_numero_punto(texto):
    
    if isinstance(texto, str):
        # Eliminar saltos de línea y caracteres especiales al inicio y al final
        texto = re.sub(r'[0-9.]', '', texto)
        return texto
    return texto  # Retorna el valor original si no es una cadena
def QuitarFilaConMinusculas(df, columna):
    # Filtrar el DataFrame para mantener solo las filas donde 'columna1' está en mayúsculas
    return df[df[columna].str.isupper()]
#funcion que reemplaza valor en una columna del dataset
def ReemplazarValorDataSet(datset, Nobrecolumna, ValorBusar, ValorReemplazar):
    datset.columns = datset.columns.str.replace(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', regex=True) #para quitar salto de linea y espacios al inicio y al final en el nombre columna
    datset[Nobrecolumna] = datset[Nobrecolumna].replace(ValorBusar, ValorReemplazar) # reemplaza el valor para unificar data
    return datset
# funcion que calcula el promedio de dimension por componente y persona y despues por dimension
def CalcularPromedioDimension(DataSet, Año, tipoExcel):
    # 1. Promedia el resultados por persona componeten y dimension
    promedio_dimension_componente = DataSet.groupby(['Dimension','Subdimension', 'Persona'])['Valor'].mean().reset_index()
    # 1. haciendo agrupacion de la dimesiones
    ResultadoDimensiones = DataSet.groupby('Dimension', as_index=False)['Valor'].mean()
    # 2. Agregando la columna año
    ResultadoDimensiones['año'] = Año
    # 3. Agregando la columna tipo de Excel para saber cual excel uso para la informacion
    ResultadoDimensiones['Excel Origen'] = f"{tipoExcel} {Año}"
    return ResultadoDimensiones
#funcion que calcula el promedio de dimension por componente y persona y despues por componente
def CalculosPromediosComponenteDataSet(DataSet, Año, tipoExcel):
    
    # 1. Promedia el resultados por persona componeten y dimension
    promedio_dimension_componente = DataSet.groupby(['Dimension','Subdimension', 'Persona'])['Valor'].mean().reset_index()
    
    # 2. Promedia esos resultados por dimension y componetn
    promedio_componente = promedio_dimension_componente.groupby(['Dimension','Subdimension'])['Valor'].mean().reset_index()
   
    # 3. Renombrar la columna para mayor claridad
    promedio_componente.rename(columns={'Respuesta': 'promedio_respuesta'}, inplace=True)

    # 4. agrega la columna de año
    promedio_componente["año"]=Año
    # 5. agrega la columan de  tipo de excel para saber cual excel uso para los calculos
    promedio_componente["Excel Origen"]=f"{tipoExcel} {Año}"

    return promedio_componente
def AgregarComponenteFaltantes(df1, df2,columnaDimension, columnaCoponente):
    valores_df1 = set(df1[columnaDimension].dropna().unique())

    for colDimension in valores_df1:

        colDimension = colDimension.strip()
        # Obtener listado único del dataset2
        df2_filtrado = df2[df2[columnaDimension] == colDimension]["Subdimension"].dropna().unique()

        if len(df2_filtrado) == 0:
            # Si no hay coincidencias, crear una nueva fila con el valor de df1
            listado_componente = df1[df1[columnaDimension] == colDimension]["Componente"].dropna().unique()
            nueva_filas = pd.DataFrame(columns=df2.columns)
            nueva_filas[columnaCoponente] = listado_componente
            nueva_filas[columnaDimension] = colDimension
            # for col in df2.columns:
            #     if col != columnaCoponente or col != columnaDimension:
            #         nueva_fila[col] = pd.NA
            
            df2_actualizado = pd.concat([df2, nueva_filas], ignore_index=True)
        else:
                          
            valores_df2 = set(df2_filtrado[columnaCoponente].dropna().unique())
            # Identificar los valores que están en df1 pero no en df2
            faltantes = valores_df1 - valores_df2

            # Crear nuevas filas con los valores faltantes
            # Rellenamos el resto de columnas con NaN
            nuevas_filas = pd.DataFrame({columnaCoponente: list(faltantes)})

            for col in df2.columns:
                if col != columnaCoponente:
                    nuevas_filas[col] = pd.NA # o puedes usar None
            # Concatenar las nuevas filas al dataset2
            df2_actualizado = pd.concat([df2, nuevas_filas], ignore_index=True)
              
    #print(f"Se agregaron {len(faltantes)} valores nuevos a '{columnaCoponente}' en el dataset2.")
    return df2_actualizado
# Función para quitar acentos
def quitar_acentos(texto):
    if isinstance(texto, str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
        return texto_sin_acentos
    return texto

#cargando los dataset de los miembros y directivos de la encuesta 2025 y las preguntas de la encuesta
df_2025Miembros = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Miembros")
df_2025Directivos = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Directivos")
df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_general_090425.xlsx',sheet_name="Hoja1",header=0)
df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_general_090425.xlsx',sheet_name="Hoja1",header=1)

#quitando cualquier caracter especial que pueda provovar errors en el dataset
df_2025Miembros = df_2025Miembros.applymap(limpiar_texto)
df_2025Directivos = df_2025Directivos.applymap(limpiar_texto)
df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.applymap(limpiar_texto)
df_2025PreguntasMiembro = df_2025PreguntasMiembro.applymap(limpiar_texto)

#quitando acentos en los dataset
df_2025Miembros = df_2025Miembros.applymap(quitar_acentos)
df_2025Directivos = df_2025Directivos.applymap(quitar_acentos)
df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.applymap(quitar_acentos)
df_2025PreguntasMiembro = df_2025PreguntasMiembro.applymap(quitar_acentos)

#quitando los numeros y puntos
df_2025Miembros = df_2025Miembros.applymap(limpiar_numero_punto)
df_2025Directivos = df_2025Directivos.applymap(limpiar_numero_punto)
df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.applymap(limpiar_numero_punto)
df_2025PreguntasMiembro = df_2025PreguntasMiembro.applymap(limpiar_numero_punto)

# quitando acentos de los nombres de las columnas
df_2025Miembros.columns = [quitar_acentos(col) for col in df_2025Miembros.columns]
df_2025Directivos.columns = [quitar_acentos(col) for col in df_2025Directivos.columns]
df_2025PreguntasDirectivo.columns = [quitar_acentos(col) for col in df_2025PreguntasDirectivo.columns]
df_2025PreguntasMiembro.columns = [quitar_acentos(col) for col in df_2025PreguntasMiembro.columns]

# quitando filas en Minusculas
df_2025Miembros =  QuitarFilaConMinusculas(df_2025Miembros, "Persona")
df_2025Directivos =  QuitarFilaConMinusculas(df_2025Directivos, "Persona")

#creando diccionario para reemplazar los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
diccionario_dimension = {
    "Dimension de la Estrategia y Direccion":"Estrategia y direccion",
    "Dimension Humana": "Humana",
    "Dimension de los Procesos de Gestion del Conocimiento":"Procesos",
    "Dimension de la Tecnologia": "Tecnologia",
    "Dimension de Indicadores":"Indicadores"
}

#reemplazando los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
for llave, valor in diccionario_dimension.items():
    df_2025Directivos = ReemplazarValorDataSet(df_2025Directivos
                                          ,"Dimension"
                                          ,valor
                                          ,llave)
    df_2025Miembros = ReemplazarValorDataSet(df_2025Miembros
                                          ,"Dimension"
                                          ,valor
                                          ,llave)


#agregando los componente que faltan en el dataset de los miembros y directivos 
df_2025Directivos = AgregarComponenteFaltantes(df_2025PreguntasDirectivo, df_2025Directivos,"Dimension","Subdimension")
df_2025Miembros = AgregarComponenteFaltantes(df_2025PreguntasMiembro, df_2025Miembros,"Dimension","Subdimension")


#calculos de los promedios por dimension
# ResultadoDimensionesDirectivo2025=CalcularPromedioDimension(df_2025Directivos
#                                                             ,"2025"
#                                                             ,"Directiva")
# ResultadoDimensionesMiembro2025=CalcularPromedioDimension(df_2025Miembros
#                                                           ,"2025"
#                                                           ,"Miembro")

# #calculo por el promedio de dimension componentes y persona

# promedio_dimension_directivo= CalculosPromediosComponenteDataSet(df_2025Directivos
#                                                                  ,"2025"
#                                                                  ,"Directivo")
# promedio_dimension_Miembro= CalculosPromediosComponenteDataSet(df_2025Miembros
#                                                                ,"2025"
#                                                                ,"Miembro")



with pd.ExcelWriter('Respuestas2.xlsx', engine='openpyxl') as writer:
      df_2025Miembros.to_excel(writer, sheet_name='Miembros', index=False)
      df_2025Directivos.to_excel(writer, sheet_name='Directivos', index=False)
    
print("fin")
