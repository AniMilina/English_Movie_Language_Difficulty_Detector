#!/usr/bin/env python
# coding: utf-8

# In[24]:
!pip install --upgrade pip
!pip install -r requirements.txt
!pip uninstall click
!pip install click==7.1.2 

import pandas as pd
import joblib
import pickle
import requests

from io import StringIO
from typing import List, Dict

import streamlit as st

import requests
import io
from PIL import Image


# In[25]:


MODEL_URL = 'https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/best_model.pkl'
MOVIES_DATA_URL = 'https://api.themoviedb.org/3/search/movie'

# загрузка модели
try:
    model = joblib.load(MODEL_URL)
except:
    st.write('Error loading the model file.')

# функция для получения информации о фильме из API
def get_movie_info(movie_name: str) -> Dict:
    payload = {'api_key': 'c831eb220940792881b5d28c4e3ea02a', 'query': movie_name}
    r = requests.get(MOVIES_DATA_URL, params=payload)
    if r.status_code == 200:
        data = r.json()['results'][0]
        movie_info = {'title': data['original_title'], 'overview': data['overview'], 'release_date': data['release_date']}
        return movie_info
    else:
        st.write('Error getting movie data from the API.')


# In[28]:


# функция для определения уровня сложности английского языка в фильме

def predict_level(movie_name: str) -> str:
    try:
        movie_info = get_movie_info(movie_name)
        # здесь можно использовать дополнительные признаки, такие как жанр фильма, сложность диалогов и т.д.
        level = model.predict([movie_info['overview']])[0]
        return level
    except:
        st.write('Error predicting the level.')


# In[29]:


# устанавливаем заголовок и обложку приложения

st.set_page_config(page_title='English Movie Language Difficulty Detector', page_icon=':clapper:', layout='wide', initial_sidebar_state='auto', menu_items=None)


# In[30]:


# загружаем картинку в качестве обложки

from PIL import Image
cover_image = Image.open("https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/eng_cover.jpg")
st.image(cover_image, use_column_width=True)


# In[31]:


# задаем заголовок приложения

st.title('English Movie Language Difficulty Detector')


# In[32]:


# пояснительный текст

st.write('This application will help English learners to determine the level of a movie by subtitles. Just enter the name of a movie and the incredibly cool artificial intelligence will do it.')


# In[33]:


# форма для ввода названия фильма

movie_name = st.text_input('Enter the name of a movie')


# In[34]:


if movie_name:
    # проверяем, есть ли информация о фильме в нашем списке
    movie_info = movies_df[movies_df['movie_title'] == movie_name].iloc[0]
    if not movie_info:
        st.write('Sorry, we do not have subtitles for this movie. Please try another one.')
    else:
        # получаем уровень сложности английского языка
        level = predict_level(movie_name)
        # отображаем уровень с использованием разных цветов шрифта
        if level == 'Beginner':
            color = 'green'
        elif level == 'Intermediate':
            color = 'orange'
        elif level == 'Advanced':
            color = 'red'
        else:
            color = 'black'
        st.subheader(f'Level of your movie: ')
        st.subheader(f'{level}',  style=f'color:{color};font-size:30px')
else:
    st.write('Please enter a movie name.')


# In[ ]:





# In[ ]:




