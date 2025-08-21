# ------------------ ABOUT SECTION ------------------
st.header("About")
st.write(
    """
    DETAILS HINGI AKO HAHAHA
    """
)

# ------------------ FOOTER WITH CONTACT SECTION ------------------
st.markdown(
    """
    <style>
    .footer {
        background: linear-gradient(90deg, #800000, #a00000);
        color: white;
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-radius: 12px 12px 0 0;
    }
    .footer h2 {
        color: white;
        margin-bottom: 10px;
    }
    .footer p {
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="footer"><h2>Contact Us</h2>', unsafe_allow_html=True)

with st.form(key="contact_form"):
    name = st.text_input("Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    message = st.text_area("Message", placeholder="Your inquiry or message")
    submit_button = st.form_submit_button("Send Message")
    if submit_button:
        if name and email and message:
            st.success(f"Thank you, {name}! Your message has been received. We'll get back to you at {email} soon.")
        else:
            st.error("Please fill out all fields.")

st.markdown(
    """
    <p>📧 Email: placeholder@gmail.com</p>
    <p>📍 Address: Your Office Address Here</p>
    <p>&copy; 2025 Lucas Grey Scrap Trading. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
