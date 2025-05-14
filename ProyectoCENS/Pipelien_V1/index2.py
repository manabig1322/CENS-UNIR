import pandas as pd
from limpieza import LimpiezaDatos
from calculos import CalcularPromedioDimension, CalculosPromediosComponenteDataSet,calcularPromedioTotalComponente,calcularPromedioTotalCategoria,calcularPromedioTotalDimension
from utils import AgregarComponenteFaltantes, AgregarConteoPreguntasSeleccionMultiple, AgregarConteoPreguntasLikert, AgregarCategoria2025
from graficos import generar_graficas_componentes_total,generar_grafica_radar_total, GenerarGraficaComponente, GenerarGraficaPorPreguntaLikert,graficar_por_categoria,GenerarGraficaPorPregunta,GenerarGraficaRadarDimensiones


def main():
    

    #cargando los dataset de los miembros y directivos de la encuesta 2025 y las preguntas de la encuesta
    df_2023 = pd.read_excel('datos_2023.xlsx',sheet_name="Data privot")
    df_2025Miembros = pd.read_excel('datos_2025_2.xlsx',sheet_name="Miembros")
    df_2025Directivos = pd.read_excel('datos_2025_2.xlsx',sheet_name="Directivos")
    #df_2025Directivos = pd.read_excel('Encuesta GC 9 de Mayo 2025.xlsx',sheet_name="Hoja1")
    df_2025PreguntasDirectivo =  pd.read_excel('encuesta_diagnóstico_alternativa_directivos_170325.xlsx',sheet_name="Hoja1",header=0)
    df_2025PreguntasMiembro = pd.read_excel('encuesta_diagnóstico_alternativa_miembros_170325.xlsx',sheet_name="Hoja1",header=1)
    df_2025Categoria = pd.read_excel('datos_2025_categoria.xlsx',sheet_name="Resumen",header=0)

    df_2023,df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro = LimpiezaDatos(df_2023,df_2025Directivos,df_2025Miembros,df_2025PreguntasDirectivo,df_2025PreguntasMiembro)
    
    df_2025Directivos = AgregarCategoria2025(df_2025Directivos,df_2025Categoria)
    df_2025Miembros = AgregarCategoria2025(df_2025Miembros,df_2025Categoria)
    #agregando los componente que faltan en el dataset de los miembros y directivos 
    df_2025Directivos = AgregarComponenteFaltantes(df_2025PreguntasDirectivo, df_2025Directivos,"Dimension","Subdimension","Valor")
    df_2025Miembros = AgregarComponenteFaltantes(df_2025PreguntasMiembro, df_2025Miembros,"Dimension","Subdimension","Valor")
   
    
   
    df_ListadoPreguntasEstructuradaDirectiva2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Directivos,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")
    df_ListadoPreguntasEstructuradaMiembro2025 =  AgregarConteoPreguntasSeleccionMultiple(df_2025Miembros,"Dimension","Subdimension","Pregunta","TipoPregunta","Valor")
    
    df_ListadoPreguntasLikertDirectiva2025 = AgregarConteoPreguntasLikert(df_2025Directivos)
    df_ListadoPreguntasLikertMiembro2025 = AgregarConteoPreguntasLikert(df_2025Miembros)
    df_2025PreguntasDirectivo.to_csv("df_2025PreguntasDirectivo.csv")
    df_ListadoPreguntasLikertDirectiva2025.to_csv("df_ListadoPreguntasLikertDirectiva2025.csv")
    GenerarGraficaPorPreguntaLikert(df_ListadoPreguntasLikertDirectiva2025,"Directiva",df_2025PreguntasDirectivo)
    GenerarGraficaPorPreguntaLikert(df_ListadoPreguntasLikertMiembro2025,"Miembros",df_2025PreguntasMiembro)
    
    GenerarGraficaPorPregunta(df_ListadoPreguntasEstructuradaDirectiva2025,"Directiva")
    GenerarGraficaPorPregunta(df_ListadoPreguntasEstructuradaMiembro2025,"Miembros")

    df_2025DirectivosImpresion = df_2025Directivos.copy()
    df_2025MiembrosImpresion = df_2025Miembros.copy()

    #calculos de los promedios por dimension
    
  
    
    df_total2025 = pd.concat([df_2025Directivos, df_2025Miembros], ignore_index=True)
    df_promedioCategoria2023 =calcularPromedioTotalCategoria(df_2023,"Categoria","Dimension","Valor","2023","Excel 2023")
    df_promedioCategoria2025 =calcularPromedioTotalCategoria(df_total2025,"Categoria","Dimension","Valor","2025","Excel 2025")
    
    df_promedioTotalCategoria = pd.concat([df_promedioCategoria2023, df_promedioCategoria2025], ignore_index=True)
    df_promedioTotalCategoria.to_csv('DataPromedioTotalCategoria.csv', index=False, encoding='utf-8')
    graficar_por_categoria(df_promedioTotalCategoria)
    
    df_promedio_dimension_total_2023 = CalcularPromedioDimension(df_2023
                                                                ,"Valor"
                                                                ,"2023"
                                                                ,"Total")
    df_promedio_dimension_total_2025 = CalcularPromedioDimension(df_total2025
                                                                ,"Valor"
                                                                ,"2025"
                                                                ,"Total")
  
    
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
    df_promedio_total = pd.concat([df_promedio_dimension_total_2023, df_promedio_dimension_total_2025], ignore_index=True)
    generar_grafica_radar_total(df_promedio_total,'Dimension','Valor')
    GenerarGraficaRadarDimensiones(df_promedio_total)


    df_promedio_componente = pd.concat([promedio_dimension_directivo, promedio_dimension_Miembro], ignore_index=True)
    df_promedio_total_componente = calcularPromedioTotalComponente(df_promedio_componente,'Dimension','Subdimension','Valor')
    generar_graficas_componentes_total(df_promedio_total_componente)
    GenerarGraficaComponente(df_promedio_componente)

    with pd.ExcelWriter('Respuestas.xlsx', engine='openpyxl') as writer:
        df_2025MiembrosImpresion.to_excel(writer, sheet_name='Miembros', index=False)
        df_2025DirectivosImpresion.to_excel(writer, sheet_name='Directivos', index=False)
      #  ResultadoDimensionesDirectivo2025.to_excel(writer, sheet_name='PromedioDirectivosDimension', index=False)
      #  ResultadoDimensionesMiembro2025.to_excel(writer, sheet_name='PromedioMiembroDimension', index=False)
      #  promedio_dimension_directivo.to_excel(writer, sheet_name='PromedioDirectivoComponente', index=False)
      #  promedio_dimension_Miembro.to_excel(writer, sheet_name='PromedioMiembroComponente', index=False)
      #  df_ListadoPreguntasEstructuradaDirectiva2025.to_excel(writer, sheet_name='ListadoPreguntasEstructuradaDirector2025', index=False)
    
    
    
    print("fin de ejecucion")


# llamando de la funcion principal
if __name__ == "__main__":
    main()