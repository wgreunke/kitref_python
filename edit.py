import streamlit as st
from supabase import create_client, Client
url: str = st.secrets["connections"]["supabase"]["url"]
key: str = st.secrets["connections"]["supabase"]["key"]
supabase: Client = create_client(url, key)

#When you are ready to turn this into react!
#https://adevait.com/react/building-crud-app-with-react-js-supabase

#Dummy link to test editing a part

page_action=""
test_card_url="/?page_action=edit_card&card_id=Milwaukee_123"
blank_url="http://localhost:8501/"
st.write(f"[Load test card]({test_card_url})")
st.write(f"[Show blank page]({blank_url})")

#Declare varibles used to hold values for edit.
old_title=""
old_card_body =""
old_main_url = ""
old_card_type = ""
old_card_family = ""
#MFG and model number are fixed for life of card. May have to revist this later.



#Grab the query parameters
#check if query params is empty
if st.query_params.get("page_action") is None:
    st.write("No paramaters")
else:
    if st.query_params["page_action"]=="edit_card":
        page_action="edit_card"
        card_id=st.query_params["card_id"]
        st.write("Lets edit a card!")
        st.write(st.query_params["card_id"])
        #Load the values so they can be passed to the card.
        



st.title("KitRef Card Editor")
st.write("Please share your accessory or organization tips on Kitref.")

#Here are the fields for a card
#"card_id":"Milwaukee_48-22-8302"
#"created_at":"2025-03-04T20:42:10.042099+00:00"
#"card_title":"PACKOUT Compact Low-Profile Organizer"
#"main_url":"https://www.milwaukeetool.com/Products/48-22-8302"
#"model_number":"48-22-8302"
#"card_body":"Compact Low-Profile Organizer"
#"mfg":"Milwaukee"
#"card_type":"Product"
#"main_card_image":NULL
#"mfg_price":NULL
#"card_family":"Milwaukee Packout"
# "product_status":NULL
#"active_card":true
#"source":NULL


def make_card_id(mfg, model_number):
    return f"{mfg}_{model_number}"


#For the edit card action, grab the values for the existing card
if page_action=="edit_card":

    existing_card_response = (
        supabase.table("cards")
        .select("*")
        .eq("card_id", card_id)
        .execute()
    )
    #Show the first card
    st.write(existing_card_response.data[0])
    old_card=existing_card_response.data[0]
    old_title=old_card["card_title"]
    old_card_body =old_card["card_body"]
    old_main_url = old_card["main_url"]
    old_card_type = old_card["card_type"]
    old_card_family = old_card["card_family"]
    #Set the default values for the form





source="test"

#now create some fields to add a new card
with st.form("card_form"):
    mfg = st.text_input("Card Manufacturer - Enter Reddit if you are sharing a Reddit post")
    model_number = st.text_input("Model Number - For Reddit posts enter the number after /comments/ in the URL")
    st.write("Example use 1jc5wbs for https://www.reddit.com/r/Packout/comments/1jc5wb3/")


    card_title = st.text_input("Title",old_title)
    card_body = st.text_input("Description", old_card_body)
    main_url = st.text_input("Link to product page or post",old_main_url)
    card_type = st.selectbox("Type", [old_card_type,"Product", "Accessory", "Organization"])
    card_family = st.selectbox("Family", [old_card_family,"Milwaukee Packout", "M12", "M18"])
    card_button=st.form_submit_button("Add Card")

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





#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase
