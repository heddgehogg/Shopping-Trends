import pandas as pd
import streamlit as st

# page settings
st.set_page_config(page_title='Shopping Trends',
                   page_icon=':necktie:',
                   layout='wide',
                   primaryColor="#9b67e2"
                   )

df = pd.read_csv('/Users/julie/Downloads/Shopping_Trends.csv')

st.title(':necktie: Shopology: Decoding Customer Shopping Trends')

st.write("**The Shopping Trends Dataset** offers valuable insights into consumer behavior "
         "and purchasing patterns. Understanding customer preferences and trends is critical "
         "for businesses to tailor their products, marketing strategies, and overall customer experience. ")
st.write("\nThis dataset captures a **wide range of customer attributes** including age, gender, purchase history, "
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
