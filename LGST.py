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
# Section 1: Current Project (Image Browser)
# ==============================
st.header("Current Project")

# List of image URLs from GitHub repo
max_images = 10  # adjust when adding more images
image_urls = [
    f"https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/refs/heads/main/pic{i}.jpg"
    for i in range(1, max_images + 1)
]

# Session state for navigation
if "start_index" not in st.session_state:
    st.session_state.start_index = 0
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

images_per_page = 3  # number of thumbnails per page

# --- Custom CSS for gallery look ---
st.markdown(
    """
    <style>
    .gallery-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        position: relative;
    }
    .thumbnail-container {
        width: 250px;
        height: 180px;
        overflow: hidden;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #f4f4f4;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .thumbnail-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .thumbnail-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .selected {
        border: 5px solid #FFD700; /* gold border */
    }
    .arrow {
        background-color: #800000;
        color: white;
        border: none;
        padding: 12px 18px;
        font-size: 24px;
        border-radius: 50%;
        cursor: pointer;
        position: absolute;
        top: 40%;
        z-index: 10;
    }
    .arrow:hover {
        background-color: #a00000;
    }
    .arrow-left {
        left: -60px;
    }
    .arrow-right {
        right: -60px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Navigation + Gallery ---
col_gallery = st.container()
with col_gallery:
    st.markdown("<div class='gallery-container'>", unsafe_allow_html=True)

    # Prev button
    if st.session_state.start_index > 0:
        if st.button("⬅️", key="prev", help="Previous"):
            st.session_state.start_index -= images_per_page

    # Display thumbnails
    cols = st.columns(images_per_page, gap="large")
    for i, col in enumerate(cols):
        idx = st.session_state.start_index + i
        if idx < len(image_urls):
            img_url = image_urls[idx]
            is_selected = st.session_state.selected_image == img_url
            css_class = "thumbnail-container"
            if is_selected:
                css_class += " selected"

            if col.button(" ", key=f"imgbtn{idx}"):
                st.session_state.selected_image = img_url

            col.markdown(
                f"<div class='{css_class}'><img src='{img_url}'></div>",
                unsafe_allow_html=True,
            )

    # Next button
    if st.session_state.start_index + images_per_page < len(image_urls):
        if st.button("➡️", key="next", help="Next"):
            st.session_state.start_index += images_per_page

    st.markdown("</div>", unsafe_allow_html=True)

# --- Enlarged image with details ---
if st.session_state.selected_image:
    st.markdown("---")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.image(st.session_state.selected_image, use_container_width=True, caption="Selected Image")
    with c2:
        st.subheader("Project Details")
        st.write("📝 Placeholder description for this image.")
        st.write("Replace this with real scrap trading project details.")
        st.info("Tip: Use this section to explain the type, quality, or source of the scrap.")

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
