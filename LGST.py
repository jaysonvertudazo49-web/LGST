import streamlit as st

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ==============================
# Custom Header with Logo
# ==============================
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                background-color: #800000; padding: 15px; border-radius: 8px;">
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

# ==============================
# Section 1: Current Project
# ==============================
st.header("Current Project")

# Assume we have images: pic1.jpg, pic2.jpg, ..., picN.jpg
# Let's define the number of images manually for now (update when more are added)
max_images = 5  # change this when more images are uploaded
image_urls = [
    f"https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/refs/heads/main/pic{i}.jpg"
    for i in range(1, max_images + 1)
]

# Arrow selector
selected_index = st.slider("Select an image", 1, max_images, 1)

# Display selected image
col1, col2 = st.columns([2, 1])  # image on left, placeholder text on right
with col1:
    st.image(image_urls[selected_index - 1], use_container_width=True, caption=f"Image {selected_index}")

with col2:
    st.subheader("Project Details")
    st.write("📝 Placeholder text for the selected image.")
    st.write("You can add descriptions or notes for each project image here.")

# ==============================
# Section 2: About
# ==============================
st.header("About")
st.write(
    """
    This website is a basic example to help you get started.  
    Lucas Grey Scrap Trading is dedicated to providing excellent scrap trading services.
    """
)

# ==============================
# Section 3: Contact
# ==============================
st.header("Contact")
st.write("Email me at: [your.email@example.com](mailto:your.email@example.com)")
