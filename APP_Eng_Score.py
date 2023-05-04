#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import joblib
import pickle
import requests

from io import StringIO
from typing import List, Dict


# In[17]:


import streamlit as st


# In[18]:


#добавляем возможность загрузки модели на GitHub
import requests
import io


# In[19]:


MODEL_PATH = 'best_model.pkl'
MOVIES_DATA_URL = 'https://api.themoviedb.org/3/search/movie'


# In[20]:


# загрузка модели
try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
except:
    st.write('Error loading the model file.')


# In[21]:


# функция для получения информации о фильме из API
def get_movie_info(movie_name: str) -> Dict:
    payload = {'api_key': 'API_KEY', 'query': movie_name}
    r = requests.get(MOVIES_DATA_URL, params=payload)
    if r.status_code == 200:
        data = r.json()['results'][0]
        movie_info = {'title': data['original_title'], 'overview': data['overview'], 'release_date': data['release_date']}
        return movie_info
    else:
        st.write('Error getting movie data from the API.')


# In[22]:


# функция для определения уровня сложности английского языка в фильме
def predict_level(movie_name: str) -> str:
    try:
        movie_info = get_movie_info(movie_name)
        # здесь можно использовать дополнительные признаки, такие как жанр фильма, сложность диалогов и т.д.
        level = model.predict([movie_info['overview']])[0]
        return level
    except:
        st.write('Error predicting the level.')


# In[23]:


# задаем заголовок приложения
st.title('English Subtitles Level Prediction')


# In[24]:


#пояснительный текст
st.write('This application will help English learners to determine the level of a movie by subtitles. Just enter the name of a movie and the incredibly cool artificial intelligence will do it.')


# In[25]:


#форма для ввода названия фильма
movie_name = st.text_input('Enter the name of a movie')


# In[26]:


if movie_name:
    # проверяем, есть ли информация о фильме в нашем списке
    movie_info = movies_df[movies_df['movie_title'] == movie_name].iloc[0]
    if not movie_info:
        st.write('Sorry, we do not have subtitles for this movie. Please try another one.')
    else:
        # получаем уровень сложности английского языка
        level = predict_level(movie_name)
        st.subheader(f'Level of your movie: {level}')
else:
    st.write('Please enter a movie name.')


# In[31]:


# Сохраняем модель в формате .pkl на локальный компьютер

def save_model_to_local(model):
    path = 'C:/Users/Admin/Desktop/DS studies/Data/English_score/English_score_all_files/V_2'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, 'best_model.pkl')
    joblib.dump(model, file_path)
    st.write('Model saved successfully to local computer.')

# Сохраняем модель в формате .pkl на GitHub

def save_model_to_github(model):
    url = 'https://github.com/AniMilina/English-Movie-Language-Difficulty-Detector/blob/main/best_model.pkl' 
    headers = {'Authorization': 'token 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'}
    response = requests.put(url, headers=headers, data=open('best_model.pkl', 'rb'))
    if response.status_code == 200:
        st.write('Model saved successfully to GitHub.')
    else:
        st.write('Error saving the model to GitHub.')
    
    # Сохраняем модель в формате .py на GitHub
    
    url = 'https://github.com/AniMilina/English-Movie-Language-Difficulty-Detector/blob/main/best_model.py' 
    headers = {'Authorization': 'token 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'}
    response = requests.put(url, headers=headers, data=open('best_model.py', 'rb'))
    if response.status_code == 200:
        st.write('Model saved successfully to Streamlit.')
    else:
        st.write('Error saving the model to Streamlit.')
    
    # Сохраняем модель в формате .pkl на локальный компьютер
    
    save_model_to_local(model)


# In[32]:


# #сохраняем модель на GitHub

# def save_model_to_github():
#     # Сохраняем в формате .pkl на GitHub
#     url = 'https://github.com/AniMilina/English-Movie-Language-Difficulty-Detector/blob/main/best_model.pkl' 
#     headers = {'Authorization': 'token YOUR_TOKEN'}
#     response = requests.put(url, headers=headers, data=open('best_model.pkl', 'rb'))
#     if response.status_code == 200:
#         st.write('Model saved successfully to GitHub.')
    
#     # Сохраняем в формате .py для Streamlit
#     url = 'https://github.com/AniMilina/English-Movie-Language-Difficulty-Detector/blob/main/best_model.py' 
#     headers = {'Authorization': 'token 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  '}
#     response = requests.put(url, headers=headers, data=open('best_model.py', 'rb'))
#     if response.status_code == 200:
#         st.write('Model saved successfully to Streamlit.')
    
#     # Если сохранение не удалось
#     else:
#         st.write('Error saving the model.') 


# In[33]:


#добавляем кнопку для сохранения модели на GitHub
if st.button('Save model to GitHub'):
    save_model_to_github()


# In[34]:


def save_app_to_github():
    
    # Сохраняем на GitHub
    
    url = 'https://github.com/AniMilina/English-Movie-Language-Difficulty-Detector/blob/main/eng_app.py' 
    headers = {'Authorization': 'token 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'}
    response = requests.put(url, headers=headers, data=open('eng_app.py', 'rb'))
    if response.status_code == 200:
        print('Code saved successfully to GitHub.')
    
    # Сохраняем на локальный компьютер
    
    local_path = r'C:\Users\Admin\Desktop\DS studies\Data\English_score\English_score_all_files\V_2\eng_app.py'
    with open(local_path, 'wb') as f:
        f.write(response.content)
    print(f'Code saved successfully to {local_path}.')


# In[ ]:




