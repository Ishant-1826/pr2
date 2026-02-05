import streamlit as st
import pandas as pd
from datetime import datetime

# UI Configuration - High Contrast & Minimalist
st.set_page_config(page_title="NEXUS // CORE", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050508; }
    h1, h2, h3, p, span, label { color: #00f2fe !important; }
    .stButton>button { 
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); 
        color: black !important; font-weight: bold; border: none;
    }
    div[data-testid="stExpander"] { background-color: #000000; border: 1px solid #1a1a2e; }
    </style>
    """, unsafe_allow_html=True)

# 1. SIMPLE LOGIN (Uses Session State)
if 'username' not in st.session_state:
    st.title("NEXUS // AUTHORIZATION")
    user_id = st.text_input("ENTER STUDENT ID (e.g., 2025KUAD3005)")
    if st.button("INITIALIZE"):
        st.session_state.username = user_id
        st.rerun()
    st.stop()

# 2. APP INTERFACE
st.title("🎯 Real-Time Peer Optimizer")
st.write(f"Active Node: **{st.session_state.username}**")

# Use st.cache_resource or a simple global dict for local testing
# In a real cloud app, you would link this to a Database
if 'peer_db' not in st.session_state:
    st.session_state.peer_db = {}

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Settings")
    # Default is OFF as requested
    is_active = st.toggle("BROADCAST GAP", value=False)
    
    # Pre-set interests based on your focus
    focus_options = ["Python", "DSA", "Machine Learning", "Linear Algebra", "Digital Electronics"]
    my_focus = st.multiselect("Current Focus:", focus_options, default=["Python"])

    # Update the "Database"
    if is_active:
        st.session_state.peer_db[st.session_state.username] = {
            "focus": my_focus,
            "time": datetime.now().strftime("%H:%M")
        }
    else:
        st.session_state.peer_db.pop(st.session_state.username, None)

with col2:
    st.subheader("🤝 Peer Network")
    if is_active:
        # Filter out yourself
        others = {k: v for k, v in st.session_state.peer_db.items() if k != st.session_state.username}
        
        if not others:
            st.info("Waiting for peers to join the network...")
        else:
            for peer, data in others.items():
                with st.expander(f"👤 {peer} is ACTIVE"):
                    st.write(f"**Studying:** {', '.join(data['focus'])}")
                    st.write(f"**Gap Detected at:** {data['time']}")
                    if st.button(f"Sync with {peer}"):
                        st.success(f"Connection request sent to {peer}!")
    else:
        st.warning("Toggle 'BROADCAST GAP' to see active peers.")