import streamlit as st
from google import genai

# ==============================================================================
# 1. DESIGN & THEMING (Professional Navy & Gold)
# ==============================================================================
st.set_page_config(page_title="EliteDevice AI Advisor", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000033; }
    .main-block {
        border: 2px solid #D4AF37; 
        border-radius: 20px;
        padding: 30px;
        background-color: #000044;
        color: white;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3);
    }
    .main-title {
        color: #D4AF37;
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 40px;
        margin-bottom: 10px;
    }
    .sub-title {
        color: #C0C0C0;
        text-align: center;
        font-size: 16px;
        margin-bottom: 40px;
    }
    label {
        color: #D4AF37 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    .stButton>button {
        background: linear-gradient(45deg, #D4AF37, #F9E272) !important;
        color: #000033 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 22px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s ease-in-out;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4);
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.6); }
    .stSelectbox, .stTextInput {
        border: 1px solid #D4AF37 !important;
        background-color: #000033 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. DYNAMIC MODEL DISCOVERY ENGINE
# ==============================================================================
def get_best_available_model(client):
    """
    Queries the API to find all available models and selects the best one 
    based on a priority hierarchy.
    """
    try:
        available_models = client.models.list()
        hierarchy = ["pro", "flash", "gemini-1.0"] 
        model_names = [m.name for m in available_models]
        
        for pref in hierarchy:
            for name in model_names:
                if pref in name.lower(): 
                    return name
        return model_names[0] if model_names else None
    except Exception as e:
        st.error(f"Discovery Engine Error: {e}")
        return None

# ==============================================================================
# 3. AI CONFIGURATION (SECURE)
# ==============================================================================
# We use st.secrets to keep your API Key private and safe from GitHub bots.
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' to your Streamlit Secrets vault.")
    st.stop()

# ==============================================================================
# 4. DASHBOARD UI LOGIC
# ==============================================================================
st.markdown('<div class="main-title">ELITE DEVICE ADVISOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Precision-Engineered Smartphone Recommendations</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-block">', unsafe_allow_html=True)
    
    user_prefs = {}
    factors = {
        "Screen Size": ["Compact (<6.1\")", "Standard (6.1\"-6.5\")", "Large (6.5\"-6.8\")", "Ultra (>6.8\")"],
        "Budget": ["Entry Level", "Mid-Range", "Premium", "Ultra-Luxury"],
        "Battery Backup": ["4000-5000 mAh", "5000-6000 mAh", "6000+ mAh"],
        "Display Type": ["AMOLED", "S-AMOLED", "LED", "TFT"],
        "Processor": ["Power Efficiency", "Gaming Performance", "All-rounder"],
        "RAM & Storage": ["8GB/128GB", "12GB/256GB", "16GB/512GB+", "Max Spec"],
        "Weight": ["Very Light (<180g)", "Light (180g-200g)", "Standard (200g-220g)", "Heavy (>220g)"],
        "Camera": ["Natural Colors", "Zoom Capabilities", "Low Light King", "Vlogging/Selfie"],
        "Fast Charging": ["18W-33W", "33W-65W", "65W-120W", "120W+"],
        "Brand Reputation": ["Tier 1 (Apple/Samsung/OnePlus)", "Tier 2 (Pixel/Xiaomi/Nothing)", "Tier 3 (Others)"]
    }

    cols = st.columns(2)

    for i, (factor, options) in enumerate(factors.items()):
        with cols[i % 2]:
            st.write(f"---")
            weight = st.slider(f"{factor} Importance", 1, 5, 3, key=f"sld_{factor}")
            
            if weight == 5:
                with st.expander(f"✨ Specify Ideal {factor}", expanded=True):
                    choice = st.selectbox(f"Select preferred {factor}", options, key=f"sel_{factor}")
                    user_prefs[factor] = choice
            else:
                user_prefs[factor] = "Not a priority"

    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
    run_button = st.button("RUN SCORING")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. AI ANALYSIS ENGINE
# ==============================================================================
if run_button:
    with st.spinner("Connecting to AI Brain..."):
        best_model = get_best_available_model(client)
        
        if not best_model:
            st.error("No compatible AI models found for this API key.")
        else:
            with st.spinner(f"Analyzing market using {best_model}..."):
                prompt = f"""
                You are a professional mobile device analyst. 
                User Preferences (1-5 weight): {user_prefs}
                
                Task:
                1. Suggest the top 3-5 mobile phones globally.
                2. Calculate a 'Match Score' out of 50 based on how well the phone matches the factors given a weight of '5'.
                3. ONLY suggest phones with a score > 40/50.
                4. Brand Logic: Apple/Samsung/OnePlus = 5/5, Pixel/Xiaomi/Nothing = 4/5, others = 3/5.
                
                Format:
                - **Phone Name**
                - **Final Score: X/50**
                - **Why it matched:** (Bullets)
                - **Key Specs:** (List)
                """
                
                try:
                    response = client.models.generate_content(
                        model=best_model, 
                        contents=prompt
                    )
                    
                    st.markdown('<div class="main-block">', unsafe_allow_html=True)
                    st.markdown(f'<h3 style="color:#D4AF37; text-align:center;">AI Recommendation Results</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color:grey; text-align:center; font-size:12px;">Dynamically optimized via: {best_model}</p>', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Generation Error: {e}")
