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



st.title("KitRef Card Editor")
st.write("Please share your accessory or organization tip on Kitref.")

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

    #Set the default values for the form



source="test"

#now create some fields to add a new card
mfg = st.text_input("Card Manufacturer - Enter Reddit if you are sharing a Reddit post")

model_number = st.text_input("Model Number - For Reddit posts enter the number after /comments/ in the URL")
st.write("Example use 1jc5wbs for https://www.reddit.com/r/Packout/comments/1jc5wb3/")


card_title = st.text_input("Title")
card_body = st.text_input("Description")
main_url = st.text_input("Link to product page or post")
card_type = st.selectbox("Type", ["Product", "Accessory", "Organization"])
card_family = st.selectbox("Family", ["Milwaukee Packout", "M12", "M18"])

button_add_card = st.button("Add Card")

if button_add_card:
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


#Supabase https://docs.streamlit.io/develop/tutorials/databases/supabase
