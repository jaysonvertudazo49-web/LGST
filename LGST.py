import streamlit as st

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# Custom Header with Logo
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                background-color: red; padding: 15px; border-radius: 8px;">
        <h1 style="color: white; text-align: center; flex: 1; margin: 0;">
            LUCAS GREY SCRAP TRADING
        </h1>
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/refs/heads/main/LOGO1.png" 
             alt="Logo" style="height: 60px; margin-left: 20px;">
    </div>
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
