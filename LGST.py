import streamlit as st
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
/* Header */
.header-container {
    background: linear-gradient(90deg, #800000, #ffffff);
    padding: 20px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.header-container h1 { color: black; font-size: 2.5em; text-align: center; flex: 1; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);}
.header-container img { height: 70px; }

/* Buttons */
.stButton>button { background: #800000; color:#000; font-weight:bold; border:none; border-radius:8px; padding:5px 15px; }
.stButton>button:hover { text-decoration: underline; background:none; }

/* Gallery */
.img-card { background:white; border-radius:10px; padding:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1); transition:0.3s; }
.img-card:hover { transform:translateY(-5px); box-shadow:0 4px 10px rgba(0,0,0,0.2); border:2px solid #800000;}
.img-card img { width:100%; height:200px; object-fit:contain; border-radius:8px; }
.img-caption { margin-left:20px; font-size:1em; color:#333; }

/* Modal Simulation */
.modal-container {
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background: rgba(0,0,0,0.7);
    display:flex;
    justify-content:center;
    align-items:center;
    z-index:1000;
}
.modal-content {
    background:white;
    border-radius:12px;
    padding:20px;
    display:flex;
    gap:20px;
    max-width:90%;
    max-height:90%;
}
.modal-content img { max-width:700px; max-height:80vh; object-fit:contain; }
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state: st.session_state.page = "Home"
if "images" not in st.session_state: st.session_state.images = []
if "page_num" not in st.session_state: st.session_state.page_num = 0
if "view_image" not in st.session_state: st.session_state.view_image = None

# ------------------ HEADER ------------------
col1, col2, col3 = st.columns([2,6,2])
with col1: st.image("https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png", width=80)
with col2: st.markdown("<h1 style='text-align:center;'>LUCAS GREY SCRAP TRADING</h1>", unsafe_allow_html=True)
with col3:
    if st.button("Home"): st.session_state.page="Home"; st.rerun()
    if st.button("About"): st.session_state.page="About"; st.rerun()
    if st.button("Contact Us"): st.session_state.page="Contact"; st.rerun()
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ HOME PAGE ------------------
if st.session_state.page=="Home":
    repo_url = "https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/"
    max_images = 15
    possible_exts = ["jpg","jpeg","png"]

    # Load images
    if not st.session_state.images:
        with st.spinner("Loading images..."):
            for i in range(1, max_images+1):
                for ext in possible_exts:
                    url=f"{repo_url}pic{i}.{ext}"
                    try:
                        if requests.head(url).status_code==200:
                            st.session_state.images.append(url)
                            break
                    except: pass
    images=st.session_state.images
    image_descriptions={
        0:"Pic 1: Vroom Vroom",1:"Pic 2: Yellow boys",2:"Pic 3: Blackshirts",
        3:"Pic 4: I love red",4:"Pic 5: Blue is my color",5:"Pic 6: Batelec 1",
        6:"Pic 7: Meralco",7:"Pic 8: Stainless steel scraps",8:"Pic 9: Copper pipes",
        9:"Pic 10: Assorted metal alloys",10:"Pic 11: Scrap aluminum sheets",11:"Pic 12: High-grade steel beams",
        12:"Pic 13: Copper radiators",13:"Pic 14: Mixed non-ferrous metals",14:"Pic 15: Scrap metal sorted"
    }

    # Search
    st.subheader("Search Images")
    search_query=st.text_input("Filter images by keyword","")
    filtered_images=[img for idx,img in enumerate(images) if search_query.lower() in image_descriptions.get(idx,"").lower()] if search_query else images

    # Pagination
    images_per_page=3
    start_idx=st.session_state.page_num*images_per_page
    end_idx=start_idx+images_per_page
    current_images=filtered_images[start_idx:end_idx]
    total_pages=(len(filtered_images)+images_per_page-1)//images_per_page
    st.markdown(f"<p style='text-align:center;'>Page {st.session_state.page_num+1} of {total_pages}</p>", unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,10,1])
    with col1:
        if st.button("⬅️ Back", disabled=st.session_state.page_num==0): st.session_state.page_num-=1; st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=end_idx>=len(filtered_images)): st.session_state.page_num+=1; st.rerun()

    # Gallery
    st.subheader("Image Gallery")
    img_cols=st.columns(min(len(current_images),3))
    for idx,col in enumerate(img_cols):
        if idx<len(current_images):
            img_url=current_images[idx]
            absolute_idx=images.index(img_url)
            col.markdown(f"<div class='img-card'><img src='{img_url}'></div>", unsafe_allow_html=True)
            if col.button("View Details", key=f"view_{absolute_idx}"):
                st.session_state.view_image=absolute_idx
                st.rerun()

    # Modal overlay
    if st.session_state.view_image is not None:
        idx=st.session_state.view_image
        img_url=images[idx]
        caption=image_descriptions.get(idx,"No description")
        st.markdown("<div class='modal-container'>", unsafe_allow_html=True)
        col_img,col_caption=st.columns([2,1])
        with col_img: st.image(img_url,width=700)
        with col_caption:
            st.markdown(f"**{caption}**")
            if st.button("Close"): st.session_state.view_image=None; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page=="About":
    st.header("About Lucas Grey Scrap Trading")
    st.write("""
        Lucas Grey Scrap Trading provides sustainable scrap trading services.
        We recycle metals such as copper, aluminum, and steel for small-scale and industrial clients.
        **Services Offered:**
        - Scrap metal collection
        - Sorting and processing
        - Wholesale and retail supply
        - Partnerships for industrial recycling
    """)
    if st.button("⬅️ Back to Home"): st.session_state.page="Home"; st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page=="Contact":
    st.header("Contact Us")
    with st.form("contact_form"):
        name=st.text_input("Name"); email=st.text_input("Email"); message=st.text_area("Message")
        if st.form_submit_button("Send Message"):
            if name and email and message: st.success(f"Thank you {name}! We'll reply to {email}.")
            else: st.error("Please fill out all fields.")
    st.markdown("📧 Email: **charlottevazquez78@gmail.com**  \n📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  \n© 2025 Lucas Grey Scrap Trading")
    if st.button("⬅️ Back to Home"): st.session_state.page="Home"; st.rerun()
