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

# Descriptions for each image (edit these texts inline)
image_descriptions = {
    0: "Pic 1 description: This is the description for picture 1.",
    1: "Pic 2 description: Description text can go here.",
    2: "Pic 3 description: Another placeholder description.",
    3: "Pic 4 description: Add your descriptions here.",
    4: "Pic 5 description: Customize as needed.",
    # Add more descriptions as needed up to max_images
}

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
if "selected_img_idx" not in st.session_state:
    st.session_state.selected_img_idx = None

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

img_cols = st.columns(3)
for idx, col in enumerate(img_cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        absolute_idx = start_idx + idx
        # Display image container with hover effect
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
        # Add a "View" button to open popup modal
        if col.button("View", key=f"view_{absolute_idx}"):
            st.session_state.selected_img_idx = absolute_idx
    else:
        col.empty()

# Display popup modal if an image is selected
if st.session_state.selected_img_idx is not None:
    selected_idx = st.session_state.selected_img_idx
    if 0 <= selected_idx < len(images):
        selected_img_url = images[selected_idx]
        selected_description = image_descriptions.get(selected_idx, "No description available.")
        # Modal with side-by-side image and description
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
                padding: 20px;
                max-width: 90vw;
                max-height: 90vh;
                overflow-y: auto;
                display: flex;
                gap: 20px;
                align-items: center;
            }
            .modal-image {
                flex: 2;
                max-height: 80vh;
                overflow: hidden;
            }
            .modal-image img {
                width: 100%;
                height: auto;
                border-radius: 8px;
            }
            .modal-description {
                flex: 1;
                font-size: 1.1em;
                color: #333;
            }
            .modal-close-btn {
                margin-top: 15px;
            }
            </style>
            <div class="modal-overlay">
                <div class="modal-content">
                    <div class="modal-image">
            """,
            unsafe_allow_html=True,
        )
        st.image(selected_img_url, use_column_width=True)
        st.markdown(
            f"""
                    </div>
                    <div class="modal-description">
                        <h3>Description</h3>
                        <p>{selected_description}</p>
                        <button class="modal-close-btn" onclick="window.location.reload();">Close</button>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Provide fallback close button in Streamlit for accessibility
        if st.button("Close"):
            st.session_state.selected_img_idx = None
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
