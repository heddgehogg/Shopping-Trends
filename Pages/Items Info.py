import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('Shopping_Trends.csv')

st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

st.write("Here, you can easily discover a wealth of relevant information tailored to your needs. "
         "Navigate effortlessly through the data by employing our user-friendly filtering options. "
         "Explore details related to Categories, delve into specifics about individual Items, "
         "and gain insights into Size and Color attributes. ")
st.write('Your journey to comprehensive and insightful data exploration begins here...')

# sidebar
st.sidebar.header('Choose Filter Here: ')
gender = st.sidebar.multiselect(
    "Select the Gender: ",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

season = st.sidebar.multiselect(
    'Select the Season: ',
    options=df['Season'].unique(),
    default=df['Season'].unique()
)

segmentation = st.sidebar.multiselect(
    'Select the Customer Segmentation: ',
    options=df["Customer Segmentation"].unique(),
    default=df['Customer Segmentation'].unique()
)

df_selection = df.query(
    "Gender == @gender & Season == @season & `Customer Segmentation` == @segmentation"
)

# main page
total_sales = int(df_selection['Purchase Amount (USD)'].sum())
average_rating = round(df_selection['Review Rating'].mean(), 1)
star_rating = ':star:' * int(round(average_rating, 0))
average_amount_of_orders = round(df_selection['Number of Items Purchased'].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Sales:')
    st.write(f'**USD $ {total_sales}**')
with middle_column:
    st.subheader('Average Rating:')
    st.write(f'**{average_rating} {star_rating}**')
with right_column:
    st.subheader('Average Items Purchased:')
    st.write(f'**{average_amount_of_orders} items**')

st.markdown('---')

# Data Set
st.dataframe(df_selection)

# first left graph
items_line = df_selection.groupby(by=['Item Purchased']).sum()[['Purchase Amount (USD)']].\
    sort_values(by='Purchase Amount (USD)')

fig_items = px.histogram(
    items_line,
    x=items_line.index,
    y='Purchase Amount (USD)',
    title='<b>Purchase Amount for each item (USD)</b>',
    color_discrete_sequence=['#9B67E2'] * len(items_line),
    template='plotly_white'
)

# st.plotly_chart(fig_items)

# first right graph
category_line = df_selection.groupby(by=['Category']).sum()[['Purchase Amount (USD)']]
fig_category = px.bar(
    category_line,
    x='Purchase Amount (USD)',
    y=category_line.index,
    title='<b>Purchase Amount for each category (USD)</b>',
    color_discrete_sequence=['#FBE426'] * len(category_line),
    template='plotly_white'
)

# right place
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_items, use_container_width=True)
right_column.plotly_chart(fig_category, use_container_width=True)

# second left graph
colors = df_selection['Color'].unique()
selected_color = st.multiselect('Choose color:', colors)
filtered_df = df_selection[df_selection['Color'].isin(selected_color)]

color_graph = px.histogram(
    filtered_df,
    x='Purchase Amount (USD)',
    y='Color',
    title=f'<b>Purchase amount for {", ".join(selected_color)} items<b>',
    color_discrete_sequence=['#FBE426'] * len(category_line),
    template='plotly_white'
)

# second right graph
size_graph = px.pie(filtered_df,
                    title='<b>Purchase Amount for each Size<b>',
                    values='Purchase Amount (USD)',
                    names='Size',
                    color='Size',
                    color_discrete_map={'M': '#9B67E2',
                                        'L': '#BEADFA',
                                        'S': '#DFCCFB',
                                        'XL': '#FFF8C9'},
                    hole=0.4
                    )

# right place
left_column, right_column = st.columns(2)
left_column.plotly_chart(color_graph, use_container_width=True)
right_column.plotly_chart(size_graph, use_container_width=True)
