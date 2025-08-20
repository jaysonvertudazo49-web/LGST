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

# Repo base URL
repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
max_images = 15  # adjust based on repo
possible_exts = ["jpg", "jpeg", "png"]

# Build image list (try all extensions)
images = []
for i in range(1, max_images + 1):
    for ext in possible_exts:
        url = f"{repo_url}pic{i}.{ext}"
        images.append(url)

# Session state
if "page" not in st.session_state:
    st.session_state.page = 0
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

images_per_page = 3
start = st.session_state.page * images_per_page
end = start + images_per_page
current_images = images[start:end]

# Layout: arrows + images
left_col, mid_col, right_col = st.columns([1, 10, 1])

# Left arrow
with left_col:
    if st.button("⬅️", use_container_width=True):
        if st.session_state.page > 0:
            st.session_state.page -= 1
        st.rerun()

# Images in a row (3 per page)
with mid_col:
    img_cols = st.columns(images_per_page)
    for idx, img in enumerate(current_images):
        with img_cols[idx]:
            # Each image clickable with hover effect
            if st.button(
                f" ",
                key=f"img_btn_{start+idx}",
                help=f"Click to view image {start+idx+1}",
            ):
                st.session_state.selected_img = img
                st.rerun()

            st.markdown(
                f"""
                <style>
                    #img_btn_{start+idx} {{
                        background-image: url('{img}');
                        background-size: cover;
                        background-position: center;
                        width: 100%; height: 220px;
                        border-radius: 8px;
                        border: 2px solid transparent;
                        transition: transform 0.3s ease, border 0.3s ease;
                    }}
                    #img_btn_{start+idx}:hover {{
                        transform: scale(1.05);
                        border: 2px solid #800000;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

# Right arrow
with right_col:
    if st.button("➡️", use_container_width=True):
        if end < len(images):
            st.session_state.page += 1
        st.rerun()

# ------------------ MODAL POPUP ------------------
if st.session_state.selected_img:
    st.markdown(
        """
        <div style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center;
            z-index: 9999;">
            <div style="background: white; padding: 20px; border-radius: 10px; width: 75%; display: flex; gap: 20px;">
        """,
        unsafe_allow_html=True,
    )

    img_col, text_col = st.columns([2, 1])
    with img_col:
        st.image(st.session_state.selected_img, use_container_width=True)
    with text_col:
        st.subheader("Image Details")
        st.write("📌 This is a placeholder description for the selected image.")
        if st.button("Close"):
            st.session_state.selected_img = None
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------ ABOUT SECTION ------------------
st.header("About")
st.write(
    """
    Lucas Grey Scrap Trading is dedicated to providing excellent scrap trading services.
    """
)

# ------------------ CONTACT SECTION ------------------
st.header("Contact")
st.write("Email me at: [your.email@example.com](mailto:your.email@example.com)")
