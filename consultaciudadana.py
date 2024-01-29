import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px



df_encuesta = pd.read_excel('datos/Resultados conuslta ciudadana.xlsx', sheet_name='Base de datos')
df_encuesta['count_discapacidad']=np.where(df_encuesta['discapacidad']=='Sí',1,0)

nombres_columnas = df_encuesta.columns
df_encuesta.rename(columns={nombres_columnas[0]: 'Portal',nombres_columnas[1]: 'Ultima_Postulacion',nombres_columnas[2]:'Nota_facilidad_postulación',nombres_columnas[3]:'Nota_pertinencia_info_solicitada',nombres_columnas[4]:'Contactada_en_proceso',nombres_columnas[5]:'Nota_calidad_evaluacion_realizada',nombres_columnas[6]:'Nota_oportunidad_entrega_resultados',nombres_columnas[7]:'Nota_proceso_reclutamiento_seleccion',nombres_columnas[8]:'comentario_sugerencia_proceso_postulación',nombres_columnas[9]:'informacion_relevante_sobre_instituciones_publicas'}, inplace=True)


tb_portal = df_encuesta.groupby(['Portal', 'genero', 'rango_etario', 'region', 'discapacidad']).agg(Respuestas=('genero', 'count')).reset_index()


rango_etario=df_encuesta.rango_etario.unique()
region=df_encuesta.region.unique()
portal=df_encuesta.Portal.unique()


unique_rango_etario = df_encuesta['rango_etario'].unique()
rango_etario = pd.DataFrame({'rango_etario': unique_rango_etario})
nuevo_registro = pd.DataFrame({'rango_etario': ['Todos']})
rango_etario = pd.concat([nuevo_registro, rango_etario])
rango_etario = rango_etario.reset_index(drop=True)
rango_etario = rango_etario['rango_etario'].tolist()


with st.container():
    col1,col2,col3=st.columns(3)
    with col1:
        option1=st.multiselect('Rango etario',rango_etario)
    with col2:
        option2=st.multiselect('Región',region)
    with col3:
        option3=st.multiselect('Portal', portal)

with st.container():
    st.dataframe(tb_portal)
