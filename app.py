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
# SIDEBAR
# ============================================

with st.sidebar:
    
    # Logo/Title
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">🛡️</h1>
        <h2 style="margin: 0; color: #4A90D9;">CyberShield</h2>
        <p style="color: #888; font-size: 0.8rem;">Cyberbullying Detection System</p>
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
    st.write("Talian Kasih: 15999")
    st.write("Befrienders KL: 03-7627 2929")
    st.write("Online Support: befrienders.org.my")

# ============================================
# HEADER / GREETING
# ============================================

current_hour = datetime.now().hour

if current_hour < 12:
    greeting = "Good Morning"
elif current_hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 20px 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #333;
">
    <h1 style="color: white; margin: 0; font-size: 1.8rem;">
        {greeting}, Adriana
    </h1>
    <p style="color: #aaa; margin: 5px 0 0 0; font-size: 1rem;">
        Use this tool to detect and understand cyberbullying content. 
        Your safety matters.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================

# === BUANG 3 BARIS INI ===
# st.markdown("### Lexicon-Based Cyberbullying Detection System")
# 
# try:
#     model = joblib.load("svm_model.pkl")
#     vectorizer = joblib.load("tfidf_vectorizer.pkl")
#     st.success("Model loaded successfully!")
# ...

# === GANTI DENGAN INI ===

# Load model (silent - tak tunjuk apa-apa)
try:
    model = joblib.load("svm_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# User Input - terus je tanpa tajuk
user_input = st.text_area(
    "Enter Social Media Text",
    height=150,
    placeholder="Example: You are stupid and ugly."
)

# Detect Button
detect = st.button("Detect", type="primary")

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

        # ==========================================
        # NO KEYWORDS FOUND
        # ==========================================

        if len(keywords) == 0:

            col1, col2 = st.columns([2, 1])

            with col1:
                st.success("NON-CYBERBULLYING")

                st.metric(
                    label="Confidence",
                    value="100.00%"
                )

                st.info("No cyberbullying keywords found in the text.")

            with col2:
                st.metric(
                    label="Total Keywords",
                    value="0"
                )

        # ==========================================
        # KEYWORDS FOUND
        # ==========================================

        else:

            # Get keyword categories
            categories = get_keyword_categories(keywords)

            # Prediction
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0]
            confidence = max(probability) * 100

            # ======================================
            # RESULT - TWO COLUMNS
            # ======================================

            col1, col2 = st.columns([2, 1])

            with col1:

                # Prediction
                if prediction == 1:
                    st.error("CYBERBULLYING DETECTED")
                    
                    st.warning("""
                    Remember: This content may be harmful. 
                    If you or someone you know is affected, please reach out for support.
                    """)

                else:
                    st.success("NON-CYBERBULLYING")

                st.metric(
                    label="Confidence",
                    value=f"{confidence:.2f}%"
                )

            with col2:

                st.metric(
                    label="Total Keywords",
                    value=len(keywords)
                )

            # ======================================
            # DETECTED KEYWORDS
            # ======================================

            st.markdown("### Detected Keywords")

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
                <span style="
                    background: {color}22;
                    color: {color};
                    padding: 5px 12px;
                    border-radius: 20px;
                    margin: 3px;
                    display: inline-block;
                    font-size: 0.9rem;
                    border: 1px solid {color}55;
                ">
                    {kw}
                </span>
                """
            
            st.markdown(keyword_html, unsafe_allow_html=True)

            # ======================================
            # KEYWORD CATEGORIES
            # ======================================

            st.markdown("### Keyword Categories")

            for category in categories:
                st.write(f"- {category}")

        # ==========================================
        # QUICK TIPS
        # ==========================================

        st.markdown("---")
        st.markdown("### Quick Tips")

        col_tip1, col_tip2, col_tip3, col_tip4, col_tip5 = st.columns(5)

        with col_tip1:
            st.info("Stay safe online")
        with col_tip2:
            st.info("Think twice before posting")
        with col_tip3:
            st.info("Report cyberbullying")
        with col_tip4:
            st.info("Block harmful users")
        with col_tip5:
            st.info("Reach out for help")

# ============================================
# FOOTER
# ============================================

st.divider()

st.caption("""
CyberShield - Cyberbullying Detection System | 
Made with care for a safer internet | Your safety matters.
""")