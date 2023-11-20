import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('Shopping_Trends.csv')

st.title(':bar_chart: Sales Dashboard')
st.markdown('##')

st.write("Comprehensive payment methods information page. "
         "Here, you'll effortlessly discover everything you need to know about various payment methods. "
         "Our platform provides a user-friendly interface that allows you to navigate seamlessly and explore "
         "details related to payment options, ensuring a smooth and informed experience. "
         "Whether you're interested in understanding available payment methods, comparing their features, "
         "or seeking insights into payment trends, this page is your go-to resource. "
         "Simplify your quest for payment information and make informed decisions with ease."
         "Take your exploration to the next level by customizing your payment methods information based on age "
         "and customer segmentation. ")

# selection
customer = df['Customer Segmentation'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.sidebar.slider('**Age:**',
                                  min_value=min(ages),
                                  max_value=max(ages),
                                  value=(min(ages), max(ages)))

customer_selection = st.sidebar.multiselect('**Customer Segmentation:**',
                                            customer,
                                            default=customer)

# filter dataframe
mask = (df['Age'].between(*age_selection)) & (df['Customer Segmentation'].isin(customer_selection))
number_of_results = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_results}*')

# group dataframe
df_grouped = df[mask].groupby(by=['Payment Method']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Number of Customers'})
df_grouped = df_grouped.reset_index()

# first left graph
bar_chart = px.bar(df_grouped,
                   title='<b>Number of Customers for every Payment Method<b>',
                   x='Payment Method',
                   y='Number of Customers',
                   text='Number of Customers',
                   color_discrete_sequence=['#9B67E2']*len(df_grouped),
                   template='plotly_white')

bar_chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')
bar_chart.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# first right graph
pie_chart = px.pie(df_grouped,
                   title='<b>Percent of Customers for every Payment Method<b>',
                   values='Number of Customers',
                   names='Payment Method',
                   color='Payment Method',
                   color_discrete_map={'Credit Card': '#FF9B9B',
                                       'Venmo': '#FFD28F',
                                       'Cash': '#D0BFFF',
                                       'Paypal': '#FFFAD7',
                                       'Debit Card': '#FFFEC4',
                                       'Bank Transfer': '#CBFFA9'},
                   hole=0.4
                   )

left_column, right_column = st.columns(2)
left_column.plotly_chart(bar_chart, use_container_width=True)
right_column.plotly_chart(pie_chart, use_container_width=True)


