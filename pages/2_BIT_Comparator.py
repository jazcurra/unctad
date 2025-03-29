# main.py (Backend - Streamlit and Gemini API)
import streamlit as st
import google.generativeai as genai
from google.genai import types
import tempfile
import os
from PyPDF2 import PdfReader

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def compare_documents(doc1_text, doc2_text):
    """Compares two documents using Gemini API and returns the differences."""
    try:
        prompt = f"""
        Compare the following two documents and highlight the key differences between them. Focus on changes in clauses, terms, obligations, and any other significant modifications.

        Document 1:
        {doc1_text}

        Document 2:
        {doc2_text}

        Differences:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during comparison: {e}"

def main():
    st.title("BIT Document Comparator")
    st.subheader("Compare two Bilateral Investment Treaty (BIT) documents to find the differences.")

    uploaded_file1 = st.file_uploader("Upload the first BIT document (PDF)", type=["pdf"], key="file1")
    uploaded_file2 = st.file_uploader("Upload the second BIT document (PDF)", type=["pdf"], key="file2")

    if uploaded_file1 is not None and uploaded_file2 is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file2:
            temp_file1.write(uploaded_file1.getvalue())
            temp_file_path1 = temp_file1.name
            temp_file2.write(uploaded_file2.getvalue())
            temp_file_path2 = temp_file2.name

        doc1_text = extract_text_from_pdf(temp_file_path1)
        doc2_text = extract_text_from_pdf(temp_file_path2)

        os.unlink(temp_file_path1)
        os.unlink(temp_file_path2)

        if "Error" not in doc1_text and "Error" not in doc2_text:
            if st.button("Compare Documents"):
                with st.spinner("Comparing documents..."):
                    comparison_result = compare_documents(doc1_text, doc2_text)
                    st.subheader("Comparison Result:")
                    st.write(comparison_result)
        else:
            if "Error" in doc1_text:
                st.error(f"Error processing the first document: {doc1_text}")
            if "Error" in doc2_text:
                st.error(f"Error processing the second document: {doc2_text}")

if __name__ == "__main__":
    main()