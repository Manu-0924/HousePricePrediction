import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

# Load data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Grouping data
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

# Sector Price per Sqft Geomap
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                        mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)

# Features Wordcloud
st.header('Features Wordcloud')

wordcloud = WordCloud(width=800, height=800,
                      background_color='black',
                      stopwords=set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size=10).generate(feature_text)

# Updated to pass the figure explicitly to st.pyplot()
fig_wc, ax_wc = plt.subplots(figsize=(8, 8))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis("off")
st.pyplot(fig_wc)

# Area Vs Price
st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat', 'house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)

# BHK Pie Chart
st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

# Side by Side BHK price comparison
st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

# Side by Side Distplot for property type
st.header('Side by Side Distplot for property type')

fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='house', kde=True, ax=ax4)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat', kde=True, ax=ax4)
ax4.legend()
st.pyplot(fig4)
