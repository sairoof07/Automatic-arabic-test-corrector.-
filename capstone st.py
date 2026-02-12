import streamlit as st 
from PIL import Image
import pytesseract
import numpy as np
import google.generativeai as genai
import pandas as pd 
import io
dff = pd.DataFrame()
st.title('automatic test corrector')

textbook = pd.DataFrame()
textbook = st.file_uploader('add a textbook (optional)')
answer_key = pd.DataFrame()
answer_key = st.file_uploader('answer key (optional)')
test = st.file_uploader('add your test here (image)')
#test_name = str(test.name)

if st.button('submit'):
    
    st.write(test.name)
    
    image = Image.open(test)
    
    st.image(test)
    
    genai.configure(api_key="KEY visit https://aistudio.google.com/app/api-keys to get yours")
    model = genai.GenerativeModel('gemini-2.5-flash')
    book_file = genai.upload_file(path="ثاني اعدادي 1.pdf", display_name="Textbook")
    
    
    
    
   # chat = model.start_chat(history=[
   #     {"role": "user", "parts": [textbook, answer_key ,"You are a grader for this written test based on this textbook if uploaded."]}
   # ])
   # 
    
    
    prompt = """
    Act as an academic grader. Analyze the provided image/file against the textbook context. Correct the student's work and provide the results strictly as a Markdown table.
    
    Rules:
    
    Use the textbook to determine the correct answers.
    
    Assign a score for each question based on the marks shown or total points.
    
    Return exactly one Markdown table with these columns: [ID, name, Q1, Q2, ..., Qn, final_score].
    
    Leave ID empty if not found.
    
    Do not include any conversational text, explanations, or code blocks—only the table.
    
    """
    
    response = model.generate_content([prompt, image])
    
    
    data = io.StringIO(response.text)
    df = pd.read_table(data, sep="|", header=0, skipinitialspace=True).dropna(axis=1, how='all')


    df.columns = df.columns.str.strip()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    dff = pd.concat([dff, df])
    st.write(dff)
    
