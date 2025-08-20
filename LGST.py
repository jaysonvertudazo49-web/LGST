import streamlit as st
import requests

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ HEADER ------------------
st.markdown(
    """
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

# Determine which images exist using HEAD requests
images = []
for i in range(1, max_images + 1):
    for ext in possible_exts:
        url = f"{repo_url}pic{i}.{ext}"
        try:
            if requests.head(url).status_code == 200:
                images.append(url)
                break
        except:
            continue

if "page" not in st.session_state:
    st.session_state.page = 0
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

images_per_page = 3
start_idx = st.session_state.page * images_per_page
end_idx = start_idx + images_per_page
current_images = images[start_idx:end_idx]

col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("⬅️", use_container_width=True) and st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()
with col3:
    if st.button("➡️", use_container_width=True) and end_idx < len(images):
        st.session_state.page += 1
        st.rerun()

# Image containers with proper scaling inside fixed-height boxes
img_cols = st.columns(3)
for idx, col in enumerate(img_cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        # Use markdown with CSS containers to preserve aspect ratio and scale properly
        col.markdown(
            f"""
            <style>
            .img-container-{start_idx+idx} {{
                width: 100%;
                height: 220px;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                cursor: pointer;
                transition: transform 0.3s ease;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f9f9f9;
            }}
            .img-container-{start_idx+idx}:hover {{
                transform: scale(1.05);
                border: 2px solid #800000;
            }}
            .img-container-{start_idx+idx} img {{
                height: 100%;
                width: auto;
                object-fit: contain;
            }}
            </style>
            <div class="img-container-{start_idx+idx}" onclick="window.location.href='?selected={start_idx+idx}'">
                <img src="{img_url}" alt="project image">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        col.empty()

# Use st.query_params instead of deprecated experimental_get_query_params
query_params = st.query_params
if "selected" in query_params:
    idx = int(query_params["selected"][0])
    if 0 <= idx < len(images):
        st.session_state.selected_img = images[idx]
    # Clear query params so popup doesn't reopen on refresh
    st.experimental_set_query_params()

if st.session_state.selected_img:
    # Modal popup fallback with button to close, using markdown & session state
    st.markdown(
        """
        <style>
        .modal-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        }
        .modal-content {
            background: white;
            border-radius: 10px;
            padding: 15px;
            max-width: 80vw;
            max-height: 80vh;
            overflow: auto;
            position: relative;
        }
        </style>
        <div class="modal-overlay">
            <div class="modal-content">
        """,
        unsafe_allow_html=True,
    )
    st.image(st.session_state.selected_img, use_column_width=True)
    if st.button("Close"):
        st.session_state.selected_img = None
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

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
