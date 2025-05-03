import streamlit as st
from io import BytesIO
import PyPDF2
import docx

st.set_page_config(page_title="Phrase Search Tool", layout="centered")

st.title("🔍 Phrase Search in Transcripts (.pdf and .docx)")

uploaded_files = st.file_uploader("📂 Upload your files", type=["pdf", "docx"], accept_multiple_files=True)
search_phrase = st.text_input("🔎 Enter the word or phrase you want to search for")

def extract_text_from_pdf(file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
    return text

if uploaded_files and search_phrase:
    st.write("## 📄 Results:")
    search_phrase_lower = search_phrase.lower()
    for uploaded_file in uploaded_files:
        file_text = ""
        if uploaded_file.name.endswith(".pdf"):
            file_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            file_text = extract_text_from_docx(uploaded_file)

        if search_phrase_lower in file_text.lower():
            st.markdown(f"**✅ Found in:** `{uploaded_file.name}`")

            # Show context around the matched phrase
            lines = file_text.splitlines()
            for i, line in enumerate(lines):
                if search_phrase_lower in line.lower():
                    before = lines[i-1] if i > 0 else ""
                    after = lines[i+1] if i < len(lines) - 1 else ""
                    st.text(f"... {before}\n>>> {line}\n... {after}")
                    st.markdown("---")