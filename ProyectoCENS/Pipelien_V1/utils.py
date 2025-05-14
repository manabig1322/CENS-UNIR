import pandas as pd
import numpy as np
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
    df_filtrado = df[df['TipoPregunta'].isin(['Likert', 'Texto'])]
    
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

def AgregarCategoria2025(dsPreguntas, dsCategoria):
        # Merge usando la columna 'Categoría 2025' en lugar de 'Cargo'
    df_merged = dsPreguntas.merge(
        dsCategoria[['E-mail Corporativo', 'Categoria 2025']], 
        left_on='Email', 
        right_on='E-mail Corporativo',
        how='left'  # Mantenemos todas las respuestas
    )
    
      # Eliminar columna duplicada de email
    df_merged.drop(columns=['E-mail Corporativo'], inplace=True)
    
    # Si ya existía una columna 'Categoría 2025' en df_respuestas, eliminarla antes de reordenar
    # (excepto la nueva que viene del merge)
    duplicated_cols = df_merged.columns[df_merged.columns.duplicated()].tolist()
    if 'Categoría 2025' in duplicated_cols:
        # Mantener solo la última aparición (del merge)
        #first_index = df_merged.columns.get_loc('Categoria 2025')
        cols_to_keep = []
        seen = False
        for col in df_merged.columns:
            if col == 'Categoria 2025':
                if not seen:
                    seen = True
                    cols_to_keep.append(col)
            else:
                cols_to_keep.append(col)
        df_merged = df_merged[cols_to_keep]
    
    # Reordenar columnas para poner 'Categoría 2025' justo después de 'Email'
    cols = list(df_merged.columns)
    email_index = cols.index('Email')
    # Mover 'Categoría 2025'
    if 'Categoria 2025' in cols:
        cols.remove('Categoria 2025')
        cols.insert(email_index + 1, 'Categoria 2025')
    df_merged = df_merged[cols]
    df_merged = df_merged.rename(columns={'Categoria 2025': 'Categoria'})
    return df_merged
