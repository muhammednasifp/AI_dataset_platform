import streamlit as st


st.title("AI Dataset Platform")

st.header("Dataset Builder")

content = st.text_area(
    "Enter document content",
    height=200
)

st.write("Characters:", len(content))