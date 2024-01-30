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
df_encuesta=df_encuesta[~df_encuesta['Portal'].isin(['Nunca he postulado','No aplica'])]
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
    tb_g3=resultado_encuesta.groupby(['Nota_pertinencia_info_solicitada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g4=resultado_encuesta.groupby(['Contactada_en_proceso','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g5=resultado_encuesta.groupby(['Nota_calidad_evaluacion_realizada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g6=resultado_encuesta.groupby(['Nota_oportunidad_entrega_resultados','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g7=resultado_encuesta.groupby(['Nota_proceso_reclutamiento_seleccion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    
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
    resultado_encuesta=df_encuesta[filtro]
    tb_g0=resultado_encuesta[filtro].groupby(['genero']).agg(Total=('contador', 'sum')).reset_index()
    tb_g1=resultado_encuesta[filtro].groupby(['Ultima_Postulacion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g2=resultado_encuesta[filtro].groupby(['Nota_facilidad_postulación','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g3=resultado_encuesta[filtro].groupby(['Nota_pertinencia_info_solicitada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g4=resultado_encuesta[filtro].groupby(['Contactada_en_proceso','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g5=resultado_encuesta[filtro].groupby(['Nota_calidad_evaluacion_realizada','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g6=resultado_encuesta[filtro].groupby(['Nota_oportunidad_entrega_resultados','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
    tb_g7=resultado_encuesta[filtro].groupby(['Nota_proceso_reclutamiento_seleccion','genero']).agg(Respuestas=('contador', 'sum')).reset_index()
#------------------------------------------------------------------------
respuestas=tb_portal['Respuestas'].sum()
tb_g1['porcentaje']=tb_g1['Respuestas']/tb_g1['Total']

with st.container():
    col1, col2=st.columns(spec=[0.2,0.8])
    with col1:
        valor = f"{respuestas:,}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>Número de respuestas</h3>", unsafe_allow_html=True)
        file_content = generate_file_content(resultado_encuesta)
        st.download_button(
            label='Descargar',
            data=file_content,
            file_name='resultados_encuesta.csv',
            mime='text/csv'
            )
    with col2:
        st.dataframe(resultado_encuesta.head(5), width=1500, height=200)
        st.caption('muestra del dataset')
        #st.dataframe(tb1, width=1500, height=500)

# Define el orden deseado para la categoría 'genero'
ult_post_order = ['Menos de un mes','Entre un mes y seis (6) meses', 'Más de seis (6) meses y menos de un año', 'Más de un año y menos de tres años','Hace más de tres años']     
afirmacion_order = ['Sí','No', 'No aplica']     
graf_g1_p=px.bar(tb_g1, x='genero', y='porcentaje',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})
graf_g1_c=px.bar(tb_g1, x='genero', y='Respuestas',color='Ultima_Postulacion',barmode='group' ,title='Hace cuanto fue la última postulación?',category_orders={'Ultima_Postulacion': ult_post_order})
graf_g2=px.bar(tb_g2, x='genero', y='Respuestas',color='Nota_facilidad_postulación',barmode='group' ,title='Cuan fácil fue la última postulación?')
graf_g3=px.bar(tb_g3, x='genero', y='Respuestas',color='Nota_pertinencia_info_solicitada',barmode='group' ,title='Cuan pertinente es la información solicitada en la postulación?')
graf_g4=px.bar(tb_g4, x='genero', y='Respuestas',color='Contactada_en_proceso',barmode='group' ,title='Fue contactada para entregar feedback del proceso?',category_orders={'Contactada_en_proceso':afirmacion_order})
graf_g5=px.bar(tb_g5, x='genero', y='Respuestas',color='Nota_calidad_evaluacion_realizada',barmode='group' ,title='Con que nota calificas el proceso de evaluación?')
graf_g6=px.bar(tb_g6, x='genero', y='Respuestas',color='Nota_oportunidad_entrega_resultados',barmode='group' ,title='Con que nota calificas la oportunidad de entrega de resultados?')
graf_g7=px.bar(tb_g7, x='genero', y='Respuestas',color='Nota_proceso_reclutamiento_seleccion',barmode='group' ,title='Con que nota calificas el proceso de reclutamiento al que postuló?')


with st.container():
    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(graf_g1_p, use_container_width=True)
    with col2:
        st.plotly_chart(graf_g1_c, use_container_width=True)
    

    st.plotly_chart(graf_g2, use_container_width=True)
    st.plotly_chart(graf_g3, use_container_width=True)
    st.plotly_chart(graf_g4, use_container_width=True)
    st.plotly_chart(graf_g5, use_container_width=True)
    st.plotly_chart(graf_g6, use_container_width=True)
    st.plotly_chart(graf_g7, use_container_width=True)