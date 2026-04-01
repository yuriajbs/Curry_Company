#Bibliotecas
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from PIL import Image
# Para dar certo, tem fazer uma nova pagina em python com o nome home. Ai vc coloca cada visualização em um pasta única denominada "pages".
st.set_page_config(page_title='Home')

#Barra lateral
#image_path = "C:/Users/yuri_/2313844.png" --> remove o caminho da imagem do seu pc e coloca na nuvem
image = Image.open ( '2313844.png')
st.sidebar.image( image, width =120)


# Barra lateral inicial da apresentação dos 3 paineis
st.sidebar.markdown( "# Cury Company" )

st.sidebar.markdown( "## Fastest Delivery in Town" )
st.sidebar.markdown( """___""" )

st.write( "# Curry Company Growth Dashboard")

st.markdown ('''
    Growth Dashboard foi constrúido oara acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar o Growth Dashboard?
    - Visão Empresa: 
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de gelolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento dos entregadores;
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes. ''')