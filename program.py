import streamlit as st
import requests
import json
from datetime import datetime

# 1. SETUP: We use a public 'bin' to share data between your two laptops.
# This replaces the need for an IP address or 'localhost'.
BIN_ID = "iiit_kota_optimizer_v1" 
API_URL = f"https://jsonbin.org/me/{BIN_ID}"
# Use a public key or a simple header for this 'Zero-Config' approach
HEADERS = {"token": "99f47101-7101-4999-9999-710171017101"} # Example Public Token

st.set_page_config(page_title="NEXUS // CORE", layout="centered")

# Minimalist Styling - No Dynamic Classes (Avoids Black Screen)
st.markdown("""
    <style>
    .stApp { background-color: #050508; }
    h1, h2, h3, p, label { color: #00f2fe !important; }
    .stButton>button { 
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); 
        color: black !important; font-weight: bold; border: none; width: 100%;
    }
    .peer-card {
        border: 1px solid #1a1a2e; padding: 15px; border-radius: 10px; background: #000; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN: Adding Name and Branch (For AI & Data Engineering)
if 'user' not in st.session_state:
    st.title("🎓 NEXUS // REGISTRATION")
    sid = st.text_input("Enter Roll Number (e.g., 2025KUAD3005)")
    name = st.text_input("Enter Full Name")
    branch = st.selectbox("Select Branch", ["AI & Data Engineering", "Computer Science", "Electronics"])
    
    if st.button("INITIALIZE NODE"):
        if sid and name:
            st.session_state.user = {"id": sid, "name": name, "branch": branch}
            st.rerun()
        else:
            st.error("Please fill all details.")
    st.stop()

user = st.session_state.user
st.title("🎯 Real-Time Peer Optimizer")
st.write(f"Active Node: **{user['name']}** | Branch: **{user['branch']}**")

# 3. SETTINGS: Default is OFF
is_active = st.toggle("BROADCAST MY GAP", value=False)
my_focus = st.multiselect("Study Focus:", ["Python", "DSA", "Machine Learning", "Linear Algebra"], default=["Python"])

# 4. DATA SYNC: Send your data to the Cloud Bin
def sync_data(data):
    # This sends your name/branch to the shared folder
    requests.post(API_URL, json=data, headers=HEADERS)

def get_data():
    # This pulls everyone's data from the shared folder
    res = requests.get(API_URL, headers=HEADERS)
    return res.json() if res.status_code == 200 else {}

# Logic to update the shared pool
all_peers = get_data()

if is_active:
    all_peers[user['id']] = {
        "name": user['name'],
        "branch": user['branch'],
        "focus": my_focus,
        "last_seen": datetime.now().strftime("%H:%M")
    }
    sync_data(all_peers)
else:
    if user['id'] in all_peers:
        all_peers.pop(user['id'])
        sync_data(all_peers)

# 5. PEER LIST: Showing your friend
st.divider()
st.subheader("🤝 Available Peers")

if is_active:
    # Filter out your own ID
    others = {k: v for k, v in all_peers.items() if k != user['id']}
    
    if not others:
        st.info("Network is empty. Waiting for peers to join... (Tell your friend to toggle ON)")
    else:
        for pid, pdata in others.items():
            st.markdown(f"""
                <div class="peer-card">
                    <h4 style="margin:0; color:#00f2fe;">{pdata['name']}</h4>
                    <p style="margin:0; font-size:0.85em; color:#888;">{pdata['branch']} • Gap at {pdata['last_seen']}</p>
                    <p style="margin-top:10px; color:#fff;">Studying: <b>{", ".join(pdata['focus'])}</b></p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Sync with {pdata['name']}", key=pid):
                st.toast(f"Connection request sent to {pdata['name']}")
else:
    st.warning("Switch 'BROADCAST GAP' to ON to see active peers.")