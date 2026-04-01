#Visao_Entregador
#No terminal, o comando crlt+c para de rodar
#libraries
# Todas precisam do comando pip install "nome da biblioteca"
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image # pil =  pillow (biblioteca para maniuplar imagens)  (bilioteca no terminal)
#Bibliotecas necessárias
import pandas as pd
import folium
from streamlit_folium import folium_static # cannot be  -, only _
# Reparing bug of Streamlit
import warnings
warnings.filterwarnings('ignore')

#Import dataset
df=pd.read_csv("train.csv")

# Import cleaning 
df['City'] = df['City'].str.strip()

df['Order_Date'] = df['Order_Date'].str.strip()
df = df.dropna(subset=['Order_Date'])

linhas_vazias3 = df['City'] != 'NaN'
df = df.loc[linhas_vazias3, :]

linhas_vazias1 = df['Time_taken(min)'] != 'NaN '
df = df.loc[linhas_vazias1, :]

linhas_vazias1 = df['multiple_deliveries'] != 'NaN '
df = df.loc[linhas_vazias1, :]

linhas_vazias2 = df['Delivery_person_Age'] != 'NaN '
df = df.loc[linhas_vazias2, :]

linhas_vazias_festival = df['Festival'] != 'NaN '
df= df.loc[linhas_vazias_festival, :]

linhas_vazias = df['Delivery_person_Age'] != 'NaN '
df = df.loc[linhas_vazias, :]

linhas_vazias3 = df['Road_traffic_density'] != 'NaN '
df = df.loc[linhas_vazias3, :]

linhas_vazias3 = df['City'] != 'NaN '
df = df.loc[linhas_vazias3, :]

df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )

df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )

df['Delivery_location_latitude'] = df['Delivery_location_latitude'].astype( float )

df['Delivery_location_longitude'] = df['Delivery_location_longitude'].astype( float )

df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )

# Clean and convert 'Time_taken(min)' more robustly
df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min) ', '', regex=False)
df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')
df.dropna(subset=['Time_taken(min)'], inplace=True)
df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)
df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

df1=df
#LATERAL BAR

import streamlit as st
st.title ("Marketplace- Visão Entregadores")
#Criar uma imagem no Streamlit
#image_path = "C:/Users/yuri_/2313844.png" # Não funciona com barras invertidas
image = Image.open ( '2313844.png')
st.sidebar.image( image, width =120)

st.sidebar.markdown( "# Cury Company" )

st.sidebar.markdown( "## Fastest Delivery in Town" )
st.sidebar.markdown( """___""" )

st.sidebar.markdown( "## Selecione uma data limite")

data_inicio = datetime(2022, 2, 11)
data_fim    = datetime(2022, 4, 13)
data_padrao = datetime(2022, 4, 6)


data_selecionada = st.sidebar.slider(
    "Até qual valor?",
    value=data_padrao,
    min_value=data_inicio,
    max_value=data_fim,
    format="DD-MM-YYYY"
)

df_filtrado = df.loc[df['Order_Date'] <= data_selecionada, :]
df1=df=df_filtrado 
#st.dataframe (df1) me permite visualizar a tabela e ver a data máxima e mínima
st.sidebar.markdown( """___""" )

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam' ])

st.sidebar.markdown( """___""" )

#lAYOUT IN THE STREAMLIT. É interessante primeiro fazer o layout e depois colocar as informações

tab1, tab2, tab3 =st.tabs ([ 'Visão Gerencial', '', ''])

with tab1:
    with st.container(): #This function divede the tab1 in several parts
        st.subheader('Metricas Gerais') 
        
        col1,col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            #st.subheader ('Maior de idade') #se usar o st.title, a palavra fica maior. Usando o st.subheader fica menor
            Entregador_mais_velho = df.loc[:, "Delivery_person_Age"].max()
            col1.metric('Maior de idade',Entregador_mais_velho)
                  
        with col2:
            #st.subheader ('Menor de idade')
            Entregador_mais_novo = df.loc[:,"Delivery_person_Age"].min()
            col2.metric('Menor de idade',Entregador_mais_novo)
                                
        with col3:
            #st.subheader ('Melhor condição de veículos')
            Melhor_condicao = df.loc[:, "Vehicle_condition"].max()
            col3.metric('Melhor condição de veículos',Melhor_condicao)
    
        with col4:
            #st.subheader ('Pior condição de veículos') 
            Pior_condicao = df.loc[:,"Vehicle_condition"].min()
            col4.metric('Pior condição de veículos', Pior_condicao)
   
    
        with st.container():
            st.markdown('''___''') 
            st.subheader('Avaliações')

        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown ('Avaliação media')
            Avaliacao_media = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            #Não da pra usar a col1.metric porque quero exibir uma tabela
            st.dataframe(Avaliacao_media)
        
        with col2:
            st.markdown ('Avaliação média por trânsito')
            Entregas_avaliacoes_por_trafego = df1.loc[:, ["Road_traffic_density", "Delivery_person_Ratings"]].groupby("Road_traffic_density")["Delivery_person_Ratings"].agg(['mean', 'std'])
            #Mudança de nome das colunas
            Entregas_avaliacoes_por_trafego.columns = ['Média por entregador', 'Desvio padrão por entregador']
            #Reset_index
            Entregas_avaliacoes_por_trafego=Entregas_avaliacoes_por_trafego.reset_index()
            st.dataframe( Entregas_avaliacoes_por_trafego)
            
            
            st.markdown ('Avaliação média por clima')
            entregas_avaliacoes_por_condicoes_climaticas = df1.groupby("Weatherconditions")["Delivery_person_Ratings"].agg(['mean', 'std'])
            entregas_avaliacoes_por_condicoes_climaticas.columns = ['Média', 'Desvio padrão']
            #Reset_index
            entregas_avaliacoes_por_condicoes_climaticas=entregas_avaliacoes_por_condicoes_climaticas.reset_index()
            st.dataframe(  entregas_avaliacoes_por_condicoes_climaticas)
            
            
    

    with st.container():
        st.markdown('''___''') 
        st.subheader('Velocidade de entrega')

        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown('Top entregadores mais rápidos')
            df2 = df1.loc[:, ['Delivery_person_ID', "City", "Time_taken(min)"]].groupby( ["City", "Delivery_person_ID"] )['Time_taken(min)'].min().reset_index().sort_values(["City", "Time_taken(min)"])
            df_aux01=df2.loc[df2["City"] == "Metropolitian", :].head(10)
            df_aux02=df2.loc[df2["City"] == "Urban", :].head(10)
            df_aux03=df2.loc[df2["City"] == "Semi-Urban", :].head(10)
            df3 = pd.concat( [df_aux01, df_aux02, df_aux03]).reset_index( drop=True)
            st.dataframe(df3)


        
        with col2:
            st.markdown ('Top entregadores mais lentos')
            df2 = df1.loc[:, ['Delivery_person_ID', "City", "Time_taken(min)"]].groupby( ["City", "Delivery_person_ID"] )['Time_taken(min)'].max().reset_index().sort_values(["City", "Time_taken(min)"], ascending=False)            
            df_aux01=df2.loc[df2["City"] == "Metropolitian", :].head(10)
            df_aux02=df2.loc[df2["City"] == "Urban", :].head(10)
            df_aux03=df2.loc[df2["City"] == "Semi-Urban", :].head(10)
            df3 = pd.concat( [df_aux01, df_aux02, df_aux03]).reset_index( drop=True)
            st.dataframe(df3)








