import streamlit as st
import PyPDF2
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def read_pdf(file):
    """Reads the text content of a PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_txt(file):
    """Reads the text content of a TXT file."""
    return file.read().decode()

def analyze_document_with_gemini(document_text, instructions, ad_hoc_instructions=""):
    """
    Analyzes the document using Gemini based on the provided instructions.

    Args:
        document_text (str): The text content of the document.
        instructions (str): The instructions for analysis.
        ad_hoc_instructions (str): Additional instructions from the user.

    Returns:
        str: The analysis result as plain text.
    """
    prompt = f"""
    Analyze the following document based on the provided instructions.

    Instructions:
    {instructions}

    Additional Instructions:
    {ad_hoc_instructions}

    Document Text:
    {document_text}

    Provide the analysis as plain text.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return ""

st.title("Document Analyzer")

# 1. File Upload
st.subheader("Upload Files")
instructions_file = st.file_uploader("Upload Instructions (PDF or TXT)", type=["pdf", "txt"])
document_file = st.file_uploader("Upload Document (PDF or TXT)", type=["pdf", "txt"])

# Ad-hoc Instructions
ad_hoc_instructions = st.text_area("Enter Additional Instructions (Optional)", "Using the instructions analyze the document and show the result")

# 2. Analysis Execution
st.subheader("Analyze")
if st.button("Analyze Document"):
    if instructions_file and document_file:
        with st.spinner("Analyzing..."):
            if instructions_file.type == "application/pdf":
                instructions = read_pdf(instructions_file)
            else:
                instructions = read_txt(instructions_file)

            if document_file.type == "application/pdf":
                document_text = read_pdf(document_file)
            else:
                document_text = read_txt(document_file)

            analysis_result = analyze_document_with_gemini(document_text, instructions, ad_hoc_instructions)

        # 3. Results Display
        st.subheader("Analysis Results")
        if analysis_result:
            st.text(analysis_result)  # Display as plain text
        else:
            st.warning("Analysis failed or returned no results.")
    else:
        st.warning("Please upload both instructions and a document.")

        