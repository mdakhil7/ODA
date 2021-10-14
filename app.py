import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.tools import FigureFactory as FF

df = pd.read_csv(
    r"C:\Users\hp\PycharmProjects\olmpycis_Analysis\athlete_events.csv")
region_df = pd.read_csv(
    r"C:\Users\hp\PycharmProjects\olmpycis_Analysis\noc_regions.csv")

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall-Analysis', 'Athlete-Analysis', 'Country-wise-Analysis')
)
st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_years = st.sidebar.selectbox("Select Years", years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally = helper.fetch_medal_tally(
        df, selected_years, selected_country)
    if selected_years == ' Overall ' and selected_country == ' Overall ':
        st.title("Overall Tally")
    if selected_years != ' Overall ' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_years) + " Olympics")
    if selected_years == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall performance ")
    if selected_years != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance " +
                 str(selected_years))

    st.table(medal_tally)


# Overall Analysis

if user_menu == 'Overall-Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Editions", y="region")
    st.title("Participating Nations over all the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Editions", y="Event")
    st.title("Events over all the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Editions", y="Name")
    st.title("Athletes over all the years")
    st.plotly_chart(fig)

    st.title("No. of Events over the time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                     annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful1(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise-Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = FF.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist',
                                                'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=400)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
