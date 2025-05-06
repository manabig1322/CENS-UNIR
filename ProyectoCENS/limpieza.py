
import re
import unicodedata

def LimpiezaDatos(df_2023,df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro):
    
    
    df_2023  = QuitarEspaciosCeldasAcentosColumnas(df_2023)
    df_2025Directivos = QuitarEspaciosCeldasAcentosColumnas(df_2025Directivos)
    df_2025Miembros = QuitarEspaciosCeldasAcentosColumnas(df_2025Miembros)
    df_2025PreguntasDirectivo = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasDirectivo)
    df_2025PreguntasMiembro = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasMiembro)

    #renombrando las columnas para unificar nombres
    df_2023 = df_2023.rename(columns={'Respuesta': 'Valor'})
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Opcion de Respuesta': 'Opciones'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Opcion de Respuesta': 'Opciones'})

    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Dimensión': 'Dimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Dimensión': 'Dimension'})

    df_2023 = df_2023.rename(columns={'Area': 'Categoria'})

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
    df_2023 = limpiar_columna_numeros(df_2023,"Dimension")
    df_2025Miembros = limpiar_columna_numeros(df_2025Miembros,"Dimension")
    df_2025Directivos = limpiar_columna_numeros(df_2025Directivos,"Dimension")
    df_2025PreguntasDirectivo = limpiar_columna_numeros(df_2025PreguntasDirectivo,"Dimension")
    df_2025PreguntasMiembro = limpiar_columna_numeros(df_2025PreguntasMiembro,"Dimension")
    
    df_2023 = limpiar_columna_numeros(df_2023,"Subdimension")
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
           df_2023 = ReemplazarValorDataSet(df_2023
                                               ,"Dimension"
                                               ,llave
                                               ,valor)
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
           df_2023 = ReemplazarValorDataSet(df_2023
                                               ,"Subdimension"
                                               ,llave
                                               ,valor)
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
    df_2023  =  QuitarFilaConMinusculas(df_2023, "Persona")
    df_2025Miembros =  QuitarFilaConMinusculas(df_2025Miembros, "Persona")
    df_2025Directivos =  QuitarFilaConMinusculas(df_2025Directivos, "Persona")
    
    return df_2023,df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro

#funcion que quita los numeros y puntos
def limpiar_columna_numeros(df,columna):
    
    if columna not in df.columns:
        return df
    # Limpiar dejando solo dígitos (y opcionalmente punto decimal)
    df[columna] = df[columna].astype(str).apply(limpiar_texto)
    return df
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
#funcion que quitas los campos que tiene minusculas
def QuitarFilaConMinusculas(df, columna):
    # Filtrar el DataFrame para mantener solo las filas donde 'columna1' está en mayúsculas
    return df[df[columna].str.isupper()]
def limpiar_texto(texto):
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'[0-9.]', '',texto)
    return texto.strip()
def quitar_acentos(texto):
    if isinstance(texto, str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
        return texto_sin_acentos
    return texto
