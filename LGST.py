import streamlit as st
import requests

st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# Custom CSS for enhanced aesthetics
st.markdown(
    """
    <style>
    /* Global styles */
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
    /* Buttons */
    .stButton>button {
        background-color: #800000;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1em;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #a00000;
    }
    /* Navigation buttons */
    .nav-button {
        font-size: 1.2em;
        width: 100%;
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
    /* Contact form */
    .stTextInput label, .stTextArea label {
        color: #800000;
        font-weight: bold;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .header-container h1 {
            font-size: 1.8em;
        }
        .header-container img {
            height: 50px;
        }
        .img-card {
            margin-bottom: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="header-container">
        <h1>LUCAS GREY SCRAP TRADING</h1>
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" alt="Logo">
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

# Descriptions for each image
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

# Search functionality
st.subheader("Search Images")
search_query = st.text_input("Enter keywords to filter images (e.g., 'copper' or 'steel')", "")
filtered_images = images
if search_query:
    filtered_images = [
        img for idx, img in enumerate(images)
        if search_query.lower() in image_descriptions.get(idx, "").lower()
    ]

# Pagination
if "page" not in st.session_state:
    st.session_state.page = 0

images_per_page = 3
start_idx = st.session_state.page * images_per_page
end_idx = start_idx + images_per_page
current_images = filtered_images[start_idx:end_idx]

# Navigation and image count
total_pages = (len(filtered_images) + images_per_page - 1) // images_per_page
st.markdown(f"<p style='text-align: center; color: #333;'>Page {st.session_state.page + 1} of {total_pages} | Showing {len(current_images)} of {len(filtered_images)} images</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("⬅️ Back", use_container_width=True, key="prev_page", disabled=st.session_state.page == 0):
        st.session_state.page -= 1
        st.rerun()
with col3:
    if st.button("Next ➡️", use_container_width=True, key="next_page", disabled=end_idx >= len(filtered_images)):
        st.session_state.page += 1
        st.rerun()

# Define the modal dialog function
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
            # Placeholder: Additional image details
            #st.write("**Weight**: [Placeholder: e.g., 50kg]")
            #st.write("**Material**: [Placeholder: e.g., Aluminum]")
            #st.write("**Price**: [Placeholder: e.g., $100/ton]")
        # Explicit Close button
        if st.button("Close", key=f"close_modal_{idx}"):
            st.rerun()

# Image gallery
st.subheader("Image Gallery")
img_cols = st.columns(min(len(current_images), 3))
for idx, col in enumerate(img_cols):
    if idx < len(current_images):
        img_url = current_images[idx]
        absolute_idx = images.index(img_url)  # Map to original index for descriptions
        caption = image_descriptions.get(absolute_idx, "No description").split(": ")[1][:30] + "..." if len(image_descriptions.get(absolute_idx, "")) > 30 else image_descriptions.get(absolute_idx, "").split(": ")[1]
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

# ------------------ ABOUT SECTION ------------------
st.header("About")
st.write(
    """
    DETAILS HINGI AKO HAHAHA
    """
)

# ------------------ CONTACT SECTION ------------------
st.header("Contact Us")
st.write("""placeholder@gmail.com""")
with st.form(key="contact_form"):
    name = st.text_input("Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    message = st.text_area("Message", placeholder="Your inquiry or message")
    submit_button = st.form_submit_button("Send Message")
    if submit_button:
        if name and email and message:
            # Placeholder: Send message to backend or email service
            st.success(f"Thank you, {name}! Your message has been received. We'll get back to you at {email} soon.")
        else:
            st.error("Please fill out all fields.")








