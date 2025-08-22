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
    background: linear-gradient(135deg, #111, #222);
    margin: 0;
    padding: 0;
    color: white;
}

/* Header */
.header-container {
    display: flex;
    align-items: center;
    padding: 15px 20px;
    background: #000000cc;
    border-bottom: 2px solid maroon;
}
.header-title {
    font-size: 26px;
    font-weight: bold;
    color: maroon;
    margin-left: 20px;
}

/* Top-right nav */
.nav-buttons-top {
    position: absolute;
    top: 20px;
    right: 30px;
    display: flex;
    gap: 10px;
}
.nav-buttons-top button {
    background: #800000;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.nav-buttons-top button:hover {
    background: #a00000;
}

/* Cards */
.card {
    background: #111;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    text-align: center;
    transition: transform 0.2s;
}
.card:hover {
    transform: scale(1.03);
}
.card img {
    width: 100%;
    border-radius: 10px;
}

/* Modal */
.modal {
    background: #000000cc;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: #111;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.modal-content img {
    max-width: 700px;
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 15px;
    margin-top: 40px;
    border-top: 2px solid maroon;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# ------------------ STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = []
if "page_num" not in st.session_state:
    st.session_state.page_num = 0
if "modal_image" not in st.session_state:
    st.session_state.modal_image = None

# ------------------ HEADER ------------------
st.markdown("""
<div class="header-container">
    <div>
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" width="80">
    </div>
    <div class="header-title">
        LUCAS GREY SCRAP TRADING
    </div>
</div>

<!-- Nav buttons outside header -->
<div class="nav-buttons-top">
    <form action="#" method="get">
        <button name="page" value="About">About</button>
        <button name="page" value="Contact">Contact Us</button>
    </form>
</div>
""", unsafe_allow_html=True)

# Handle navigation
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"][0]

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    st.header("Welcome to Lucas Grey Scrap Trading")

    # Load sample images (replace with your GitHub images)
    if not st.session_state.images:
        base_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
        st.session_state.images = [
            {"url": base_url + "pic1.jpg", "caption": "Scrap Metals"},
            {"url": base_url + "pic2.png", "caption": "Recycling Facility"},
            {"url": base_url + "pic3.jpg", "caption": "Processed Copper"},
            {"url": base_url + "pic4.jpg", "caption": "Aluminum Piles"},
            {"url": base_url + "pic5.png", "caption": "Steel Bundles"},
            {"url": base_url + "pic6.jpg", "caption": "Warehouse Storage"}
        ]

    # Search bar
    search = st.text_input("Search Images", placeholder="Type to search...")
    filtered = [img for img in st.session_state.images if search.lower() in img["caption"].lower()] if search else st.session_state.images

    # Pagination
    per_page = 3
    total = len(filtered)
    start = st.session_state.page_num * per_page
    end = start + per_page
    current = filtered[start:end]

    if total > 0:
        cols = st.columns(3)
        for i, img in enumerate(current):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card">
                    <img src="{img['url']}" alt="{img['caption']}">
                    <p>{img['caption']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View Details {i}", key=f"btn_{i}"):
                    st.session_state.modal_image = img

        # Pagination controls
        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.session_state.page_num > 0 and st.button("⬅️ Prev"):
                st.session_state.page_num -= 1
                st.rerun()
        with col3:
            if end < total and st.button("Next ➡️"):
                st.session_state.page_num += 1
                st.rerun()
    else:
        st.write("No results found.")

    # Modal
    if st.session_state.modal_image:
        img = st.session_state.modal_image
        st.markdown(f"""
        <div class="modal">
            <div class="modal-content">
                <img src="{img['url']}">
                <p>{img['caption']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Close"):
            st.session_state.modal_image = None
            st.rerun()

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.write("""
        Lucas Grey Scrap Trading provides sustainable scrap trading services.
        We recycle metals such as copper, aluminum, and steel for small-scale and industrial clients.
    """)

    st.subheader("Organization Chart")
    st.graphviz_chart("""
    digraph {
        node [shape=box, style="rounded,filled", color=maroon, fontcolor=white, fontsize=12, fontname="Arial", fillcolor=black];

        CEO [label="CEO\\nLucas Grey"];
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

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            if not name or not email or not message:
                st.error("Please fill in all fields")
            else:
                st.success("✅ Your message has been sent successfully!")

    st.write("📧 Email: lucasgreyscrap@email.com")
    st.write("📍 Address: Cebu City, Philippines")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# ------------------ FOOTER ------------------
st.markdown('<div class="footer">© 2025 Lucas Grey Scrap Trading. All rights reserved.</div>', unsafe_allow_html=True)
