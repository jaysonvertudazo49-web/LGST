import streamlit as st
import requests

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ HEADER ------------------
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:center;
                background-color:#800000; padding:15px; border-radius:8px;">
        <h1 style="color:white; flex:1; margin:0;">LUCAS GREY SCRAP TRADING</h1>
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" style="height:60px; margin-left:20px;">
    </div><hr>
    """, unsafe_allow_html=True
)

# Repo base URL
repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
max_images = 15
possible_exts = ["jpg", "jpeg", "png"]

# Determine which images actually exist (using HEAD requests)
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

col1, _, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("⬅️", use_container_width=True) and st.session_state.page > 0:
        st.session_state.page -= 1
        st.experimental_rerun()
with col3:
    if st.button("➡️", use_container_width=True) and end_idx < len(images):
        st.session_state.page += 1
        st.experimental_rerun()

cols = st.columns(3)
for idx, col in enumerate(cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        col.image(img_url, use_column_width=True)
        if col.button("View", key=f"view_{start_idx+idx}"):
            st.session_state.selected_img = img_url
    else:
        col.empty()

if st.session_state.selected_img:
    # Custom modal HTML popup controlled by session state
    st.markdown(
        f"""
        <style>
        .modal-backdrop {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.7);
            display: flex; justify-content: center; align-items: center;
            z-index: 10000;
        }}
        .modal-content {{
            position: relative;
            background: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 80vw;
            max-height: 80vh;
            overflow: auto;
        }}
        .modal-close {{
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
            color: #800000;
        }}
        </style>
        <div class="modal-backdrop" onclick="document.querySelector('.modal-backdrop').style.display='none';">
            <div class="modal-content" onclick="event.stopPropagation();">
                <span class="modal-close" onclick="document.querySelector('.modal-backdrop').style.display='none';">&times;</span>
                <img src="{st.session_state.selected_img}" style="width:100%; height:auto;"/>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Close"):
        st.session_state.selected_img = None
        st.experimental_rerun()

# ------------------ ABOUT SECTION ------------------
st.header("About")
st.write("""
    This website is a basic example to help you get started.  
    Lucas Grey Scrap Trading is dedicated to providing excellent scrap trading services.
""")

# ------------------ CONTACT SECTION ------------------
st.header("Contact")
st.write("Email me at: [your.email@example.com](mailto:your.email@example.com)")
