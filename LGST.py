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
    /* About Button */
    .about-link button {
        background: none;
        border: none;
        color: #800000;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
    }
    .about-link button:hover {
        text-decoration: underline;
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
    if st.button("About", key="about_btn"):
        st.session_state.page = "About"
        st.rerun()
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    st.subheader("Search Images")

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

    st.subheader("Image Gallery")
    img_cols = st.columns(min(len(current_images), 3))
    for idx, col in enumerate(img_cols):
        if idx < len(current_images):
            img_url = current_images[idx]
            absolute_idx = images.index(img_url)
            caption = image_descriptions.get(absolute_idx, "No description")
            col.image(img_url, caption=caption, use_container_width=True)

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
        
        📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  
        📧 Email: charlottevazquez78@gmail.com  
        """
    )
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
