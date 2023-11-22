import streamlit as st
from streamlit_extras.stateful_button import button 

import firebase_admin
from firebase_admin import credentials, db

import json

DB_URL = st.secrets["DB_URL"]

FIREBASE_JSON = {
    "type":st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"],
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_X509_CERT_URL"],
    "universe_domain": st.secrets["FIREBASE_UNIVERSE_DOMAIN"]
}

st.set_page_config(page_title="Genme", page_icon="Genme Original Img.png", layout="centered", initial_sidebar_state="expanded")

# Initialize Firebase Admin SDK
@st.cache_resource
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_JSON)
        firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
        
@st.cache_resource
def get_location_details():
    with open("pincode_db.json", "r") as f:
        location_details = json.load(f)
    return location_details


aov_monthly_ranges = ["0-1 lakhs", "1-5 lakhs", "5-15 lakhs", "15-30 lakhs", "30-50 lakhs", "50 lakhs - 1 Cr", "1+ Cr"]

#--------------------------------------------------------------------------------------------------------------------
def store_details(form_type, details):
    try:
        ref = db.reference(f'/forms/{form_type}')
        new_form = ref.push({"details": details})
    except:
        print("DB error")

#--------------------------------------------------------------------------------------------------------------------
def retailer_form(loc_details):
    st.title("Retailer Registration Form")

    name_val = st.text_input("Full name:")
    
    col1, col2 = st.columns((1,1))
    with col1:
        phone_val = st.number_input("Phone number (+91):", min_value=1000000000, max_value=9999999999, value=1111111111, step=1)
    with col2:
        email_val = st.text_input("Email Address:")

    address_val = st.text_input("Address:")

    col1, col2 = st.columns((5,1))
    with col1:
        state_val = st.selectbox(label="State (India):", options=loc_details.keys())
        
    with col2:
        submit_state = button("Submit State", key="Submit State")
    
    if submit_state:
        col1, col2 = st.columns((5,1))
        with col1:
            district_val = st.selectbox(label="District:", options=loc_details[state_val].keys())
        with col2:
            submit_district = button("Submit District", key="Submit District")
    
        if submit_district:
            col1, col2 = st.columns((5,1))
            with col1:
                pincode_val = st.selectbox(label="Pincode:", options=loc_details[state_val][district_val].keys())
            with col2:
                submit_pincode = button("Submit Pincode", key="Submit Pincode")
            
            if submit_pincode:
                col1, col2 = st.columns((5,1))
                with col1:
                    area_val = st.selectbox(label="Area:", options=loc_details[state_val][district_val][pincode_val])
                with col2:
                    submit_area = button("Submit Area", key="Submit Area")
                
                if submit_area:
                    drug_license_number_val = st.text_input("Drug License Number:")
                    
                    avg_order_value_monthly_val = st.selectbox("Average Monthly Order Value (INR):", aov_monthly_ranges)
                    
                    submitted = st.button("Submit Form")
                    if submitted:
                        if name_val and phone_val and email_val and address_val and state_val and pincode_val and drug_license_number_val and avg_order_value_monthly_val:
                            try:
                                form_type = "retailer"
                                
                                details = {
                                    "name": name_val,
                                    "phone": phone_val,
                                    "email": email_val,
                                    "address": address_val,
                                    "state": state_val,
                                    "pincode": pincode_val,
                                    "drug_license_number": drug_license_number_val,
                                    "avg_order_value_monthly": avg_order_value_monthly_val
                                }
                                
                                store_details(form_type, details)
                                
                                st.success("Form Submitted Sucessfully")
                            except:
                                st.error("Error in Submitting the Form")
                        else:
                            st.error("All fields are mandatory. Please fill them.")


#--------------------------------------------------------------------------------------------------------------------
def hospital_form(loc_details):
    st.title("Hospital Registration Form")
    
    name_val = st.text_input("Full name:")
    
    col1, col2 = st.columns((1,1))
    with col1:
        phone_val = st.number_input("Phone number (+91):", min_value=1000000000, max_value=9999999999, value=1111111111, step=1)
    with col2:
        email_val = st.text_input("Email Address:")

    address_val = st.text_input("Address:")

    col1, col2 = st.columns((5,1))
    with col1:
        state_val = st.selectbox(label="State (India):", options=loc_details.keys())
        
    with col2:
        submit_state = button("Submit State", key="Submit State")
    
    if submit_state:
        col1, col2 = st.columns((5,1))
        with col1:
            district_val = st.selectbox(label="District:", options=loc_details[state_val].keys())
        with col2:
            submit_district = button("Submit District", key="Submit District")
    
        if submit_district:
            col1, col2 = st.columns((5,1))
            with col1:
                pincode_val = st.selectbox(label="Pincode:", options=loc_details[state_val][district_val].keys())
            with col2:
                submit_pincode = button("Submit Pincode", key="Submit Pincode")
            
            if submit_pincode:
                col1, col2 = st.columns((5,1))
                with col1:
                    area_val = st.selectbox(label="Area:", options=loc_details[state_val][district_val][pincode_val])
                with col2:
                    submit_area = button("Submit Area", key="Submit Area")
                
                if submit_area:
                    drug_license_number_val = st.text_input("Drug License Number:")
                    
                    operating_under_pharmacist_name_val = st.text_input("Operating Under Pharmacist name:")
                    
                    avg_order_value_monthly_val = st.selectbox("Average Monthly Order Value (INR):", aov_monthly_ranges)
                    
                    submitted = st.button("Submit Form")
                    if submitted:
                        if name_val and phone_val and email_val and address_val and state_val and pincode_val and drug_license_number_val and avg_order_value_monthly_val:
                            try:
                                form_type = "hospital"
                                
                                details = {
                                    "name": name_val,
                                    "phone": phone_val,
                                    "email": email_val,
                                    "address": address_val,
                                    "state": state_val,
                                    "pincode": pincode_val,
                                    "drug_license_number": drug_license_number_val,
                                    "operating_under_pharmacist_name": operating_under_pharmacist_name_val,
                                    "avg_order_value_monthly": avg_order_value_monthly_val
                                }
                                
                                store_details(form_type, details)
                                
                                st.success("Form Submitted Sucessfully")
                            except:
                                st.error("Error in Submitting the Form")
                        else:
                            st.error("All fields are mandatory. Please fill them.")

#--------------------------------------------------------------------------------------------------------------------
def pharmacist_form(loc_details):
    st.title("Pharmacist Registration Form")

    name_val = st.text_input("Full name:")
    
    col1, col2 = st.columns((1,1))
    with col1:
        phone_val = st.number_input("Phone number (+91):", min_value=1000000000, max_value=9999999999, value=1111111111, step=1)
    with col2:
        email_val = st.text_input("Email Address:")

    address_val = st.text_input("Address:")

    col1, col2 = st.columns((5,1))
    with col1:
        state_val = st.selectbox(label="State (India):", options=loc_details.keys())
        
    with col2:
        submit_state = button("Submit State", key="Submit State")
    
    if submit_state:
        col1, col2 = st.columns((5,1))
        with col1:
            district_val = st.selectbox(label="District:", options=loc_details[state_val].keys())
        with col2:
            submit_district = button("Submit District", key="Submit District")
    
        if submit_district:
            col1, col2 = st.columns((5,1))
            with col1:
                pincode_val = st.selectbox(label="Pincode:", options=loc_details[state_val][district_val].keys())
            with col2:
                submit_pincode = button("Submit Pincode", key="Submit Pincode")
            
            if submit_pincode:
                col1, col2 = st.columns((5,1))
                with col1:
                    area_val = st.selectbox(label="Area:", options=loc_details[state_val][district_val][pincode_val])
                with col2:
                    submit_area = button("Submit Area", key="Submit Area")
                
                if submit_area:
                    drug_license_number_val = st.text_input("Drug License Number:")
                    
                    avg_order_value_monthly_val = st.selectbox("Average Monthly Order Value (INR):", aov_monthly_ranges)
                    
                    submitted = st.button("Submit Form")
                    if submitted:
                        if name_val and phone_val and email_val and address_val and state_val and pincode_val and drug_license_number_val and avg_order_value_monthly_val:
                            try:
                                form_type = "retailer"
                                
                                details = {
                                    "name": name_val,
                                    "phone": phone_val,
                                    "email": email_val,
                                    "address": address_val,
                                    "state": state_val,
                                    "pincode": pincode_val,
                                    "drug_license_number": drug_license_number_val,
                                    "avg_order_value_monthly": avg_order_value_monthly_val
                                }
                                
                                store_details(form_type, details)
                                
                                st.success("Form Submitted Sucessfully")
                            except:
                                st.error("Error in Submitting the Form")
                        else:
                            st.error("All fields are mandatory. Please fill them.")

#--------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    initialize_firebase()
    loc_details = get_location_details()

    st.sidebar.image("Genme-removebg-preview.png")
    st.sidebar.title("Welcome to Genme")
    
    st.sidebar.subheader("Register with us as a Partner:")
    option = st.sidebar.radio("Select:", ("Retailer", "Hospital", "Pharmacist"))

    # Perform actions based on user selection
    if option == "Retailer":
        retailer_form(loc_details)
    elif option == "Hospital":
        hospital_form(loc_details)
    elif option == "Pharmacist":
        pharmacist_form(loc_details)  
