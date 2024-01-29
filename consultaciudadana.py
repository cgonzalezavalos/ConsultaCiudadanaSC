import pandas as pd
import numpy as np
import streamlit as st


df_encuesta = pd.read_excel('datos/Resultados conuslta ciudadana.xlsx', sheet_name='Base de datos')
df_encuesta['count_discapacidad']=np.where(df_encuesta['discapacidad']=='Sí',1,0)

nombres_columnas = df_encuesta.columns
df_encuesta.rename(columns={nombres_columnas[0]: 'Portal',nombres_columnas[1]: 'Ultima_Postulacion',nombres_columnas[2]:'Nota_facilidad_postulación',nombres_columnas[3]:'Nota_pertinencia_info_solicitada',nombres_columnas[4]:'Contactada_en_proceso',nombres_columnas[5]:'Nota_calidad_evaluacion_realizada',nombres_columnas[6]:'Nota_oportunidad_entrega_resultados',nombres_columnas[7]:'Nota_proceso_reclutamiento_seleccion',nombres_columnas[8]:'comentario_sugerencia_proceso_postulación',nombres_columnas[9]:'informacion_relevante_sobre_instituciones_publicas'}, inplace=True)


with st.container():
    st.dataframe(df_encuesta.head(5))
