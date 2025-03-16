import streamlit as st  
from st_supabase_connection import st_supabase_connection
#Using Streamit to for card crud operations

st.title("Edit Card")

conn=st.connection("supabase",type=SupabaseConnection)

rows=conn.table("cards").select("*").execute()
for row in rows:
    st.write(row["card_id"], row["card_title"])
    


#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase


#Start by showing a list of existing cards

#pull secrets from .env
import os
from dotenv import load_dotenv

load_dotenv()
