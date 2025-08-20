import streamlit as st

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ HEADER ------------------
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                background-color: #800000; padding: 15px; border-radius: 8px;">
        <h1 style="color: white; text-align: center; flex: 1; margin: 0;">
            LUCAS GREY SCRAP TRADING
        </h1>
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" 
             alt="Logo" style="height: 60px; margin-left: 20px;">
    </div>
    <hr>
    """,
    unsafe_allow_html=True,
)

# ------------------ IMAGE GALLERY ------------------
st.header("Current Project")

# GitHub image repo
repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
max_images = 10  # adjust this number to however many images you actually have

# Load images dynamically
images = [f"{repo_url}pic{i}.jpg" for i in range(1, max_images + 1)]

# Session state for navigation
if "page" not in st.session_state:
    st.session_state.page = 0

images_per_page = 3
start = st.session_state.page * images_per_page
end = start + images_per_page
current_images = images[start:end]

# Layout for navigation arrows + images
col1, col2, col3 = st.columns([1, 10, 1])

# Left arrow
with col1:
    if st.button("⬅️", use_container_width=True):
        if st.session_state.page > 0:
            st.session_state.page -= 1
        st.rerun()

# Image container grid
with col2:
    img_cols = st.columns(len(current_images))
    for idx, img in enumerate(current_images):
        with img_cols[idx]:
            st.markdown(
                f"""
                <div style="width: 100%; height: 250px; display: flex; justify-content: center; align-items: center;
                            border: 1px solid #ddd; border-radius: 8px; overflow: hidden; margin-bottom: 10px;">
                    <img src="{img}" style="width:100%; height:100%; object-fit:cover; cursor:pointer;"
                         onclick="window.open('{img}', '_blank')">
                </div>
                """,
                unsafe_allow_html=True,
            )

# Right arrow
with col3:
    if st.button("➡️", use_container_width=True):
        if end < len(images):
            st.session_state.page += 1
        st.rerun()

# ------------------ ABOUT SECTION ------------------
st.header("About")
st.write(
    """
    This website is a basic example to help you get started.  
    Lucas Grey Scrap Trading is dedicated to providing excellent scrap trading services.
    """
)

# ------------------ CONTACT SECTION ------------------
st.header("Contact")
st.write("Email me at: [your.email@example.com](mailto:your.email@example.com)")
