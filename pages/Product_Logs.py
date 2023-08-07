import streamlit as st
import pyodbc

# Azure SQL Database connection parameters
server = 'pilventory-server.database.windows.net'
database = 'pilventory-db'
username = 'pilventory'
password = 'Team@57san'
driver = '{SQL Server}'  # Update this with the appropriate driver version

conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_string)

st.title('Product Logs.')
st.write('')

def accept_values():
    invoiceId = st.text_input('Enter invoice number [XXX-XX-XXXX format]:')

    # For 'enter value' warning
    # if not invoiceId:
    #     st.warning("Please enter a value.")

    product = st.text_input('Enter the product name:')
    city_list = ['Chennai', 'Bangalore', 'Gurugram']
    city = st.selectbox('Select a city:', city_list)
    category_list = ['Food and beverages', 'Health and beauty', 'Sports and travel', 'Fashion accessories', 'Electronic accessories', 'Home and lifestyle']
    category = st.selectbox('Selected Category:', category_list)
    unit_price = st.number_input('Enter the unit price of each product: ', min_value=0.0, step = 0.1)
    quantity = st.number_input('Enter the quantity of products:', min_value=0, max_value=20, step = 1)

    cogs = unit_price * quantity
    st.write('Cost of goods: ',cogs)
    return invoiceId, product, city, category, unit_price, quantity, cogs

# st.text_input('')
invoiceId, product, city, category, unit_price, quantity, cogs = accept_values()

if st.button('Submit'):
    insert_query = "INSERT INTO dbo.current_data(Invoice_ID,Product,City,Category,Unit_price,Quantity,cogs) VALUES (?,?,?,?,?,?,?);"
    values = (invoiceId, product, city, category, unit_price, quantity, cogs)

    cursor = conn.cursor()
    cursor.execute(insert_query, values)
    conn.commit()
    st.write("Product details updated")

    cursor.close()
    conn.close()
