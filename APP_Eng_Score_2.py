
import streamlit as st
from PIL import Image
import pandas as pd
import joblib
import requests
from io import BytesIO

# Заголовок и обложку приложения
st.set_page_config(page_title='English Movie Language Difficulty Detector', page_icon=':clapper:', layout='wide', initial_sidebar_state='auto')

MODEL_FILE = './best_model.pkl'.
MOVIES_DATA_URL = 'https://api.themoviedb.org/3/search/movie'
SUBTITLES_DATA_URL = 'https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/EDA_movies_subtitles.csv'
#MODEL_PATH = 'C:/Users/Admin/Desktop/DS studies/Data/English_score/English_score_all_files/V_2/best_model.pkl'

# Загрузка модели
try:
    with open(MODEL_FILE, 'rb') as f:
        model = joblib.load(MODEL_FILE)
except:
    st.write('Error loading the model file.')

# Загрузка картинки в качестве обложки
response = requests.get("https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/eng_cover.jpg")
cover_image = Image.open(BytesIO(response.content))
st.image(cover_image, use_column_width=True)

# Заголовок приложения
st.title('English Movie Language Difficulty Detector')

# Пояснительный текст
st.write('This application will help English learners to determine the level of a movie by subtitles. Just enter the name of a movie and the incredibly cool artificial intelligence will do it.')

# Форма для ввода названия фильма
movie_name = st.text_input('Enter the name of a movie')

# Загрузка данных о субтитрах
subtitles_df = pd.read_csv(SUBTITLES_DATA_URL)

if movie_name:
    # проверяем, есть ли информация о фильме в нашем списке
    movie_info = subtitles_df[subtitles_df['Movie'] == movie_name]
    if movie_info.empty:
        st.write('Sorry, we do not have subtitles for this movie. Please try another one.')
    else:
        # получаем уровень сложности английского языка
        level = model.predict(movie_info['Subtitle'])
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
            color = 'gray'
        st.subheader(f'Level of your movie: ')
        st.subheader(f'{level}',  style=f'color:{color};font-size:30px')
