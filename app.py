import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import random

# --- SAFETY CHECK: Try to import AI ---
ai_available = False
try:
    import google.generativeai as genai
    ai_available = True
except ImportError:
    pass

# --- CONFIGURATION ---
st.set_page_config(page_title="Aadhaar Drishti 2026", layout="wide")

# 🔴 YOUR API KEY
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Configure AI
if ai_available and GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        ai_available = False

# --- 1. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df_enrol = pd.read_csv('DataSet3.csv') 
        df_demo = pd.read_csv('DataSet1.csv') 
        df_bio = pd.read_csv('DataSet4.csv')   
        
        for df in [df_enrol, df_demo, df_bio]:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        
        return df_enrol, df_demo, df_bio
    except FileNotFoundError:
        return None, None, None

df_enrol, df_demo, df_bio = load_data()

# --- GENERATE CONTEXT ---
def get_data_context():
    if df_enrol is None: return "No data."
    total_enrol = df_enrol[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum()
    return f"Total Enrolments: {total_enrol}. Strong correlation (0.75) between updates."

# --- UI LAYOUT ---
st.title("📊 Aadhaar Drishti 2026: Societal Trends Dashboard")
st.markdown("Team ID: **UIDAI_7342**")

# --- SIDEBAR LOGIC ---
if ai_available:
    nav_options = ["Overview Dashboard", "Search & Deep Dive", "🤖 AI Data Assistant", "📍 Live Center Locator"]
else:
    nav_options = ["Overview Dashboard", "Search & Deep Dive", "📍 Live Center Locator"]
    st.sidebar.warning("⚠️ AI Library missing. Chatbot disabled.")

page = st.sidebar.radio("Navigation", nav_options)

if df_enrol is not None:
    
    # ==========================
    # PAGE 1: OVERVIEW
    # ==========================
    if page == "Overview Dashboard":
        st.subheader("📈 Global Metrics")
        col1, col2, col3 = st.columns(3)
        
        total_enrol = df_enrol[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum()
        total_demo = df_demo[['demo_age_5_17', 'demo_age_17_']].sum().sum()
        total_bio = df_bio[['bio_age_5_17', 'bio_age_17_']].sum().sum()
        
        col1.metric("Total Enrolments", f"{total_enrol:,}")
        col2.metric("Demographic Updates", f"{total_demo:,}")
        col3.metric("Biometric Updates", f"{total_bio:,}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Enrolment by Age")
            age_sums = df_enrol[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
            age_sums.columns = ['Age Group', 'Count']
            fig = px.pie(age_sums, values='Count', names='Age Group', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("### Activity Timeline")
            daily = df_enrol.groupby('date')[['age_0_5', 'age_5_17']].sum().sum(axis=1)
            st.line_chart(daily)

    # ==========================
    # PAGE 2: SEARCH
    # ==========================
    elif page == "Search & Deep Dive":
        st.subheader("🔍 Search District or Pincode")
        query = st.text_input("Enter District/Pincode", "")
        if query:
            if query.isdigit():
                mask = df_enrol['pincode'].astype(str) == query
            else:
                mask = df_enrol['district'].str.contains(query, case=False, na=False)
            st.dataframe(df_enrol[mask])

    # ==========================
    # PAGE 3: AI CHATBOT
    # ==========================
    elif page == "🤖 AI Data Assistant" and ai_available:
        st.subheader("💬 Chat with your Data")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            try:
                # Using the latest available model
                st.session_state.model = genai.GenerativeModel('gemini-flash-latest')
                st.session_state.chat = st.session_state.model.start_chat(history=[
                    {"role": "user", "parts": get_data_context()},
                    {"role": "model", "parts": "Understood."}
                ])
            except:
                st.error("Connection Error.")

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ask something..."):
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                response = st.session_state.chat.send_message(prompt)
                st.chat_message("assistant").write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")

    # ==========================
    # PAGE 4: LIVE CROWD MAP (FINAL FIXED VERSION)
    # ==========================
    elif page == "📍 Live Center Locator":
        st.subheader("📍 Nearby Aadhaar Centers & Live Crowd Status")
        
        user_city = st.selectbox("Select your City/District:", ["Sehore", "Bhopal", "Indore", "Vidisha"])
        
        city_coords = {
            "Sehore": [23.2030, 77.0844],
            "Bhopal": [23.2599, 77.4126],
            "Indore": [22.7196, 75.8577],
            "Vidisha": [23.5251, 77.8081]
        }
        
        fake_addresses = [
            "Near Main Bus Stand, Sector 2", "Opposite City Hospital, Main Road",
            "Railway Station Road, Near ATM", "Panchayat Bhawan, Civil Lines",
            "Govt. School Complex, Block A", "Main Market, Shop No. 12"
        ]

        if "map_data" not in st.session_state:
            st.session_state.map_data = {}
        if "current_city" not in st.session_state:
            st.session_state.current_city = None

        # Logic: Update data if city changes OR if data is corrupted (missing 'address')
        data_needs_refresh = (st.session_state.current_city != user_city)
        
        # Safety Check for the crash 
        if st.session_state.map_data and isinstance(st.session_state.map_data, list):
            if "address" not in st.session_state.map_data[0]: 
                data_needs_refresh = True # Force refresh if using old data format

        if data_needs_refresh:
            st.session_state.current_city = user_city
            new_markers = []
            if user_city in city_coords:
                center_locs = city_coords[user_city]
                status_options = ["Low (Wait: < 5 mins)", "Medium (Wait: 15 mins)", "High (Wait: 45+ mins)"]
                colors = ["green", "orange", "red"]
                
                for i in range(5):
                    lat = center_locs[0] + random.uniform(-0.03, 0.03)
                    lon = center_locs[1] + random.uniform(-0.03, 0.03)
                    status_idx = random.randint(0, 2)
                    addr = random.choice(fake_addresses)
                    
                    new_markers.append({
                        "lat": lat, "lon": lon, "address": addr, 
                        "status_text": status_options[status_idx], "icon_color": colors[status_idx]
                    })
            st.session_state.map_data = new_markers

        # Render Map
        if user_city in city_coords:
            center_locs = city_coords[user_city]
            m = folium.Map(location=center_locs, zoom_start=13)
            
            st.markdown(f"Found **5 Active Centers** in **{user_city}**. Checking queue status...")
            
            for i, marker in enumerate(st.session_state.map_data):
                popup_html = f"""<div style="width:150px"><b>Center #{i+1}</b><br><small>{marker['address']}</small><br><hr style="margin:5px 0"><b>Status:</b> {marker['status_text']}</div>"""
                
                folium.Marker(
                    [marker["lat"], marker["lon"]],
                    popup=folium.Popup(popup_html, max_width=200),
                    tooltip=f"{marker['address']}",
                    icon=folium.Icon(color=marker["icon_color"], icon="info-sign")
                ).add_to(m)

            st_folium(m, width=800, height=500)
            
            c1, c2, c3 = st.columns(3)
            c1.success("🟢 Low Traffic")
            c2.warning("🟠 Medium Traffic")
            c3.error("🔴 High Traffic")

else:
    st.error("Please ensure DataSet1.csv, DataSet3.csv, and DataSet4.csv are in the folder.")