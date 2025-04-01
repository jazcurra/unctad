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

def ask_question(document_text, question, chat_history):
    """Asks a question about the document using Gemini API, considering chat history."""
    try:
        context = "\n".join([f"Question: {q}\nAnswer: {a}" for q, a in chat_history])
        prompt = f"""
        You are an expert at answering questions based on the following Bilateral Investment Treaty (BIT) document.
        Use only the information provided in the document to answer the question.
        If the answer is not explicitly in the document, state that you cannot answer based on the provided text.

        BIT Document:
        {document_text}

        Previous Conversation:
        {context}

        Current Question:
        {question}

        Answer:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during question answering: {e}"

def main():
    st.title("BIT Document Q&A")
    st.subheader("Ask questions about the uploaded Bilateral Investment Treaty (BIT) document.")

    uploaded_file = st.file_uploader("Upload a BIT document (PDF)", type=["pdf"], key="qa_file")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
            document_text = extract_text_from_pdf(temp_file_path)
            os.unlink(temp_file_path)

            if "Error" in document_text:
                st.error(f"Error processing the document: {document_text}")
                return

            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            question = st.text_input("Ask your question about the document:")
            if st.button("Ask"):
                if question:
                    with st.spinner("Answering..."):
                        answer = ask_question(document_text, question, st.session_state["chat_history"])
                        st.session_state["chat_history"].append((question, answer))
                        # Keep only the last 5 Q&A pairs
                        st.session_state["chat_history"] = st.session_state["chat_history"][-5:]

            st.subheader("Chat History:")
            if st.session_state["chat_history"]:
                for q, a in st.session_state["chat_history"]:
                    st.markdown(f"**Question:** {q}")
                    st.markdown(f"**Answer:** {a}")
                    st.markdown("---")
            else:
                st.info("No questions asked yet.")

    else:
        st.info("Please upload a BIT document to start asking questions.")

if __name__ == "__main__":
    main()