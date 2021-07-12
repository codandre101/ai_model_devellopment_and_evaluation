import streamlit as st
import pandas as pd
import numpy as np
import pickle
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import requests
import time
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def print_trending(possible_likes,index_carry=0):
    colA,colB, colC,colD,colE = st.beta_columns([1,1,1,1,1])
    #for place 1 colA
    start=index_carry+1
    max_for_row=5
    end=max_for_row+index_carry
    for col in range(start,end+1):
        row=col-1
        scrape_link=possible_likes.iloc[row,2]
        recommend_rating=possible_likes.iloc[row,3]
        if col==(index_carry+1):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colA.image(image_url)
                else:
                    pass
                btnA=colA.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnA==True:
                    main()
                colA.write(release_)
            except:
                pass
        elif col==(index_carry+2):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colB.image(image_url)
                else:
                    pass
                btnB=colB.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnB==True:
                    main()
                colB.write(release_)
            except:
                pass
        elif col==(index_carry+3):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colC.image(image_url)
                else:
                    pass
                btnC=colC.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnC==True:
                    main()
                colC.write(release_)
            except:
                pass
        elif col==(index_carry+4):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colD.image(image_url)
                else:
                    pass
                btnD=colD.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnD==True:
                    main()
                colD.write(release_)
            except:
                pass
        elif col==(index_carry+5):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colE.image(image_url)
                else:
                    pass
                btnE=colE.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnE==True:
                    main()
                colE.write(release_)
            except:
                pass
        else:
            break

    index_carry=index_carry+max_for_row
    return index_carry
def print_row(possible_likes,index_carry=0):
    colA,colB, colC,colD,colE = st.beta_columns([1,1,1,1,1])
    #for place 1 colA
    start=index_carry+1
    max_for_row=5
    end=max_for_row+index_carry
    for col in range(start,end+1):
        row=col-1
        scrape_link=possible_likes.iloc[row,4]
        recommend_rating=possible_likes.iloc[row,2]
        if col==(index_carry+1):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colA.image(image_url)
                else:
                    pass
                btnA=colA.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnA==True:
                    main()
                colA.write(recommend_rating)
                colA.write(release_)
            except:
                pass
        elif col==(index_carry+2):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colB.image(image_url)
                else:
                    pass
                btnB=colB.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnB==True:
                    main()
                colB.write(recommend_rating)
                colB.write(release_)
            except:
                pass
        elif col==(index_carry+3):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colC.image(image_url)
                else:
                    pass
                btnC=colC.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnC==True:
                    main()
                colC.write(recommend_rating)
                colC.write(release_)
            except:
                pass
        elif col==(index_carry+4):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colD.image(image_url)
                else:
                    pass
                btnD=colD.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnD==True:
                    main()
                colD.write(recommend_rating)
                colD.write(release_)
            except:
                pass
        elif col==(index_carry+5):
            try:
                image_url, title_, synopsis_,genre_,directors_,actors_,duration_,quality_,release_=scrape_selected_movie(scrape_link)
                #displaying image
                if(image_url is not None):
                    colE.image(image_url)
                else:
                    pass
                btnE=colE.button("TITLE:{}".format(title_),key="submit_title",help="copy title in search bar to view movie")
                if btnE==True:
                    main()
                colE.write(recommend_rating)
                colE.write(release_)
            except:
                pass
        else:
            break

    index_carry=index_carry+max_for_row
    return index_carry

def main(val=None):
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

    st.title("""
    # MOVIE RECOMMENDATION SYSTEM
    """)

    local_css("styles.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    icon("search")
    #creates set of inputs requires selection_options
    col1, col2 = st.beta_columns([3, 1.5])

    selected=col1.text_input("movie search",value=val)
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
                break
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
        st.write("")
        st.title("TRENDING MOVIES")
        st.write(print_trending(review_df))
        #generate recommendations showing the overall rating of each recommended movie
        selected_options=pd.DataFrame(selection_options.loc[ selection_options['select_option']==suggestion_select ] )
        selected_options=selected_options.merge(review_df,on='title')
        # append this
        url=selected_options.iloc[0,3]
        rating=selected_options.iloc[0,-1]
        rating_= "Rating: {}".format(rating)
        with st.spinner('Establishing Connection , make sure you have an Internet Connection :)'):
            time.sleep(5)
        st.write("")
        st.write("")
        st.title("SEARCH RESULT")
        #print the suggestion_selections details
        col3, col4 = st.beta_columns([1,2])
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
            #print recommendations
            required_genres=genre_.split(":")[1].split(",")
            required_genres=list( map(lambda x: x.lower(), required_genres) )
            clean_genres=[]
            for genre in required_genres:
                genre=genre.replace(" ","")
                clean_genres.append(genre)
            required_genres=clean_genres
            #df of possible suggestable videos equiv to reviews_list
            suggestions_df=review_df.loc[ review_df["genre"].isin(required_genres) ]
            #split the data
            suggestions_df=suggestions_df.drop('watch_link',axis=1)
            suggestions_df.reset_index(inplace=True)
            suggestions_df=suggestions_df.drop('index',axis=1)
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
            reccomandable_col=pd.DataFrame(pred)
            #st.write(reccomandable_col)
            suggestions_df['like']=pred
            #st.write(suggestions_df)
            #first five
            st.write(" ")
            st.write(" ")
            st.title("  ***YOU MIGHT ALSO LIKE***")
            st.write(" ")
            st.write(" ")
            reccommendations_=suggestions_df.loc[ suggestions_df['like']==1]
            possible_likes=reccommendations_.sort_values( by="movie_rating" ,ascending=False)
            possible_likes.reset_index(inplace=True)
            possible_likes=possible_likes.drop('index',axis=1)
            #st.write(possible_likes)
            possible_likes=possible_likes.merge(review_df,on=['title',"genre","movie_rating"])
            st.write(" ")
            st.write(" ")
            #st.write(possible_likes)
            #like-3 link-4

            #print row
            try:
                index_carry=0
                st.write(print_row(possible_likes,index_carry) )
            except IndexError:
                st.write("")
            try:
                index_carry=index_carry+5
                st.write(print_row(possible_likes,index_carry) )
            except IndexError:
                st.write("")
            try:
                index_carry=index_carry+10
                st.write(print_row(possible_likes,index_carry))
            except IndexError:
                st.write("")
            try:
                index_carry=index_carry+15
                st.write(print_row(possible_likes,index_carry))
            except IndexError:
                st.write("")
            try:
                index_carry=index_carry+20
                st.write(print_row(possible_likes,index_carry) )
            except IndexError:
                st.write("")
            try:
                index_carry=index_carry+25
                st.write(print_row(possible_likes,index_carry) )
            except IndexError:
                st.write("")
        except (ConnectionError):
            st.warning("dear user , please check your Internet Connection to view results :(")
            st.stop()

if __name__ == '__main__':
    main()
