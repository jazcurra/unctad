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

def generate_answer(context, question):
    """Generates an answer to the question based on the context using Gemini AI."""
    try:
        prompt = f"""
        You are an experimented lawer in Bilateral Investments Treaties (BIT) working with UNCTAD and Intracen knowledge.
        Use the following context to answer the question at the end.
        If you don't find the answer in the context, just say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question: {question}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during Gemini AI question answering: {e}")
        return None

st.title("BIT Q&A with Gemini AI")

# Initialize session state for question-answer history
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])

if uploaded_file:
    pdf_text = parse_pdf(uploaded_file)

    if pdf_text:
        st.success("PDF document loaded successfully!")

        question = st.text_area("Ask a question about the BIT document:")

        if question:
            with st.spinner("Generating answer..."):
                answer = generate_answer(pdf_text, question)

            if answer:
                st.subheader("Answer:")
                st.write(answer)

                # Add the question and answer to the history
                st.session_state.qa_history.append({"question": question, "answer": answer})

                # Keep only the last 5 questions and answers
                st.session_state.qa_history = st.session_state.qa_history[-5:]

            else:
                st.error("Failed to generate an answer.")
        #Display the Q&A history
        if st.session_state.qa_history:
            st.subheader("Q&A History:")
            for qa in reversed(st.session_state.qa_history):  # Show in reverse chronological order
                st.write(f"**Question:** {qa['question']}")
                st.write(f"**Answer:** {qa['answer']}")
                st.write("---")  # Separator

    else:
        st.error("Failed to parse the PDF document.")

else:
    st.info("Please upload a PDF document to begin.")