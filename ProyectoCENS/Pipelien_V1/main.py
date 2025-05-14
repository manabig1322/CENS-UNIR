
import pandas as pd
from limpieza import LimpiezaDatos
from calculos import CalcularPromedioDimension, CalculosPromediosComponenteDataSet
from utils import ReemplazarValorDataSet

# Cargar datos de ejemplo
ruta_archivo = 'tu_archivo.xlsx'  # Cambia esto a tu archivo real
hoja = 'NombreHoja'               # Cambia esto a la hoja correspondiente

try:
    df = pd.read_excel(ruta_archivo, sheet_name=hoja)

    # Limpiar datos
    df = LimpiezaDatos(df, 'Respuesta')

    # Reemplazo ejemplo (ajustar valores)
    df = ReemplazarValorDataSet(df, 'Dimension', 'AntiguoValor', 'NuevoValor')

    # Calcular promedios
    resultado_dim = CalcularPromedioDimension(df, 2025, 'Directiva')
    resultado_comp = CalculosPromediosComponenteDataSet(df, 2025, 'Directiva')

    # Guardar resultados
    with pd.ExcelWriter('resultados.xlsx') as writer:
        resultado_dim.to_excel(writer, sheet_name='Promedios Dimensión', index=False)
        resultado_comp.to_excel(writer, sheet_name='Promedios Componente', index=False)

    print("Procesamiento completo. Resultados guardados en 'resultados.xlsx'.")

except Exception as e:
    print(f"Error al procesar el archivo: {e}")
