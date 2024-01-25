import streamlit as st
from streamlit_extras.stateful_button import button 

import firebase_admin
from firebase_admin import credentials, db

import json

DB_URL = st.secrets["DB_URL"]
LOGO_PATH = "logo.jpeg"

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

st.set_page_config(page_title="Genme", page_icon=LOGO_PATH, layout="centered", initial_sidebar_state="expanded")

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
def privacy_policy():
    st.title("Privacy Policy")
    st.write("""Genme (Semika Technology) cares about your privacy with utmost attention.
            Here, we talk about when, how and why do we collect user information. This includes personal as well as behavioral information. We also talk about how we use such information and the scenarios where we may disclose such information to others.
            1. Profile Details
            On Genme (Semika Technology).in, one can signup via email address, mobile number. During signup, user creates a unique password. Each user also fills personal details like official name, mobile number, email address, drug license number, GST number, shop address, preferences. Currently, nothing can be publicly viewed by others on Genme (Semika Technology).in or open internet.  We may email our users from time to time depending on the usage patterns and to send you updates. We don’t believe in sharing or selling database with any 3rd party organization. You define who we are and we care the most about your privacy.
            2. Information Collection Practices
            2.1. Types of Information Collected
            (a) Traffic Data: We automatically track and collect the following categories of information when you visit our Site: (1) IP addresses; (2) domain servers; and (3) types of web browsers used to access the Site (collectively “Traffic Data”). Traffic Data is anonymous information that does not personally identify you but is helpful for marketing purposes or for improving your experience on the Site.
            (b) Personal Information: In order for you to access our Services, including paid features that we offer via the Site, we require you to provide us with certain information that personally identifies you (“Personal Information”). Personal Information includes the following categories of information: (1) Contact Data (such as your name and e-mail address); (2) Financial Data (such as your credit card details); and (3) for Genme (Semika Technology) account registration using your social networking accounts, your social media account log-in information. If you communicate with us by e-mail, post messages to our blog, or otherwise communicate to use via social media, any information provided in such communication may be collected as Personal Information.
            When you use or register for our Service or otherwise interact with us, we may collect the following information from our users that may, in certain circumstances, constitute personal data:
            Username;
            Password;
            E-mail address;
            Address;
            Phone number;
            Name;
            Drug License No.;
            GST No.;
            Social media account log-in info, where applicable;
            Billing and payment information;
            Product and order information (optional information);
            Client contacts and feedback (optional information);
            Information concerning the use of the Service;
            Information necessary for communications;
            Permits and consents; and
            Other data obtained under the user's consent.
            (c) Cookies: Cookies are pieces of text that may be sent to and saved by your browser when you access our Site; your web browser stores these cookies in a way associated with each website you visit, and you can see your cookies through your browser settings. We use cookies to enable our servers to recognize your web browser and tell us how and when you use our Services. Our cookies do not, by themselves, contain information that personally identifies you, and we don’t combine the general information collected through cookies with other such information to tell us who you are. However, we do use cookies to identify that you have logged in and that your web browser has accessed aspects of the Services, and that we may associate that information the account you may have created for your use of the Services. This information, in turn, is something used to personalize your experience with the Services. Most web browsers have an option for turning off the cookie feature, which will prevent your browser from accepting new cookies, as well as (depending on the sophistication of your web browser software) allowing you to decide on acceptance of each new cookie in a variety of ways. Genme (Semika Technology) does not collect personally identifiable browsing information from users that exercise the “Do Not Track option on their browser(s). Please note that this Privacy Policy applies to our use of cookies only, and does not cover the use of cookies by third parties.
            (d) Information Retention Policy: Personal Information will only be retained by company for as long as necessary to provide you with Services. Company’s billing options for non-free plans provide for periodic billing, and Company may retain your Financial Data for that purpose.
            3. Our Use of Your Information
            Any of the personal information we collect from you may be used in one of the following ways:
            To process transactions - (your information, whether public or private, will not be sold, exchanged, transferred, or given to any other company for any reason whatsoever, without your consent, other than for the express purpose of delivering the services requested)
            To improve our website - (we continually strive to improve our website offerings based on the information and feedback we receive from you)
            To improve customer service - (your information helps us to more effectively respond to your customer service requests and support needs)
            To send periodic newsletters or other promotional emails may be sent to you from us. Users have the option to unsubscribe from the newsletter at any time and at their sole discretion.
            Your personal information will not be used for any other purpose without your consent.
            4. Our Disclosure of Your Information
            We do not buy/sell, trade, or otherwise transfer to outside parties your personal information. This does not include trusted third parties who assist us in operating our website, conducting our business, or servicing you, so long as those parties agree to keep this information confidential.
            We may also release your personal information when we believe the release is appropriate to comply with the law, enforce our site policies, or protect ours or others rights, property, or safety. However, non-personally identifiable visitor information or information that has been rendered anonymous may be provided to other parties for marketing, advertising, or other uses.
            5. Payment and accounts information
            Genme (Semika Technology) uses third party as our payment service provider of choice to process all payments. As a result, Genme (Semika Technology) is not responsible for the security of your related banking details. Genme (Semika Technology) does not retain any user banking information on any of our servers.
            6. Updates and Changes to Policy
            We encourage you to review this Privacy Policy regularly for any changes. If we materially change the ways in which we use and disclose personal data, we will update the Effective Date at the top of this page, and send a notification email to our registered users. Your continued use of the Service following any changes to this Privacy Policy constitutes your acceptance of any such changes.
            """)

#--------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    initialize_firebase()
    loc_details = get_location_details()

    st.sidebar.image(LOGO_PATH)
    st.sidebar.title("Welcome to Genme")
    
    st.sidebar.subheader("Register with us as a Partner:")
    option = st.sidebar.radio("Select:", ("Retailer", "Hospital", "Pharmacist", "Privacy Policy"))

    # Perform actions based on user selection
    if option == "Retailer":
        retailer_form(loc_details)
    elif option == "Hospital":
        hospital_form(loc_details)
    elif option == "Pharmacist":
        pharmacist_form(loc_details)
    elif option == "Privacy Policy":
        
