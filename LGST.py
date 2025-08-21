import streamlit as st
import requests

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ INITIAL STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------ CUSTOM CSS ------------------
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }
    .header-container {
        background: linear-gradient(90deg, #800000, #ffffff);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        color: black;
        font-size: 2.5em;
        text-align: center;
        flex: 1;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .header-logo {
        height: 70px;
    }
    .header-menu button {
        background-color: #800000 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        font-size: 1em !important;
    }
    .header-menu button:hover {
        background-color: #a00000 !important;
    }
    .img-card {
        background: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .img-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        border: 2px solid #800000;
    }
    .img-card img {
        width: 100%;
        height: 200px;
        object-fit: contain;
        border-radius: 8px;
    }
    .img-caption {
        text-align: center;
        font-size: 0.9em;
        color: #333;
        margin-top: 8px;
    }
    .stTextInput input {
        border: 2px solid #800000;
        border-radius: 8px;
        padding: 8px;
    }
    h2 {
        color: #800000;
        font-size: 1.8em;
        margin-top: 20px;
        border-bottom: 2px solid #800000;
        padding-bottom: 5px;
    }
    .footer {
        background: linear-gradient(90deg, #800000, #a00000);
        color: white;
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-radius: 12px 12px 0 0;
    }
    .footer h2 {
        color: white;
        margin-bottom: 10px;
    }
    .footer p {
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ HEADER ------------------
col_logo, col_title, col_menu = st.columns([1, 4, 1])
with col_logo:
    st.image("https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png", use_container_width=True)
with col_title:
    st.markdown("<h1 class='header-title'>LUCAS GREY SCRAP TRADING</h1>", unsafe_allow_html=True)
with col_menu:
    if st.button("About", key="about_btn"):
        st.session_state.page = "about"

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ PAGE ROUTING ------------------
if st.session_state.page == "home":
    # ------------------ IMAGE REPO ------------------
    repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
    max_images = 15
    possible_exts = ["jpg", "jpeg", "png"]

    if "images" not in st.session_state:
        st.session_state.images = []
        with st.spinner("Loading images..."):
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

    image_descriptions = {
        0: "Pic 1: Vroom Vroom",
        1: "Pic 2: Yellow boys",
        2: "Pic 3: Blackshirts",
        3: "Pic 4: I love red",
        4: "Pic 5: Blue is my color",
        5: "Pic 6: Batelec 1",
        6: "Pic 7: Meralco",
        7: "Pic 8: Stainless steel scraps for manufacturing",
        8: "Pic 9: Copper pipes cleaned and ready for reuse",
        9: "Pic 10: Assorted metal alloys for specialized applications",
        10: "Pic 11: Scrap aluminum sheets for construction projects",
        11: "Pic 12: High-grade steel beams for recycling",
        12: "Pic 13: Copper radiators in bulk quantities",
        13: "Pic 14: Mixed non-ferrous metals for sale",
        14: "Pic 15: Scrap metal sorted by type for easy processing"
    }

    # ------------------ SEARCH ------------------
    st.subheader("Search Images")
    search_query = st.text_input("Enter keywords to filter images (e.g., 'copper' or 'steel')", "")
    filtered_images = images
    if search_query:
        filtered_images = [
            img for idx, img in enumerate(images)
            if search_query.lower() in image_descriptions.get(idx, "").lower()
        ]

    # ------------------ PAGINATION ------------------
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    images_per_page = 3
    start_idx = st.session_state.page_num * images_per_page
    end_idx = start_idx + images_per_page
    current_images = filtered_images[start_idx:end_idx]

    total_pages = (len(filtered_images) + images_per_page - 1) // images_per_page
    st.markdown(f"<p style='text-align: center; color: #333;'>Page {st.session_state.page_num + 1} of {total_pages} | Showing {len(current_images)} of {len(filtered_images)} images</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("⬅️ Back", use_container_width=True, key="prev_page", disabled=st.session_state.page_num == 0):
            st.session_state.page_num -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️", use_container_width=True, key="next_page", disabled=end_idx >= len(filtered_images)):
            st.session_state.page_num += 1
            st.rerun()

    # ------------------ IMAGE GALLERY ------------------
    st.subheader("Image Gallery")
    img_cols = st.columns(min(len(current_images), 3))
    for idx, col in enumerate(img_cols):
        if idx < len(current_images):
            img_url = current_images[idx]
            absolute_idx = images.index(img_url)
            caption = image_descriptions.get(absolute_idx, "No description").split(": ")[1]
            col.markdown(
                f"""
                <div class="img-card">
                    <img src="{img_url}" alt="project image">
                    <div class="img-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif st.session_state.page == "about":
    # ------------------ ABOUT PAGE ------------------
    st.header("About")
    st.write(
        """
        Lucas Grey Scrap Trading is a trusted partner in sustainable recycling,
        specializing in copper, aluminum, and other non-ferrous scrap materials.  

        We help industries convert waste into value while promoting
        environmental responsibility and sustainable development.
        """
    )
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))

# ------------------ FOOTER ------------------
st.markdown('<div class="footer"><h2>Contact Us</h2>', unsafe_allow_html=True)
with st.form(key="contact_form"):
    name = st.text_input("Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    message = st.text_area("Message", placeholder="Your inquiry or message")
    submit_button = st.form_submit_button("Send Message")
    if submit_button:
        if name and email and message:
            st.success(f"Thank you, {name}! Your message has been received. We'll get back to you at {email} soon.")
        else:
            st.error("Please fill out all fields.")

st.markdown(
    """
    <p>📧 Email: placeholder@gmail.com</p>
    <p>📍 Address: Your Office Address Here</p>
    <p>&copy; 2025 Lucas Grey Scrap Trading. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
