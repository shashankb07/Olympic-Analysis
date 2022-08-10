import streamlit as st
import pandas as pd

import helper
import preprocessor

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

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
