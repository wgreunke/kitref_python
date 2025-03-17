import streamlit as st
from supabase import create_client, Client
url: str = st.secrets["connections"]["supabase"]["url"]
key: str = st.secrets["connections"]["supabase"]["key"]
supabase: Client = create_client(url, key)

#load_dotenv()

st.title("Edit Card")



response = (
    supabase.table("cards")
    .select("*")
    .execute()
)

#Show the first card
st.write(response)


#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase
