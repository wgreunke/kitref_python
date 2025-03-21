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
st.write(f"[Show blank page]({blank_url})")

# Initialize default values
old_title = ""
old_card_body = ""
old_main_url = ""
old_card_type = ""
old_card_family = ""
source="test"
#MFG and model number are fixed for life of card. May have to revist this later.

# Check query parameters first
if st.query_params.get("page_action") is not None:
    if st.query_params["page_action"] == "edit_card":
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
            old_title = old_card["card_title"]
            old_card_body = old_card["card_body"]
            old_main_url = old_card["main_url"]
            old_card_type = old_card["card_type"]
            old_card_family = old_card["card_family"]

# Now create the form with the loaded values
with st.form("card_form"):
    mfg = st.text_input("Card Manufacturer", value=old_card.get("mfg", ""))
    model_number = st.text_input("Model Number", value=old_card.get("model_number", ""))
    card_title = st.text_input("Title", value=old_title)
    card_body = st.text_input("Description", value=old_card_body)
    main_url = st.text_input("Link to product page or post", value=old_main_url)
    card_type = st.selectbox("Type", ["Product", "Accessory", "Organization"], index=0 if not old_card_type else ["Product", "Accessory", "Organization"].index(old_card_type))
    card_family = st.selectbox("Family", ["Packout", "M12", "M18"], index=0 if not old_card_family else ["Packout", "M12", "M18"].index(old_card_family))
    card_button=st.form_submit_button("Submit")

#Handle the submit button

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
            "source": source
        }).execute()

        st.success("Card added successfully")
    #After the card is added, show the card
        st.write(card_id)
    #Show the card in the table
#    st.write(supabase.table("cards").select("*").eq("card_id", card_id).execute().data[0])
    #Add a link to the card
        new_card_url = f"https://www.kitref.com/products/{card_id}"
        st.write(f"[View Card]({new_card_url})")
    elif page_action=="edit_card":
        supabase.table("cards").update({
            "card_title": card_title,
            "card_body": card_body,
            "main_url": main_url,
            "model_number": model_number,
            "mfg": mfg,
            "card_type": card_type,
            "card_family": card_family,
            "source": source
        }).eq("card_id", card_id).execute()

        st.success("Card updated successfully")
        # Add a link to the updated card
        card_url = f"https://www.kitref.com/products/{card_id}"
        st.write(f"[View Updated Card]({card_url})")





#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase

def make_card_id(mfg, model_number):
    return f"{mfg}_{model_number}"

source="test"
