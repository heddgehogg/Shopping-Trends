import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium

df = pd.read_csv('Shopping_Trends.csv')

st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

st.write("Step into the next level of precision by filtering information based on Location and Shipping Type columns."
         " Seamlessly refine your search to pinpoint data relevant to specific locations and shipping preferences."
         " Whether you're seeking details about a particular region or looking to understand the nuances of different "
         "shipping methods, our platform empowers you to tailor your exploration. "
         "Navigate with ease as you unlock insights tied to location-based dynamics and shipping intricacies. "
         "Your quest for targeted and refined data analysis continues here.")

# filter the data
st.sidebar.header('Choose Filter Here: ')
# create for location
location = st.sidebar.multiselect('Pick your State', df['Location'].unique())
if not location:
    df2 = df.copy()
else:
    df2 = df[df['Location'].isin(location)]

# create for shipping type
shipping = st.sidebar.multiselect('Pick your Shipping Type', df2['Shipping Type'].unique())
if not shipping:
    df3 = df2.copy()
else:
    df3 = df2[df2['Shipping Type'].isin(shipping)]

# filter the data
if not location and not shipping:
    filtered_df = df
elif location and shipping:
    filtered_df = df3[df['Location'].isin(location) & df3['Shipping Type'].isin(shipping)]
elif location:
    filtered_df = df3[df['Location'].isin(location)]
else:
    filtered_df = df3[df['Shipping Type'].isin(shipping)]

# Data Set
st.dataframe(filtered_df)

# left graph

st.markdown('### Percentage by Gender/Season/Customer Segmentation:')
fig = px.sunburst(
    data_frame=filtered_df,
    path=['Gender', 'Season', 'Customer Segmentation'],
    color='Season',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    maxdepth=-1
)

fig.update_traces(textinfo='label+percent entry')
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

st.markdown("---")  # Add horizontal space
st.plotly_chart(fig)
st.markdown("---")  # Add more horizontal space


# map
st.title(':world_map: Sales Map')
st.markdown('##')

st.write("Here you can explore and uncover insights into the spending habits of different states across the "
         "United States. Dive into the data to find 8 states that lead the way in terms of purchase expenditures. ")

df_map = pd.read_csv('map_file.csv')

st.dataframe(df_map)

fig = px.scatter_geo(
    df_map,
    locations='Code',
    locationmode='USA-states',
    color='Code',
    scope='usa',
    color_discrete_map={'MT': '#636EFA', 'ME': '#00CC96', 'FL': '#AB63FA', 'DE': '#FFA15A', 'VA': '#B6E880',
                        'KY': '#B6E880', 'IN': '#FBE426', 'AR': '#DEA0FD'}
)

st.plotly_chart(fig)
