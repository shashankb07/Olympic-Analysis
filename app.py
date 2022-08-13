import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from matplotlib import pyplot as plt

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

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


