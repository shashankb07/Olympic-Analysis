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

    return years, country


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


def countryWise_Medal(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Year', 'Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    region_df = temp_df[temp_df['region'] == country]
    final_df = region_df.groupby('Year')['Medal'].count().reset_index()
    fig = px.line(final_df, x="Year", y='Medal', title='')
    return fig


def country_list(df):
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    return country


def countryWise_Heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Year', 'Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    region_df = temp_df[temp_df['region'] == country]
    heatmap_region = region_df.pivot_table(index=['Sport'], columns=['Year'], values='Medal', aggfunc='count')
    heatmap_region = heatmap_region.fillna(0).astype('int')
    return heatmap_region


def country_multiple_medalist(df, country):
    multiple_medalist = df.dropna(subset=['Medal'])

    multiple_medalist = multiple_medalist[multiple_medalist['region'] == country]
    multiple_medalist = multiple_medalist['Name'].value_counts().reset_index()
    multiple_medalist = multiple_medalist.head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Sport', 'Name_x']].drop_duplicates('index')
    multiple_medalist = multiple_medalist.rename(columns={"index": "Name", "Name_x": "Medals"})

    return multiple_medalist


def weight_vs_height(df, sports):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sports != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sports]
        return temp_df
    else:
        return athlete_df


def Men_vs_Women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    Men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    Final = Men.merge(Women, on='Year', how='left')
    Final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'}, inplace=True)
    Final.fillna(0, inplace=True)

    return Final
