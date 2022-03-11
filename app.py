import os
import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# Python Part

movies_dict = pickle.load(open('data/moviedb_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)

similarity = pickle.load(open('data/moviedb_similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    API_KEY = os.getenv('TMDB_API_KEY')
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_index]
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda k: k[1])[1:6]
    rec_mov_list = []
    rec_mov_posters = []
    for i in recommended_movies:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        rec_mov_list.append(movies_df.iloc[i[0]]['title'])
        rec_mov_posters.append(fetch_poster(movie_id))
    return rec_mov_list, rec_mov_posters

# Webapp Part

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown(
    """
    <style>
        #movie-recommendation-app{
            text-align: center;
        }
    </style>
    """,unsafe_allow_html=True,
)

st.title("Movie Recommendation App")

cols_mov_selectbox = st.columns([3,6,3])

with cols_mov_selectbox[1]:
    fav_movie = st.selectbox(
        'Enter your favourite movie',
        movies_df['title'].values
    )

if st.button('Recommend'):
    rec_names, posters = recommend(fav_movie)
    st.write(f'Based on your favourite movie, we recommend:')
    
    cols = st.columns(5)
    # cols = (col1,col2,col3,col4,col5)
    
    for col in cols:
        with col:
            st.text(rec_names[cols.index(col)])
            st.image(posters[cols.index(col)])



