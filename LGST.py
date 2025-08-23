import streamlit as st
import requests

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
}
/* Header */
.header-container {
    background: linear-gradient(90deg, #800000, #ffffff);
    padding: 15px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    display: flex;
    justify-content: space-between; 
    align-items: center;
}
.header-title h1 { 
    margin: 0; 
    color: black; 
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}


/* Gallery */
.img-card {
    background: maroon;
    border-radius: 12px;
    padding: 10px;
    height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.img-card:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.img-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 10px;
}

/* Modal */
.modal {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
    text-align: center;
}
.modal img {
    border-radius: 12px;
    max-width: 100%;
    height: auto;
}

/* Search bar */
.stTextInput input {
    border: 2px solid #800000;
    border-radius: 12px;
    padding: 10px 40px 10px 12px;
    font-size: 16px;
    width: 100%;
    background-image: url("https://img.icons8.com/ios-filled/24/search.png");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 18px;
}

/* Buttons */
.stButton button {
    background: black;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton button:hover {
    background: #a00000;
}

/* Contact form */
.contact-form {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    max-width: 500px;
    margin: auto;
}

/* Section headers */
h2 { 
    color: #800000; 
    font-size: 1.8em; 
    margin-top: 15px; 
    margin-bottom: 10px; 
    border-bottom: 2px solid #800000; 
    padding-bottom: 5px; 
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    font-size: 14px;
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = []
if "page_num" not in st.session_state:
    st.session_state.page_num = 0
if "view_image" not in st.session_state:
    st.session_state.view_image = None

# ------------------ HEADER ------------------
col1, col2 = st.columns([8,2])
with col1:
    st.image("https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png", width=80)
    st.markdown("<h1 style='margin:0;color:black;text-shadow:1px 1px 2px rgba(0,0,0,0.3);'>LUCAS GREY SCRAP TRADING</h1>", unsafe_allow_html=True)
with col2:
    if st.button("About"):
        st.session_state.page = "About"
        st.rerun()
    if st.button("Contact Us"):
        st.session_state.page = "Contact"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ ABOUT PAGE ------------------
if st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    
    st.subheader("Who We Are")
    st.write("""
        Lucas Grey Scrap Trading is a leading scrap metal recycling company in Quezon City.  
        We are committed to sustainability by collecting, processing, and supplying high-quality scrap metals.
    """)

    st.subheader("Our Mission")
    st.info("To provide eco-friendly recycling services while supporting industries with sustainable raw materials.")

    st.subheader("Our Vision")
    st.success("To be the trusted partner in scrap metal recycling across the Philippines.")

    st.subheader("Core Values")
    st.markdown("""
    - ♻️ **Sustainability** – We recycle to reduce waste.  
    - 🤝 **Integrity** – We value fairness and transparency.  
    - ⚡ **Efficiency** – We deliver timely and reliable services.  
    - 👥 **Community** – We create partnerships for growth.  
    """)

    st.subheader("Organization Chart")
    st.graphviz_chart("""
    digraph {
        node [shape=box, style="rounded,filled", color=maroon, fontcolor=white, fontsize=12, fontname="Arial", fillcolor=black];

        CEO [label="CEO\nLucas Grey"];
        OPS [label="Operations Manager"];
        SALES [label="Sales Manager"];
        FIN [label="Finance & Admin"];
        WAREHOUSE [label="Warehouse Supervisor"];
        DRIVERS [label="Drivers"];
        STAFF [label="Staff"];

        CEO -> OPS;
        CEO -> SALES;
        CEO -> FIN;

        OPS -> WAREHOUSE;
        OPS -> DRIVERS;
        OPS -> STAFF;
    }
    """)

    st.subheader("Key Roles & Responsibilities")
    st.write("""
    - **CEO (Lucas Grey):** Oversees company strategy and growth.  
    - **Operations Manager:** Manages logistics, warehouse, and drivers.  
    - **Sales Manager:** Handles clients, partnerships, and pricing.  
    - **Finance & Admin:** Controls accounting, payroll, and documentation.  
    - **Warehouse Supervisor:** Ensures safe and organized scrap handling.  
    - **Drivers & Staff:** Collect, deliver, and sort materials.  
    """)

    st.subheader("Company Milestones")
    milestones = [
        {"year": "2015", "event": "Founded in Quezon City"},
        {"year": "2018", "event": "Expanded to industrial scrap collection"},
        {"year": "2021", "event": "Reached 1,000+ tons of recycled metal"},
        {"year": "2024", "event": "Partnered with major construction firms"},
    ]
    for item in milestones:
        st.write(f"**{item['year']}** – {item['event']}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ HOME PAGE ------------------
elif st.session_state.page == "Home":
    repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
    max_images = 15
    possible_exts = ["jpg", "jpeg", "png"]

    if not st.session_state.images:
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
        0: "Pic 1: Vroom Vroom", 1: "Pic 2: Yellow boys", 2: "Pic 3: Blackshirts",
        3: "Pic 4: I love red", 4: "Pic 5: Blue is my color", 5: "Pic 6: Batelec 1",
        6: "Pic 7: Meralco", 7: "Pic 8: Stainless steel scraps for manufacturing",
        8: "Pic 9: Copper pipes cleaned and ready for reuse",
        9: "Pic 10: Assorted metal alloys for specialized applications",
        10: "Pic 11: Scrap aluminum sheets for construction projects",
        11: "Pic 12: High-grade steel beams for recycling",
        12: "Pic 13: Copper radiators in bulk quantities",
        13: "Pic 14: Mixed non-ferrous metals for sale",
        14: "Pic 15: Scrap metal sorted by type for easy processing"
    }

    st.subheader("WELCOME TO LUCAS GREY SCRAP TRADING")
    search_query = st.text_input("", "")
    filtered_images = images
    if search_query:
        filtered_images = [img for idx, img in enumerate(images) if search_query.lower() in image_descriptions.get(idx, "").lower()]
        st.session_state.page_num = 0

    images_per_page = 3
    start_idx = st.session_state.page_num * images_per_page
    end_idx = start_idx + images_per_page
    current_images = filtered_images[start_idx:end_idx]
    total_pages = (len(filtered_images) + images_per_page - 1) // images_per_page

    if filtered_images:
        st.markdown(f"<p style='text-align:center;'>Page {st.session_state.page_num+1} of {total_pages}</p>", unsafe_allow_html=True)
    else:
        st.warning("No results found.")

    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("⬅️ Back", disabled=st.session_state.page_num == 0):
            st.session_state.page_num -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=end_idx >= len(filtered_images)):
            st.session_state.page_num += 1
            st.rerun()

    if filtered_images:
        st.subheader("CURRENT PROJECT")
        img_cols = st.columns(min(len(current_images), 3))
        for idx, col in enumerate(img_cols):
            if idx < len(current_images):
                img_url = current_images[idx]
                absolute_idx = images.index(img_url)
                caption = image_descriptions.get(absolute_idx, "No description")
                col.markdown(
                    f"""
                    <div class="img-card">
                        <img src="{img_url}" alt="{caption}">
                        <p>{caption}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if col.button("View Details", key=f"view_{absolute_idx}"):
                    st.session_state.view_image = absolute_idx
                    st.rerun()

    if st.session_state.view_image is not None:
        idx = st.session_state.view_image
        img_url = images[idx]
        caption = image_descriptions.get(idx, "No description")
        st.markdown(f"""
        <div class="modal">
            <img src="{img_url}" width="700">
            <p><b>{caption}</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Close", key=f"close_{idx}"):
            st.session_state.view_image = None
            st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    with st.form(key="contact_form"):
        name = st.text_input("Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        message = st.text_area("Message", placeholder="Your inquiry or message")
        submit_button = st.form_submit_button("Send Message")
        if submit_button:
            if name and email and message:
                st.success(f"Thank you, {name}! Your message has been received. We'll get back to you at {email}.")
            else:
                st.error("Please fill out all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        📧 Email: **charlottevazquez78@gmail.com**  
        📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  
    """)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
    © 2025 Lucas Grey Scrap Trading. All rights reserved.
</div>
""", unsafe_allow_html=True)





