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
    background: linear-gradient(90deg, #800000, #ffffff);
    padding: 15px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
    background: maroon;
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
    background: maroon;
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
    st.session_state.images = []  # list of raw URLs
if "page_num" not in st.session_state:
    st.session_state.page_num = 0
if "view_image" not in st.session_state:
    st.session_state.view_image = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "descriptions" not in st.session_state:
    # maps filename (e.g., "pic12.jpg") -> description
    st.session_state.descriptions = {}

# ------------------ GITHUB CONFIG ------------------
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except Exception:
    GITHUB_TOKEN = None

REPO_OWNER = "jaysonvertudazo49-web"
REPO_NAME = "LGST"
BRANCH = "main"

# If your images live in a subfolder, set IMAGE_DIR = "images"
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
    # safe join for GitHub paths (no leading slash)
    return "/".join([p.strip("/") for p in parts if p is not None and p != ""])

def _raw_url(filename):
    path = _join_path(IMAGE_DIR, filename)
    return f"{RAW_ROOT}/{path}"

def github_list(path=""):
    """List files in a path on a specific branch."""
    url = f"{API_ROOT}/contents/{path}" if path else f"{API_ROOT}/contents"
    resp = requests.get(url, headers=_headers(), params={"ref": BRANCH})
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub list failed [{resp.status_code}]: {resp.text}")
    return resp.json()

def github_get_file(path):
    """Get a single file metadata including sha and content (base64)."""
    url = f"{API_ROOT}/contents/{path}"
    resp = requests.get(url, headers=_headers(), params={"ref": BRANCH})
    if resp.status_code == 200:
        return resp.json()  # includes 'sha' and 'content' (base64)
    elif resp.status_code == 404:
        return None
    else:
        raise RuntimeError(f"GitHub get file failed [{resp.status_code}]: {resp.text}")

def github_put_file(path, content_bytes, message, sha=None):
    """Create or update a file via the Contents API."""
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
    """Check repo for highest existing picX.(jpg|jpeg|png) in IMAGE_DIR and return that number."""
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
    """Return list of raw URLs for picX files sorted by X ascending."""
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
    pics.sort(key=lambda x: x[0])
    return [_raw_url(name) for _, name in pics]

def load_state_json():
    """Load existing state.json, return dict. If not found, return default structure."""
    try:
        file_info = github_get_file("state.json")
        if not file_info:
            return {"descriptions": {}}, None  # content, sha
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
    """Update state.json (requires sha) or create if missing."""
    try:
        payload = json.dumps(state_data, ensure_ascii=False, indent=2).encode("utf-8")
        return github_put_file("state.json", payload, "Update state.json", sha=sha_before)
    except RuntimeError as e:
        # If file didn't exist (sha None) and server expects no sha, retry without sha
        if sha_before is None:
            payload = json.dumps(state_data, ensure_ascii=False, indent=2).encode("utf-8")
            return github_put_file("state.json", payload, "Create state.json")
        raise

def convert_to_jpg_bytes(uploaded_file):
    """
    Convert any uploaded image to JPEG bytes.
    If Pillow isn't available, return original bytes and hope it's already JPEG.
    """
    data = uploaded_file.getvalue()
    if not PIL_AVAILABLE:
        return data  # fallback
    try:
        with Image.open(BytesIO(data)) as im:
            # Convert to RGB to avoid issues with PNG transparency / P mode
            rgb = im.convert("RGB")
            buf = BytesIO()
            rgb.save(buf, format="JPEG", quality=92, optimize=True)
            return buf.getvalue()
    except Exception:
        # If conversion fails, return original
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
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

# ------------------ HOME PAGE ------------------
elif st.session_state.page == "Home":
    # Load images from GitHub (only once)
    if not st.session_state.images:
        with st.spinner("Loading images from GitHub..."):
            st.session_state.images = list_pic_urls_sorted()

    # Load state.json to bring in persistent descriptions
    state_data, _sha = load_state_json()
    repo_descriptions = state_data.get("descriptions", {})

    st.subheader("WELCOME TO LUCAS GREY SCRAP TRADING")

    # Search
    search_query = st.text_input("", "")
    col_clear = st.columns([9, 1.1])
    with col_clear[1]:
        if st.button("Clear Search"):
            search_query = ""
            st.session_state.page_num = 0

    # Build a helper: URL -> filename
    def filename_from_url(url: str) -> str:
        return url.rsplit("/", 1)[-1]

    images = st.session_state.images

    # Filtering by description (from state.json)
    def desc_for_url(url: str) -> str:
        fname = filename_from_url(url)
        return repo_descriptions.get(fname, "")

    filtered_images = images
    if search_query:
        filtered_images = [u for u in images if search_query.lower() in desc_for_url(u).lower()]
        st.session_state.page_num = 0

    # Pagination
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

    # Pagination buttons
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("⬅️ Back", disabled=st.session_state.page_num == 0):
            st.session_state.page_num -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=end_idx >= len(filtered_images)):
            st.session_state.page_num += 1
            st.rerun()

    # Display images
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

    # Modal
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        📧 Email: **vonryan0110@gmail.com**  
        📍 Address: Blk-5 Lot-7 Sta. Fe st. Amlac Ville Payatas B, Quezon City  
    """)

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
        if not GITHUB_TOKEN:
            st.error("Missing GITHUB_TOKEN in st.secrets. Add it first to enable uploads.")
        uploaded_files = st.file_uploader(
            "Upload new project images (they will be renamed to picX.jpg)",
            accept_multiple_files=True,
            type=["jpg", "jpeg", "png"]
        )

        descriptions_local = {}
        if uploaded_files:
            for i, file in enumerate(uploaded_files):
                desc = st.text_area(f"Description for {file.name}", key=f"desc_{i}")
                descriptions_local[file.name] = desc

            if st.button("Save Project"):
                if not GITHUB_TOKEN:
                    st.stop()

                # Load state.json (existing)
                state_data, state_sha = load_state_json()
                if "descriptions" not in state_data or not isinstance(state_data["descriptions"], dict):
                    state_data["descriptions"] = {}

                # Determine latest pic number
                latest_num = get_latest_pic_number()

                # Upload each file -> pic{num}.jpg
                new_urls = []
                errors = []
                for i, file in enumerate(uploaded_files):
                    file_num = latest_num + i + 1
                    new_filename = f"pic{file_num}.jpg"

                    # Convert to jpg bytes
                    img_bytes = convert_to_jpg_bytes(file)

                    # Upload image
                    img_path = _join_path(IMAGE_DIR, new_filename)
                    try:
                        github_put_file(
                            img_path,
                            img_bytes,
                            message=f"Add {new_filename}"
                        )
                        # Update state.json descriptions
                        desc_value = descriptions_local.get(file.name, "").strip()
                        if desc_value:
                            state_data["descriptions"][new_filename] = desc_value
                        new_urls.append(_raw_url(new_filename))
                    except Exception as e:
                        errors.append(f"{new_filename}: {e}")

                # Save updated state.json
                try:
                    save_state_json(state_data, state_sha)
                except Exception as e:
                    errors.append(f"state.json update failed: {e}")

                if errors:
                    st.error("Some items failed to upload:\n- " + "\n- ".join(errors))
                if new_urls:
                    # Refresh local gallery list (merge and re-sort by pic number)
                    try:
                        st.session_state.images = list_pic_urls_sorted()
                    except Exception:
                        # Fallback: just append the new ones
                        st.session_state.images.extend(new_urls)
                    st.success("✅ Project(s) uploaded to GitHub successfully!")
                    st.rerun()

                if st.button("Logout"):
                    st.session_state.is_admin = False
                    st.session_state.page = "Home"  # set to Home page
                    st.rerun()


# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
    © 2025 Lucas Grey Scrap Trading. All rights reserved.
</div>
""", unsafe_allow_html=True)






