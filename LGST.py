import streamlit as st
import requests

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

# Repo base URL
repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
max_images = 15
possible_exts = ["jpg", "jpeg", "png"]

# Determine which images actually exist (using HEAD requests)
images = []
for i in range(1, max_images + 1):
    found = False
    for ext in possible_exts:
        url = f"{repo_url}pic{i}.{ext}"
        try:
            response = requests.head(url)
            if response.status_code == 200:
                images.append(url)
                found = True
                break
        except:
            continue

# Initialize session state for pagination and image selection
if "page" not in st.session_state:
    st.session_state.page = 0
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

images_per_page = 3
start_idx = st.session_state.page * images_per_page
end_idx = start_idx + images_per_page
current_images = images[start_idx:end_idx]

# Navigation buttons
col1, col2, col3 = st.columns([1, 10, 1])

with col1:
    if st.button("⬅️", use_container_width=True) and st.session_state.page > 0:
        st.session_state.page -= 1
        st.experimental_rerun()

with col3:
    if st.button("➡️", use_container_width=True) and end_idx < len(images):
        st.session_state.page += 1
        st.experimental_rerun()

# Display image cards in 3 columns with hover effect and View button for popup
cols = st.columns(3)

for idx, col in enumerate(cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        col.markdown(
            f"""
            <style>
                .img-container-{start_idx+idx} {{
                    width: 100%; height: 220px;
                    border: 1px solid #ddd; border-radius: 8px;
                    overflow: hidden; cursor: pointer;
                    transition: transform 0.3s ease;
                }}
                .img-container-{start_idx+idx}:hover {{
                    transform: scale(1.05);
                    border: 2px solid #800000;
                }}
            </style>
            <img src='{img_url}' class='img-container-{start_idx+idx}'></img>
            """,
            unsafe_allow_html=True,
        )
        if col.button("View", key=f"view_{start_idx+idx}"):
            st.session_state.selected_img = img_url
    else:
        col.empty()

# Modal popup for selected image
if st.session_state.selected_img:
    with st.modal("Image Preview", True):
        st.image(st.session_state.selected_img, use_container_width=True)
        if st.button("Close", key="close_modal"):
            st.session_state.selected_img = None

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
