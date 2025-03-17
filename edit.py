
import streamlit as st
#from st_supabase_connection import SupabaseConnection

st.title("Edit Card")

# Initialize connection.

# Initialize connection
""""
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

conn = st.connection("supabase",type=SupabaseConnection)
st.title("Edit Card")

# Query data
rows = conn.query("cards").select("*").execute()
for row in rows:
    st.write(row["card_id"], row["card_title"])
    


#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase


#Start by showing a list of existing cards

#pull secrets from .env
import os
from dotenv import load_dotenv

load_dotenv()
"""