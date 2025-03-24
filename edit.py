import streamlit as st
from supabase import create_client, Client
url: str = st.secrets["connections"]["supabase"]["url"]
key: str = st.secrets["connections"]["supabase"]["key"]
supabase: Client = create_client(url, key)

#When you are ready to turn this into react!
#https://adevait.com/react/building-crud-app-with-react-js-supabase

#Dummy link to test editing a part

page_action = ""
test_card_url="/?page_action=edit_card&card_id=Milwaukee_123"
blank_url="http://localhost:8501/"
st.write(f"[Load test card]({test_card_url})")
st.write(f"[Create new card]({blank_url})")


def make_card_id(mfg, model_number):
    return f"{mfg}_{model_number}"


# Initialize default values
old_title = ""
old_mfg = ""
old_model_number = ""
old_card_body = ""
old_main_url = ""
old_card_type = ""
old_card_family = ""
old_embed_code=""
source=""
#MFG and model number are fixed for life of card. May have to revist this later.

# Check query parameters first
if st.query_params.get("page_action") is None:
    page_action = "new"
elif st.query_params["page_action"] == "edit_card":
    page_action = "edit_card"
    card_id = st.query_params["card_id"]
        
        # Load existing card data immediately after confirming it's an edit
    existing_card_response = (
            supabase.table("cards")
            .select("*")
            .eq("card_id", card_id)
            .execute()
        )
        
    if existing_card_response.data:
            old_card = existing_card_response.data[0]
            old_model_number = old_card["model_number"]
            old_title = old_card["card_title"]
            old_mfg = old_card["mfg"]
            old_card_body = old_card["card_body"]
            old_main_url = old_card["main_url"]
            old_card_type = old_card["card_type"]
            old_card_family = old_card["card_family"]
            old_embed_code=old_card["embed_code"]

# Create form with submit button
with st.form("card_form"):
    #Lock the mfg and model number if you are doing an edit
    if page_action == "new":
        mfg = st.text_input("Card Manufacturer - Enter Reddit if you are sharing a Reddit post", value=old_mfg)
        model_number = st.text_input("Model Number - For Reddit posts enter the number after /comments/ in the URL", value=old_model_number)
        st.markdown("Example use **1jc5wbs** for https://www.reddit.com/r/Packout/comments/1jc5wb3/**")
    else:
        st.markdown("**Manufacturer:** " + old_mfg)
        st.markdown("**Model Number:** " + old_model_number)

    card_title = st.text_input("Title", value=old_title)
    card_body = st.text_input("Description", value=old_card_body)
    main_url = st.text_input("Link to product page or post", value=old_main_url)
    card_type = st.selectbox("Type", [old_card_type,"Product", "Accessory", "Organization"])
    card_family = st.selectbox("Family", [old_card_family,"Packout", "M12", "M18"])
    embed_code=st.text_input("Embedded code",value=old_embed_code)
    source=st.selectBox("What is the source of the link?",["OEM","YouTube","Reddit","Etsy","Amazon","Other"])
    
    # Submit button must be inside the form block
    button_text = "Update Card" if page_action == "edit_card" else "Add Card"
    card_button = st.form_submit_button(button_text)

# Form handling code goes after the form block
if card_button:
    if page_action=="new":
        card_id = make_card_id(mfg, model_number)
    #Send to supabase
        supabase.table("cards").insert({
            "card_id": card_id,
            "card_title": card_title,
            "card_body": card_body,
            "main_url": main_url,
            "model_number": model_number,
            "mfg": mfg,
            "card_type": card_type,
            "card_family": card_family,
            "embed_code":embed_code,
            "source": source
        }).execute()

        st.success("Card added successfully")
    #After the card is added, show the card
        st.write(card_id)
    #Add a link to new the card
        new_card_url = f"https://www.kitref.com/products/{card_id}"
        st.write(f"[View new Card]({new_card_url})")
    elif page_action=="edit_card":
        supabase.table("cards").update({
            "card_title": card_title,
            "card_body": card_body,
            "main_url": main_url,
            "card_type": card_type,
            "card_family": card_family,
            "source": source
        }).eq("card_id", card_id).execute()

        st.success("Card updated successfully")
        # Add a link to the updated card
        card_url = f"https://www.kitref.com/products/{card_id}"
        st.write(f"[View Updated Card]({card_url})")





#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase


