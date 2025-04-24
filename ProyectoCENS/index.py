import pandas as pd
import re
import unicodedata


#funcion que limpia los textos de cualquier caracter especial que puede provoca errores
def limpiar_texto(texto):
    if isinstance(texto, str):
        # Eliminar saltos de línea y caracteres especiales al inicio y al final
        texto = re.sub(r'^[^\w\s]+|[^\w\s]+$|^[ \n\r\t]+|[ \n\r\t]+$', '', texto)
        return texto
    return texto  # Retorna el valor original si no es una cadena
#funcion que quita los numeros y puntos
def limpiar_numero_punto(texto):
    
    if isinstance(texto, str):
        # Eliminar saltos de línea y caracteres especiales al inicio y al final
        texto = re.sub(r'[0-9.]', '', texto)
        return texto
    return texto  # Retorna el valor original si no es una cadena
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
# Función para quitar acentos
def quitar_acentos(texto):
    if isinstance(texto, str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
        return texto_sin_acentos
    return texto
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
#funcion Principal que inicia el programa
def main():
    

    #cargando los dataset de los miembros y directivos de la encuesta 2025 y las preguntas de la encuesta
    df_2025Miembros = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Miembros")
    df_2025Directivos = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Directivos")
    df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_general_090425.xlsx',sheet_name="Hoja1",header=0)
    df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_general_090425.xlsx',sheet_name="Hoja1",header=1)

    #renombrando las columnas para unificar nombres
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Componente': 'Subdimension'})

    #quitando cualquier caracter especial que pueda provocar errors en el dataset
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

    #Quitando los espacios en blanco y quitando acentos de los nombres de las columnas
    df_2025Directivos = QuitarEspaciosCeldasAcentosColumnas(df_2025Directivos)
    df_2025Miembros = QuitarEspaciosCeldasAcentosColumnas(df_2025Miembros)
    df_2025PreguntasDirectivo = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasDirectivo)
    df_2025PreguntasMiembro = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasMiembro)


    # quitando filas en Minusculas
    df_2025Miembros =  QuitarFilaConMinusculas(df_2025Miembros, "Persona")
    df_2025Directivos =  QuitarFilaConMinusculas(df_2025Directivos, "Persona")


    #creando diccionario para reemplazar los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
    diccionario_dimension = {
    'Dimension de Indicadores':'Indicadores',
        'Dimension de los Procesos de Gestion del Conocimiento':'Procesos',
        'Dimension de la Tecnologia':'Tecnologia',
        'Dimension Humana':'Humana',
        'Dimension de la Estrategia y Direccion':'Estrategia y direccion'
    }

    #creando diccionario para reemplazar los nombres de las componente por su nombre corto de componente en el dataset
    diccionario_componente = {
        "Definicion del Gestion del Conocimiento en la organizacion":"Definicion de gestion del conocimiento",
        "Motivacion e incentivos":"Motivacion",
        "Matriz de conocimiento estrategico": "Matriz de conocimiento",
        "Procesos de gestion del conocimiento" :"Procesos",

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



    #agregando los componente que faltan en el dataset de los miembros y directivos 
    df_2025Directivos = AgregarComponenteFaltantes(df_2025PreguntasDirectivo, df_2025Directivos,"Dimension","Subdimension","Valor")
    df_2025Miembros = AgregarComponenteFaltantes(df_2025PreguntasMiembro, df_2025Miembros,"Dimension","Subdimension","Valor")


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



    with pd.ExcelWriter('Respuestas.xlsx', engine='openpyxl') as writer:
        df_2025Miembros.to_excel(writer, sheet_name='Miembros', index=False)
        df_2025Directivos.to_excel(writer, sheet_name='Directivos', index=False)
        ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='PromedioDirectivosDimension', index=False)
        ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='PromedioMiembroDimension', index=False)
        promedio_dimension_directivo.to_excel(writer, sheet_name='PromedioDirectivoComponente', index=False)
        promedio_dimension_Miembro.to_excel(writer, sheet_name='PromedioMiembroComponente', index=False)
    print("fin de ejecucion")


# llamando de la funcion principal
if __name__ == "__main__":
    main()
