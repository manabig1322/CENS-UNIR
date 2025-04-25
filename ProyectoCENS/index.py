
import pandas as pd
import re
from unidecode import unidecode
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns

#funcion que limpia los dataset de los miembros y directivos y sus preguntas
def  LimpiezaDataSet(df_2025Directivos, df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro):
    
    df_2025Directivos = QuitarEspaciosCeldasAcentosColumnas(df_2025Directivos)
    df_2025Miembros = QuitarEspaciosCeldasAcentosColumnas(df_2025Miembros)
    df_2025PreguntasDirectivo = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasDirectivo)
    df_2025PreguntasMiembro = QuitarEspaciosCeldasAcentosColumnas(df_2025PreguntasMiembro)

    #renombrando las columnas para unificar nombres
    df_2025PreguntasDirectivo = df_2025PreguntasDirectivo.rename(columns={'Componente': 'Subdimension'})
    df_2025PreguntasMiembro = df_2025PreguntasMiembro.rename(columns={'Componente': 'Subdimension'})
  
    #Quitando los espacios en blanco y quitando acentos de los nombres de las columnas
    
    # df_2025Directivos =quitar_acentos_columna(df_2025Miembros,"Dimension")
    # df_2025Miembros =quitar_acentos_columna(df_2025Miembros,"Dimension")
    # df_2025PreguntasDirectivo =quitar_acentos_columna(df_2025PreguntasDirectivo,"Dimension")
    # df_2025PreguntasMiembro =quitar_acentos_columna(df_2025PreguntasMiembro,"Dimension")
 
        
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
    df_2025Directivos.to_csv("Directivos2025.csv", index=False)
    df_2025Miembros =  QuitarFilaConMinusculas(df_2025Miembros, "Persona")
    df_2025Directivos =  QuitarFilaConMinusculas(df_2025Directivos, "Persona")
     #creando diccionario para reemplazar los nombres de las dimensiones por su nombre corto de dimensiones en el dataset
    diccionario_dimension = {
    'Dimension de Indicadores':'Indicadores',
        'Dimensión de los Procesos de Gestión del Conocimiento':'Procesos',
        'Dimensión de la Tecnología':'Tecnologia',
        'Dimensión Humana':'Humana',
        'Dimensión de la Estrategía y Dirección':'Estrategia y direccion'
    }

    #creando diccionario para reemplazar los nombres de las componente por su nombre corto de componente en el dataset
    diccionario_componente = {
        "Definición del Gestión del Conocimiento en la organización":"Definicion de gestion del conocimiento",
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


    return df_2025Directivos, df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro
#funcion que valida si hay coma en la cadena
def contiene_coma(cadena):
    if pd.isna(cadena):
        return False
    return ',' in cadena
#funcion que quita los numeros y puntos que limpia el texto
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
# Función para quitar acentos en columnas específicas
def quitar_acentos_columna(df, nombre_columna):
    df[nombre_columna] = df[nombre_columna].apply(quitar_acentos)
    return df
def quitar_acentos(texto):
   if pd.isna(texto):
        return texto
   texto = unidecode(str(texto)).replace('ñ', 'n').replace('Ñ', 'N')
   return texto.strip()  # Si no es string, lo devuelve igual
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
     # Paso 1: Promedio por Persona y Subdimensión
    persona_sub = DataSet.groupby(['Persona', 'Subdimension'])[columnaValor].mean().reset_index()
    # Unir con la columna Dimensión (desde el original)
    # Primero eliminamos duplicados para no repetir Dimensión-Subdimensión
    dim_sub = DataSet[['Dimension', 'Subdimension']].drop_duplicates()
    # Unimos para recuperar la Dimensión asociada
    persona_sub = pd.merge(persona_sub, dim_sub, on='Subdimension', how='left')
    # Paso 2: Promedio final por Dimensión
    ResultadoDimensiones = persona_sub.groupby('Dimension')[columnaValor].mean().reset_index()
    # 4. Agregando la columna año
    ResultadoDimensiones['año'] = Año
    # 5. Agregando la columna tipo de Excel para saber cual excel uso para la informacion
    ResultadoDimensiones['Excel Origen'] = f"{tipoExcel} {Año}"
    return ResultadoDimensiones
#funcion que calcula el promedio de dimension por componente y persona y despues por componente
def CalculosPromediosComponenteDataSet(DataSet, ColumnaValor, Año, tipoExcel):
    
    # Convertir 'valor' a numérico, ignorando errores (no numéricos se convierten en NaN)
    DataSet[ColumnaValor] = pd.to_numeric(DataSet[ColumnaValor], errors='coerce')
    # Eliminar filas con valores NaN en 'valor'
    DataSet = DataSet.dropna(subset=[ColumnaValor])
   # Paso 1: Calcular el promedio por Persona y Subdimensión
    promedios_por_persona = DataSet.groupby(['Dimension', 'Subdimension', 'Persona'])[ColumnaValor].mean().reset_index()
    # Paso 2: Calcular el promedio final por Subdimensión (promediando los promedios individuales)
    promedios_finales = promedios_por_persona.groupby(['Dimension', 'Subdimension'])[ColumnaValor].mean().reset_index()
    # 5. agrega la columna de año
    promedios_finales["año"]=Año
    # 6. agrega la columan de  tipo de excel para saber cual excel uso para los calculos
    promedios_finales["Excel Origen"]=f"{tipoExcel} {Año}"

    return promedios_finales
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
      
  ListadoPreguntas = df2[df2[ColumnaTipoPregunta] == "Seleccion multiple con texto"][
        [columnaDimension, columnaComponente, ColumnaPregunta, ColumnaValor]
    ]
  df_resultadoFinal = pd.DataFrame()

  if len(ListadoPreguntas) >= 1:
        for _, fila in ListadoPreguntas.iterrows():
            dimension = fila[columnaDimension]
            componente = fila[columnaComponente]
            pregunta = fila[ColumnaPregunta]
            respuestas = fila[ColumnaValor]

            if pd.isna(respuestas):
                continue

            if isinstance(respuestas, int):
                todos_los_numeros = [respuestas]
            elif isinstance(respuestas, str):
                todos_los_numeros = [int(x) for x in respuestas.split(',') if x.isdigit()]
            else:
                continue

            if not todos_los_numeros:
                continue

            valor_maximo = max(todos_los_numeros)
            fila_procesada = procesar_fila(respuestas, valor_maximo)
            columnas = [f'col{i}' for i in range(1, valor_maximo + 1)]

            nueva_fila = {f'col{i}': (i if i in fila_procesada else np.nan) for i in range(1, valor_maximo + 1)}
            df_temp = pd.DataFrame([nueva_fila])

            df_temp['dimension'] = dimension
            df_temp['componente'] = componente
            df_temp['preguntas'] = pregunta

            df_melted = df_temp.melt(id_vars=['dimension', 'componente', 'preguntas'], 
                                        value_vars=columnas,
                                        var_name='columna', value_name='valor')
            df_melted = df_melted.dropna(subset=['valor'])

            df_agrupado = df_melted.groupby(['dimension', 'componente', 'preguntas', 'valor']).size().reset_index(name='conteo')

            df_resultado = df_agrupado.pivot_table(index=['dimension', 'componente', 'preguntas'],
                                                    columns='valor',
                                                    values='conteo',
                                                    fill_value=0).reset_index()

            df_resultado.columns.name = None
            df_resultado.columns = [str(col) if isinstance(col, int) else col for col in df_resultado.columns]

            df_resultadoFinal = pd.concat([df_resultadoFinal, df_resultado], ignore_index=True)

        # NUEVO: Agrupar por dimensión, componente y pregunta sumando conteos
        columnas_a_sumar = [col for col in df_resultadoFinal.columns if col not in ['dimension', 'componente', 'preguntas']]
        df_resultadoFinal = df_resultadoFinal.groupby(['dimension', 'componente', 'preguntas'])[columnas_a_sumar].sum().reset_index()

  print(df_resultadoFinal.to_string())
  return df_resultadoFinal
#funcion que genera la grafica de radar por dimension
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


 # Función para radar chart
#funcion que genera la grafica de radar por componente
def crear_grafica_radar_componente(data, dimension,colores_excel_origen):
    etiquetas = list(data['Subdimension'].unique())
    origenes = data['Excel Origen'].unique()
    num_vars = len(etiquetas)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

    for origen in origenes:
        subset = data[data['Excel Origen'] == origen]
        valores = subset.set_index('Subdimension').reindex(etiquetas)['Valor'].fillna(0).tolist()
        valores += valores[:1]
        ax.plot(angles, valores, linewidth=2, linestyle='solid', label=origen, color=colores_excel_origen.get(origen, '#333333'))
        ax.fill(angles, valores, alpha=0.1, color=colores_excel_origen.get(origen, '#333333'))

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), etiquetas)
    ax.set_title(f"Dimensión: {dimension}", y=1.1)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=len(origenes))
    plt.tight_layout()
    plt.show()
# Función que genera la gráfica de barras por componente
def crear_grafica_barras_componente(data, dimension,colores_excel_origen):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=data,
        x='Subdimension',
        y='Valor',
        hue='Excel Origen',
        palette=colores_excel_origen,
        ax=ax
    )
    ax.set_title(f'Dimensión: {dimension} (Gráfico de Barras)')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)
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

    
    #Llamando funcion que hace toda la limpieza de los dataset
    df_2025Directivos, df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro=LimpiezaDataSet(df_2025Directivos, df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro)
   
    
    #agregando los componente que faltan en el dataset de los miembros y directivos 
    df_2025Directivos = AgregarComponenteFaltantes(df_2025PreguntasDirectivo, df_2025Directivos,"Dimension","Subdimension","Valor")
    df_2025Miembros = AgregarComponenteFaltantes(df_2025PreguntasMiembro, df_2025Miembros,"Dimension","Subdimension","Valor")
   
    df_ListadoPreguntasEstructuradaDirectivo2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Directivos,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")
    df_ListadoPreguntasEstructuradaMienbro2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Miembros,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")

    df_2025DirectivosImpresion = df_2025Directivos.copy()
    df_2025MiembrosImpresion = df_2025Miembros.copy()

    df_2025DirectivosPromeDimension = df_2025Directivos.copy()
    df_2025MiembrosPromeDimension = df_2025Miembros.copy()

    df_2025DirectivosPromeComponente= df_2025Directivos.copy()
    df_2025MiembrosPromeComponente = df_2025Miembros.copy()

    #calculos de los promedios por dimension
    ResultadoDimensionesDirectivo2025=CalcularPromedioDimension(df_2025DirectivosPromeDimension
                                                                ,"Valor"
                                                                ,"2025"
                                                                ,"Directiva")
    ResultadoDimensionesMiembro2025=CalcularPromedioDimension(df_2025MiembrosPromeDimension
                                                            ,"Valor"
                                                            ,"2025"
                                                            ,"Miembro")

    #calculo por el promedio de dimension componentes y persona
    promedio_dimension_directivo= CalculosPromediosComponenteDataSet(df_2025DirectivosPromeComponente
                                                                    ,"Valor"
                                                                    ,"2025"
                                                                    ,"Directivo")
    promedio_dimension_Miembro= CalculosPromediosComponenteDataSet(df_2025MiembrosPromeComponente
                                                                    ,"Valor"
                                                                ,"2025"
                                                                ,"Miembro")

    df_promedio_dimension = pd.concat([ResultadoDimensionesDirectivo2025, ResultadoDimensionesMiembro2025], ignore_index=True)
    GenerarGraficaRadarDimensiones(df_promedio_dimension)

    df_promedio_componente = pd.concat([promedio_dimension_directivo, promedio_dimension_Miembro], ignore_index=True)
    GenerarGraficaComponente(df_promedio_componente)


    with pd.ExcelWriter('Respuestas.xlsx', engine='openpyxl') as writer:
        df_2025MiembrosImpresion.to_excel(writer, sheet_name='Miembros', index=False)
        df_2025DirectivosImpresion.to_excel(writer, sheet_name='Directivos', index=False)
        ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='PromedioDirectivosDimension', index=False)
        ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='PromedioMiembroDimension', index=False)
        promedio_dimension_directivo.to_excel(writer, sheet_name='PromedioDirectivoComponente', index=False)
        promedio_dimension_Miembro.to_excel(writer, sheet_name='PromedioMiembroComponente', index=False)
        df_ListadoPreguntasEstructuradaDirectivo2025.to_excel(writer, sheet_name='ListadoPreguntasEstructuradaDirector2025', index=False)
        df_ListadoPreguntasEstructuradaMienbro2025.to_excel(writer, sheet_name='ListadoPreguntasEstructuradaMienbro2025', index=False)
    
    
    
    print("fin de ejecucion")


# llamando de la funcion principal
if __name__ == "__main__":
    main()
