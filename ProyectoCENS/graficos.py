import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from math import pi
from utils import dividir_titulo

def graficar_por_categoria(df, colores_por_anio=None):
    if colores_por_anio is None:
        colores_por_anio = {
            "2023": '#00bf74',
            "2025": '#007bd2'
        }

    categorias = df['Categoria'].unique()

    for categoria in categorias:
        df_cat = df[df['Categoria'] == categoria]
        dimensiones = df_cat['Dimension'].unique()

        if len(dimensiones) <= 2:
            # Gráfico de barras
            pivot = df_cat.pivot(index='Dimension', columns='Año', values='Valor').fillna(0)
            pivot.plot(kind='bar', color=[colores_por_anio.get(a, '#999999') for a in pivot.columns])
            plt.title(f'Categoría: {categoria} - Barras por Año')
            plt.ylabel('Valor')
            plt.xticks(rotation=0)
            plt.legend(title='Año')
            plt.tight_layout()
            plt.show()

        else:
            # Gráfico de radar
            df_pivot = df_cat.pivot(index='Dimension', columns='Año', values='Valor').fillna(0)
            labels = df_pivot.index.tolist()
            num_vars = len(labels)
            angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))

            # Escala con margen de 2 unidades
            max_raw = df_pivot.max().max()
            max_val = int(np.floor(max_raw + 2))
           # Escala radial sin el 0, comenzando en 1
            ticks = list(range(1, max_val + 1))
            ax.set_ylim(1, max_val)
            ax.set_yticks(ticks)
            ax.set_yticklabels([str(t) for t in ticks])

            for anio in df_pivot.columns:
                valores = df_pivot[anio].tolist()
                valores += valores[:1]
                ax.plot(angles, valores, label=str(anio), color=colores_por_anio.get(anio, '#333333'))
                ax.fill(angles, valores, alpha=0.1, color=colores_por_anio.get(anio, '#333333'))

                # Mostrar valores en las puntas
                for i, (angle, value) in enumerate(zip(angles[:-1], valores[:-1])):
                    ax.text(
                        angle, value + 0.2, f"{value:.1f}",
                        ha='center', va='bottom', fontsize=9,
                        color=colores_por_anio.get(anio, '#333333')
                    )

            # Etiquetas numéricas en los ejes
            ax.set_theta_offset(np.pi/2)
            ax.set_theta_direction(-1)
            ax.set_thetagrids(np.degrees(angles[:-1]), [str(i+1) for i in range(num_vars)])

            # Título y leyenda
            fig.suptitle(f"Categoría: {categoria} - Radar por Dimensión", fontsize=14, y=0.95)
            ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)

            # Leyenda textual con número y dimensión
            texto_dim = "\n".join([f"{i+1}: {dim}" for i, dim in enumerate(labels)])
            plt.figtext(0.75, 0.5, texto_dim, ha='left', va='center', fontsize=10, fontfamily='monospace')

            fig.subplots_adjust(left=0.05, right=0.7, top=0.9, bottom=0.2)
            plt.show()

def generar_graficas_componentes_total(df):
    
    dimensiones = df['Dimension'].unique()

    # Colores personalizables para subdimensiones
   # colores_subdimensiones = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

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
                #color = colores_subdimensiones[idx % len(colores_subdimensiones)]
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
        plt.savefig(f"graficas/{dimension}_{subdimension}_{pregunta}.png", bbox_inches='tight')
        plt.show()
        plt.close()


def GenerarGraficaPorPreguntaLikert(df,ArchivoOrigen,df_preguntas):
        # Leer el datset de pregunta likert procesasa
    conteo_final =df
    
    # Diccionario de mapeo de nombres (puedes personalizarlo aquí)
    # if(ArchivoOrigen=="Directiva"):
    #     valor_map = {
    #         'valor_1': '1 (Nada efectivas)',
    #         'valor_2': '2 (Poco efectivas)',
    #         'valor_3': '3 (Moderadamente efectivas)',
    #         'valor_4': '4 (Efectivas)',
    #         'valor_5': '5 (Muy efectivas)',
    #         'valor_nan': 'N/A (No Aplica)'
    #     }
    # else:
    #     valor_map = {
    #         'valor_1': '1 (Nunca)',
    #         'valor_2': '2 (1 vez al mes)',
    #         'valor_3': '3 (2-3 veces al mes)',
    #         'valor_4': '4 (1 vez a la semana)',
    #         'valor_5': '5 (Más de una vez a la semana)',
    #         'valor_nan': 'N/A (No Aplica)'
    #     }

    # Crear carpeta de salida
    #os.makedirs("graficas", exist_ok=True)
    
      # Agrupar por pregunta completa
    grupos = conteo_final.groupby(['Dimension', 'Subdimension', 'Pregunta'])
    i=1
    # Función para extraer orden y número
    def obtener_orden(valor_nombre):
        if valor_nombre == 'valor_nan':
            return float('inf'), 'N/A'
        try:
            num = int(valor_nombre.split('_')[1])
            return num, str(num)
        except:
            return float('inf'), 'N/A'
    
   
       # Generar gráfico por grupo
    for (dim, sub, preg), df_grupo in grupos:
        df_plot = df_grupo.copy()
    
        # Buscar opciones para este grupo
        opciones_row = df_preguntas[
                (df_preguntas['Dimension'] == dim) &
                (df_preguntas['Subdimension'] == sub) &
                (df_preguntas['Pregunta'] == preg)
            ]
    
        if not opciones_row.empty:
            opciones_texto = opciones_row.iloc[0]['Opciones']
            lista_opciones = [op.strip() for op in opciones_texto.split(',')]
            valor_map = {f'valor_{i+1}': texto for i, texto in enumerate(lista_opciones)}
        else:
            # Si no hay coincidencia, usar etiquetas por defecto
            valor_map = {}
    
        # Agregar valor_nan
        valor_map['valor_nan'] = 'Sin respuesta'
    
        # Extraer orden y etiquetas
        df_plot[['Orden', 'Etiqueta']] = df_plot['Valor_Nombre'].apply(lambda v: pd.Series(obtener_orden(v)))
        df_plot = df_plot.sort_values('Orden')
    
        etiquetas = df_plot['Etiqueta'].tolist()
        cantidades = df_plot['Cantidad'].tolist()
        nombres_originales = df_plot['Valor_Nombre'].tolist()
        total = sum(cantidades)
    
        # Crear colores degradados en azul (oscuro a claro)
        cmap = cm.get_cmap('Blues')
        colores = cmap(np.linspace(0.9, 0.4, len(cantidades)))
        # Crear gráfico
        plt.figure(figsize=(8, 6))
        bars = plt.bar(etiquetas, cantidades, color=colores, edgecolor='black')
    
        # Mostrar valores encima
        for bar, cantidad in zip(bars, cantidades):
            yval = bar.get_height()
            porcentaje = (cantidad / total) * 100 if total > 0 else 0
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.8, f"{cantidad} ({porcentaje:.0f}%)",
                     ha='center', va='bottom', fontsize=9)
    
        plt.title(f'{dim} - {sub} - {preg}', fontsize=10)
        plt.xlabel('Valor')
        plt.ylabel('Cantidad')
        plt.ylim(0, max(cantidades) * 1.4 if cantidades else 5)
    
        # Crear leyenda visual con colores y textos
        legend_labels = [valor_map.get(orig, orig) for orig in nombres_originales]
        legend_patches = [mpatches.Patch(color=col, label=label)
                          for col, label in zip(colores, legend_labels)]
    
        plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.15),
                   ncol=2, frameon=False, fontsize=8)
    
        plt.tight_layout()
        plt.savefig(f"graficas/{ArchivoOrigen}_{i}.png", bbox_inches='tight')
        i+=1
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
        'Total 2023': '#0000FF',
        'Total 2025': '#228B22'
    }

    # Calcular el valor máximo real y aumentar en 2 unidades
    max_raw = df_pivot.max().max()
    max_val = int(np.floor(max_raw + 2))  # Limite máximo redondeado hacia abajo
    
    # Aplicar límites y ticks enteros
    ax.set_ylim(0, max_val)
    ax.set_yticks(range(0, max_val + 1, 1))
    ax.set_yticklabels(map(str, range(0, max_val + 1, 1)))

    for origen in df_pivot.columns:
        vals = df_pivot[origen].tolist()
        vals += vals[:1]
        ax.plot(angles, vals, label=origen, color=colores.get(origen,'#999999'))
        ax.fill(angles, vals, alpha=0.1, color=colores.get(origen,'#999999'))

        # Añadir etiquetas de valor en cada punta
        for i, (angle, value) in enumerate(zip(angles[:-1], vals[:-1])):
            angle_rad = angle
            ax.text(
                angle_rad, value + 0.2, f"{value:.1f}",
                color=colores.get(origen,'#999999'),
                fontsize=9, ha='center', va='bottom'
            )

    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels_num)

    fig.suptitle(
        "Prom. Total por Dimensión 2023-2025",
        fontsize=14, y=0.97, ha='center'
    )

    fig.subplots_adjust(left=0.05, right=0.7, top=0.9, bottom=0.2)

      # Mostrar número y nombre de cada dimensión, sin el promedio
    lines = [f"{i+1}: {dim}" for i, dim in enumerate(labels_real)]
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
    valores = df_promedio[Valor].tolist()
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
