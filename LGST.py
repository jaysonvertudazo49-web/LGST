import streamlit as st
import requests
import base64
import json
import re
from io import BytesIO

# Pillow for image conversion to JPG
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Lucas Grey Scrap Trading", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
/* Apply to main content area in Streamlit */
.stApp {
    background: linear-gradient(-45deg, #0f0f0f, #800000, #1a1a1a, #4d0000);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: white;  /* makes text visible */
}

/* Keyframes for smooth shifting */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Optional glowing overlay effect */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    animation: glowMove 12s linear infinite;
    z-index: 0;
}

/* Glow movement */
@keyframes glowMove {
    0% { transform: translate(-20%, -20%) scale(1); }
    50% { transform: translate(20%, 20%) scale(1.2); }
    100% { transform: translate(-20%, -20%) scale(1); }
}

/* Header */
.header-container {
    background: linear-gradient(135deg, black, maroon);
    padding: 15px 30px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between; 
    align-items: center;
}
.header-title {
    display: flex;
    align-items: center;
}
.header-title img {
    margin-right: 15px;
    width: 200px;
    height: auto;
}
.header-title h1 { 
    margin: 0; 
    color: white; 
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}
.header-buttons {
    display: flex;
    gap: 10px;
}
.header-buttons button {
    background: black;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: bold;
    border: none;
    cursor: pointer;
}
.header-buttons button:hover {
    background: #a00000;
}

/* Gallery */
.img-card {
    background: black;
    border-radius: 12px;
    padding: 10px;
    min-height: 280px;
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
    max-height: 180px;
    object-fit: cover;
    border-radius: 10px;
}

/* Modal */
.modal {
    background: black;
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
    background: maroon;
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: bold;
    border: none;
    transition: all 0.2s ease;
    cursor: pointer;
}

/* Hover effect */
.stButton button:hover {
    background: #a00000;
    transform: scale(1.05);
}

/* Click effect (press down) */
.stButton button:active {
    transform: scale(0.9);       /* shrink */
    background: #660000;         /* darker */
    box-shadow: 0 2px 8px rgba(0,0,0,0.4) inset; /* pressed look */
}


.contact-form {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    max-width: 500px;
    margin: auto;
    color: white;  /* 👈 makes all text inside white */
}

/* Section headers */
h2 { 
    color: white; 
    font-size: 1.8em; 
    margin-top: 15px; 
    margin-bottom: 10px; 
    border-bottom: 2px solid #800000; 
    padding-bottom: 5px; 
}

h2 {
    color: white !important;
}

/* Make st.subheader text white */
h3 {
    color: white !important;
}

/* Make st.markdown text white */
.stMarkdown, .stMarkdown p {
    color: white !important;
}

/* Target only vision/mission text */
.vision-text, .mission-text {
    color: white !important;
}

/* Force all text white */
body, p, h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: white; 
    text-align: center;
    padding: 15px;
    font-size: 14px;
    font-family: 'Arial', sans-serif;
    background: url("https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png") no-repeat center center;
    background-size: cover;
    background-color: rgba(0, 0, 0, 0.6); /* fallback overlay */
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = []  # list of raw URLs
if "page_num" not in st.session_state:
    st.session_state.page_num = 0
if "view_image" not in st.session_state:
    st.session_state.view_image = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ------------------ GITHUB CONFIG ------------------
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except Exception:
    GITHUB_TOKEN = None

REPO_OWNER = "jaysonvertudazo49-web"
REPO_NAME = "LGST"
BRANCH = "main"

IMAGE_DIR = ""  # root directory

API_ROOT = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
RAW_ROOT = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}"

def _headers():
    if not GITHUB_TOKEN:
        return {"Accept": "application/vnd.github+json"}
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def _join_path(*parts):
    return "/".join([p.strip("/") for p in parts if p])

def _raw_url(filename):
    path = _join_path(IMAGE_DIR, filename)
    return f"{RAW_ROOT}/{path}"

def github_list(path=""):
    url = f"{API_ROOT}/contents/{path}" if path else f"{API_ROOT}/contents"
    resp = requests.get(url, headers=_headers(), params={"ref": BRANCH})
    resp.raise_for_status()
    return resp.json()

def github_get_file(path):
    url = f"{API_ROOT}/contents/{path}"
    resp = requests.get(url, headers=_headers(), params={"ref": BRANCH})
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 404:
        return None
    else:
        raise RuntimeError(f"GitHub get file failed [{resp.status_code}]: {resp.text}")

def github_put_file(path, content_bytes, message, sha=None):
    url = f"{API_ROOT}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode("utf-8"),
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    resp = requests.put(url, headers=_headers(), data=json.dumps(data))
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        raise RuntimeError(f"GitHub put file failed [{resp.status_code}]: {resp.text}")

def get_latest_pic_number():
    try:
        files = github_list(IMAGE_DIR)
    except Exception as e:
        st.error(f"Unable to list repository contents: {e}")
        return 0
    max_num = 0
    for f in files:
        if f.get("type") == "file":
            m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", f["name"], flags=re.IGNORECASE)
            if m:
                max_num = max(max_num, int(m.group(1)))
    return max_num

def list_pic_urls_sorted():
    try:
        files = github_list(IMAGE_DIR)
    except Exception as e:
        st.error(f"Unable to load image list from GitHub: {e}")
        return []
    pics = []
    for f in files:
        if f.get("type") == "file":
            m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", f["name"], flags=re.IGNORECASE)
            if m:
                pics.append((int(m.group(1)), f["name"]))
    pics.sort(key=lambda x: x[0], reverse=True)
    return [_raw_url(name) for _, name in pics]

def load_state_json():
    try:
        file_info = github_get_file("state.json")
        if not file_info:
            return {"descriptions": {}, "messages": []}, None
        content_b64 = file_info["content"]
        sha = file_info.get("sha")
        content = base64.b64decode(content_b64).decode("utf-8")
        data = json.loads(content) if content.strip() else {}
        if "descriptions" not in data or not isinstance(data["descriptions"], dict):
            data["descriptions"] = {}
        if "messages" not in data or not isinstance(data["messages"], list):
            data["messages"] = []
        return data, sha
    except Exception as e:
        st.warning(f"Could not load state.json: {e}")
        return {"descriptions": {}, "messages": []}, None

def save_state_json(state_data, sha_before):
    payload = json.dumps(state_data, ensure_ascii=False, indent=2).encode("utf-8")
    return github_put_file("state.json", payload, "Update state.json", sha=sha_before)

def convert_to_jpg_bytes(uploaded_file):
    data = uploaded_file.getvalue()
    if not PIL_AVAILABLE:
        return data
    try:
        with Image.open(BytesIO(data)) as im:
            rgb = im.convert("RGB")
            buf = BytesIO()
            rgb.save(buf, format="JPEG", quality=92, optimize=True)
            return buf.getvalue()
    except Exception:
        return data

# ------------------ HEADER ------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png" width="80">
        <h1>LUCAS GREY SCRAP TRADING</h1>
    </div>
    <div class="header-buttons">
        <form action="" method="get">
            <button type="submit" name="page" value="About">About</button>
            <button type="submit" name="page" value="Contact">Contact Us</button>
            <button type="submit" name="page" value="Admin">Admin</button>
        </form>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# Handle query param buttons
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# ------------------ ABOUT PAGE ------------------
if st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.subheader("Who We Are")
    st.write("""
        Lucas Grey Scrap Trading (LGST) is a trusted scrap buying and dismantling company based in Quezon City, Philippines. We specialize in the purchase of scrap materials, 
        dismantling of copper wires, and hauling services of unserviceable equipment and properties.
        With years of hands-on experience, we have proudly served both private companies and government agencies—including hospitals and public institutions—earning a reputation for honesty, 
        reliability, and competitive pricing. Our strong workforce and organized system ensure that every project is handled with efficiency, professionalism, and care for the environment.
    """)
    st.subheader("Our Mission")
    st.info("""To deliver top-quality scrap trading and copper wire dismantling that prioritize client satisfaction.
        We are committed to honesty, safety, and efficiency in every transaction, ensuring value and trust in our long-term partnerships.
    """)
    st.subheader("Our Vision")
    st.success("""To become one of the most recognized and respected service providers in the scrap and dismantling industry in the Philippines—offering excellence, 
        sustainability, and integrity while upholding our responsibility to society and the environment.
    """)
    st.subheader("Core Values")
    st.markdown("""
        * Integrity & Honesty – We uphold transparency and fairness in every deal.
        * Customer Priority – Our clients’ needs and satisfaction are always at the center of our service.
        * Excellence in Service – We are committed to delivering high-quality work without compromise.
        * Safety & Responsibility – We ensure safe, compliant, and environmentally responsible practices in all operations.
        * Commitment to Relationships – We aim to build long-term partnerships based on trust, reliability, and mutual growth.
    """)
    st.subheader("Brief History")
    st.write("""
        Lucas Grey Scrap Trading was formally established in 2021 by Von Ryan Veloso, following more than four years of active experience in the scrap and dismantling business. 
        Starting from small transactions involving scrap and unserviceable goods, LGST expanded its services to include large-scale dismantling projects.
        Today, the company manages a warehouse team of over 40 staff members, operates with modern hauling and transport vehicles, and continues to serve both government and private institutions. 
        Accredited by PHILGEPS, LGST has built its reputation on competitive pricing, timely service completion, and client satisfaction.
    """)
    st.subheader("What We Do")
    st.markdown("""
        * Scrap Buying – Purchase of various scrap materials, including copper wires, IT equipment, office supplies, and unserviceable vehicles.
        * Copper Wire Dismantling – Safe and efficient dismantling of copper wires to recover valuable materials.
        * Sustainable Recycling – We support environmental responsibility by ensuring proper recycling and waste management practices.
    """)
    st.subheader("Our Commitment")
    st.markdown("""
        ### At Lucas Grey Scrap Trading, we are dedicated to:
        
        ✅ Providing safe and efficient services for every client.  
        ⏱️ Completing projects on time with guaranteed satisfaction.  
        🤝 Building long-term, mutually beneficial business relationships.  
        🌍 Upholding our social and environmental responsibilities.  
        """)

if st.button("⬅️ Back to Home"):
    st.session_state.page = "Home"
    st.query_params.clear()
    st.rerun()

# ------------------ HOME PAGE ------------------
elif st.session_state.page == "Home":
    if not st.session_state.images:
        with st.spinner("Loading images..."):
            st.session_state.images = list_pic_urls_sorted()
    state_data, _ = load_state_json()
    repo_descriptions = state_data.get("descriptions", {})
    st.subheader("WELCOME TO LUCAS GREY SCRAP TRADING")
    search_query = st.text_input("", "")
    if st.button("Clear Search"):
        search_query = ""
        st.session_state.page_num = 0
    def filename_from_url(url): return url.rsplit("/", 1)[-1]
    def desc_for_url(url): return repo_descriptions.get(filename_from_url(url), "")
    images = st.session_state.images
    filtered_images = [u for u in images if search_query.lower() in desc_for_url(u).lower()] if search_query else images
    st.session_state.page_num = 0 if search_query else st.session_state.page_num
    per_page = 3
    start = st.session_state.page_num * per_page
    end = start + per_page
    current_images = filtered_images[start:end]
    total_pages = (len(filtered_images) + per_page - 1) // per_page if filtered_images else 1
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
        if st.button("Next ➡️", disabled=end >= len(filtered_images)):
            st.session_state.page_num += 1
            st.rerun()
    if filtered_images:
        st.subheader("CURRENT PROJECT")
        cols = st.columns(min(len(current_images), 3))
        for idx, col in enumerate(cols):
            if idx < len(current_images):
                url = current_images[idx]
                caption = desc_for_url(url) or "No description"
                col.markdown(f"""<div class="img-card"><img src="{url}"><p>{caption}</p></div>""", unsafe_allow_html=True)
                if col.button("View Details", key=f"view_{url}"):
                    st.session_state.view_image = url
                    st.rerun()
    if st.session_state.view_image:
        url = st.session_state.view_image
        caption = repo_descriptions.get(filename_from_url(url), "No description")
        st.markdown(f"""<div class="modal"><img src="{url}" width="700"><p><b>{caption}</b></p></div>""", unsafe_allow_html=True)
        if st.button("Close"):
            st.session_state.view_image = None
            st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        attachments = st.file_uploader(
            "Attach files or images", 
            accept_multiple_files=True, 
            type=["jpg","jpeg","png","pdf","docx","txt"]
        )
        submit = st.form_submit_button("Send Message")

        if submit:
            if name and email and message:
                state_data, sha = load_state_json()

                # Save uploaded files to GitHub
                attachment_names = []
                if attachments:
                    for file in attachments:
                        file_bytes = file.getvalue()
                        safe_name = f"msg_{len(state_data['messages'])+1}_{file.name}"
                        github_put_file(f"attachments/{safe_name}", file_bytes, f"Add attachment {safe_name}")
                        attachment_names.append(safe_name)

                # Store message + attachments in state.json
                state_data["messages"].append({
                    "name": name,
                    "email": email,
                    "message": message,
                    "attachments": attachment_names
                })

                try:
                    save_state_json(state_data, sha)
                    st.success(f"✅ Thank you, {name}! Your message has been sent.")
                except Exception as e:
                    st.error(f"⚠️ Failed to save: {e}")
            else:
                st.error("Please fill out all fields.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(""" Email: **vonryan0110@gmail.com**  
 Address: Amlac Ville Payatas B, Quezon City""")
    st.markdown(""" Tel #: 85365516, 84632485, 84632412""")
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()


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
        st.subheader("📩 Received Messages")
        state_data, _ = load_state_json()
        msgs = state_data.get("messages", [])

        if msgs:
            for i, m in enumerate(reversed(msgs), 1):
                st.markdown(f"""
                **Message {i}:**
                - 👤 {m['name']}
                - 📧 {m['email']}
                - 📝 {m['message']}
                """)

                if m.get("attachments"):
                    st.markdown("📎 **Attachments:**")
                    for att in m["attachments"]:
                        url = _raw_url(f"attachments/{att}")
                        if att.lower().endswith((".jpg", ".jpeg", ".png")):
                            st.image(url, caption=att, use_container_width=True)
                        else:
                            st.markdown(f"- [{att}]({url})")
                st.markdown("---")
        else:
            st.info("No messages yet.")

        # Project upload feature
        if not GITHUB_TOKEN:
            st.error("Missing GITHUB_TOKEN in st.secrets.")

        uploaded_files = st.file_uploader(
            "Upload project images", 
            accept_multiple_files=True, 
            type=["jpg","jpeg","png"]
        )

        if uploaded_files:
            descs = {f.name: st.text_area(f"Description for {f.name}") for f in uploaded_files}
            if st.button("Save Project"):
                state_data, sha = load_state_json()
                latest = get_latest_pic_number()
                for i, file in enumerate(uploaded_files):
                    new_name = f"pic{latest+i+1}.jpg"
                    img_bytes = convert_to_jpg_bytes(file)
                    github_put_file(new_name, img_bytes, f"Add {new_name}")
                    if descs[file.name].strip():
                        state_data["descriptions"][new_name] = descs[file.name]
                save_state_json(state_data, sha)
                st.success("✅ Uploaded successfully!")
                st.session_state.images = list_pic_urls_sorted()
                st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Home"):
                st.session_state.page = "Home"
                st.query_params.clear()
                st.rerun()
        with col2:
            if st.button("🚪 Logout"): 
                st.session_state.is_admin = False; st.rerun()


    <div class="footer">
             2025 Lucas Grey Scrap Trading. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )
















