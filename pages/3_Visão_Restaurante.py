#Visao_Restaurante
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
import numpy as np
# Reparing bug of Streamlit
import warnings
warnings.filterwarnings('ignore')

#Import dataset
df=pd.read_csv("train.csv")

# Import cleaning 
df['City'] = df['City'].str.strip()

df['Festival'] = df['Festival'].str.strip()

df['Order_Date'] = df['Order_Date'].str.strip()
df = df.dropna(subset=['Order_Date'])

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

linhas_vazias3 = df['City'] != 'NaN'
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
st.title ("Marketplace- Visão Restaurantes")
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

#lAYOUT IN THE STREAMLIT

tab1, tab2, tab3 =st.tabs ([ 'Visão Gerencial', '', ''])

with tab1:
    with st.container():
        st.subheader('Metricas Gerais') 
        col1, col2, col3, col4, col5, col6 = st.columns(6)       
    
        with col1:
            Numero_total_de_entregadores_unicos = df.loc[:, "Delivery_person_ID"].unique().size
            col1.metric('Entregadores Únicos', Numero_total_de_entregadores_unicos)
        
        with col2:
            def haversine_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Radius of Earth in kilometers
            
                lat1_rad = np.radians(lat1)
                lon1_rad = np.radians(lon1)
                lat2_rad = np.radians(lat2)
                lon2_rad = np.radians(lon2)
            
                dlon = lon2_rad - lon1_rad
                dlat = lat2_rad - lat1_rad
            
                a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
            
                distance = R * c
                return distance
        
            df['Distance'] = df.apply(lambda row: haversine_distance(row['Restaurant_latitude'], row['Restaurant_longitude'],
                                                                row['Delivery_location_latitude'], row['Delivery_location_longitude']), axis=1)
        
            mean_distance = np.round (df['Distance'].mean(), 2) #np. round é para definir quanto número depois da , vc quer
            col2.metric('Distância média em km', mean_distance)
            
        
        with col3:
            df_aux = df1.loc[:, ["Festival", "Time_taken(min)"]].groupby("Festival")["Time_taken(min)"].agg(['mean', 'std'])
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            res = df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time']           
            valor_final = round(res.iloc[0], 2) if not res.empty else 0
            col3.metric('Média de tempo (Festival)', valor_final)
            
        with col4: 
            df_aux = df1.loc[:, ["Festival", "Time_taken(min)"]].groupby("Festival")["Time_taken(min)"].agg(['mean', 'std'])
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            res = df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time']           
            valor_final = round(res.iloc[0], 2) if not res.empty else 0
            col4.metric('Desvio padrão médio (Festival)', valor_final)        
        
        with col5:
            df_aux = df1.loc[:, ["Festival", "Time_taken(min)"]].groupby("Festival")["Time_taken(min)"].agg(['mean', 'std'])
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            res = df_aux.loc[df_aux['Festival'] == 'No', 'avg_time']           
            valor_final = round(res.iloc[0], 2) if not res.empty else 0
            col5.metric('Média de tempo (S/Festival)', valor_final)           
        
        with col6:
            df_aux = df1.loc[:, ["Festival", "Time_taken(min)"]].groupby("Festival")["Time_taken(min)"].agg(['mean', 'std'])
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            res = df_aux.loc[df_aux['Festival'] == 'No', 'std_time']           
            valor_final = round(res.iloc[0], 2) if not res.empty else 0
            col6.metric('Desvio padrão médio (S/Festival)', valor_final)      
        
        
        
        
        
    with st.container():
        st.markdown('''___''') 
        
        st.subheader('Distância Média da cidade até o local de entrega')
        avg_distance_city = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()
        avg_distance_city['Distance'] = np.round(avg_distance_city['Distance'], 2) #arredondar a variavel distance
        fig = px.pie(avg_distance_city, 
             values='Distance', 
             names='City')                          
                    
        fig.update_traces(pull=[0, 0.05, 0]) #para dar destaque a uma fatia
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('''___''') 
        st.subheader('Média e  desvio padrão do tempo de entrega por cidade')         
        entregas_tempo_por_cidade = df1.loc[:, ["City", "Time_taken(min)"]].groupby("City")["Time_taken(min)"].agg(['mean', 'std']).reset_index()
        fig = px.bar(entregas_tempo_por_cidade, 
             x='City', 
             y='mean', 
             error_y='std', # Adiciona as hastes do desvio padrão
             labels={'City': 'Cidade', 'mean': 'Tempo Médio (min)'}, # Renomeia os eixos
             color='City') # Dá uma cor diferente para cada cidade
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.markdown('''___''') 
        st.subheader('Média e  desvio padrão do tempo de entrega por tipo de trafégo')        
        entregas_tempo_por_cidade_trafego = df1.loc[:, ["City",'Road_traffic_density', "Time_taken(min)"]].groupby(["City", 'Road_traffic_density'])["Time_taken(min)"].agg(['mean', 'std']).reset_index()
        fig = px.sunburst(entregas_tempo_por_cidade_trafego, 
                      path=['City', 'Road_traffic_density'], 
                      values='mean',
                      color='std', # Cor baseada no desvio padrão (mais escuro = mais variação)
                      color_continuous_scale='RdBu_r',
                      color_continuous_midpoint=np.average( entregas_tempo_por_cidade_trafego['std']))
        st.plotly_chart(fig, use_container_width=True)
        
        
    with st.container():
        st.markdown('''___''') 
        st.subheader('Tempo médio e o desvio padrão de entrega por cidade e tipo de pedido') 
        entregas_tempo_por_cidade_pedido = df1.loc[:, ["City",'Type_of_order', "Time_taken(min)"]].groupby(["City", 'Type_of_order'])["Time_taken(min)"].agg(['mean', 'std']).reset_index()
        st.dataframe( entregas_tempo_por_cidade_pedido)
        
         
         
        

  
        
        
        
        
        
        
        
        
        




















