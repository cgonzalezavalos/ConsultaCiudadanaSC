import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


st.set_page_config(layout='wide')

# Set Page Header
st.header("Resultados Encuesta Ciuadadana Servicio Civil")
# Set custom CSS for hr element
st.markdown(
    """
        <style>
            hr {
                margin-top: 0.0rem;
                margin-bottom: 0.5rem;
                height: 3px;
                background-color: #333;
                border: none;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

# Add horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# --------- genera archivo csv -----------------------------
def generate_file_content(df):
    # Generate the file content (e.g., CSV, JSON, etc.)
    # In this example, we'll generate a CSV file
    csv_content = df.to_csv(index=False)
    return csv_content
#------------------------------------------------------------------------


#------------ carga de datos ------------------------------------
@st.cache_data
def encuesta():
    df_consulta=pd.read_excel('datos/Resultados conuslta ciudadana.xlsx', sheet_name='Base de datos')
    df_consulta['count_discapacidad']=np.where(df_consulta['discapacidad']=='Sí',1,0)
    nombres_columnas = df_consulta.columns
    df_consulta.rename(columns={nombres_columnas[0]: 'Portal',nombres_columnas[1]: 'Ultima_Postulacion',nombres_columnas[2]:'Nota_facilidad_postulación',
                                nombres_columnas[3]:'Nota_pertinencia_info_solicitada',nombres_columnas[4]:'Contactada_en_proceso',
                                    nombres_columnas[5]:'Nota_calidad_evaluacion_realizada',nombres_columnas[6]:'Nota_oportunidad_entrega_resultados',
                                        nombres_columnas[7]:'Nota_proceso_reclutamiento_seleccion',nombres_columnas[8]:'comentario_sugerencia_proceso_postulación',
                                            nombres_columnas[9]:'informacion_relevante_sobre_instituciones_publicas'}, inplace=True)
    df_consulta.fillna('No aplica', inplace=True)
    df_consulta['contador']=1
    return df_consulta

df_encuesta = encuesta()
#df_encuesta=df_encuesta[~df_encuesta['Portal'].isin(['Nunca he postulado','No aplica'])]
df_encuesta=df_encuesta[~df_encuesta['Portal'].isin(['No aplica'])]
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# listas valores filtros
#------------------------------------------------------------------------
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
#------------------------------------------------------------------------
#------------------------------------------------------------------------
# Filtros
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
#------------------------------------------------------------------------
# aplicacion de filtros
#------------------------------------------------------------------------
if option1 == 'Todos' and option2 == 'Todos' and option3 == 'Todos' and option4 == 'Todos' and option5 == 'Todos':
    tb_portal = df_encuesta.groupby(['Portal', 'genero', 'rango_etario', 'region', 'discapacidad']).agg(Respuestas=('genero', 'count')).reset_index()
    resultado_encuesta=df_encuesta
    tb_g0=resultado_encuesta.groupby(['genero']).agg(Total=('contador', 'sum')).reset_index()
    tb_g1=resultado_encuesta.groupby(['Ultima_Postulacion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g1=pd.merge(tb_g1,tb_g0,how='left',on='genero')
    tb_g2=resultado_encuesta.groupby(['Nota_facilidad_postulación','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g2=pd.merge(tb_g2,tb_g0,how='left',on='genero')
    tb_g3=resultado_encuesta.groupby(['Nota_pertinencia_info_solicitada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g3=pd.merge(tb_g3,tb_g0,how='left',on='genero')
    tb_g4=resultado_encuesta.groupby(['Contactada_en_proceso','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g4=pd.merge(tb_g4,tb_g0,how='left',on='genero')
    tb_g5=resultado_encuesta.groupby(['Nota_calidad_evaluacion_realizada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g5=pd.merge(tb_g5,tb_g0,how='left',on='genero')
    tb_g6=resultado_encuesta.groupby(['Nota_oportunidad_entrega_resultados','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g6=pd.merge(tb_g6,tb_g0,how='left',on='genero')
    tb_g7=resultado_encuesta.groupby(['Nota_proceso_reclutamiento_seleccion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g7=pd.merge(tb_g7,tb_g0,how='left',on='genero')

    tb_p0=resultado_encuesta.groupby(['Portal']).agg(Total=('contador', 'sum')).reset_index()
    tb_p1=resultado_encuesta.groupby(['Ultima_Postulacion','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p1=pd.merge(tb_p1,tb_p0,how='left',on='Portal')
    tb_p2=resultado_encuesta.groupby(['Nota_facilidad_postulación','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p2=pd.merge(tb_p2,tb_p0,how='left',on='Portal')
    tb_p3=resultado_encuesta.groupby(['Nota_pertinencia_info_solicitada','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p3=pd.merge(tb_p3,tb_p0,how='left',on='Portal')
    tb_p4=resultado_encuesta.groupby(['Contactada_en_proceso','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p4=pd.merge(tb_p4,tb_p0,how='left',on='Portal')
    tb_p5=resultado_encuesta.groupby(['Nota_calidad_evaluacion_realizada','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p5=pd.merge(tb_p5,tb_p0,how='left',on='Portal')
    tb_p6=resultado_encuesta.groupby(['Nota_oportunidad_entrega_resultados','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p6=pd.merge(tb_p6,tb_p0,how='left',on='Portal')
    tb_p7=resultado_encuesta.groupby(['Nota_proceso_reclutamiento_seleccion','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p7=pd.merge(tb_p7,tb_p0,how='left',on='Portal')

    tb_reg0=resultado_encuesta.groupby(['region']).agg(Total=('contador', 'sum')).reset_index()
    tb_reg1=resultado_encuesta.groupby(['Ultima_Postulacion','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg1=pd.merge(tb_reg1,tb_reg0,how='left',on='region')
    tb_reg2=resultado_encuesta.groupby(['Nota_facilidad_postulación','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg2=pd.merge(tb_reg2,tb_reg0,how='left',on='region')
    tb_reg3=resultado_encuesta.groupby(['Nota_pertinencia_info_solicitada','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg3=pd.merge(tb_reg3,tb_reg0,how='left',on='region')
    tb_reg4=resultado_encuesta.groupby(['Contactada_en_proceso','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg4=pd.merge(tb_reg4,tb_reg0,how='left',on='region')
    tb_reg5=resultado_encuesta.groupby(['Nota_calidad_evaluacion_realizada','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg5=pd.merge(tb_reg5,tb_reg0,how='left',on='region')
    tb_reg6=resultado_encuesta.groupby(['Nota_oportunidad_entrega_resultados','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg6=pd.merge(tb_reg6,tb_reg0,how='left',on='region')
    tb_reg7=resultado_encuesta.groupby(['Nota_proceso_reclutamiento_seleccion','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg7=pd.merge(tb_reg7,tb_reg0,how='left',on='region')

    tb_ret0=resultado_encuesta.groupby(['rango_etario']).agg(Total=('contador', 'sum')).reset_index()
    tb_ret1=resultado_encuesta.groupby(['Ultima_Postulacion','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret1=pd.merge(tb_ret1,tb_ret0,how='left',on='rango_etario')
    tb_ret2=resultado_encuesta.groupby(['Nota_facilidad_postulación','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret2=pd.merge(tb_ret2,tb_ret0,how='left',on='rango_etario')
    tb_ret3=resultado_encuesta.groupby(['Nota_pertinencia_info_solicitada','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret3=pd.merge(tb_ret3,tb_ret0,how='left',on='rango_etario')
    tb_ret4=resultado_encuesta.groupby(['Contactada_en_proceso','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret4=pd.merge(tb_ret4,tb_ret0,how='left',on='rango_etario')
    tb_ret5=resultado_encuesta.groupby(['Nota_calidad_evaluacion_realizada','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret5=pd.merge(tb_ret5,tb_ret0,how='left',on='rango_etario')
    tb_ret6=resultado_encuesta.groupby(['Nota_oportunidad_entrega_resultados','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret6=pd.merge(tb_ret6,tb_ret0,how='left',on='rango_etario')
    tb_ret7=resultado_encuesta.groupby(['Nota_proceso_reclutamiento_seleccion','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret7=pd.merge(tb_ret7,tb_ret0,how='left',on='rango_etario')



    
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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
    resultado_encuesta=df_encuesta[filtro]
    tb_g0=resultado_encuesta[filtro].groupby(['genero']).agg(Total=('contador', 'sum')).reset_index()
    tb_g1=resultado_encuesta[filtro].groupby(['Ultima_Postulacion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g1=pd.merge(tb_g1,tb_g0,how='left',on='genero')
    tb_g2=resultado_encuesta[filtro].groupby(['Nota_facilidad_postulación','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g2=pd.merge(tb_g2,tb_g0,how='left',on='genero')
    tb_g3=resultado_encuesta[filtro].groupby(['Nota_pertinencia_info_solicitada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g3=pd.merge(tb_g3,tb_g0,how='left',on='genero')
    tb_g4=resultado_encuesta[filtro].groupby(['Contactada_en_proceso','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g4=pd.merge(tb_g4,tb_g0,how='left',on='genero')
    tb_g5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g5=pd.merge(tb_g5,tb_g0,how='left',on='genero')
    tb_g6=resultado_encuesta[filtro].groupby(['Nota_oportunidad_entrega_resultados','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g6=pd.merge(tb_g6,tb_g0,how='left',on='genero')
    tb_g7=resultado_encuesta[filtro].groupby(['Nota_proceso_reclutamiento_seleccion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g7=pd.merge(tb_g7,tb_g0,how='left',on='genero')

    tb_p0=resultado_encuesta[filtro].groupby(['Portal']).agg(Total=('contador', 'sum')).reset_index()
    tb_p1=resultado_encuesta[filtro].groupby(['Ultima_Postulacion','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p1=pd.merge(tb_p1,tb_p0,how='left',on='Portal')
    tb_p2=resultado_encuesta[filtro].groupby(['Nota_facilidad_postulación','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p2=pd.merge(tb_p2,tb_p0,how='left',on='Portal')
    tb_p3=resultado_encuesta[filtro].groupby(['Nota_pertinencia_info_solicitada','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p3=pd.merge(tb_p3,tb_p0,how='left',on='Portal')
    tb_p4=resultado_encuesta[filtro].groupby(['Contactada_en_proceso','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p4=pd.merge(tb_p4,tb_p0,how='left',on='Portal')
    tb_p5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p5=pd.merge(tb_p5,tb_p0,how='left',on='Portal')
    tb_p6=resultado_encuesta[filtro].groupby(['Nota_oportunidad_entrega_resultados','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p6=pd.merge(tb_p6,tb_p0,how='left',on='Portal')
    tb_p7=resultado_encuesta[filtro].groupby(['Nota_proceso_reclutamiento_seleccion','Portal']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_p7=pd.merge(tb_p7,tb_p0,how='left',on='Portal')

    tb_reg0=resultado_encuesta[filtro].groupby(['region']).agg(Total=('contador', 'sum')).reset_index()
    tb_reg1=resultado_encuesta[filtro].groupby(['Ultima_Postulacion','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg1=pd.merge(tb_reg1,tb_reg0,how='left',on='region')
    tb_reg2=resultado_encuesta[filtro].groupby(['Nota_facilidad_postulación','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg2=pd.merge(tb_reg2,tb_reg0,how='left',on='region')
    tb_reg3=resultado_encuesta[filtro].groupby(['Nota_pertinencia_info_solicitada','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg3=pd.merge(tb_reg3,tb_reg0,how='left',on='region')
    tb_reg4=resultado_encuesta[filtro].groupby(['Contactada_en_proceso','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg4=pd.merge(tb_reg4,tb_reg0,how='left',on='region')
    tb_reg5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg5=pd.merge(tb_reg5,tb_reg0,how='left',on='region')
    tb_reg6=resultado_encuesta[filtro].groupby(['Nota_oportunidad_entrega_resultados','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg6=pd.merge(tb_reg6,tb_reg0,how='left',on='region')
    tb_reg7=resultado_encuesta[filtro].groupby(['Nota_proceso_reclutamiento_seleccion','region']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_reg7=pd.merge(tb_reg7,tb_reg0,how='left',on='region')

    tb_ret0=resultado_encuesta[filtro].groupby(['rango_etario']).agg(Total=('contador', 'sum')).reset_index()
    tb_ret1=resultado_encuesta[filtro].groupby(['Ultima_Postulacion','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret1=pd.merge(tb_ret1,tb_ret0,how='left',on='rango_etario')
    tb_ret2=resultado_encuesta[filtro].groupby(['Nota_facilidad_postulación','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret2=pd.merge(tb_ret2,tb_ret0,how='left',on='rango_etario')
    tb_ret3=resultado_encuesta[filtro].groupby(['Nota_pertinencia_info_solicitada','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret3=pd.merge(tb_ret3,tb_ret0,how='left',on='rango_etario')
    tb_ret4=resultado_encuesta[filtro].groupby(['Contactada_en_proceso','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret4=pd.merge(tb_ret4,tb_ret0,how='left',on='rango_etario')
    tb_ret5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret5=pd.merge(tb_ret5,tb_ret0,how='left',on='rango_etario')
    tb_ret6=resultado_encuesta[filtro].groupby(['Nota_oportunidad_entrega_resultados','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret6=pd.merge(tb_ret6,tb_ret0,how='left',on='rango_etario')
    tb_ret7=resultado_encuesta[filtro].groupby(['Nota_proceso_reclutamiento_seleccion','rango_etario']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_ret7=pd.merge(tb_ret7,tb_ret0,how='left',on='rango_etario')



#------------------------------------------------------------------------
respuestas=tb_portal['Respuestas'].sum()
tb_g1['porcentaje']=tb_g1['Respuestas']/tb_g1['Total']
tb_g2['porcentaje']=tb_g2['Respuestas']/tb_g2['Total']
tb_g3['porcentaje']=tb_g3['Respuestas']/tb_g3['Total']
tb_g4['porcentaje']=tb_g4['Respuestas']/tb_g4['Total']
tb_g5['porcentaje']=tb_g5['Respuestas']/tb_g5['Total']
tb_g6['porcentaje']=tb_g6['Respuestas']/tb_g6['Total']
tb_g7['porcentaje']=tb_g7['Respuestas']/tb_g7['Total']

tb_p1['porcentaje']=tb_p1['Respuestas']/tb_p1['Total']
tb_p2['porcentaje']=tb_p2['Respuestas']/tb_p2['Total']
tb_p3['porcentaje']=tb_p3['Respuestas']/tb_p3['Total']
tb_p4['porcentaje']=tb_p4['Respuestas']/tb_p4['Total']
tb_p5['porcentaje']=tb_p5['Respuestas']/tb_p5['Total']
tb_p6['porcentaje']=tb_p6['Respuestas']/tb_p6['Total']
tb_p7['porcentaje']=tb_p7['Respuestas']/tb_p7['Total']

tb_reg1['porcentaje']=tb_reg1['Respuestas']/tb_reg1['Total']
tb_reg2['porcentaje']=tb_reg2['Respuestas']/tb_reg2['Total']
tb_reg3['porcentaje']=tb_reg3['Respuestas']/tb_reg3['Total']
tb_reg4['porcentaje']=tb_reg4['Respuestas']/tb_reg4['Total']
tb_reg5['porcentaje']=tb_reg5['Respuestas']/tb_reg5['Total']
tb_reg6['porcentaje']=tb_reg6['Respuestas']/tb_reg6['Total']
tb_reg7['porcentaje']=tb_reg7['Respuestas']/tb_reg7['Total']

tb_ret1['porcentaje']=tb_ret1['Respuestas']/tb_ret1['Total']
tb_ret2['porcentaje']=tb_ret2['Respuestas']/tb_ret2['Total']
tb_ret3['porcentaje']=tb_ret3['Respuestas']/tb_ret3['Total']
tb_ret4['porcentaje']=tb_ret4['Respuestas']/tb_ret4['Total']
tb_ret5['porcentaje']=tb_ret5['Respuestas']/tb_ret5['Total']
tb_ret6['porcentaje']=tb_ret6['Respuestas']/tb_ret6['Total']
tb_ret7['porcentaje']=tb_ret7['Respuestas']/tb_ret7['Total']




with st.container():
    col1, col2=st.columns(spec=[0.2,0.8])
    with col1:
        valor = f"{respuestas:,}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>Número de respuestas</h3>", unsafe_allow_html=True)

    with col2:
        st.dataframe(resultado_encuesta.head(5), width=1500, height=200)
        st.caption('muestra del dataset')
        #st.dataframe(tb1, width=1500, height=500)
        file_content = generate_file_content(resultado_encuesta)
        st.download_button(
            label='Descargar',
            data=file_content,
            file_name='resultados_encuesta.csv',
            mime='text/csv'
            )



# Define el orden deseado para la categoría ultima postulacion, afirmacion, region
ult_post_order = ['Menos de un mes','Entre un mes y seis (6) meses', 'Más de seis (6) meses y menos de un año', 'Más de un año y menos de tres años','Hace más de tres años']     
afirmacion_order = ['Sí','No', 'No aplica'] 
region_order=['Región de Arica y Parinacota','Región de Tarapacá','Región de Antofagasta','Región de Atacama','Región de Coquimbo','Región de Valparaíso','Región Metropolitana','Región de O’Higgins','Región del Maule','Región del Ñuble','Región del Biobío','Región de la Araucanía','Región de Los Lagos','Región de Los Ríos','Región de Aysén','Región de Magallanes']    

graf_g1_p=px.bar(tb_g1, x='genero', y='porcentaje',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_g1_c=px.bar(tb_g1, x='genero', y='Respuestas',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})

graf_p1_p=px.bar(tb_p1, x='Portal', y='porcentaje',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_p1_c=px.bar(tb_p1, x='Portal', y='Respuestas',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})

graf_reg1_p=px.bar(tb_reg1, x='region', y='porcentaje',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg1_c=px.bar(tb_reg1, x='region', y='Respuestas',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})

graf_ret1_p=px.bar(tb_ret1, x='rango_etario', y='porcentaje',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret1_c=px.bar(tb_ret1, x='rango_etario', y='Respuestas',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})

graf_g2_p=px.bar(tb_g2, x='genero', y='porcentaje',color='Nota_facilidad_postulación',barmode='group' ,title='Cuan fácil fue la última postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_g2_c=px.bar(tb_g2, x='genero', y='Respuestas',color='Nota_facilidad_postulación',barmode='group',title='Cuan fácil fue la última postulación?')

graf_p2_p=px.bar(tb_p2, x='Portal', y='porcentaje',color='Nota_facilidad_postulación',barmode='group' ,title='Cuan fácil fue la última postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_p2_c=px.bar(tb_p2, x='Portal', y='Respuestas',color='Nota_facilidad_postulación',barmode='group',title='Cuan fácil fue la última postulación?')

graf_reg2_p=px.bar(tb_reg2, x='region', y='porcentaje',color='Nota_facilidad_postulación',barmode='group' ,title='Cuan fácil fue la última postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg2_c=px.bar(tb_reg2, x='region', y='Respuestas',color='Nota_facilidad_postulación',barmode='group',title='Cuan fácil fue la última postulación?')

graf_ret2_p=px.bar(tb_ret2, x='rango_etario', y='porcentaje',color='Nota_facilidad_postulación',barmode='group' ,title='Cuan fácil fue la última postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret2_c=px.bar(tb_ret2, x='rango_etario', y='Respuestas',color='Nota_facilidad_postulación',barmode='group',title='Cuan fácil fue la última postulación?')

graf_g3_p=px.bar(tb_g3, x='genero', y='porcentaje',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_g3_c=px.bar(tb_g3, x='genero', y='Respuestas',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?')

graf_p3_p=px.bar(tb_p3, x='Portal', y='porcentaje',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_p3_c=px.bar(tb_p3, x='Portal', y='Respuestas',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?')

graf_reg3_p=px.bar(tb_reg3, x='region', y='porcentaje',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg3_c=px.bar(tb_reg3, x='region', y='Respuestas',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?')

graf_ret3_p=px.bar(tb_ret3, x='rango_etario', y='porcentaje',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret3_c=px.bar(tb_ret3, x='rango_etario', y='Respuestas',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?')

graf_g4_p=px.bar(tb_g4, x='genero', y='porcentaje',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_g4_c=px.bar(tb_g4, x='genero', y='Respuestas',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order})

graf_p4_p=px.bar(tb_p4, x='Portal', y='porcentaje',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_p4_c=px.bar(tb_p4, x='Portal', y='Respuestas',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order})

graf_reg4_p=px.bar(tb_reg4, x='region', y='porcentaje',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg4_c=px.bar(tb_reg4, x='region', y='Respuestas',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order})

graf_ret4_p=px.bar(tb_ret4, x='rango_etario', y='porcentaje',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order}).update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret4_c=px.bar(tb_ret4, x='rango_etario', y='Respuestas',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order})

graf_g5_p=px.bar(tb_g5, x='genero', y='porcentaje',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_g5_c=px.bar(tb_g5, x='genero', y='Respuestas',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?')

graf_p5_p=px.bar(tb_p5, x='Portal', y='porcentaje',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_p5_c=px.bar(tb_p5, x='Portal', y='Respuestas',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?')

graf_reg5_p=px.bar(tb_reg5, x='region', y='porcentaje',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg5_c=px.bar(tb_reg5, x='region', y='Respuestas',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?')

graf_ret5_p=px.bar(tb_ret5, x='rango_etario', y='porcentaje',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret5_c=px.bar(tb_ret5, x='rango_etario', y='Respuestas',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?')

graf_g6_p=px.bar(tb_g6, x='genero', y='porcentaje',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_g6_c=px.bar(tb_g6, x='genero', y='Respuestas',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?')

graf_p6_p=px.bar(tb_p6, x='Portal', y='porcentaje',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_p6_c=px.bar(tb_p6, x='Portal', y='Respuestas',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?')

graf_reg6_p=px.bar(tb_reg6, x='region', y='porcentaje',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg6_c=px.bar(tb_reg6, x='region', y='Respuestas',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?')

graf_ret6_p=px.bar(tb_ret6, x='rango_etario', y='porcentaje',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret6_c=px.bar(tb_ret6, x='rango_etario', y='Respuestas',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?')

graf_g7_p=px.bar(tb_g7, x='genero', y='porcentaje',color='Nota_proceso_reclutamiento_seleccion',barmode='group' ,title='Con que nota calificas el proceso de reclutamiento al que postuló?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_g7_c=px.bar(tb_g7, x='genero', y='Respuestas',color='Nota_proceso_reclutamiento_seleccion',barmode='group',title='Con que nota calificas el proceso de reclutamiento al que postuló?')

graf_p7_p=px.bar(tb_p7, x='Portal', y='porcentaje',color='Nota_proceso_reclutamiento_seleccion',barmode='group' ,title='Con que nota calificas el proceso de reclutamiento al que postuló?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_p7_c=px.bar(tb_p7, x='Portal', y='Respuestas',color='Nota_proceso_reclutamiento_seleccion',barmode='group',title='Con que nota calificas el proceso de reclutamiento al que postuló?')

graf_reg7_p=px.bar(tb_reg7, x='region', y='porcentaje',color='Nota_proceso_reclutamiento_seleccion',barmode='group' ,title='Con que nota calificas el proceso de reclutamiento al que postuló?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_reg7_c=px.bar(tb_reg7, x='region', y='Respuestas',color='Nota_proceso_reclutamiento_seleccion',barmode='group',title='Con que nota calificas el proceso de reclutamiento al que postuló?')

graf_ret7_p=px.bar(tb_ret7, x='rango_etario', y='porcentaje',color='Nota_proceso_reclutamiento_seleccion',barmode='group' ,title='Con que nota calificas el proceso de reclutamiento al que postuló?').update_yaxes(tickformat=".2%",range=[0, 1])
graf_ret7_c=px.bar(tb_ret7, x='rango_etario', y='Respuestas',color='Nota_proceso_reclutamiento_seleccion',barmode='group',title='Con que nota calificas el proceso de reclutamiento al que postuló?')

with st.container():
    dimension=st.selectbox('Selecciona la dimensión por la cual visualizar los resultados.',['Género','Portal','Región','Rango Etario'])

if dimension == 'Género':
    with st.container():
        visualizacion=st.selectbox('Selecciona como ver los datos',['Porcentaje','Cantidad'])

    if visualizacion == 'Porcentaje':
        with st.container():
            st.plotly_chart(graf_g1_p, use_container_width=True)
            st.plotly_chart(graf_g2_p, use_container_width=True)
            st.plotly_chart(graf_g3_p, use_container_width=True)
            st.plotly_chart(graf_g4_p, use_container_width=True)
            st.plotly_chart(graf_g5_p, use_container_width=True)
            st.plotly_chart(graf_g6_p, use_container_width=True)
            st.plotly_chart(graf_g7_p, use_container_width=True)
    else:
        with st.container():
            st.plotly_chart(graf_g1_c, use_container_width=True)
            st.plotly_chart(graf_g2_c, use_container_width=True)
            st.plotly_chart(graf_g3_c, use_container_width=True)
            st.plotly_chart(graf_g4_c, use_container_width=True)
            st.plotly_chart(graf_g5_c, use_container_width=True)
            st.plotly_chart(graf_g6_c, use_container_width=True)
            st.plotly_chart(graf_g7_c, use_container_width=True)

if dimension=='Portal':
    with st.container():
        visualizacion=st.selectbox('Selecciona como ver los datos',['Porcentaje','Cantidad'])

    if visualizacion == 'Porcentaje':
        with st.container():
            st.plotly_chart(graf_p1_p, use_container_width=True)
            st.plotly_chart(graf_p2_p, use_container_width=True)
            st.plotly_chart(graf_p3_p, use_container_width=True)
            st.plotly_chart(graf_p4_p, use_container_width=True)
            st.plotly_chart(graf_p5_p, use_container_width=True)
            st.plotly_chart(graf_p6_p, use_container_width=True)
            st.plotly_chart(graf_p7_p, use_container_width=True)
    else:
        with st.container():
            st.plotly_chart(graf_p1_c, use_container_width=True)
            st.plotly_chart(graf_p2_c, use_container_width=True)
            st.plotly_chart(graf_p3_c, use_container_width=True)
            st.plotly_chart(graf_p4_c, use_container_width=True)
            st.plotly_chart(graf_p5_c, use_container_width=True)
            st.plotly_chart(graf_p6_c, use_container_width=True)
            st.plotly_chart(graf_p7_c, use_container_width=True)

if dimension=='Región':
    with st.container():
        visualizacion=st.selectbox('Selecciona como ver los datos',['Porcentaje','Cantidad'])

    if visualizacion == 'Porcentaje':
        with st.container():
            st.plotly_chart(graf_reg1_p, use_container_width=True)
            st.plotly_chart(graf_reg2_p, use_container_width=True)
            st.plotly_chart(graf_reg3_p, use_container_width=True)
            st.plotly_chart(graf_reg4_p, use_container_width=True)
            st.plotly_chart(graf_reg5_p, use_container_width=True)
            st.plotly_chart(graf_reg6_p, use_container_width=True)
            st.plotly_chart(graf_reg7_p, use_container_width=True)
    else:
        with st.container():
            st.plotly_chart(graf_reg1_c, use_container_width=True)
            st.plotly_chart(graf_reg2_c, use_container_width=True)
            st.plotly_chart(graf_reg3_c, use_container_width=True)
            st.plotly_chart(graf_reg4_c, use_container_width=True)
            st.plotly_chart(graf_reg5_c, use_container_width=True)
            st.plotly_chart(graf_reg6_c, use_container_width=True)
            st.plotly_chart(graf_reg7_c, use_container_width=True)

if dimension=='Rango Etario':
    with st.container():
        visualizacion=st.selectbox('Selecciona como ver los datos',['Porcentaje','Cantidad'])

    if visualizacion == 'Porcentaje':
        with st.container():
            st.plotly_chart(graf_ret1_p, use_container_width=True)
            st.plotly_chart(graf_ret2_p, use_container_width=True)
            st.plotly_chart(graf_ret3_p, use_container_width=True)
            st.plotly_chart(graf_ret4_p, use_container_width=True)
            st.plotly_chart(graf_ret5_p, use_container_width=True)
            st.plotly_chart(graf_ret6_p, use_container_width=True)
            st.plotly_chart(graf_ret7_p, use_container_width=True)
    else:
        with st.container():
            st.plotly_chart(graf_ret1_c, use_container_width=True)
            st.plotly_chart(graf_ret2_c, use_container_width=True)
            st.plotly_chart(graf_ret3_c, use_container_width=True)
            st.plotly_chart(graf_ret4_c, use_container_width=True)
            st.plotly_chart(graf_ret5_c, use_container_width=True)
            st.plotly_chart(graf_ret6_c, use_container_width=True)
            st.plotly_chart(graf_ret7_c, use_container_width=True)   
    