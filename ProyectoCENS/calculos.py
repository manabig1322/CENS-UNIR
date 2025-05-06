
import pandas as pd

def calcularPromedioTotalCategoria(df,columna1,columna2,columna3,valor):
    # 1. Convertir 'valor' a numérico, forzando ignorar los valores no numericas
    df[valor] = pd.to_numeric(df[valor], errors='coerce')
    # Agrupar por 'dimension' y calcular el promedio de 'valor' para cada grupo
    df_promedio = df.groupby([columna1,columna2,columna3])[valor].mean().reset_index()

    # Devolver el nuevo dataset con 'dimension' y 'valor'
    return df_promedio

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
