import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings("ignore")

import helper
import preprocessor

from PIL import Image

image = Image.open('Olympic_rings_with_transparent_rims.svg.png')

st.sidebar.image(image, width=175)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.header("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
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
    fig, ax = plt.subplots(figsize=(28, 22))
    heatmap_df = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        heatmap_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.header('List of Olympic medals over career')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sports_list)
    top_medalist = helper.multiple_medalist(df, selected_sport)
    st.table(top_medalist)

if user_menu == 'Country-wise Analysis':

    st.title('Country-Wise Analysis')
    selected_country = helper.country_list(df)
    country = st.selectbox('Select A Country', selected_country)

    country_medals = helper.countryWise_Medal(df, country)
    st.header(str(country) + ' at the Olympics ')
    st.plotly_chart(country_medals)
    st.header('heatmap of medals  won by '+ str(country))
    heatmap_region = helper.countryWise_Heatmap(df, country)
    heatmap = helper.countryWise_Heatmap(df, country)
    f, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(heatmap, annot=True, ax=ax)
    st.pyplot(f)
    st.header(str(country)+"'s Top 10 athletes")
    countryWise_performer = helper.country_multiple_medalist(df, country)
    st.table(countryWise_performer)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    st.title('Age distribution')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Players Age With respect to Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    st.title('Medal distribution based on Height And Weight')
    selected_sport = st.selectbox('Select a Sport', sports_list)
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'],hue=temp_df["Medal"], style= temp_df['Sex'], s = 100)
    st.pyplot(fig)

    st.title('Men vs Women Participation over years')
    final_df = helper.Men_vs_Women(df)
    fig = px.line(final_df, x='Year', y=['Men', 'Women'])
    st.plotly_chart(fig)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


