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
/* Global */
body { 
    font-family: 'Arial', sans-serif; 
    background-color: #f9f9f9;
    margin: 0; 
    padding: 0;
}

/* Header */
.header-container {
    background: white;
    padding: 15px 30px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between; 
    align-items: center;
}

/* Gallery */
.gallery-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
}
.gallery-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.gallery-card img {
    width: 100%;
    border-radius: 8px;
    cursor: pointer;
}

/* Modal */
.modal {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(0,0,0,0.7);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 12px;
    max-width: 600px;
}

/* Search */
.search-container {
    margin: 20px 0;
}

/* Contact */
.contact-container {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "images" not in st.session_state:
    st.session_state.images = []
if "view_image" not in st.session_state:
    st.session_state.view_image = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ------------------ GITHUB CONFIG ------------------
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = "jaysonvertudazo49-web/LGST"
GITHUB_API = "https://api.github.com"
IMAGE_DIR = "project"
STATE_FILE = "state.json"

def github_headers():
    return {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def github_list(path):
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/{path}"
    r = requests.get(url, headers=github_headers())
    r.raise_for_status()
    return r.json()

def github_get(path):
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/{path}"
    r = requests.get(url, headers=github_headers())
    if r.status_code == 404:
        return None, None
    r.raise_for_status()
    data = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content, data["sha"]

def github_put(path, content_b64, message, sha=None):
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/{path}"
    payload = {"message": message, "content": content_b64}
    if sha: payload["sha"] = sha
    r = requests.put(url, headers=github_headers(), json=payload)
    r.raise_for_status()
    return r.json()

# ------------------ STATE JSON ------------------
def load_state():
    text, _ = github_get(STATE_FILE)
    if not text:
        return {}
    return json.loads(text)

def save_state(state):
    text, sha = github_get(STATE_FILE)
    content_b64 = base64.b64encode(json.dumps(state, indent=2).encode()).decode()
    return github_put(STATE_FILE, content_b64, "Update state.json", sha)

# ------------------ IMAGE HANDLING ------------------
def _raw_url(filename):
    return f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{IMAGE_DIR}/{filename}"

def list_pic_urls_sorted():
    """Return list of raw URLs for picX files sorted newest first."""
    try:
        files = github_list(IMAGE_DIR)
    except Exception as e:
        st.error(f"Unable to load image list from GitHub: {e}")
        return []
    pics = []
    for f in files:
        if f.get("type") != "file": continue
        name = f.get("name", "")
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", name, flags=re.IGNORECASE)
        if m:
            num = int(m.group(1))
            pics.append((num, name))
    pics.sort(key=lambda x: x[0], reverse=True)   # NEWEST first
    return [_raw_url(name) for _, name in pics]

def get_next_pic_name():
    try:
        files = github_list(IMAGE_DIR)
    except: return "pic1.jpg"
    maxn = 0
    for f in files:
        name = f.get("name","")
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", name, flags=re.IGNORECASE)
        if m: maxn = max(maxn, int(m.group(1)))
    return f"pic{maxn+1}.jpg"

def upload_image_and_description(file, description):
    if not file: return
    if PIL_AVAILABLE:
        image = Image.open(file).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        content = buffer.getvalue()
    else:
        content = file.read()
    filename = get_next_pic_name()
    content_b64 = base64.b64encode(content).decode()
    github_put(f"{IMAGE_DIR}/{filename}", content_b64, f"Upload {filename}")
    state = load_state()
    state[filename] = {"description": description}
    save_state(state)
    st.success("✅ Uploaded successfully!")

# ------------------ UI FUNCTIONS ------------------
def show_header():
    with st.container():
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("<h2>Lucas Grey Scrap Trading</h2>", unsafe_allow_html=True)
        with col2:
            st.button("Home", on_click=lambda: set_page("Home"))
            st.button("About", on_click=lambda: set_page("About"))
            st.button("Contact Us", on_click=lambda: set_page("Contact"))
            st.button("Admin", on_click=lambda: set_page("Admin"))

def set_page(page):
    st.session_state.page = page

def show_gallery():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    query = st.text_input("🔍 Search projects by description", "").lower()
    st.markdown('</div>', unsafe_allow_html=True)

    urls = list_pic_urls_sorted()
    state = load_state()
    if query:
        urls = [u for u in urls if query in state.get(u.split("/")[-1], {}).get("description","").lower()]

    per_page = 6
    total_pages = (len(urls) + per_page - 1) // per_page
    page = st.session_state.get("gallery_page", 1)
    if page < 1: page = 1
    if page > total_pages: page = total_pages
    start = (page-1)*per_page
    end = start + per_page
    subset = urls[start:end]

    st.markdown('<div class="gallery-container">', unsafe_allow_html=True)
    for url in subset:
        filename = url.split("/")[-1]
        desc = state.get(filename, {}).get("description","")
        st.markdown(f"""
        <div class="gallery-card">
            <img src="{url}" onclick="window.location.href='?view={filename}'"/>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("⬅ Previous") and page>1:
            st.session_state.gallery_page = page-1
            st.experimental_rerun()
    with col2: st.write(f"Page {page}/{total_pages}")
    with col3:
        if st.button("Next ➡") and page<total_pages:
            st.session_state.gallery_page = page+1
            st.experimental_rerun()

def show_modal():
    if st.session_state.view_image:
        filename = st.session_state.view_image
        url = _raw_url(filename)
        state = load_state()
        desc = state.get(filename, {}).get("description","")
        st.markdown(f"""
        <div class="modal">
          <div class="modal-content">
            <img src="{url}" style="width:100%; border-radius:8px"/>
            <p>{desc}</p>
            <button onclick="window.location.href='/'">Close</button>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------ PAGES ------------------
if st.session_state.page == "Home":
    show_header()
    st.subheader("📌 Current Projects")
    show_gallery()
    show_modal()

elif st.session_state.page == "About":
    show_header()
    st.subheader("🏢 About Us")
    st.info("At Lucas Grey Scrap Trading, we are dedicated to: ...")

elif st.session_state.page == "Contact":
    show_header()
    st.subheader("📞 Contact Us")
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Send"):
        st.success("✅ Thank you for contacting us!")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Admin":
    show_header()
    st.header("🔑 Admin Login" if not st.session_state.is_admin else "📂 Admin Dashboard")

    if not st.session_state.is_admin:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username=="admin" and password=="1234":
                st.session_state.is_admin = True
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        uploaded = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])
        desc = st.text_area("Description")
        if st.button("Upload"):
            upload_image_and_description(uploaded, desc)
        if st.button("🏠 Back to Home"):
            set_page("Home")
            st.experimental_rerun()
        if st.button("🚪 Logout"):
            st.session_state.is_admin = False
            set_page("Home")
            st.experimental_rerun()

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("© 2025 Lucas Grey Scrap Trading. All Rights Reserved.")
