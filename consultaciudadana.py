import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


@st.cache_data
def encuesta():
    df_consulta=pd.read_excel('datos/Resultados conuslta ciudadana.xlsx', sheet_name='Base de datos')
    df_consulta['count_discapacidad']=np.where(df_consulta['discapacidad']=='Sí',1,0)
    nombres_columnas = df_consulta.columns
    df_consulta.rename(columns={nombres_columnas[0]: 'Portal',nombres_columnas[1]: 'Ultima_Postulacion',nombres_columnas[2]:'Nota_facilidad_postulación',nombres_columnas[3]:'Nota_pertinencia_info_solicitada',nombres_columnas[4]:'Contactada_en_proceso',nombres_columnas[5]:'Nota_calidad_evaluacion_realizada',nombres_columnas[6]:'Nota_oportunidad_entrega_resultados',nombres_columnas[7]:'Nota_proceso_reclutamiento_seleccion',nombres_columnas[8]:'comentario_sugerencia_proceso_postulación',nombres_columnas[9]:'informacion_relevante_sobre_instituciones_publicas'}, inplace=True)
    return df_consulta

df_encuesta = encuesta()

# listas valores filtros
unique_rango_etario = df_encuesta['rango_etario'].unique()
rango_etario = pd.DataFrame({'rango_etario': unique_rango_etario})
nuevo_registro = pd.DataFrame({'rango_etario': ['Todos']})
rango_etario = pd.concat([nuevo_registro, rango_etario])
rango_etario = rango_etario.reset_index(drop=True)
rango_etario = rango_etario['rango_etario'].tolist()

unique_region = df_encuesta['region'].unique()
region = pd.DataFrame({'region': unique_region})
nuevo_registro = pd.DataFrame({'region': ['Todos']})
region = pd.concat([nuevo_registro, region])
region = region.reset_index(drop=True)
region = region['region'].tolist()

unique_portal = df_encuesta['Portal'].unique()
portal = pd.DataFrame({'Portal': unique_portal})
nuevo_registro = pd.DataFrame({'Portal': ['Todos']})
portal = pd.concat([nuevo_registro, portal])
portal = portal.reset_index(drop=True)
portal = portal['Portal'].tolist()

unique_genero = df_encuesta['genero'].unique()
genero = pd.DataFrame({'genero': unique_genero})
nuevo_registro = pd.DataFrame({'genero': ['Todos']})
genero = pd.concat([nuevo_registro, genero])
genero = genero.reset_index(drop=True)
genero = genero['genero'].tolist()

unique_discapacidad = df_encuesta['discapacidad'].unique()
discapacidad = pd.DataFrame({'discapacidad': unique_discapacidad})
nuevo_registro = pd.DataFrame({'discapacidad': ['Todos']})
discapacidad = pd.concat([nuevo_registro, discapacidad])
discapacidad = discapacidad.reset_index(drop=True)
discapacidad = discapacidad['discapacidad'].tolist()


with st.container():
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        option1=st.selectbox('Rango etario',rango_etario)
    with col2:
        option2=st.selectbox('Región',region)
    with col3:
        option3=st.selectbox('Portal', portal)
    with col4:
        option4=st.selectbox('Genero', genero)  
    with col5:
        option5=st.selectbox('Discapacidad', discapacidad)  

if option1 == 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
    tb_portal = df_encuesta.groupby(['Portal', 'genero', 'rango_etario', 'region', 'discapacidad']).agg(Respuestas=('genero', 'count')).reset_index()
else:
    if option1 != 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = df_encuesta['rango_etario'] == option1
    elif option1 != 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['Portal'] == option3)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = df_encuesta['region'] == option2
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = df_encuesta['Portal'] == option3
    elif option1 != 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1)  & (df_encuesta['genero'] == option4)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2)  & (df_encuesta['genero'] == option4)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['genero'] == option4)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['Portal'] == option3) & (df_encuesta['genero'] == option4)

    elif option1 != 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2) & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['Portal'] == option3) & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3) & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3) & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['Portal'] == option3) & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1)  & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2)  & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1) & (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['Portal'] == option3)  & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['region'] == option2) & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['Portal'] == option3) & (df_encuesta['genero'] == option4)  & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['discapacidad'] == option5)
    elif option1 != 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['rango_etario'] == option1)
    elif option1 == 'Todos' and option2 != 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['region'] == option2)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['Portal'] == option3)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 == 'Todos':
        filtro = (df_encuesta['genero'] == option4)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 != 'Todos' and option4 == 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['Portal'] == option3) & (df_encuesta['discapacidad'] == option5)
    elif option1 == 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 != 'Todos' and option5 != 'Todos':
        filtro = (df_encuesta['genero'] == option4) & (df_encuesta['discapacidad'] == option5)


    tb_portal = df_encuesta[filtro].groupby(['Portal', 'genero', 'rango_etario', 'region', 'discapacidad']).agg(Respuestas=('genero', 'count')).reset_index()


with st.container():
    st.dataframe(tb_portal)
