import streamlit as st
from io import BytesIO
import PyPDF2
import docx
import fitz  # PyMuPDF

st.set_page_config(page_title="Phrase Search Tool", layout="centered")

st.title("🔍 Phrase Search in Transcripts (.pdf and .docx)")

uploaded_files = st.file_uploader("📂 Upload your files", type=["pdf", "docx"], accept_multiple_files=True)
search_phrase = st.text_input("🔎 Enter the word or phrase you want to search for")

# Función para extraer texto de PDF usando PyMuPDF (fitz)
def extract_text_from_pdf(file):
    text = ""
    try:
        doc = fitz.open(file)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# Función para extraer texto de archivo DOCX
def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        for para_num, para in enumerate(doc.paragraphs):
            text += f"Para {para_num + 1}: {para.text}\n"
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

            # Para PDF, mostrar el número de página
            if uploaded_file.name.endswith(".pdf"):
                doc = fitz.open(uploaded_file)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    page_text = page.get_text("text")
                    if search_phrase_lower in page_text.lower():
                        st.markdown(f"**Page {page_num + 1}:**")
                        lines = page_text.splitlines()
                        for i, line in enumerate(lines):
                            if search_phrase_lower in line.lower():
                                before = lines[i-1] if i > 0 else ""
                                after = lines[i+1] if i < len(lines) - 1 else ""
                                st.text(f"... {before}\n>>> {line}\n... {after}")
                        st.markdown("---")

            # Para DOCX, mostrar el número de párrafo
            elif uploaded_file.name.endswith(".docx"):
                lines = file_text.splitlines()
                for line in lines:
                    if search_phrase_lower in line.lower():
                        st.text(f"Found in: {line}")
                        st.markdown("---")