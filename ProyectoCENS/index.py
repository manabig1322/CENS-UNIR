import pandas as pd
import re
import unicodedata
import numpy as np
import matplotlib.pyplot as plt

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
# Función para quitar acentos
def quitar_acentos_columna(df, columna):
    if columna not in df.columns:
        return df
    
    # Función auxiliar para quitar acentos
    def quitar_acentos(texto):
        if isinstance(texto, str):
            return ''.join(
                c for c in unicodedata.normalize('NFKD', texto)
                if not unicodedata.combining(c)
            )
        return texto  # Si no es string, lo devuelve igual

    # Aplicar a la columna
    df[columna] = df[columna].apply(quitar_acentos)
    return df
def quitar_acentos(texto):
    if isinstance(texto, str):
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)
        return texto_sin_acentos
    return texto
# Función para procesar con máximo como parámetro
def procesar_fila(entrada, maximo):
    if pd.isna(entrada):
        return []
    if isinstance(entrada, int):
        return [entrada] if 1 <= entrada <= maximo else []
    if isinstance(entrada, str):
        return sorted([int(x) for x in entrada.split(',') if x.isdigit() and 1 <= int(x) <= maximo])
    return []
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
def AgregarConteoPreguntasSeleccionMultiple(df2,columnaDimension, columnaComponente,ColumnaPregunta,ColumnaTipoPregunta, ColumnaValor):
      
    # Obtener listado único de Dimension
   
    ListadoPreguntas = df2[(df2[ColumnaTipoPregunta] == "Seleccion multiple con texto")
                                ][[columnaDimension
                                   ,columnaComponente
                                   ,ColumnaPregunta
                                   ,ColumnaValor]]

   
           
           # Separar por líneas
    ListaRespuesta = ListadoPreguntas[ColumnaValor].dropna().tolist()
  # Extraer todos los números válidos para encontrar el máximo
    todos_los_numeros = []

    for item in ListaRespuesta:
        if isinstance(item, int):
            todos_los_numeros.append(item)
        elif isinstance(item, str):
            numeros = [int(x) for x in item.split(',') if x.isdigit()]
            todos_los_numeros.extend(numeros)

    # Detectar el número más alto
    valor_maximo = max(todos_los_numeros)

    # Procesar las filas con el valor máximo detectado
    filas_procesadas = [procesar_fila(x, valor_maximo) for x in ListaRespuesta]

    # Crear columnas dinámicas del 1 al valor máximo encontrado
    columnas = [f'col{i}' for i in range(1, valor_maximo + 1)]

    # Construir el DataFrame
    df_final = pd.DataFrame(columns=columnas)

    for fila in filas_procesadas:
        nueva_fila = {f'col{i}': (i if i in fila else np.nan) for i in range(1, valor_maximo + 1)}
        df_final = pd.concat([df_final, pd.DataFrame([nueva_fila])], ignore_index=True)

    # Agregar las columnas adicionales
    df_final['dimension'] = "dimension"
    df_final['componente'] = "componente"
    df_final['preguntas'] = "preguntas"

    # Contar cuántas veces aparece cada número en las columnas col1 a colN
    # Derretir el DataFrame para facilitar el conteo
    df_melted = df_final.melt(id_vars=['dimension', 'componente', 'preguntas'], 
                          value_vars=columnas,
                          var_name='columna', value_name='valor')

    # Eliminar los NaN
    df_melted = df_melted.dropna(subset=['valor'])

    # Contar ocurrencias agrupadas
    df_agrupado = df_melted.groupby(['dimension', 'componente', 'preguntas', 'valor']).size().reset_index(name='conteo')

    # Opcional: Pivot para que los valores aparezcan como columnas (1, 2, 3...)
    df_resultado = df_agrupado.pivot_table(index=['dimension', 'componente', 'preguntas'],
                                       columns='valor',
                                       values='conteo',
                                       fill_value=0).reset_index()

    # Renombrar las columnas de números
    df_resultado.columns.name = None  # Quita el nombre del índice de columnas
    df_resultado.columns = [str(col) if isinstance(col, int) else col for col in df_resultado.columns]

    return df_resultado

def GenerarGraficaRadarDimensiones(df_promedio_dimension):
     print(df_promedio_dimension.columns)

    # Asegúrate de tener estas columnas (ajusta si el nombre varía)
     col_dim = 'Dimension'
     col_origen = 'Excel Origen'
     col_valor = 'Valor'

     # Pivot para que las dimensiones sean ejes
     df_pivot = df_promedio_dimension.pivot(index=col_dim, columns=col_origen, values=col_valor).fillna(0)

     # Ordenar dimensiones para cerrar el radar
     labels = df_pivot.index.tolist()
     num_vars = len(labels)

     # Añadir el primer valor al final para cerrar el círculo
     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
     angles += angles[:1]

    # Inicializar la figura
     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Colores personalizados
     colores = {
        'Miembro 2025': '#0000FF',
        'Directiva 2025': '#228B22'
     }

     # Dibujar cada línea
     for origen in df_pivot.columns:
        valores = df_pivot[origen].tolist()
        valores += valores[:1]  # Cierre del círculo
        ax.plot(angles, valores, label=origen, color=colores.get(origen, '#999999'))
        ax.fill(angles, valores, alpha=0.1, color=colores.get(origen, '#999999'))

    # Ajustar los ejes
     ax.set_theta_offset(np.pi / 2)
     ax.set_theta_direction(-1)
     ax.set_thetagrids(np.degrees(angles[:-1]), labels)

     # Título y leyenda
     plt.title("Promedio por Dimensión con Directiva y Miembros ", size=14, pad=20)
     plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2)

     plt.tight_layout()
     plt.show()


           

#funcion Principal que inicia el programa
def main():
    

    #cargando los dataset de los miembros y directivos de la encuesta 2025 y las preguntas de la encuesta
    df_2025Miembros = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Miembros")
    df_2025Directivos = pd.read_excel('Respuestas KM 20042025 1918hr.xlsx',sheet_name="Directivos")
    df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_general_090425.xlsx',sheet_name="Hoja1",header=0)
    df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_general_090425.xlsx',sheet_name="Hoja1",header=1)


    
    df_2025Directivos = QuitarEspaciosCeldasAcentosColumnas(df_2025Directivos)
    df_2025Miembros = QuitarEspaciosCeldasAcentosColumnas(df_2025Miembros)
    df_2025PreguntasDirectivo = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasDirectivo)
    df_2025PreguntasMiembro = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasMiembro)

    #renombrando las columnas para unificar nombres
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Componente': 'Subdimension'})


    #Quitando los espacios en blanco y quitando acentos de los nombres de las columnas
    df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"Dimension")
    df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"Dimension")
    df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"Dimension")
    df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"Dimension")
    
    df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"Subdimension")
    df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"Subdimension")
    df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"Subdimension")
    df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"Subdimension")

    df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"TipoPregunta")
    df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"TipoPregunta")
    df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"TipoPregunta")
    df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"TipoPregunta")

    
    #quitando los numeros y puntos
    df_2025Miembros = limpiar_columna_numeros(df_2025Miembros,"Dimension")
    df_2025Directivos = limpiar_columna_numeros(df_2025Directivos,"Dimension")
    df_2025PreguntasDirectivo = limpiar_columna_numeros(df_2025PreguntasDirectivo,"Dimension")
    df_2025PreguntasMiembro = limpiar_columna_numeros(df_2025PreguntasMiembro,"Dimension")
    
    df_2025Miembros = limpiar_columna_numeros(df_2025Miembros,"Subdimension")
    df_2025Directivos = limpiar_columna_numeros(df_2025Directivos,"Subdimension")
    df_2025PreguntasDirectivo = limpiar_columna_numeros(df_2025PreguntasDirectivo,"Subdimension")
    df_2025PreguntasMiembro = limpiar_columna_numeros(df_2025PreguntasMiembro,"Subdimension")
    

   


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

    df_ListadoPreguntasEstructuradaDirector2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Directivos,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")

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

    df_promedio_dimension = pd.concat([ResultadoDimensionesDirectivo2025, ResultadoDimensionesMiembro2025], ignore_index=True)
    GenerarGraficaRadarDimensiones(df_promedio_dimension)

    with pd.ExcelWriter('Respuestas.xlsx', engine='openpyxl') as writer:
        df_2025MiembrosImpresion.to_excel(writer, sheet_name='Miembros', index=False)
        df_2025DirectivosImpresion.to_excel(writer, sheet_name='Directivos', index=False)
        ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='PromedioDirectivosDimension', index=False)
        ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='PromedioMiembroDimension', index=False)
        promedio_dimension_directivo.to_excel(writer, sheet_name='PromedioDirectivoComponente', index=False)
        promedio_dimension_Miembro.to_excel(writer, sheet_name='PromedioMiembroComponente', index=False)
        df_ListadoPreguntasEstructuradaDirector2025.to_excel(writer, sheet_name='ListadoPreguntasEstructuradaDirector2025', index=False)
    
    
    
    print("fin de ejecucion")


# llamando de la funcion principal
if __name__ == "__main__":
    main()
