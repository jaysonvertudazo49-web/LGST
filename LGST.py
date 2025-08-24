import streamlit as st
import base64

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
/* Global */
body { 
    font-family: 'Arial', sans-serif; 
    background: linear-gradient(135deg, #111111, #222222); 
    margin:0;
    padding:0;
    color:white;
}
h1, h2, h3, h4, h5, h6, p, div, span, button { 
    color:white !important; 
}
.stButton>button {
    background: #444444;
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    border: none;
    cursor: pointer;
}
.stButton>button:hover {
    background: #666666;
}
.header-container {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 20px;
    background:#000;
    border-radius:12px;
}
.header-title {
    font-size:24px;
    font-weight:bold;
    color:white;
}
.header-menu {
    display:flex;
    gap:15px;
}
.header-menu button {
    background:#333;
    color:white;
    border:none;
    padding:8px 14px;
    border-radius:8px;
}
.header-menu button:hover {
    background:#555;
}
.gallery img {
    border-radius:12px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = [
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/1.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/2.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/3.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/4.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/5.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/6.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/7.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/8.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/9.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/10.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/11.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/12.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/13.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/14.jpg",
        "https://raw.githubusercontent.com/jaysonvertudazo49/CDN/main/15.jpg",
    ]
if "modal_image" not in st.session_state:
    st.session_state.modal_image = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "descriptions" not in st.session_state:
    st.session_state.descriptions = {}

# ------------------ HEADER ------------------
st.markdown(f"""
<div class="header-container">
    <div class="header-title">Lucas Grey Scrap Trading</div>
    <form action="/" method="get" class="header-menu">
        <button type="submit" name="page" value="Home">Home</button>
        <button type="submit" name="page" value="About">About</button>
        <button type="submit" name="page" value="Contact">Contact Us</button>
        <button type="submit" name="page" value="Admin">Admin</button>
    </form>
</div>
""", unsafe_allow_html=True)

# ------------------ HANDLE HEADER BUTTONS ------------------
query_params = st.experimental_get_query_params()
if "page" in query_params:
    st.session_state.page = query_params["page"][0]

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    st.header("📸 Current Projects")

    # Default descriptions
    default_descriptions = {
        0: "Pic 1: Vroom Vroom",
        1: "Pic 2: Yellow boys",
        2: "Pic 3: Blackshirts",
        3: "Pic 4: Dudes",
        4: "Pic 5: Form",
        5: "Pic 6: Pic niyo",
        6: "Pic 7: More Pic",
        7: "Pic 8: Karunungan",
        8: "Pic 9: Lights",
        9: "Pic 10: Toga",
        10: "Pic 11: Graduate",
        11: "Pic 12: BlackToga",
        12: "Pic 13: BlueToga",
        13: "Pic 14: Groupies",
        14: "Pic 15: Macho",
    }

    # Merge with admin descriptions
    image_descriptions = default_descriptions.copy()
    image_descriptions.update(st.session_state.descriptions)

    # Search
    search_query = st.text_input("🔍 Search Projects", "").lower()

    # Pagination
    items_per_page = 6
    total_pages = (len(st.session_state.images) - 1) // items_per_page + 1
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, step=1) - 1

    # Gallery
    start_idx = page_number * items_per_page
    end_idx = start_idx + items_per_page
    filtered_images = []
    for i, img in enumerate(st.session_state.images):
        desc = image_descriptions.get(i, "")
        if search_query in desc.lower():
            filtered_images.append((i, img, desc))

    for i, img, desc in filtered_images[start_idx:end_idx]:
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("View", key=f"view_{i}"):
                st.session_state.modal_image = img
        with col2:
            st.image(img, use_container_width=True)
            st.caption(desc)

    # Modal
    if st.session_state.modal_image:
        st.image(st.session_state.modal_image, use_container_width=True)
        if st.button("Close"):
            st.session_state.modal_image = None

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page == "About":
    st.header("ℹ️ About Us")
    st.write("Lucas Grey Scrap Trading is dedicated to sustainable scrap trading.")
    st.write("### Organizational Chart")
    st.write("- CEO: Von Ryan Veloso")
    st.write("- Secretary: Jayson Vertudazo")
    st.write("- Accountant: Your Future Teammate")

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("📞 Contact Us")
    st.write("For inquiries, email us at: support@lucasgreyscrap.com")
    st.write("Or call: +63 912 345 6789")

# ------------------ ADMIN PAGE ------------------
elif st.session_state.page == "Admin":
    st.header("🔑 Admin Login" if not st.session_state.is_admin else "📂 Admin Dashboard")

    if not st.session_state.is_admin:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.is_admin = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        uploaded_files = st.file_uploader(
            "Upload new project images", 
            accept_multiple_files=True, 
            type=["jpg", "jpeg", "png"]
        )
        description = st.text_area("Image Description", placeholder="Enter a description for the uploaded image(s)")

        if st.button("Save Project"):
            if uploaded_files:
                for file in uploaded_files:
                    encoded = base64.b64encode(file.getvalue()).decode()
                    img_url = f"data:image/png;base64,{encoded}"
                    st.session_state.images.append(img_url)
                    st.session_state.descriptions[len(st.session_state.images)-1] = description
                st.success("✅ Project(s) added successfully!")
                st.rerun()
            else:
                st.warning("⚠️ Please upload at least one image.")

        if st.button("Logout"):
            st.session_state.is_admin = False
            st.rerun()
