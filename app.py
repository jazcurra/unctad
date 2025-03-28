'''Comparison BIT documents using GEN AI'''

import streamlit as st
import os
import io
from pdfminer.high_level import extract_text
import PyPDF2
import google.generativeai as genai


# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')



def parse_pdf(file):
    """Parses a PDF file and returns the text content."""
    try:
        # Use PyPDF2 first, if fails use pdfminer
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"PyPDF2 failed: {e}. Trying pdfminer...")
            return extract_text(file)  # Use pdfminer if PyPDF2 fails. This is more robust.

    except Exception as e:
        st.error(f"Error parsing PDF: {e}")
        return None

def compare_with_gemini(analysis_prompt, text1, text2):
    """Compares two texts using Gemini AI and returns the analysis."""
    try:
        prompt = f"""
        Act as a legal expert in bilateral investment treaties. Analyze the following two documents and highlight their similarities and differences,
        especially focusing on key legal points, clauses, and potential risks.  Provide a concise summary
        of your analysis.

        Special instructions:
        {analysis_prompt}

        Text 1:
        {text1}

        Text 2:
        {text2}
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during Gemini AI comparison: {e}")
        return None


st.title("BIT Comparison with Gemini AI")
analysis_prompt = st.text_area("Enter your analysis instructions:", "Compare the following BIT documents.")

uploaded_files = st.file_uploader("Upload PDF Contracts", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    pdf_texts = {}
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        text = parse_pdf(uploaded_file)
        if text:
            pdf_texts[file_name] = text  # Store text for each PDF

    if len(pdf_texts) >= 2:
        # Select two PDFs for comparison
        pdf1_name = st.selectbox("Select First PDF", list(pdf_texts.keys()))
        pdf2_name = st.selectbox("Select Second PDF", list(pdf_texts.keys()))

        if pdf1_name != pdf2_name:
            # Get the text content of the selected PDFs
            text1 = pdf_texts[pdf1_name]
            text2 = pdf_texts[pdf2_name]

            with st.spinner("Comparing with Gemini AI..."):
                comparison_result = compare_with_gemini(analysis_prompt,text1, text2)

            if comparison_result:
                st.subheader("Comparison Result from Gemini AI")
                st.write(comparison_result)
            else:
                st.error("Failed to get comparison result from Gemini AI.")
        else:
            st.warning("Please select two different PDF files for comparison.")
    else:
        st.warning("Please upload at least two PDF files to perform a comparison.")
else:
    st.info("Please upload PDF contract documents to begin.")