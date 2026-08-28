import streamlit as st
import joblib
import re
from datetime import datetime

from scipy.sparse import hstack, csr_matrix

from utils import (preprocess_text, extract_lexicon_features, highlight_keywords, get_keyword_categories, CYBERBULLYING_LEXICON)

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="CyberShield - Cyberbullying Detection",
    page_icon="🛡️",
    layout="wide"
)

# ============================================
# CUSTOM CSS - LIGHT THEME
# ============================================

st.markdown("""
<style>
    /* Main background - Light */
    .stApp {
        background-color: #f5f7fa !important;
    }
    
    .main > div {
        background-color: #f5f7fa !important;
    }
    
    /* Card style - Light */
    .css-1r6slb0, .css-1v3fvcr {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid #e0e4e8 !important;
    }
    
    /* Header gradient - Light blue */
    .header-gradient {
        background: linear-gradient(135deg, #e8edf5 0%, #d5dde8 50%, #c5d0de 100%) !important;
        padding: 25px 30px !important;
        border-radius: 15px !important;
        margin-bottom: 25px !important;
        border: 1px solid #d0d6de !important;
    }
    
    .header-gradient h1 {
        color: #1a2332 !important;
    }
    
    .header-gradient p {
        color: #4a5a6e !important;
    }
    
    /* Sidebar - Light */
    .css-1d391kg {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e4e8 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4A90D9, #357ABD) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5A9EE9, #4A90D9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(74, 144, 217, 0.3) !important;
    }
    
    /* Text input - Light */
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        color: #1a2332 !important;
        border: 1px solid #d0d6de !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4A90D9 !important;
        box-shadow: 0 0 0 2px rgba(74, 144, 217, 0.2) !important;
    }
    
    /* Result cards */
    .result-cyberbullying {
        background: linear-gradient(135deg, #fde8e8, #fcd0d0) !important;
        border: 1px solid #ff4444 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
    }
    
    .result-cyberbullying h2 {
        color: #cc0000 !important;
    }
    
    .result-cyberbullying p {
        color: #990000 !important;
    }
    
    .result-non-cyberbullying {
        background: linear-gradient(135deg, #e8f5e8, #d0f0d0) !important;
        border: 1px solid #44cc44 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
    }
    
    .result-non-cyberbullying h2 {
        color: #008800 !important;
    }
    
    .result-non-cyberbullying p {
        color: #006600 !important;
    }
    
    /* Keyword badges */
    .keyword-badge {
        display: inline-block !important;
        padding: 5px 15px !important;
        border-radius: 20px !important;
        margin: 3px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(to right, transparent, #d0d6de, transparent) !important;
        margin: 20px 0 !important;
    }
    
    /* Expander - Light */
    .streamlit-expanderHeader {
        background-color: #f0f2f5 !important;
        border-radius: 10px !important;
        border: 1px solid #e0e4e8 !important;
        color: #1a2332 !important;
    }
    
    /* Metrics - Light */
    .css-1xarl3l {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 15px !important;
        border: 1px solid #e0e4e8 !important;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        background-color: #f0f4f8 !important;
        border-radius: 8px !important;
    }
    
    /* All text */
    .stMarkdown, .stText, .stCaption, .stTitle, .stHeader, .stSubheader {
        color: #1a2332 !important;
    }
    
    /* Sidebar text */
    .css-1d391kg .stMarkdown, .css-1d391kg .stText {
        color: #1a2332 !important;
    }
    
    /* Caption */
    .stCaption {
        color: #6a7a8e !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    
    # Logo/Title
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h1 style="font-size: 3rem; margin: 0;">🛡️</h1>
        <h2 style="margin: 0; color: #4A90D9; font-size: 1.5rem;">CyberShield</h2>
        <p style="color: #6a7a8e; font-size: 0.75rem;">Cyberbullying Detection & Awareness</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Helpline
    st.markdown("### Need Help?")
    
    st.info(
        "If you're experiencing cyberbullying, "
        "please reach out to someone you trust "
        "or contact a helpline."
    )
    
    st.markdown("**Helpline**")
    st.write("📞 Talian Kasih: 15999")
    st.write("📞 Befrienders KL: 03-7627 2929")
    st.write("🌐 Online Support: befrienders.org.my")

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header-gradient">
    <h1 style="margin: 0; font-size: 1.8rem;">Welcome to CyberShield</h1>
    <p style="margin: 5px 0 0 0; font-size: 1rem;">We're here to help you understand online content and stay safer.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================

try:
    model = joblib.load("svm_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ============================================
# CYBERBULLYING AWARENESS
# ============================================

with st.expander("ℹ️ Understanding Cyberbullying"):
    st.write("""
    **Cyberbullying** refers to harmful or abusive behaviour carried out
    through digital communication such as social media and online platforms.
    """)
    
    col_awareness1, col_awareness2 = st.columns(2)
    
    with col_awareness1:
        st.markdown("""
        **Common forms may include:**
        • **Insults** – using offensive or degrading language  
        • **Harassment** – repeatedly disturbing or targeting someone  
        • **Threats** – threatening to hurt or harm someone
        """)
    
    with col_awareness2:
        st.markdown("""
        • **Derogatory language** – harmful or discriminatory expressions  
        • **Exclusion** – deliberately isolating or rejecting someone  
        • **Profanity** – offensive language used in harmful contexts
        """)
    
    st.caption(
        "Note: The presence of an offensive word does not automatically mean "
        "that a message is cyberbullying. Context and usage should also be considered."
    )

# ============================================
# USER INPUT
# ============================================

user_input = st.text_area(
    "Enter Social Media Text",
    height=120,
    placeholder="Example: You are stupid and ugly."
)

# Detect Button
detect = st.button("Detect", type="primary", use_container_width=False)

# ============================================
# RESULT SECTION
# ============================================

if detect:

    if user_input.strip() == "":
        st.warning("Please enter some text to analyze.")

    else:

        # Preprocess
        clean_text = preprocess_text(user_input)

        # TF-IDF
        tfidf_features = vectorizer.transform([clean_text])

        # Lexicon Features
        features = extract_lexicon_features(clean_text)

        lexicon_features = csr_matrix([[
            features['keyword_count'],
            features['insult_count'],
            features['threat_count'],
            features['harassment_count'],
            features['derogatory_count'],
            features['exclusion_count'],
            features['profanity_count'],
            float(features['has_cyberbullying'])
        ]])

        # Combine
        X = hstack([tfidf_features, lexicon_features])

        # ==========================================
        # DISPLAY RESULT
        # ==========================================

        st.markdown("---")
        st.markdown("### Detection Result")

        # Detect keywords
        keywords = highlight_keywords(clean_text)

        # Get prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0]
        confidence = max(probability) * 100

        # ==========================================
        # RESULT HEADER
        # ==========================================

        if prediction == 1:
            st.markdown("""
            <div class="result-cyberbullying">
                <h2 style="margin: 0;">⚠️ CYBERBULLYING DETECTED</h2>
                <p style="margin: 5px 0 0 0;">
                    This content may contain harmful or offensive language.
                    If you or someone you know is affected, please reach out for support.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-non-cyberbullying">
                <h2 style="margin: 0;">✅ NON-CYBERBULLYING</h2>
                <p style="margin: 5px 0 0 0;">
                    The machine learning model classified this content as non-cyberbullying.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ==========================================
        # METRICS - 2 Columns
        # ==========================================

        col_metric1, col_metric2 = st.columns(2)

        with col_metric1:
            st.metric(
                label="Confidence",
                value=f"{confidence:.2f}%"
            )

        with col_metric2:
            st.metric(
                label="Total Keywords Detected",
                value=len(keywords)
            )

        # ==========================================
        # KEYWORDS & CATEGORIES - SIDE BY SIDE
        # ==========================================

        if len(keywords) > 0:
            
            st.markdown("### Detected Keywords & Categories")
            
            # Create 2 columns
            col_kw, col_cat = st.columns(2)
            
            with col_kw:
                st.markdown("**🔑 Keywords Detected**")
                
                keyword_html = ""
                for kw in keywords:
                    category = CYBERBULLYING_LEXICON.get(kw, "Unknown")
                    
                    color_map = {
                        'Insult': '#FF6B6B',
                        'Derogatory': '#FF9F43',
                        'Exclusion': '#FECA57',
                        'Threat': '#FF4757',
                        'Harassment': '#A29BFE',
                        'Profanity': '#FD79A8',
                        'Unknown': '#DFE6E9'
                    }
                    
                    color = color_map.get(category, '#DFE6E9')
                    
                    keyword_html += f"""
                    <span class="keyword-badge" style="
                        background: {color}22;
                        color: {color};
                        border: 1px solid {color}55;
                    ">
                        {kw}
                    </span>
                    """
                
                st.markdown(keyword_html, unsafe_allow_html=True)
            
            with col_cat:
                st.markdown("**📂 Keyword Categories**")
                
                categories = get_keyword_categories(keywords)
                for category in categories:
                    st.write(f"• {category}")
        
        else:
            
            st.info("No cyberbullying-related keywords were detected in the text.")
            
            if prediction == 1:
                st.write("""
                **Why was this classified as Cyberbullying?**
                
                Although no predefined lexicon keyword was detected,
                the machine learning model identified patterns in the
                text that were associated with cyberbullying content.
                """)

        # ==========================================
        # WHY WAS THIS DETECTED?
        # ==========================================

        if len(keywords) > 0 and prediction == 1:
            
            st.markdown("---")
            st.markdown("### 📝 Why was this classified this way?")
            
            st.write("""
            The text contains one or more keywords associated with
            cyberbullying-related categories. These lexicon features,
            together with the text features analysed by the machine
            learning model, contributed to the classification.
            """)

        # ==========================================
        # WHAT CAN YOU DO?
        # ==========================================

        st.markdown("---")
        st.markdown("### 🛡️ What Can You Do?")

        col_tip1, col_tip2, col_tip3, col_tip4 = st.columns(4)

        with col_tip1:
            st.info("""
            **📸 Save Evidence**
            
            Keep screenshots or records
            of harmful messages.
            """)

        with col_tip2:
            st.info("""
            **🚫 Block or Restrict**
            
            Limit interaction with
            harmful users when needed.
            """)

        with col_tip3:
            st.info("""
            **📢 Report**
            
            Report harmful content
            through the platform.
            """)

        with col_tip4:
            st.info("""
            **🤝 Seek Support**
            
            Talk to someone you trust
            if the situation continues.
            """)

        # ==========================================
        # IMPORTANT NOTE
        # ==========================================

        with st.expander("⚠️ Important Note About the Detection"):
            st.write("""
            CyberShield provides automated text-based detection based on
            the features and patterns learned from the dataset.
            
            A prediction should not be treated as a definitive judgement
            about a person or situation. Cyberbullying can depend on factors
            such as context, intention, relationship between users and
            repeated behaviour.
            
            The system is intended to support awareness and initial
            identification of potentially harmful content.
            """)

# ============================================
# FOOTER
# ============================================

st.divider()

st.caption("""
CyberShield - Cyberbullying Detection & Awareness System | 
Made with care for a safer internet | Your safety matters.
""")