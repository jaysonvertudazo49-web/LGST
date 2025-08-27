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
    background: linear-gradient(135deg, #111111, #222222); 
    margin:0; 
    padding:0; 
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
.header-title {
    display: flex;
    align-items: center;
}
.header-title img {
    margin-right: 10px;
}
.header-title h1 { 
    margin: 0; 
    color: black; 
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}
.header-buttons {
    display: flex;
    gap: 10px;
}
.header-buttons button {
    background: maroon;
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
    transition: 0.3s;
}
.stButton button:hover {
    background: #a00000;
}

/* Contact form */
.contact-form {
    background: #ffffff;
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
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "descriptions" not in st.session_state:
    st.session_state.descriptions = {}

# ------------------ GITHUB CONFIG ------------------
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except Exception:
    GITHUB_TOKEN = None

REPO_OWNER = "jaysonvertudazo49-web"
REPO_NAME = "LGST"
BRANCH = "main"

IMAGE_DIR = ""

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
    return "/".join([p.strip("/") for p in parts if p is not None and p != ""])

def _raw_url(filename):
    path = _join_path(IMAGE_DIR, filename)
    return f"{RAW_ROOT}/{path}"

def github_list(path=""):
    url = f"{API_ROOT}/contents/{path}" if path else f"{API_ROOT}/contents"
    resp = requests.get(url, headers=_headers(), params={"ref": BRANCH})
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub list failed [{resp.status_code}]: {resp.text}")
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
        if f.get("type") != "file":
            continue
        name = f.get("name", "")
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", name, flags=re.IGNORECASE)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num

def list_pic_urls_sorted():
    """Return list of raw URLs for picX files sorted by X descending (newest first)."""
    try:
        files = github_list(IMAGE_DIR)
    except Exception as e:
        st.error(f"Unable to load image list from GitHub: {e}")
        return []

    pics = []
    for f in files:
        if f.get("type") != "file":
            continue
        name = f.get("name", "")
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", name, flags=re.IGNORECASE)
        if m:
            num = int(m.group(1))
            pics.append((num, name))
    pics.sort(key=lambda x: x[0], reverse=True)  # newest first
    return [_raw_url(name) for _, name in pics]

def load_state_json():
    try:
        file_info = github_get_file("state.json")
        if not file_info:
            return {"descriptions": {}}, None
        content_b64 = file_info.get("content", "")
        sha = file_info.get("sha", None)
        content = base64.b64decode(content_b64).decode("utf-8")
        data = json.loads(content) if content.strip() else {}
        if not isinstance(data, dict):
            data = {}
        if "descriptions" not in data or not isinstance(data["descriptions"], dict):
            data["descriptions"] = {}
        return data, sha
    except Exception as e:
        st.warning(f"Could not load state.json: {e}")
        return {"descriptions": {}}, None

def save_state_json(state_data, sha_before):
    try:
        payload = json.dumps(state_data, ensure_ascii=False, indent=2).encode("utf-8")
        return github_put_file("state.json", payload, "Update state.json", sha=sha_before)
    except RuntimeError as e:
        if sha_before is None:
            payload = json.dumps(state_data, ensure_ascii=False, indent=2).encode("utf-8")
            return github_put_file("state.json", payload, "Create state.json")
        raise

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

# Handle button clicks via query params
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# ------------------ ABOUT PAGE ------------------
if st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.subheader("Who We Are")
    st.write("""
        Lucas Grey Scrap Trading (LGST) is a trusted scrap buying and dismantling company based in Quezon City, Philippines.
    """)
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

# ------------------ HOME PAGE ------------------
elif st.session_state.page == "Home":
    if not st.session_state.images:
        with st.spinner("Loading images from GitHub..."):
            st.session_state.images = list_pic_urls_sorted()

    state_data, _sha = load_state_json()
    repo_descriptions = state_data.get("descriptions", {})

    st.subheader("WELCOME TO LUCAS GREY SCRAP TRADING")

    search_query = st.text_input("Search projects")
    col_clear = st.columns([9, 1.1])
    with col_clear[1]:
        if st.button("Clear Search"):
            search_query = ""
            st.session_state.page_num = 0

    def filename_from_url(url: str) -> str:
        return url.rsplit("/", 1)[-1]

    images = st.session_state.images

    def desc_for_url(url: str) -> str:
        fname = filename_from_url(url)
        return repo_descriptions.get(fname, "")

    filtered_images = images
    if search_query:
        filtered_images = [u for u in images if search_query.lower() in desc_for_url(u).lower()]
        st.session_state.page_num = 0

    images_per_page = 3
    start_idx = st.session_state.page_num * images_per_page
    end_idx = start_idx + images_per_page
    current_images = filtered_images[start_idx:end_idx]
    total_pages = (len(filtered_images) + images_per_page - 1) // images_per_page if filtered_images else 1

    if filtered_images:
        st.markdown(
            f"<p style='text-align:center;'>Page {st.session_state.page_num+1} of {total_pages}</p>",
            unsafe_allow_html=True,
        )
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
                caption = desc_for_url(img_url) or "No description"
                col.markdown(
                    f"""
                    <div class="img-card">
                        <img src="{img_url}" alt="{caption}">
                        <p>{caption}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if col.button("View Details", key=f"view_{img_url}"):
                    st.session_state.view_image = img_url
                    st.rerun()

    if st.session_state.view_image is not None:
        img_url = st.session_state.view_image
        caption = (state_data.get("descriptions", {}) or {}).get(filename_from_url(img_url), "No description")
        st.markdown(
            f"""
            <div class="modal">
                <img src="{img_url}" width="700">
                <p><b>{caption}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Close", key=f"close_{img_url}"):
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
    st.markdown('</div
