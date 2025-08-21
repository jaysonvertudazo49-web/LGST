import streamlit as st
import requests

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ CSS ------------------
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }
    /* Header */
    .header-container {
        background: linear-gradient(90deg, #800000, #ffffff);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-container h1 {
        color: black;
        font-size: 2.5em;
        text-align: center;
        flex: 1;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .header-container img {
        height: 70px;
        margin-left: 20px;
    }
    /* Nav buttons */
    .stButton>button {
        background: #800000;
        border: none;
        color: #000000;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
    }
    .stButton>button:hover {
        text-decoration: underline;
        background: none;
    }
    /* Gallery */
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
    /* Search bar */
    .stTextInput input {
        border: 2px solid #800000;
        border-radius: 8px;
        padding: 8px;
    }
    /* Section headers */
    h2 {
        color: #800000;
        font-size: 1.8em;
        margin-top: 20px;
        border-bottom: 2px solid #800000;
        padding-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ SESSION STATE (Navigation) ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ------------------ HEADER ------------------
col1, col2, col3 = st.columns([2, 6, 2])
with col1:
    st.image("https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png", width=80)
with col2:
    st.markdown("<h1 style='text-align:center;'>LUCAS GREY SCRAP TRADING</h1>", unsafe_allow_html=True)
with col3:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("About", key="about_btn"):
            st.session_state.page = "About"
            st.rerun()
    with c2:
        if st.button("Contact Us", key="contact_btn"):
            st.session_state.page = "Contact"
            st.rerun()
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
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
                    except:
                        pass

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

    st.subheader("Search Images")
    search_query = st.text_input("Enter keywords to filter images (e.g., 'copper' or 'steel')", "")
    filtered_images = images
    if search_query:
        filtered_images = [
            img for idx, img in enumerate(images)
            if search_query.lower() in image_descriptions.get(idx, "").lower()
        ]

    if "page_num" not in st.session_state:
        st.session_state.page_num = 0
    images_per_page = 3
    start_idx = st.session_state.page_num * images_per_page
    end_idx = start_idx + images_per_page
    current_images = filtered_images[start_idx:end_idx]
    total_pages = (len(filtered_images) + images_per_page - 1) // images_per_page

    st.markdown(f"<p style='text-align:center;'>Page {st.session_state.page_num+1} of {total_pages}</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("⬅️ Back", disabled=st.session_state.page_num == 0):
            st.session_state.page_num -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=end_idx >= len(filtered_images)):
            st.session_state.page_num += 1
            st.rerun()

    @st.dialog("Image Details :camera:", width="large")
    def show_image_modal(idx):
        if 0 <= idx < len(images):
            img_url = images[idx]
            description = image_descriptions.get(idx, "No description available.")
            col_img, col_desc = st.columns([2, 1])
            with col_img:
                st.image(img_url, use_container_width=True)
            with col_desc:
                st.subheader("Description")
                st.write(description)
            if st.button("Close", key=f"close_modal_{idx}"):
                st.rerun()

    st.subheader("Image Gallery")
    img_cols = st.columns(min(len(current_images), 3))
    for idx, col in enumerate(img_cols):
        if idx < len(current_images):
            img_url = current_images[idx]
            absolute_idx = images.index(img_url)
            caption = image_descriptions.get(absolute_idx, "No description")
            col.markdown(
                f"""
                <div class="img-card">
                    <img src="{img_url}" alt="project image">
                    <div class="img-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if col.button("View Details", key=f"view_{absolute_idx}"):
                show_image_modal(absolute_idx)

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.write(
        """
        Lucas Grey Scrap Trading is dedicated to providing sustainable and 
        cost-effective scrap trading services. We specialize in recycling metals such 
        as copper, aluminum, and steel to support both small-scale and industrial clients.
        
        Our mission is to promote eco-friendly recycling solutions while delivering 
        reliable services to our customers. 
        
        **Services Offered:**
        - Scrap metal collection
        - Sorting and processing
        - Wholesale and retail supply of recycled metals
        - Partnerships for industrial recycling
        """
    )
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
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
        📧 Email: **charlottevazquez78@gmail.com**  
        📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  
        © 2025 Lucas Grey Scrap Trading. All rights reserved.
        """
    )
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()



