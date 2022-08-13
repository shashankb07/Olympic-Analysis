import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib import pyplot as plt

import helper
import preprocessor

from PIL import Image

image = Image.open('olympic_logo1.jpg')

st.sidebar.image(image, width=250)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.header("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')
    if selected_year == 'Overall' and selected_country != 'Overall':
        country_name = selected_country
        st.title('Medal tally of ' + str(country_name))
    if selected_year != 'Overall' and selected_country == 'Overall':
        year_sel = selected_year
        st.title(str(year_sel) + ' Summer Olympics Medal Tally')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) + ' at the ' + str(selected_year) + ' Summer Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    edition = len(df['Year'].unique())
    cities = len(df['City'].unique())
    regions = len(df['region'].unique())
    sports = len(df['Sport'].unique())
    events = len(df['Event'].unique())
    athletes = len(df['Name'].unique())
    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Editions')
        st.title(edition)
    with col2:
        st.subheader('Hosts')
        st.title(cities)
    with col3:
        st.subheader('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Events')
        st.title(events)
    with col2:
        st.subheader('Region')
        st.title(regions)
    with col3:
        st.subheader('Athletes')
        st.title(athletes)

    st.header('Participating Nations Over the Years')
    figure = helper.nations_over_time(df)
    st.plotly_chart(figure)

    st.header('Athletes Over the Years')
    figure = helper.Athletes_over_time(df)
    st.plotly_chart(figure)

    st.header('Events Over the Years')
    figure = helper.events_over_time(df)
    st.plotly_chart(figure)

    st.header('Number of Events over the Time')
    fig, ax = plt.subplots(figsize = (25,25))
    heatmap_df = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        heatmap_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

