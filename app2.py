from dotenv import load_dotenv 
load_dotenv() ## load all the environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve query from the sql database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    cur.execute(sql)
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    
    return rows

prompt = ["""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns NAME, CLASS,
    SECTION \n\nFor example, \nExample 1 How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    
    \nExample 2 Tell me all the students studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT
    where CLASS="Data Science";
    
    Example 3 Tell me all the students name studying in Data Science class?,
    the SQL command will be something like this SELECT Name FROM STUDENT
    where CLASS="Data Science";
    
    also the sql code should not have '''
    in beginning or end and sql word in output
"""]

st.set_page_config(page_title="SQL Query Retriever")
st.title("Gemini App to Retrieve SQL Data")

# Use columns for better layout
input_col, button_col = st.columns([3, 1])

with input_col:
    question = st.text_input("Input your question:", key="input")

with button_col:
    submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:")
    st.code(response, language='sql')

    data = read_sql_query(response, "student.db")

    st.subheader("The Response is")
    if data:
        st.table(data)
    else:
        st.write("No data found.")

# Adding expander for detailed instructions
with st.expander("Instructions and Examples"):
    st.write("""
        You can ask questions about the student database, for example:
        - How many entries of records are present?
        - Tell me all the students studying in Data Science class.
        - Tell me all the students' names studying in Data Science class.
        
        The app will generate the corresponding SQL query and retrieve the data from the database.
    """)

# Adding a footer
st.markdown("""
    <style>
    footer {
        visibility: hidden;
    }
    .footer {
        visibility: visible;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>SQL query Generator</p>
    </div>
""", unsafe_allow_html=True)
