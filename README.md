# 🇮🇳 Aadhaar Drishti 2026: AI-Powered Societal Insights
### 🏆 Team ID: UIDAI_7342

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit) ![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge&logo=google) ![Folium](https://img.shields.io/badge/Maps-Folium-green?style=for-the-badge)

## 📄 Executive Summary
**Aadhaar Drishti** is a next-generation analytics dashboard built to bridge the gap between raw UIDAI enrolment data and actionable societal insights. 

By integrating **Generative AI (Google Gemini)** and **Geospatial Analytics**, this solution solves two critical problems:
1.  **For Administrators:** Detecting hidden demographic trends and enrolment anomalies using AI.
2.  **For Citizens:** Reducing waiting times at Aadhaar Seva Kendras via a live crowd-monitoring map.

---

## 🚀 Key Features

### 🤖 1. AI Data Assistant (Powered by Google Gemini)
* **Context-Aware Chat:** Users can ask natural language questions like *"Why was there a spike in enrolments in March?"* or *"Summarize the demographic trends for age group 18-25."*
* **Real-Time Analysis:** The AI engine reads the active dataset to provide accurate, data-backed answers instantly.

### 📍 2. Live Center Locator & Crowd Status
* **Smart Geolocation:** A Google Maps-style interface to find nearby Aadhaar Centers in Sehore, Bhopal, Indore, and Vidisha.
* **Queue Management:** Simulates real-time crowd status (🟢 Low, 🟠 Medium, 🔴 High) to help citizens plan their visits and avoid long queues.
* **Address Discovery:** Provides precise location details for every center.

### 📊 3. Interactive Dashboard
* **Global Metrics:** Real-time tracking of Enrolments, Demographic Updates, and Biometric Updates.
* **Trend Visualizations:** Dynamic Pie Charts and Line Graphs powered by Plotly to visualize age-wise distribution and activity timelines.
* **Correlation Engine:** Identifies relationships between update types (e.g., 0.75 correlation between demographic and biometric changes).

### 🔍 4. Deep Dive Search
* **Granular Filtering:** Search specific data points by **Pincode** or **District** name to drill down into local data.

---

## 🛠️ Technology Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **AI Engine:** Google Gemini Flash (Generative AI)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express, Folium (Maps)
* **Version Control:** GitHub

---

## ⚙️ Installation & Setup Guide

### Prerequisites
* Python 3.8 or higher installed.
* A Google Gemini API Key.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Aadhaar-Drishti-2026.git](https://github.com/YOUR_USERNAME/Aadhaar-Drishti-2026.git)
cd Aadhaar-Drishti-2026



📂 Aadhaar-Drishti-2026
├── app.py                # Main Application Code
├── requirements.txt      # List of dependencies
├── DataSet1.csv          # Demographic Data
├── DataSet3.csv          # Enrolment Data
├── DataSet4.csv          # Biometric Data
└── README.md             # Project Documentation
