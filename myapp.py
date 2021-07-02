import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import requests
import time


def five(image_url,rating_):
    if(image_url is not None):
        col5.image(image_url)
        col5.write(rating)
    else:
        pass
    return 5
def six(image_url,rating_):
    if(image_url is not None):
        col6.image(image_url)
        col6.write(rating)
    else:
        pass
    return 6
def seven(image_url,rating_):
    if(image_url is not None):
        col7.image(image_url)
        col7.write(rating)
    else:
        pass
    return 7


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
#wrapped scraper for suggestion
def scrape_selected_movie(url):
    content=requests.get(url).text
    web_soup=BeautifulSoup(content,"html.parser")
    container_soup=web_soup.find("div",class_="mvi-content")
    try:
        image_url=container_soup.find("img")["src"]
    except AttributeError:
        image_url=None
    title_=container_soup.find("h3").text
    synopsis_=container_soup.find("p",class_="f-desc").text
    genre_=container_soup.find("div",class_="mvic-info").find("p").text
    genre_=genre_.replace("\xa0","")
    spans=container_soup.find("div",class_="mvic-info").find_all("span")
    director_tags=spans[0].find_all("a",rel="tag")
    directors_="Directors: "
    for tag in director_tags:
        directors_=directors_+tag.text+","
    spans=container_soup.find("div",class_="mvic-info").find_all("span")#also in directors remove
    actor_tags=spans[1].find_all("a",rel="tag")
    actors_="Actors: "
    for tag in actor_tags:
        actors_=actors_+" "+tag.text+","
    duration_=container_soup.find("div",class_="mvici-right").find("span",itemprop="duration").text
    duration_="Duration: "+duration_
    quality_=container_soup.find("div",class_="mvici-right").find("span",class_="quality").text
    quality_="Quality: "+quality_
    release_=container_soup.find("div",class_="mvici-right").find("a",rel="tag").text
    release_="Release: "+release_
    return image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_

#load model
loaded_model = pickle.load(open("model.pkl", "rb"))

#create review dataset
review_df=pd.read_csv("main_movie_ratings.csv")
review_df=review_df.drop('movie_id',axis=1).reset_index()
review_df=review_df.drop('index',axis=1)
review_df=review_df.drop_duplicates(subset='title',keep='first',inplace=False)

#creates dataset for elections requires review_df
selection_options=pd.DataFrame(review_df['title']).rename(columns={'title':'select_option'})
selection_options=pd.DataFrame(selection_options['select_option'].str.lower())
selection_options.replace({'_':' '},regex=True,inplace=True)
selection_options=selection_options.join(pd.DataFrame(review_df['title']))

st.write("""
# MOVIE RECOMMENDATION SYSTEM
""")

local_css("styles.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
icon("search")

#creates set of inputs requires selection_options
col1, col2 = st.beta_columns([3, 1.5])
selected=col1.text_input("movie search")
# loops through select options
if not selected :
    st.warning('Please input a movie title :(')
    st.stop()
presets=[]
movie_page_links=[]
count=0
for index,row in selection_options.iterrows():
    if selected.lower() in row['select_option']:
        if count<20:
            with st.spinner('Processing :)'):
                time.sleep(2)
        else:
            with st.spinner('Processing, If taking too long reEnter  Title to narrow down:)'):
                time.sleep(2)
            count=0
        presets.append(row["select_option"])
        count=count+1

suggestion_select=col2.selectbox("preset movies",presets,help="select movie to view recommendations")
with st.spinner('locked and loaded , hope you selected your preset :)'):
    time.sleep(5)
#key equiv to id in css
button_clicked = st.button("OK",key="submit_title",help="submits movie presets selection")

suggestion_status=[]
#onclick give recommendations and the movie itself
if button_clicked== True:
    #generate recommendations showing the overall rating of each recommended movie
    selected_options=pd.DataFrame(selection_options.loc[ selection_options['select_option']==suggestion_select ] )
    selected_options=selected_options.merge(review_df,on='title')
    # append this
    url=selected_options.iloc[0,3]
    rating=selected_options.iloc[0,-1]
    rating_= "Rating: {}".format(rating)
    col3, col4 = st.beta_columns([1,2])
    with st.spinner('Establishing Connection , make sure you have an Internet Connection :)'):
        time.sleep(5)
    #print the suggestion_selections details
    try:
        #scrape movie details
        image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(url)
        #Image(image_url)
        #displaying image
        if(image_url is not None):
            col3.image(image_url)
        else:
            pass
        col3.write(rating_)
        col4.write(title_)
        col4.write(synopsis_)
        col4.write(genre_)
        col4.write(directors_)
        col4.write(actors_)
        col4.write(duration_)
        col4.write(quality_)
        col4.write(release_)
        #display link
        st.write(url)
        #content
        #st.write(selected_options)
        #print recommendations
        required_genres=genre_.split(":")[1].split(",")
        required_genres=list( map(lambda x: x.lower(), required_genres) )
        #st.write(review_df)
        #st.write(review_df.loc[ review_df["genre"].isin(required_genres) ] )
        #df of possible suggestable videos equiv to reviews_list
        suggestions_df=review_df.loc[ review_df["genre"].isin(required_genres) ]
        #split the data
        suggestions_df=suggestions_df.drop('watch_link',axis=1)
        X=suggestions_df.iloc[:,:-1]
        y=pd.DataFrame(suggestions_df.iloc[:,-1])
        #test code for y label encoder and X encoder
        encoded_X=pd.get_dummies(X, prefix=['title', 'genre'])
        label_encoded_y=y.apply(LabelEncoder().fit_transform)
        avg_rating=float(label_encoded_y.mean())
        label_encoded_y.loc[ label_encoded_y['movie_rating'] < avg_rating,'movie_rating' ]=0
        label_encoded_y.loc[ label_encoded_y['movie_rating'] > avg_rating,'movie_rating' ]=1
        #st.write(suggestions_arr=np.array(suggestions_df))
        loaded_model.fit(encoded_X,label_encoded_y)
        pred=loaded_model.predict(encoded_X)
        rec=[]
        for p in pred:
            rec.append(p)
        rec=pd.Series(rec[2])
        #pd.Series(pred),ignore_index=True
        suggestions_df=suggestions_df.append(rec,ignore_index=True )
        suggestions_df.rename(columns={0:"like"},inplace=True)
        suggestions_df.loc[ suggestions_df["movie_rating"]>=rating,"like"]=1
        suggestions_df.loc[ suggestions_df["movie_rating"]<rating,"like"]=0
        st.write(" ")
        st.write(" ")
        st.title("YOU MIGHT ALSO LIKE ")
        st.write(" ")
        st.write(" ")
        recommends=suggestions_df.merge(review_df,on=['title',"genre","movie_rating"])
        #like-3 link-4
        col5, col6 = st.beta_columns([1,2])
        column = 5
        for index,row in recommends.loc[recommends["like"]==1].iterrows():
            scrape_link=row["watch_link"]
            recommend_rating=row["movie_rating"]
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #Image(image_url)
                #displaying image
                if(image_url is not None):
                    col5.image(image_url)
                else:
                    pass
                col5.write(recommend_rating)
                col6.write(title_)
                col6.write(synopsis_)
                col6.write(directors_)
                col6.write(actors_)
                col6.write(release_)
                #display link
                col6.write(url)
                st.write(" ")
                st.write(" ")
            except:
                pass
    except (ConnectionError):
        st.warning("dear user , please check your Internet Connection to view results :(")
        st.stop()

##########
#st.write(selection_options)
#suggestions=st.selectbox("",review_df)
#######

#add suggestions
