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
        
        c = st.sidebar.slider('c', 0, 130, 25)
        st.sidebar.latex(r'''
            s = c log(1 + r)
        ''')
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
        
        c = st.sidebar.slider('c', 0, 130, 25)
        gamma = st.sidebar.slider('gamma', 0., 25., .1)
        st.sidebar.latex(r'''
                    s = c r^\gammaγ
        ''')
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
            cinza_copia = np.copy(gray_arr)
            
            cinza_copia[cinza_copia < intervals[0]] = 0
            cinza_copia[(intervals[0] >= cinza_copia) & (cinza_copia <= intervals[1])] = s
            cinza_copia[cinza_copia > intervals[1]] = 0
            
            image = Image.fromarray(cinza_copia).convert('L')
        else:
            # imagem colorida
            colorida = np.copy(image)

            for i in range(3):
                colorida[colorida[:,:,i] < intervals[0]] = 0
                colorida[(intervals[0]>= colorida[:,:,i]) & (colorida[:,:,i] <= intervals[1])] = s
                colorida[colorida[:,:,i] > intervals[1]] = 0
            
            image = Image.fromarray(colorida)
            

        
    elif(option == 'Corte no nível de intensidade'):
        intervals = st.sidebar.slider( 'Intervalo', 0, 255, (25, 75))
        
        s = st.sidebar.slider( 'valor de s', 0, 255, 75)

        if color == 'tons de cinza':
            img = np.copy(gray_arr)            
            img[(intervals[0] >= img) & (img <= intervals[1])] = s
            image = Image.fromarray(img).convert('L')
        else:
            #colorida
            colorida = np.copy(image)

            for i in range(3):
                colorida[(intervals[0]>= colorida[:,:,i]) & (colorida[:,:,i] <= intervals[1])] = s
            
        image = Image.fromarray(colorida)
                
    elif(option == 'Média'):
        
        tam = st.sidebar.slider( 'tamanho do filtro', 3, 9, 3)    

        if color == 'tons de cinza':
            filtro3x3 = np.ones((tam,tam))/tam**2
            img_filtered_arr = np.convolve(filtro3x3.flatten(), gray_arr.flatten(), 'same')
            img_filtered_arr = img_filtered_arr.reshape((480, 640))
            image = Image.fromarray(img_filtered_arr).convert('L')

        else:
            # TODO: Rafa!
            image = Image.fromarray(img).convert('L')
    
    st.image(image, caption='Cage is a Sunrise 🌞 by the mountain 🌄', use_column_width=True)
