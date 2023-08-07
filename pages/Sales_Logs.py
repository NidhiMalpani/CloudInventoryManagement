import streamlit as st
import pyodbc

# Azure SQL Database connection parameters
server = 'pilventory-server.database.windows.net'
database = 'pilventory-db'
username = 'pilventory'
password = 'Team@57san'
driver = '{SQL Server}' 

conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_string)

st.title('Sales Logs.')
st.write('')

invoiceId = st.text_input('Enter invoice number of the product sold [XXX-XX-XXXX format]:')

if st.button('Submit'):
    delete_query = f"Delete from dbo.current_data where Invoice_ID = \'"+invoiceId+"\';"
    
    cursor = conn.cursor()
    cursor.execute(delete_query)
    conn.commit()
    st.write("Product details updated")

    cursor.close()
    conn.close()