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

# Cache images in session state
if "images" not in st.session_state:
    st.session_state.images = []
    for i in range(1, max_images + 1):
        for ext in possible_exts:
            url = f"{repo_url}pic{i}.{ext}"
            try:
                if requests.head(url).status_code == 200:
                    st.session_state.images.append(url)
                    break
            except Exception as e:
                print(f"Error checking {url}: {e}")

images = st.session_state.images

# Descriptions for each image (customize as needed)
image_descriptions = {
    0: "Pic 1: Vroom Vroom",
    1: "Pic 2: yellow boys",
    2: "Pic 3: blackshirts.",
    3: "Pic 4: i love red",
    4: "Pic 5: blue is my color",
    5: "Pic 6: batelec 1",
    6: "Pic 7: meralco",
   # 7: "Pic 8: Stainless steel scraps for manufacturing.",
   # 8: "Pic 9: Copper pipes cleaned and ready for reuse.",
   # 9: "Pic 10: Assorted metal alloys for specialized applications.",
   # 10: "Pic 11: Scrap aluminum sheets for construction projects.",
   # 11: "Pic 12: High-grade steel beams for recycling.",
   # 12: "Pic 13: Copper radiators in bulk quantities.",
   # 13: "Pic 14: Mixed non-ferrous metals for sale.",
   # 14: "Pic 15: Scrap metal sorted by type for easy processing."
}


if "page" not in st.session_state:
    st.session_state.page = 0

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

# Define the modal dialog function before calling it
@st.dialog("Image Details :camera:", width="large")
def show_image_modal(idx):
    if 0 <= idx < len(images):
        img_url = images[idx]
        description = image_descriptions.get(idx, "No description available.")
        col_img, col_desc = st.columns(2)
        with col_img:
            st.image(img_url, use_container_width=True)
        with col_desc:
            st.subheader("Description")
            st.write(description)
        # Explicit Close button (triggers rerun to close the modal)
        if st.button("Close", key=f"close_modal_{idx}"):
            st.rerun()

# Dynamic columns based on available images
img_cols = st.columns(min(len(current_images), 3))
for idx, col in enumerate(img_cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        absolute_idx = start_idx + idx
        col.markdown(
            f"""
            <style>
            .img-container-{absolute_idx} {{
                width: 100%;
                height: 220px;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                cursor: default;
                transition: transform 0.3s ease;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f9f9f9;
            }}
            .img-container-{absolute_idx}:hover {{
                transform: scale(1.05);
                border: 2px solid #800000;
            }}
            .img-container-{absolute_idx} img {{
                height: 100%;
                width: auto;
                object-fit: contain;
            }}
            </style>
            <div class="img-container-{absolute_idx}">
                <img src="{img_url}" alt="project image">
            </div>
            """,
            unsafe_allow_html=True,
        )
        if col.button("View", key=f"view_{absolute_idx}"):
            show_image_modal(absolute_idx)

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



