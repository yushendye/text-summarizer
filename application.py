import streamlit as st
from utils import *

text = None
st.title('Text Summarizer')
text = st.text_area('Enter your text')  

if st.button('Summarize'):
    gen_sum = generate_summary(input_text=text, top_n = 3)
    text = ' '
    for item in gen_sum:
        text += item
        text += '.'
    st.write(text)