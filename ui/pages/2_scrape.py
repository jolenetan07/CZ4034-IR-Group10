import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from langdetect import detect
import re

st.set_page_config(page_title="Crawling", page_icon="🕷️")

tweets_df = pd.DataFrame()
st.write("# Twitter Scraper")
option = st.selectbox('Search data via...',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Query')
start = st.date_input("Select start date", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select end date", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('Select number of tweets', 0, 1000, 5)
tweets_list = []


# PREPROCESS
def preprocess(tweets_df):
    timestamp_data_raw = tweets_df['Date'].values
    text_data_raw = tweets_df['Text'].values
    like_data_raw = tweets_df['LikeCount'].values

    text_data = []
    en_count = 0

    timestamp_data = []
    likes_data = []
    index = 0

    for text in text_data_raw:
        if text != '':
            try:
                language = detect(text)

                if language == 'en':
                    en_count = en_count + 1
                    text_data.append(text)
                    timestamp_data.append(timestamp_data_raw[index])
                    likes_data.append(like_data_raw[index])
            except:
                continue
            finally:
                index = index + 1

    clean_df = pd.DataFrame(
        {'Date': timestamp_data,
        'Text': text_data,
        'LikeCount': likes_data
        })

    clean_df = clean_df.drop_duplicates(keep='first')

    def clean_urls(review):
        review = review.split()
        review = ' '.join([word for word in review if not re.match('^http', word)])
        return review

    def clean_text(text):
        text = str(text)
        text = re.sub(r'(\w)\1{2,}', r'\1', text)
        text = re.sub(r'[^a-zA-Z0-9 ]+', ' ', text)
        text = re.sub(r'http\S+', ' ', text)
        text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)
        text = re.sub(r'^RT[\s]+', '', text)
        text = re.sub(r'pic.twitter\S+', ' ', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'@\w+', '', text)
        text = text.lower()

        return text

    stop_words = set(stopwords.words('english'))
    stop_words.remove('not') 
    # lemmatizer = WordNetLemmatizer()

    def data_preprocessing(review):
        
    # data cleaning
        review = re.sub(re.compile('<.*?>'), '', review) #removing html tags
        review =  re.sub('[^A-Za-z0-9]+', ' ', review) #taking only words
    
    # lowercase
        review = review.lower()
    
    # tokenization
        tokens = nltk.word_tokenize(review) # converts review to tokens
    
    # stop_words removal
        review = [word for word in tokens if word not in stop_words] #removing stop words
    
    # lemmatization
        # review = [lemmatizer.lemmatize(word) for word in review]
    
    # join words in preprocessed review
        review = ' '.join(review)
        return review

    clean_df['Clean Text'] = clean_df['Text'].apply(clean_urls).apply(clean_text)

    clean_df['Clean Text'] = clean_df['Clean Text'].apply(lambda review: data_preprocessing(review))
    
    st.write(len(clean_df))
    st.write(len(tweets_df))

    return clean_df

# SCRAPE DATA 
if word:
    try:
        if option=='Keyword':
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} lang:en since:{start} until:{end}').get_items()):
                if i>tweet_c-1:
                    break
                tweets_list.append([ tweet.date, tweet.rawContent,tweet.likeCount ])
            tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'Text', 'LikeCount'])
        else:
            for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} lang:en since:{start} until:{end}').get_items()):
                if i>tweet_c-1:
                    break            
                tweets_list.append([ tweet.date, tweet.content ])
            tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'Text'])
        tweets_df = preprocess(tweets_df)
    except Exception as e:
        st.error(e)
        st.stop()

else:
    st.warning(option,' cant be empty', icon="⚠️")

#SIDEBAR
# with st.sidebar:   
#     st.info('DETAILS', icon="ℹ️")
#     if option=='Keyword':
#         st.info('Keyword is '+word)
#     else:
#         st.info('Hashtag is '+word)
#     st.info('Starting Date is '+str(start))
#     st.info('End Date is '+str(end))
#     st.info("Number of Tweets "+str(tweet_c))
#     st.info("Total Tweets Scraped "+str(len(tweets_df)))
#     x=st.button('Show Tweets',key=1)

# DOWNLOAD AS CSV
# @st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
# def convert_df(df):    
#     return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    # with col1:
    #     csv = convert_df(tweets_df) # CSV
    #     c=st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)        
    # with col2:    # JSON
    #     json_string = tweets_df.to_json(orient ='records')
    #     j=st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    with col2: # SHOW
        y=st.button('Display Tweets',key=2)

# if c:
#     st.success("The Scraped Data is Downloaded as .CSV file:",icon="✅")  
# if j:
#     st.success("The Scraped Data is Downloaded as .JSON file",icon="✅")     
# if x: # DISPLAY
#     st.success("The Scraped Data is:",icon="✅")
#     st.write(tweets_df)
if y: # DISPLAY
    st.balloons()
    st.success("Tweets Scraped Successfully:",icon="✅")
    st.write(tweets_df)

    


            

