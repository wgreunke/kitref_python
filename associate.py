import streamlit as st
from supabase import create_client, Client
url: str = st.secrets["connections"]["supabase"]["url"]
key: str = st.secrets["connections"]["supabase"]["key"]
supabase: Client = create_client(url, key)


st.title("Associate")

st.markdown(f"[blank page](/)")
page_action = ""
parent_card_id = ""

#For testing purposes, the bare url will not have a card_id.
if st.query_params.get("parent_card_id") is None:
    #Show a link to the test card.
    test_card_url = "/?page_action=show_card_list&parent_card_id=Milwaukee_123"
    st.markdown(f"[Test card]({test_card_url})")



elif st.query_params.get("page_action") == "show_card_list":
    page_action = "show_card_list" #This is the first time you come to page.

    #Show the list of cards
    #Grab the parent card from the url.
    parent_card_id = st.query_params["parent_card_id"]
    st.write(f"Parent card: {parent_card_id}")

    #List all the cards for now, need to see how to 
    cards_list = (
            supabase.table("cards")
            .select("*")

            .execute()
        )

    #Print the list of cards.
    st.write(cards_list)
    for row in cards_list.data:
        card_id = row['card_id']
        card_title = row['card_title']
        link = f"/?page_action=add_child_card&card_id={card_id}"
        st.markdown(f"[{card_id} - {card_title}]({link})")



elif st.query_params["page_action"] == "add_child_card":
    page_action = "add_child_card"
    parent_card_id = st.query_params["card_id"]

    kitref_url = f"https://www.kitref.com/products/{parent_card_id}"
    st.markdown(f"[products/{parent_card_id}]({kitref_url})")
    
    # Automatically redirect to Kitref
    #st.markdown(f'<meta http-equiv="refresh" content="0;url={kitref_url}">', unsafe_allow_html=True)
    
    kitref_url = f"https://www.kitref.com/products/{parent_card_id}"
    st.markdown(f"[products/{parent_card_id}]({kitref_url})")
    
 









