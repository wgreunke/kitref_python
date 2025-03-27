import streamlit as st
from supabase import create_client, Client
url: str = st.secrets["connections"]["supabase"]["url"]
key: str = st.secrets["connections"]["supabase"]["key"]
supabase: Client = create_client(url, key)


st.title("Associate")
test_card_url="/?page_action=edit_card&card_id=Milwaukee_123"
blank_url="http://localhost:8501/"

page_action = ""
parent_card_id = ""

if st.query_params.get("page_action") is None:
    page_action = "show_card_list" #This is the first time you come to page.

    #Show the list of cards
    #Grab the parent card from the url.
    parent_card_id = st.query_params["card_id"]
    st.write(f"Parent card: {parent_card_id}")

    cards_list = (
            supabase.table("cards")
            .select("*")
            .eq("card_id", parent_card_id)
            .execute()
        )

    #Print the list of cards.
    for row in cards_list.data:
        card_id = row['card_id']
        link = f"?page_action=add_child_card&card_id={card_id}"
        st.markdown(f"[{card_id}]({link})")



elif st.query_params["page_action"] == "add_child_card":
    page_action = "add_child_card"
    parent_card_id = st.query_params["card_id"]

    kitref_url = f"https://www.kitref.com/products/{parent_card_id}"
    st.markdown(f"[products/{parent_card_id}]({kitref_url})")
    
    # Automatically redirect to Kitref
    #st.markdown(f'<meta http-equiv="refresh" content="0;url={kitref_url}">', unsafe_allow_html=True)
    
    kitref_url = f"https://www.kitref.com/products/{parent_card_id}"
    st.markdown(f"[products/{parent_card_id}]({kitref_url})")
    
 









