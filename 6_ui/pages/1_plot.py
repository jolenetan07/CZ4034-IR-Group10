import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Classification Graphs", page_icon="📈")

# st.markdown("# Plotting Demo")
# st.sidebar.header("Plotting Demo")
# st.write(
#     """This demo illustrates a combination of plotting and animation with
# Streamlit. We're generating a bunch of random numbers in a loop for around
# 5 seconds. Enjoy!"""
# )

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")



df = pd.read_csv("final_data.csv")
df['NFT'] = df['NFT'].astype(str)
df['Clean'] = df['Clean'].astype(str)
df['Polarity'] = df['Polarity'].astype(str)
df['Datetime'] = pd.to_datetime(df['Datetime'])

# ======================================= GRAPH PLOTTING ====================================================================================
def query_db(spec_nft, search_query, search_result_number):
    string = "Showing Graphs for: "
    for nft in spec_nft:
        string += f" {nft}" if nft == spec_nft[-1] else f" {nft},"
    st.write(string)
    fig1 = plot_overall(df,spec_nft)
    st.plotly_chart(fig1)
    fig2 = plot_timeseries(df,spec_nft)
    st.plotly_chart(fig2)

def plot_overall(df,nft_name):
    sentiment_df = df.groupby(['NFT','Polarity']).size().reset_index(name='Count of Sentiment')
    filtered_df = sentiment_df[sentiment_df['NFT'].isin(nft_name)]
    fig = px.bar(filtered_df, x="Polarity", y="Count of Sentiment", title="Sentiment Count",color = 'Polarity',color_discrete_map={
        '-1' : 'red',
        '0' : 'blue',
        '1' : 'green'
        })
    fig.update_layout(
                  xaxis = dict(
                    tickmode='array', #change 1
                    tickvals = ['neg','neu','pos'], #change 2
                    ticktext = ["Negative","Neutral","Positive"], #change 3
                    ))
    return fig

def plot_timeseries(df,nft_name):
    nft_df = df[df["NFT"].isin(nft_name)]
    nft_df['Datetime'] = pd.to_datetime(nft_df['Datetime'])
    nft_df['Polarity'] = pd.to_numeric(nft_df['Polarity'])
    nft_df = nft_df.sort_values("Datetime").reset_index(drop=True)
    grouped_data = nft_df.groupby(['NFT', pd.Grouper(key='Datetime', freq='M')])
    nft_df = grouped_data['Polarity'].mean().reset_index()
    return px.line(nft_df, x='Datetime', y="Polarity",title ="Average Sentiment Score", color='NFT')

# ======================================= MISC STREMALIT ====================================================================================
def create_streamlit_form(html_string):
    st.markdown('**Search filters**')
    # search_result_number = st.slider('Number of search results', min_value=1, max_value=50,value = 10)
    spec_nft = st.multiselect('Specific NFT Graphs', ['Azuki',
        'Bored Ape Yacht Club',
        'CloneX',
        'CryptoPunks',
        'Meebits',
        'MekaVerse',
        'Mutant Ape Yacht Club',
        'Phanta Bear',
        'Pixelmon',
        'The Potatoz'])
    search_bool = st.form_submit_button('Search')
    return spec_nft,search_bool,0


st.markdown("# :chart_with_upwards_trend: Classification Graphs")
html_string = "<br>"
st.markdown(html_string, unsafe_allow_html=True)
# string ='''
#         We have indexed **10,000** tweets. You can find Sentiment Analysis as well as their sentiment trends by searching for Tweets
#         '''
# st.markdown(string)
# search_query = st.text_input('Enter your search query')

st.markdown('This page returns graphs for the the selected NFT.')
st.markdown(html_string, unsafe_allow_html=True)

with st.form("Filters"):
    spec_nft,search_bool,search_result_number = create_streamlit_form(html_string)

if spec_nft != []:
    query_db(spec_nft, "", search_result_number)

