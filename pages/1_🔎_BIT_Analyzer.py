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

def analyze_contract(contract_text, analysis_prompt, instructions):
    """Analyzes the contract text using Gemini API."""
    try:
        prompt = f"""
        {analysis_prompt}

        Analyze the following Bilateral Investment Treaty (BIT) based on these instructions.{instructions}.
        BIT:
        {contract_text}

        Analysis Outcome:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during analysis: {e}"

def main():
    with open('mapping.txt') as f:
        instructions = f.read()
    st.set_page_config(page_title = "AI BIT Analyzer")

    st.title("BIT Analyzer - Using UNCTAD IIA Mapping project")
    st.write("""
             This solution uses *Gen AI* (Google Gemini) to analyze Bilateral Investment Treaties (BIT) using the methodology provide by IIA Mapping project. 
    
             It takes seconds to analyze a document in any language and get the outcome.
    """)

    uploaded_file = st.file_uploader("Upload a BIT PDF", type=["pdf"])
    analysis_prompt = st.text_area("Enter your analysis instructions:", "Using the IIA Mapping methodology, analyze the document.")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        contract_text = extract_text_from_pdf(temp_file_path)
        os.unlink(temp_file_path)

        if "Error" not in contract_text:
            if st.button("Analyze BIT using IIA Mapping"):
                with st.spinner("Analyzing...", show_time=True):
                    analysis_result = analyze_contract(contract_text, analysis_prompt, instructions)
                    st.subheader("Analysis Result:")
                    st.write(analysis_result)
        else:
            st.error(contract_text)

if __name__ == "__main__":
    main()