import matplotlib as matplotlib
import numpy as np
import plotly.express as px
import seaborn as sns
from matplotlib import pyplot as plt


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'index')
    nations_over_time.rename(columns={'index': 'Years', 'Year': 'Participated Nations'}, inplace=True)
    fig = px.line(nations_over_time, x="Years", y="Participated Nations")
    return fig


def Athletes_over_time(df):
    Athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'index')
    Athletes_over_time.rename(columns={'index': 'Years', 'Year': 'Athletes Participated'}, inplace=True)
    fig = px.line(Athletes_over_time, x="Years", y="Athletes Participated")
    return fig

def events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(
        'index')
    events_over_time.rename(columns={'index': 'Years', 'Year': 'Events'}, inplace=True)
    fig = px.line(events_over_time, x="Years", y="Events")
    return fig


def multiple_medalist(df, Sport):
    multiple_medalist = df.dropna(subset=['Medal'])

    if Sport != 'Overall':
        multiple_medalist = multiple_medalist[multiple_medalist['Sport'] == Sport]
    multiple_medalist = multiple_medalist['Name'].value_counts().reset_index()
    multiple_medalist = multiple_medalist.head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'region', 'Sport', 'Name_x']].drop_duplicates('index')
    multiple_medalist = multiple_medalist.rename(columns={"index": "Name", "Name_x": "Total"})

    return multiple_medalist

