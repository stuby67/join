from dotenv import load_dotenv 
load_dotenv() ## load all the environemnt variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

prompt = ["""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name SALES and has the following tables and columns:
    
    Tables:
    - customers: customer_id, customer_name, customer_email
    - products: product_id, product_name, product_price
    - sales: sale_id, customer_id, product_id, sale_date, quantity
    
    Example 1: How many sales records are there?
    The SQL command will be something like this: SELECT COUNT(*) FROM sales;
    
    Example 2: Show all sales records for the 'Laptop' product?
    The SQL command will be something like this: SELECT * FROM sales JOIN products ON sales.product_id = products.product_id WHERE product_name = "Laptop";
    
    Example 3: List the sale_id and quantity for orders placed in June 2024?
    The SQL command will be something like this: SELECT sale_id, quantity FROM sales WHERE sale_date LIKE '2024-06%';
    
    Example 4: What is the total quantity sold for the 'Smartphone' product?
    The SQL command will be something like this: SELECT SUM(quantity) FROM sales JOIN products ON sales.product_id = products.product_id WHERE product_name = "Smartphone";
    
    Also, the SQL code should not have '''
    in the beginning or end and should not contain the word SQL in the output.
"""]



st.set_page_config(page_title="Retrieve SQL Queries")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:")
    st.code(response)

    if "SELECT" in response.upper():  # Checking if the response contains SELECT statement
        try:
            data = read_sql_query(response, "sales.db")
            st.subheader("Result:")
            for row in data:
                st.write(row)
        except Exception as e:
            st.error(f"An error occurred: {e}")
