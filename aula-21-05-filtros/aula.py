import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
# import matplotlib.pyplot as plt

st.sidebar.title('Aula dia 21-05')

st.title('Filtros')

uploaded_file = st.sidebar.file_uploader("Escolha a imagem", type=['png', 'jpg'])

if uploaded_file is not None:
    image_original = Image.open(uploaded_file)    
    image = np.copy(image_original)

    color = st.sidebar.radio(
     "",
     ('colorida', 'tons de cinza'))

    if color == 'tons de cinza':
        gray_arr = np.mean(np.array(image), axis=2)
        image = Image.fromarray(gray_arr).convert('L') 
            

    option = st.sidebar.selectbox(
        'Escolha um filtro',
        (
            'Escolha um filtro',
            'Negativo',
            'Transformação em (log)',
            'Transformação (Power-Law)',
            'Alongamento de contraste',
            'Corte no nível de intensidade',
            'Média', 
            'Gaussiano',
        )
    )

    st.sidebar.text(option)

    if(option == 'Negativo'):
        if color == 'tons de cinza':
            image = Image.fromarray(255 - gray_arr).convert('L') 
        else:
            image = Image.fromarray(255 - image)
    elif(option == 'Transformação em (log)'):
        st.sidebar.latex(r'''
            s = c log(1 + r)
        ''')
        c = st.sidebar.slider('c', 0, 130, 25)
        if color == 'tons de cinza':
            log_image_arr = c * (np.log(gray_arr + 1))
            image = Image.fromarray(log_image_arr).convert('L')
            # image = Image.fromarray(255 - gray_arr).convert('L') 
        else:
            image[:,:,0] = c * (np.log(image[:,:,0] + 1))
            image[:,:,1] = c * (np.log(image[:,:,1] + 1))
            image[:,:,2] = c * (np.log(image[:,:,2] + 1))
            image = Image.fromarray(image).convert('L')
            # image = Image.fromarray(255 - gray_arr).convert('L') 
    elif(option == 'Transformação (Power-Law)'):
        st.sidebar.latex(r'''
            s = c r^\gammaγ
        ''')
        c = st.sidebar.slider('c', 0, 130, 25)
        gamma = st.sidebar.slider('gamma', 0., 25., .1)
       
        if color == 'tons de cinza':
            image = Image.fromarray(c * (gray_arr/255) ** gamma).convert('L') 
        else:
            for i in range(3):
                image[:,:,i] = (c * (image[:,:,i]/255) ** gamma)

            image = Image.fromarray(image)
            
    elif(option == 'Alongamento de contraste'):
        intervals = st.sidebar.slider( 'Intervalo', 0, 255, (25, 75))
        s = st.sidebar.slider( 'valor de s', 0, 255, 75)

        if color == 'tons de cinza':
            image = Image.fromarray(gray_arr).convert('L') 
        

    
    st.image(image, caption='Cage is a Sunrise by the mountain', use_column_width=True)