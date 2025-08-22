import streamlit as st
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
/* Global */
body { 
    font-family: 'Arial', sans-serif; 
    background: linear-gradient(135deg, #111111, #222222); 
    margin:0; 
    padding:0; 
}

/* Header */
.header-container {
    background: linear-gradient(90deg, #800000, #ffffff);
    padding: 15px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    display: flex;
    justify-content: space-between; 
    align-items: center;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}
.header-title h1 { 
    margin: 0; 
    color: black; 
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}
.nav-buttons {
    display: flex;
    gap: 10px;
}
.nav-buttons button {
    background: #800000;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.nav-buttons button:hover {
    background: #a00000;
}

/* Gallery */
.img-card {
    background: maroon;
    border-radius: 12px;
    padding: 10px;
    height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.img-card:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.img-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 10px;
}

/* Modal */
.modal {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
    text-align: center;
}
.modal img {
    border-radius: 12px;
    max-width: 100%;
    height: auto;
}

/* Search bar */
.stTextInput input {
    border: 2px solid #800000;
    border-radius: 12px;
    padding: 10px 40px 10px 12px;
    font-size: 16px;
    width: 100%;
    background-image: url("https://img.icons8.com/ios-filled/24/search.png");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 18px;
}

/* Buttons */
.stButton button {
    background: black;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton button:hover {
    background: #a00000;
}

/* Contact form */
.contact-form {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    max-width: 500px;
    margin: auto;
}

/* Section headers */
h2 { 
    color: #800000; 
    font-size: 1.8em; 
    margin-top: 15px; 
    margin-bottom: 10px; 
    border-bottom: 2px solid #800000; 
    padding-bottom: 5px; 
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    font-size: 14px;
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = []
if "page_num" not in st.session_state:
    st.session_state.page_num = 0
if "view_image" not in st.session_state:
    st.session_state.view_image = None

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="header-container">
        <div class="header-left">
            <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" width="80">
            <div class="header-title"><h1>LUCAS GREY SCRAP TRADING</h1></div>
        </div>
        <div class="nav-buttons">
            <button onclick="window.location.href='?page=About'">About</button>
            <button onclick="window.location.href='?page=Contact'">Contact Us</button>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ NAVIGATION HANDLING ------------------
# Map query params to session state
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"][0]

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    st.subheader("Welcome to Lucas Grey Scrap Trading")
    st.write("This is the Home page with gallery and search (kept same as before).")

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.write("""
        Lucas Grey Scrap Trading provides sustainable scrap trading services.
        We recycle metals such as copper, aluminum, and steel for small-scale and industrial clients.
        
        **Services Offered:**
        - Scrap metal collection
        - Sorting and processing
        - Wholesale and retail supply
        - Partnerships for industrial recycling
    """)
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    with st.form(key="contact_form"):
        name = st.text_input("Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        message = st.text_area("Message", placeholder="Your inquiry or message")
        submit_button = st.form_submit_button("Send Message")
        if submit_button:
            if name and email and message:
                st.success(f"Thank you, {name}! Your message has been received. We'll get back to you at {email}.")
            else:
                st.error("Please fill out all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        📧 Email: **charlottevazquez78@gmail.com**  
        📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  
    """)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
    © 2025 Lucas Grey Scrap Trading. All rights reserved.
</div>
""", unsafe_allow_html=True)
