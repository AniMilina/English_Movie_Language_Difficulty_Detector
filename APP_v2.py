import pandas as pd
import streamlit as st
import requests
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# функция для получения информации о фильме
def get_movie_info(movie_title):
    api_key = '6c5d6e2df1e5f6dbaa9ac7c2b2e93ea7'
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': movie_title}
    response = requests.get(base_url, params=params)
    movie_info = response.json()['results'][0]
    return movie_info

# функция для получения уровня сложности языка
def predict_level(movie_title):
    # загрузка модели
    with open('best_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # получение информации о фильме
    movie_info = get_movie_info(movie_title)
    movie_id = movie_info['id']
    language = movie_info['original_language']

    # получение субтитров
    subtitle_url = f'https://rest.opensubtitles.org/search/movie-xml?imdbid={movie_id}&sublanguageid=en'
    response = requests.get(subtitle_url)
    subtitle = response.json()['data'][0]['attributes']['SubDownloadLink']

    # загрузка субтитров
    subtitle_content = requests.get(subtitle).text
    subtitle_content = subtitle_content.replace('\n', ' ')

    # создание корпуса документов
    documents = [subtitle_content, movie_info['overview']]

    # векторизация
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    # предсказание уровня
    prediction = model.predict(X)
    if prediction == 0:
        return 'Beginner'
    elif prediction == 1:
        return 'Intermediate'
    elif prediction == 2:
        return 'Advanced'

# загрузка списка фильмов
movies_df = pd.read_csv('https://github.com/AniMilina/English_Movie_Language_Difficulty_Detector/raw/main/EDA_movies_subtitles.csv')

# форма для ввода названия фильма
movie_name = st.text_input('Enter the name of a movie')

if movie_name:
    # проверяем, есть ли информация о фильме в нашем списке
    movie_info = movies_df[movies_df['Movie'] == movie_name].iloc[0]
    if movie_info.empty:
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
