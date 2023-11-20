

def main():
    import pandas as pd
    import streamlit as st
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import folium
    from streamlit_folium import st_folium

    # page settings
    st.set_page_config(page_title='Shopping Trends',
                       page_icon=':necktie:',
                       layout='wide',
                       )

    page = st.sidebar.selectbox('Choose a page:',
                                ['DataSet',
                                 'Items Info',
                                 'Location',
                                 'Payment Methods'])
    if page == 'DataSet':

        df = pd.read_csv('Shopping_Trends.csv')

        st.title(':necktie: Shopology: Decoding Customer Shopping Trends')

        st.write("**The Shopping Trends Dataset** offers valuable insights into consumer behavior "
                 "and purchasing patterns. Understanding customer preferences and trends is critical "
                 "for businesses to tailor their products, marketing strategies, and overall customer experience. ")
        st.write(
            "\nThis dataset captures a **wide range of customer attributes** including age, gender, purchase history, "
            "preferred payment methods, frequency of purchases, and more. ")
        st.write("\nAnalyzing this data can help businesses make informed decisions, optimize product offerings, "
                 "and enhance customer satisfaction. The dataset stands as a valuable resource for businesses "
                 "aiming to align their strategies with customer needs and preferences. ")
        st.write('\nHere it is 🙃')

        st.write(df)

        st.markdown("## Details")
        st.write("**Title**: Shopping Trends ",
                 "<br>**Rows**: 3900",
                 "<br>**Columns**: 22",
                 unsafe_allow_html=True)

        st.markdown('## Data Dictionary')
        st.write("📌 **Customer ID** - Unique identifier for each customer.",
                 "<br>📌 **Age** - Age of the customer.",
                 "<br>📌 **Gender** - Gender of the customer (Male/Female)",
                 "<br>📌 **Item Purchased** - The item purchased by the customer",
                 "<br>📌 **Category** - Category of the item purchased",
                 "<br>📌 **Purchase Amount (USD)** - The amount of the purchase in USD",
                 "<br>📌 **Location** - Location where the purchase was made",
                 "<br>📌 **Size** - Size of the purchased item",
                 "<br>📌 **Color** - Color of the purchased item",
                 "<br>📌 **Season** - Season during which the purchase was made",
                 "<br>📌 **Review Rating** - Rating given by the customer for the purchased item",
                 "<br>📌 **Payment Method** - Customer's most preferred payment method",
                 "<br>📌 **Shipping Type** - Type of shipping chosen by the customer",
                 "<br>📌 **Previous Purchases** - Number of previous purchases made by the customer",
                 "<br>📌 **Preferred Payment Method** - Method which was used to pay for the purchase",
                 "<br>📌 **Frequency of Purchases** - Frequency at which the customer makes purchases",
                 "<br>📌 **Customer Segmentation** - The official label of a customer",
                 "<br>📌 **Seasonal Trends** - The purpose of purchase",
                 "<br>📌 **Delivery Time** - Duration it takes for a products to be delivered",
                 "<br>📌 **Number of Items Purchased** - The amount of items purchased by a customer",
                 unsafe_allow_html=True)

    elif page == 'Items Info':
    
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
        items_line = df_selection.groupby(by=['Item Purchased']).sum()[['Purchase Amount (USD)']]. \
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

    elif page == 'Location':

        df = pd.read_csv('Shopping_Trends.csv')

        st.title(':bar_chart: Sales Dashboard')
        st.markdown('##')

        st.write(
            "Step into the next level of precision by filtering information based on Location and Shipping Type columns."
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

    elif page == 'Payment Methods':
        

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
                           color_discrete_sequence=['#9B67E2'] * len(df_grouped),
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


main()

