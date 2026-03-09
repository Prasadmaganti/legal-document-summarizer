import streamlit as st
from langdetect import detect
from utils import extract_text_from_pdf, clean_text
from summarizer import summarize_text
from translator import translate_to_english

st.set_page_config(page_title="Legal AI Summarizer", layout="wide")

st.title("⚖️ Multilingual Legal Document Summarizer")

# Tabs for different input methods
tab1, tab2 = st.tabs(["📄 Upload PDF", "✍️ Paste Text"])

input_text = ""

with tab1:
    uploaded_file = st.file_uploader("Choose a legal PDF", type=["pdf"])
    if uploaded_file:
        input_text = extract_text_from_pdf(uploaded_file)

with tab2:
    pasted_text = st.text_area("Paste legal clauses here:", height=300, 
                               placeholder="e.g., L'employé s'engage à ne pas travailler...")
    if pasted_text:
        input_text = pasted_text

# Processing Logic
if input_text:
    # 1. Detect Language
    try:
        lang = detect(input_text)
    except:
        lang = 'en' # Fallback
    
    # 2. Preprocessing & Translation
    with st.spinner(f"Processing ({lang})..."):
        cleaned_content = clean_text(input_text)
        # Translate if not English
        text_for_summary = translate_to_english(cleaned_content, lang)

    # 3. Summarization
    with st.spinner("Generating Legal Summary..."):
        summary_result = summarize_text(text_for_summary)

    # 4. Output Display
    if summary_result:
        st.subheader("📄 Summary Results")
        st.success(summary_result)
        
        # Categorized highlights
        col1, col2 = st.columns(2)
        sentences = summary_result.split(". ")
        
        with col1:
            st.markdown("### 📝 Termination & Terms")
            for s in sentences:
                if any(k in s.lower() for k in ["notice", "termination", "month", "duration"]):
                    st.write(f"• {s.strip()}.")
        
        with col2:
            st.markdown("### 🚫 Obligations & Restrictions")
            for s in sentences:
                if any(k in s.lower() for k in ["compete", "solicit", "intellectual", "confidential"]):
                    st.write(f"• {s.strip()}.")