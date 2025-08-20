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
max_images = 10  # change based on how many pics you have in the repo

images = [f"{repo_url}pic{i}.jpg" for i in range(1, max_images + 1)]

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

images_per_page = 3
start = st.session_state.page * images_per_page
end = start + images_per_page
current_images = images[start:end]

col1, col2, col3 = st.columns([1, 10, 1])

# Left arrow
with col1:
    if st.button("⬅️", use_container_width=True):
        if st.session_state.page > 0:
            st.session_state.page -= 1
        st.rerun()

# Images Grid
with col2:
    img_cols = st.columns(len(current_images))
    for idx, img in enumerate(current_images):
        with img_cols[idx]:
            if st.button(
                f"🖼️", key=f"img_btn_{start+idx}", 
                help=f"Click to view Image {start+idx+1}"
            ):
                st.session_state.selected_img = img

            # Thumbnail preview
            st.markdown(
                f"""
                <div style="width: 100%; height: 200px; display: flex; justify-content: center; align-items: center;
                            border: 1px solid #ddd; border-radius: 8px; overflow: hidden; margin-top: -45px; cursor:pointer;">
                    <img src="{img}" style="width:100%; height:100%; object-fit:cover;">
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

# ------------------ MODAL POPUP ------------------
if st.session_state.selected_img:
    st.markdown(
        """
        <div style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center;
            z-index: 9999;">
            <div style="background: white; padding: 20px; border-radius: 10px; width: 70%; display: flex; gap: 20px;">
        """,
        unsafe_allow_html=True,
    )

    img_col, text_col = st.columns([2, 1])
    with img_col:
        st.image(st.session_state.selected_img, use_container_width=True)
    with text_col:
        st.subheader("Image Details")
        st.write("📌 This is a placeholder description for the selected image. You can update this text later.")
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
