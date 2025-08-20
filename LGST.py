import streamlit as st

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# Header
st.markdown(
    """
    <h1 style='text-align: center; color: #333;'>LUCAS GREY SCRAP TRADING</h1>
    <hr>
    """,
    unsafe_allow_html=True,
)

# Section 1: Current Project
st.header("Current Project")
st.write("🖼️ Images will be uploaded here soon (placeholder).")

# Section 2: About
st.header("About")
st.write(
    """
    This website is a basic example to help you get started.
    Lucas Grey Scrap Trading is dedicated to providing excellent scrap trading services.
    """
)

# Section 3: Contact
st.header("Contact")
st.write("Email me at: [your.email@example.com](mailto:your.email@example.com)")
