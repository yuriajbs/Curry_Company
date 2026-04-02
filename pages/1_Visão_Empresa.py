#Visao_Empresa
#libraries
# Todas precisam do comando pip install "nome da biblioteca"
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st
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


#######################################################
df1=df
#print (df1.head())

# Visão Empresa

#==========================================
#LAYOUT NO STREAMLIT --> no terminal: streamlit run visão empresa. A partir dai serão códigos do próprio Streamlit
# O terminal é compilador
# Se vc quer aplicar mais funções no Streamlit, use o manual online
#Important plannig all layouts before start 
#==========================================

#LATERAL BAR


                                                                                                                                                                                     
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

# Agora o seu slider vai funcionar sem erros:
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
st.title ("Marketplace- Visão Cliente")

tab1, tab2, tab3 =st.tabs ([ 'Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container(): #This function divede the tab1 in several parts
        st.markdown( '## Pedidos por dia')
        df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
        graph1 = px.bar ( df_aux, x='Order_Date', y='ID' ) 
    
        st.plotly_chart( graph1, use_container_width=True) # For use the graph, is necessaru st.ploty_chart

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown( '## Pedidos por trafégo')  
            df_aux = df1.loc[:, ["ID", "Road_traffic_density"]].groupby( 'Road_traffic_density' ).count().reset_index()
            df_aux['entregas_%'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
            graph2 = px.pie( df_aux, values='entregas_%', names='Road_traffic_density' )
            st.plotly_chart( graph2, use_container_width=True)

        with col2: 
            st.markdown( '## Pedidos por tipo de cidade e trafégo') 
            df_aux = df.loc[:, ["ID", 'City', 'Road_traffic_density']].groupby( ['City', 'Road_traffic_density'] ).count().reset_index()
            df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum())
            graph3 = px.bar( df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group')
            st.plotly_chart( graph3, use_container_width=True)

with tab2:
    with st.container():
        st.markdown( '## Pedidos por semana por entregador')    
        df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
        df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year' ).nunique().reset_index()
        df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
        df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        graph4=px.line( df_aux, x='week_of_year', y='order_by_delivery' )
        st.plotly_chart( graph4, use_container_width=True)

    with st.container():
        st.markdown( '## Pedidos por semana')
        df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
        df_aux= df1.loc[:, ["ID", "week_of_year"]].groupby("week_of_year").count().reset_index()
        graph5 = px.line( df_aux, x='week_of_year', y='ID' )
        st.plotly_chart( graph5, use_container_width=True)


with tab3:                
    st.markdown( '## Mapa das entregas  ') 
    df_aux = df1.loc[:,['City','Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude' ]].groupby( ['City', 'Road_traffic_density'] ).median().reset_index()
    map_ = folium.Map( zoom_start=11 )
    for index, location_info in df_aux.iterrows():
     folium.Marker( [location_info['Delivery_location_latitude'],
      location_info['Delivery_location_longitude']],
      popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )   
    
    folium_static(map_, width=1100, height = 600)