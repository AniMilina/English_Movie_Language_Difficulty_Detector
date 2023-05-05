#!/usr/bin/env python
# coding: utf-8

# Install necessary packages
# pip install --upgrade pip
# pip install -r requirements.txt
# pip uninstall click
# pip install click==7.1.2 

import streamlit as st
from PIL import Image
import pandas as pd
import joblib
import pickle
import requests
from io import StringIO
from typing import List, Dict
from io import BytesIO

# устанавливаем заголовок и обложку приложения

st.set_page_config(page_title='English Movie Language Difficulty Detector', page_icon=':clapper:', layout='wide', initial_sidebar_state='auto')


# In[25]:


MODEL_URL = 'https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/best_model.pkl'
MOVIES_DATA_URL = 'https://api.themoviedb.org/3/search/movie'
movies_df = pd.read_csv("https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/EDA_movies_subtitles.csv")

# загрузка модели
try:
    model = joblib.load(MODEL_URL)
except:
    st.write('Error loading the model file.')



# загружаем картинку в качестве обложки

response = requests.get("https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/eng_cover.jpg")
cover_image = Image.open(BytesIO(response.content))
st.image(cover_image, use_column_width=True)


# задаем заголовок приложения
st.title('English Movie Language Difficulty Detector')


# пояснительный текст
st.write('This application will help English learners to determine the level of a movie by subtitles. Just enter the name of a movie and the incredibly cool artificial intelligence will do it.')


# форма для ввода названия фильма
movie_name = st.text_input('Enter the name of a movie')


if movie_name:
    # проверяем, есть ли информация о фильме в нашем списке
    movie_info = movies_df[movies_df['Movie'] == movie_name]
if len(movie_info) == 0:
    st.write('Sorry, we do not have subtitles for this movie. Please try another one.')
else:
    if movie_info.empty:
        st.write('Sorry, we do not have subtitles for this movie. Please try another one.')
    else:
        movie_info = movie_info.iloc[0]
        # получаем уровень сложности английского языка
        level = predict_level(movie_name)
        # отображаем уровень с использованием разных цветов шрифта
        if level == 'A1':
            color = 'green'
        elif level == 'A2':
            color = 'orange'
        elif level == 'B1':
            color = 'red'
        elif level == 'B2':
            color = 'purple'
        elif level == 'C1':
            color = 'blue'
        elif level == 'C2':
            color = 'black'
        else:
            color = 'black'
        st.subheader(f'Level of your movie: ')
        st.subheader(f'{level}',  style=f'color:{color};font-size:30px')
else:
    st.write('Please enter a movie name.')
# In[ ]:





# In[ ]:




