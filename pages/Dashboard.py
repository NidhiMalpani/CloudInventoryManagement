import pyodbc
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

#connecting to azure sql database
driver='{SQL Server}'
server='tcp:pilventory-server.database.windows.net,1433'
database='pilventory-db'
username='pilventory'
password='Team@57san'

#creating a connection string
conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

#establishing connection
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()

#fetching data and creating the dataframe
query = "SELECT * FROM dbo.current_data"
df = pd.read_sql(query, conn)

#closing connection
cursor.close()
conn.close()

#preprocessing
#df.rename(columns={'Branch': 'Product'}, inplace=True)
#df.rename(columns={'Product_line': 'Category'}, inplace=True)

#vISUALIZATION
def Plot(X, Y, xlabel, ylabel, explode):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    # Plot 1: Bar chart
    axes[0].bar(X, Y)
    axes[0].set_xlabel('xlabel')
    axes[0].set_ylabel('ylabel')
    axes[0].tick_params(axis='x', rotation=60)
    axes[0].set_title('Bar Chart')

    # Plot 2: Donut chart
    wedges, texts, autotexts = axes[1].pie(Y, labels=X, autopct='%1.1f%%', startangle=90, pctdistance=0.80)
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    axes[1].add_artist(centre_circle)
    axes[1].axis('equal')
    axes[1].set_title('Donut Chart')

    plt.tight_layout()
    st.pyplot(fig)


st.title('Live Inventory')
#category vs quantity  --- currently we have this many products of this category
#bar plot
st.header('Total Stock Distribution')
categories = df['Category'].unique()
total_quantity = []
for category in categories:
    sum_quantity = df[df['Category'] == category]['Quantity'].sum()
    total_quantity.append(sum_quantity)

Plot(categories, total_quantity, 'Category', 'Quantity', [0.05, 0.05, 0.05, 0.05, 0.05, 0.05])

#product vs quantity --for a given category (entered by the user) what is the breakdown of products in stock
def get_products(category):
    products = df[df['Category'] == category]['Product'].unique()
    return products

st.header('Category Wise Stock Distribution')
cat = st.selectbox('Select a Category', categories)
products = get_products(cat)
product_quantity = []
for product in products:
    sum_quantity = df[df['Product'] == product]['Quantity'].sum()
    product_quantity.append(sum_quantity)
Plot(products, product_quantity, 'Product', 'Quantity', [0.05, 0.05, 0.05])

#city wise breakdown
st.header('City Wise Stock Distribution')
st.write('')
#Stacked bar graph
stack_columns = ['City','Category', 'Quantity']
stacked_df = df[stack_columns].copy()

# stacked_df.plot(kind = 'barh', stacked = True)
# st.pyplot()
stacked_bar = alt.Chart(stacked_df).mark_bar().encode(
    x="City:N",
    y="sum(Quantity):Q",
    color="Category:N"
)
st.altair_chart(stacked_bar, use_container_width=True)