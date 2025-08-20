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

# Descriptions for each image (edit inline as needed)
image_descriptions = {
    0: "Pic 1 description: This is the description for picture 1.",
    1: "Pic 2 description: Description text can go here.",
    2: "Pic 3 description: Another placeholder description.",
    3: "Pic 4 description: Add your descriptions here.",
    4: "Pic 5 description: Customize as needed.",
    # Extend as needed up to max_images
}

# Determine which images actually exist
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
        # Image container with hover scale effect
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
        # View button to open modal popup
        if col.button("View", key=f"view_{absolute_idx}"):
            st.session_state.selected_img_idx = absolute_idx
    else:
        col.empty()

# Modal popup with full image and description
if st.session_state.selected_img_idx is not None:
    idx = st.session_state.selected_img_idx
    if 0 <= idx < len(images):
        img_url = images[idx]
        description = image_descriptions.get(idx, "No description available.")
        # Modal with close button
        st.markdown(
            f"""
            <style>
            .modal-overlay {{
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                background: rgba(0,0,0,0.7);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            }}
            .modal-content {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                max-width: 90vw;
                max-height: 90vh;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 20px;
                align-items: center;
                box-shadow: 0 0 10px rgba(0,0,0,0.25);
            }}
            .modal-inner {{
                display: flex;
                flex-direction: row;
                gap: 20px;
                width: 100%;
            }}
            .modal-image {{
                flex: 2;
                max-height: 70vh;
                overflow: hidden;
            }}
            .modal-image img {{
                width: 100%;
                height: auto;
                border-radius: 8px;
            }}
            .modal-description {{
                flex: 1;
                font-size: 1.1em;
                color: #333;
            }}
            .modal-close-btn-container {{
                width: 100%;
                text-align: center;
            }}
            @media (max-width: 768px) {{
                .modal-inner {{
                    flex-direction: column;
                }}
                .modal-image, .modal-description {{
                    flex: 1;
                    max-height: none;
                }}
            }}
            </style>
            <div class="modal-overlay" role="dialog" aria-labelledby="modalTitle">
                <div class="modal-content">
                    <div class="modal-inner">
                        <div class="modal-image">
                            <img src="{img_url}" alt="Full image">
                        </div>
                        <div class="modal-description">
                            <h3 id="modalTitle">Description</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                    <div class="modal-close-btn-container">
                        <!-- Streamlit will replace this button -->
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Style the Streamlit button to match the modal
        st.markdown(
            """
            <style>
            .stButton>button {
                background-color: #800000;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 1em;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #a00000;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Place the close button in a container to ensure it appears in the modal
        with st.container():
            if st.button("Close", key=f"close_{idx}", help="Close the modal"):
                st.session_state.selected_img_idx = None
                st.rerun()
    else:
        # Reset invalid index to prevent modal from getting stuck
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





