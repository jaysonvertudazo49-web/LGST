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
/* Apply to main content area */
.stApp {
    background: linear-gradient(-45deg, #0f0f0f, #FFFFFF, #1a1a1a, #4d0000);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: white;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    animation: glowMove 12s linear infinite;
    z-index: 0;
}
@keyframes glowMove {
    0% { transform: translate(-20%, -20%) scale(1); }
    50% { transform: translate(20%, 20%) scale(1.2); }
    100% { transform: translate(-20%, -20%) scale(1); }
}
.header-container {
    background: linear-gradient(135deg, black, maroon);
    padding: 15px 30px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between; 
    align-items: center;
}
.header-title { display: flex; align-items: center; }
.header-title img { margin-right: 15px; width: 200px; height: auto; }
.header-title h1 { margin: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
.header-buttons { display: flex; gap: 10px; }
.header-buttons button {
    background: black; color: white; border-radius: 8px;
    padding: 6px 14px; font-weight: bold; border: none; cursor: pointer;
}
.header-buttons button:hover { background: #a00000; }
.img-card {
    background: black; border-radius: 20px; padding: 20px;
    min-height: 280px; display: flex; flex-direction: row;
    align-items: center; gap: 20px; text-align: left;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.img-card:hover { transform: scale(1.03); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.img-card img {
    width: 30%; max-height: 180px; object-fit: cover; border-radius: 10px;
}
.img-card p { flex: 1; color: white; }
.view-btn {
    background: #800000; color: white; padding: 8px 16px;
    border-radius: 6px; text-decoration: none; font-weight: bold;
    display: inline-block; margin-top: 10px; transition: 0.3s;
}
.view-btn:hover { background: #b30000; }
.stTextInput input {
    border: 2px solid #800000; border-radius: 12px; padding: 10px 40px 10px 12px;
    font-size: 16px; width: 100%;
    background-image: url("https://img.icons8.com/ios-filled/24/search.png");
    background-repeat: no-repeat; background-position: right 10px center;
    background-size: 18px;
}
.stButton button {
    background: maroon; color: white; border-radius: 8px; padding: 6px 14px;
    font-weight: bold; border: none; transition: all 0.2s ease; cursor: pointer;
}
.stButton button:hover { background: #a00000; transform: scale(1.05); }
.stButton button:active {
    transform: scale(0.9); background: #660000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4) inset;
}
.contact-form {
    background: #ffffff; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    max-width: 500px; margin: auto; color: white;
}
h2, h3, .stMarkdown, .stMarkdown p,
.vision-text, .mission-text, body, p, h1, h4, h5, h6 {
    color: white !important;
}
.footer { text-align: center; padding: 15px; font-size: 14px; color: white; }
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state: st.session_state.page = "Home"
if "images" not in st.session_state: st.session_state.images = []
if "view_image" not in st.session_state: st.session_state.view_image = None

# ------------------ GITHUB CONFIG ------------------
try: GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except Exception: GITHUB_TOKEN = None
REPO_OWNER = "jaysonvertudazo49-web"
REPO_NAME = "LGST"
BRANCH = "main"
API_ROOT = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
RAW_ROOT = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}"

def _headers(): return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"} if GITHUB_TOKEN else {"Accept": "application/vnd.github+json"}
def _raw_url(filename): return f"{RAW_ROOT}/{filename}"
def github_list(): return requests.get(f"{API_ROOT}/contents", headers=_headers(), params={"ref": BRANCH}).json()
def github_get_file(path): return requests.get(f"{API_ROOT}/contents/{path}", headers=_headers(), params={"ref": BRANCH}).json()
def github_put_file(path, content_bytes, message, sha=None):
    url = f"{API_ROOT}/contents/{path}"
    data = {"message": message, "content": base64.b64encode(content_bytes).decode("utf-8"), "branch": BRANCH}
    if sha: data["sha"] = sha
    return requests.put(url, headers=_headers(), data=json.dumps(data)).json()
def get_latest_pic_number():
    max_num = 0
    for f in github_list():
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", f["name"], re.IGNORECASE)
        if m: max_num = max(max_num, int(m.group(1)))
    return max_num
def list_pic_urls_sorted():
    pics = []
    for f in github_list():
        m = re.fullmatch(r"pic(\d+)\.(jpg|jpeg|png)", f["name"], re.IGNORECASE)
        if m: pics.append((int(m.group(1)), f["name"]))
    pics.sort(key=lambda x: x[0], reverse=True)
    return [_raw_url(name) for _, name in pics]
def load_state_json():
    try:
        f = github_get_file("state.json")
        if not f: return {"descriptions": {}, "messages": []}, None
        content = base64.b64decode(f["content"]).decode("utf-8")
        data = json.loads(content) if content.strip() else {}
        if "descriptions" not in data: data["descriptions"] = {}
        if "messages" not in data: data["messages"] = []
        return data, f.get("sha")
    except: return {"descriptions": {}, "messages": []}, None
def save_state_json(data, sha): return github_put_file("state.json", json.dumps(data, indent=2).encode("utf-8"), "Update state.json", sha=sha)
def convert_to_jpg_bytes(uploaded_file):
    data = uploaded_file.getvalue()
    if PIL_AVAILABLE:
        try:
            with Image.open(BytesIO(data)) as im:
                buf = BytesIO()
                im.convert("RGB").save(buf, format="JPEG", quality=92)
                return buf.getvalue()
        except: pass
    return data

# ------------------ HEADER ------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">
        <img src="https://raw.githubusercontent.com/jaysonvertudazo49-web/LGST/main/LOGO1.png">
        <h1>LUCAS GREY SCRAP TRADING</h1>
    </div>
    <div class="header-buttons">
        <form action="" method="get">
            <button type="submit" name="page" value="About">About Us</button>
            <button type="submit" name="page" value="Contact">Contact Us</button>
            <button type="submit" name="page" value="Admin">Admin</button>
            <button type="submit" name="page" value="Home">Home</button>
        </form>
    </div>
</div><hr>
""", unsafe_allow_html=True)
if "page" in st.query_params: st.session_state.page = st.query_params["page"]

# ------------------ ABOUT ------------------
if st.session_state.page == "About":
    st.header("About Lucas Grey Scrap Trading")
    st.subheader("Who We Are")
    st.write("Lucas Grey Scrap Trading (LGST) is a trusted scrap buying and dismantling company...")
    st.subheader("Mission")
    st.info("To deliver top-quality scrap trading and copper wire dismantling...")
    st.subheader("Vision")
    st.success("To become one of the most recognized and respected service providers...")

# ------------------ HOME ------------------
elif st.session_state.page == "Home":
    if not st.session_state.images: st.session_state.images = list_pic_urls_sorted()
    state_data, _ = load_state_json()
    repo_descriptions = state_data.get("descriptions", {})
    st.subheader("WELCOME TO LUCAS GREY SCRAP TRADING")
    search_query = st.text_input("", "")
    if st.button("Clear Search"): search_query = ""
    def filename_from_url(url): return url.rsplit("/", 1)[-1]
    def desc_for_url(url): return repo_descriptions.get(filename_from_url(url), "")
    images = st.session_state.images
    filtered = [u for u in images if search_query.lower() in desc_for_url(u).lower()] if search_query else images
    grouped = {}
    for u in filtered: grouped.setdefault(desc_for_url(u) or "No description", []).append(u)
    if not grouped: st.warning("No results found.")
    else:
        st.subheader("CURRENT PROJECT")
        for caption, urls in grouped.items():
            img_tags = "".join([f'<img src="{u}">' for u in urls])
            st.markdown(f"""
            <div class="img-card">
                <div style="flex:1; display:flex; flex-wrap:wrap; gap:10px;">{img_tags}</div>
                <div style="flex:1;"><p>{caption}</p></div>
            </div>
            """, unsafe_allow_html=True)

# ------------------ CONTACT ------------------
elif st.session_state.page == "Contact":
    st.header("Contact Us")
    st.markdown("""
    <div class="contact-form">
        <h2>Get in Touch</h2>
        <p><b>📍 Address:</b> Quezon City, Philippines</p>
        <p><b>📞 Phone:</b> +63 912 345 6789</p>
        <p><b>📧 Email:</b> contact@lucasgreyscrap.com</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ ADMIN ------------------
elif st.session_state.page == "Admin":
    st.header("Admin Dashboard")
    if not GITHUB_TOKEN: st.error("Missing GITHUB_TOKEN in st.secrets.")
    else:
        uploaded_files = st.file_uploader("Upload project images", accept_multiple_files=True, type=["jpg","jpeg","png"])
        desc = st.text_area("Project Description")
        if uploaded_files and desc and st.button("Upload Project"):
            state_data, sha = load_state_json()
            desc_map = state_data.get("descriptions", {})
            latest = get_latest_pic_number()
            new_files = []
            for uf in uploaded_files:
                latest += 1
                fname = f"pic{latest}.jpg"
                github_put_file(fname, convert_to_jpg_bytes(uf), f"Upload {fname}")
                new_files.append(fname)
            for fname in new_files: desc_map[fname] = desc
            state_data["descriptions"] = desc_map
            save_state_json(state_data, sha)
            st.success("Project uploaded successfully!")
            st.session_state.images = list_pic_urls_sorted()

# ------------------ FOOTER ------------------
st.markdown("<hr><div class='footer'>&copy; 2025 Lucas Grey Scrap Trading. All Rights Reserved.</div>", unsafe_allow_html=True)
