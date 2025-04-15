import streamlit as st

st.title("Add a child card")

source = st.selectbox("What website are you linking to?", ["Amazon", "Etsy","Reddit", "YouTube","Other"])

if source == "Reddit":
    url = st.text_area("Enter the Reddit Embed code",height=175)
   

    st.title("Instructions for Reddit:")
    st.write("1. Go to the post you want to link to.")
    st.write("2. Click Share below the post then Embed")
    st.write("3. Click Copy Code")
    st.write("4. Paste the Embed code in the box above.")








