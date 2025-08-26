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
}
h1, h2, h3 {
    color: #333;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
button {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ GITHUB SETTINGS ------------------
REPO = "jaysonvertudazo49/LGST"
IMAGE_DIR = "images"
STATE_FILE = "state.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)

# ------------------ HELPERS ------------------
def _headers():
    return {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def _api_url(path): return f"https://api.github.com/repos/{REPO}/contents/{path}"
def _raw_url(filename): return f"https://raw.githubusercontent.com/{REPO}/main/{IMAGE_DIR}/{filename}"
def _join_path(*args): return "/".join(args)

def github_get(path):
    r = requests.get(_api_url(path), headers=_headers())
    if r.status_code == 200:
        return r.json()
    return None

def github_put_file(path, content_bytes, message="Upload file"):
    b64_content = base64.b64encode(content_bytes).decode()
    sha = None
    existing = github_get(path)
    if existing and "sha" in existing:
        sha = existing["sha"]
    payload = {"message": message, "content": b64_content}
    if sha: payload["sha"] = sha
    r = requests.put(_api_url(path), headers=_headers(), data=json.dumps(payload))
    if not r.ok:
        raise Exception(f"GitHub put file failed [{r.status_code}]: {r.text}")
    return r.json()

def load_state_json():
    try:
        res = github_get(STATE_FILE)
        if res and "content" in res:
            content = base64.b64decode(res["content"]).decode()
            return json.loads(content), res["sha"]
    except Exception:
        pass
    return {}, None

def save_state_json(data, sha=None):
    content = json.dumps(data, indent=2).encode()
    b64_content = base64.b64encode(content).decode()
    payload = {"message": "Update state.json", "content": b64_content}
    if sha: payload["sha"] = sha
    r = requests.put(_api_url(STATE_FILE), headers=_headers(), data=json.dumps(payload))
    if not r.ok:
        raise Exception(f"GitHub put file failed [{r.status_code}]: {r.text}")
    return r.json()

def get_latest_pic_number():
    contents = github_get(IMAGE_DIR)
    max_num = 0
    if contents:
        for item in contents:
            m = re.match(r"pic(\d+)\.jpg", item["name"])
            if m:
                num = int(m.group(1))
                if num > max_num: max_num = num
    return max_num

def list_pic_urls_sorted():
    contents = github_get(IMAGE_DIR)
    pics = []
    if contents:
        for item in contents:
            m = re.match(r"pic(\d+)\.jpg", item["name"])
            if m:
                pics.append((int(m.group(1)), item["name"]))
    pics.sort(key=lambda x: x[0])
    return [_raw_url(name) for _, name in pics]

def convert_to_jpg_bytes(uploaded_file):
    if not PIL_AVAILABLE:
        return uploaded_file.getvalue()
    try:
        img = Image.open(uploaded_file)
        rgb = img.convert("RGB")
        buf = BytesIO()
        rgb.save(buf, format="JPEG")
        return buf.getvalue()
    except Exception:
        return uploaded_file.getvalue()

# ------------------ INIT SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "images" not in st.session_state:
    try:
        st.session_state.images = list_pic_urls_sorted()
    except Exception:
        st.session_state.images = []

# ------------------ HEADER / NAV ------------------
st.title("Lucas Grey Scrap Trading")
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

menu = ["Home", "About", "Contact", "Admin"]
choice = st.selectbox("Navigate", menu, index=menu.index(st.session_state.page))
st.session_state.page = choice

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    st.subheader("🏠 Welcome to Lucas Grey Scrap Trading")
    st.write("We specialize in scrap trading and copper wire dismantling services.")
    if st.session_state.images:
        st.subheader("📸 Current Projects")
        state_data, _ = load_state_json()
        descs = state_data.get("descriptions", {})
        for url in st.session_state.images:
            fname = url.split("/")[-1]
            st.image(url, width=400)
            if fname in descs:
                st.caption(descs[fname])

# ------------------ ABOUT PAGE ------------------
elif st.session_state.page == "About":
    st.subheader("ℹ️ About Us")
    st.write("""
        At Lucas Grey Scrap Trading, we are dedicated to:
        * Providing safe and efficient services for every client.
        * Completing projects on time with guaranteed satisfaction.
        * Building long-term, mutually beneficial business relationships.
        * Upholding our social and environmental responsibilities.
    """)
    if st.button("🏠 Back to Home", key="about_back"):
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

# ------------------ CONTACT PAGE ------------------
elif st.session_state.page == "Contact":
    st.subheader("📞 Contact Us")
    st.write("You can reach us at: **lucasgreyscrap@example.com**")
    if st.button("🏠 Back to Home", key="contact_back"):
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

# ------------------ ADMIN PAGE ------------------
elif st.session_state.page == "Admin":
    st.header("🔑 Admin Login" if not st.session_state.is_admin else "📂 Admin Dashboard")

    if not st.session_state.is_admin:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", key="admin_login_btn"):
            if username == "admin" and password == "1234":
                st.session_state.is_admin = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        # Back to home when not logged in
        if st.button("🏠 Back to Home", key="admin_back_home_not_logged"):
            st.session_state.page = "Home"
            st.query_params.clear()
            st.rerun()

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

            if st.button("Save Project", key="save_project_btn"):
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
                    try:
                        st.session_state.images = list_pic_urls_sorted()
                    except Exception:
                        st.session_state.images.extend(new_urls)
                    st.success("✅ Project(s) uploaded to GitHub successfully!")
                    st.rerun()

        # ------------------ NAVIGATION BUTTONS ------------------
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Back to Home", key="admin_back_home_logged"):
                st.session_state.page = "Home"
                st.query_params.clear()
                st.rerun()

        with col2:
            if st.button("🚪 Logout", key="admin_logout_btn"):
                st.session_state.is_admin = False
                st.session_state.page = "Home"
                st.query_params.clear()
                st.rerun()


