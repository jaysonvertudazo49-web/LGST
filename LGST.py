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

# List of image URLs from GitHub repo
max_images = 10  # adjust as needed
image_urls = [
    f"https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/refs/heads/main/pic{i}.jpg"
    for i in range(1, max_images + 1)
]

# Session state for navigation
if "start_index" not in st.session_state:
    st.session_state.start_index = 0

images_per_page = 3  # how many images to show at once

# Navigation buttons
col_nav1, col_nav2 = st.columns([1, 8])
with col_nav1:
    if st.button("⬅️ Prev") and st.session_state.start_index > 0:
        st.session_state.start_index -= images_per_page
with col_nav2:
    if st.button("Next ➡️") and st.session_state.start_index + images_per_page < len(image_urls):
        st.session_state.start_index += images_per_page

# Show multiple images in a row
cols = st.columns(images_per_page)
selected_image = None
for i, col in enumerate(cols):
    idx = st.session_state.start_index + i
    if idx < len(image_urls):
        if col.button(f"Image {idx+1}", key=f"btn{idx}"):
            selected_image = image_urls[idx]
        col.image(image_urls[idx], use_container_width=True)

# If an image was clicked, show it larger with details
if selected_image:
    st.markdown("---")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.image(selected_image, use_container_width=True)
    with c2:
        st.subheader("Project Details")
        st.write("📝 Placeholder text for this image.")
        st.write("You can replace this with a description of the scrap material or project info.")

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
