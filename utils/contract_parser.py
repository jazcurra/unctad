# utils/contract_parser.py
import io
from pdfminer.high_level import extract_text
import PyPDF2

def parse_contract(file):
    """Parses a contract file (PDF or TXT) and returns the text content."""
    file_type = file.type
    try:
        if file_type == "application/pdf":
            try:
                # Use PyPDF2 first, if fails use pdfminer
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            except Exception as e:
                print(f"PyPDF2 failed: {e}. Trying pdfminer...")
                return extract_text(file)  # Use pdfminer if PyPDF2 fails. This is more robust.

        elif file_type == "text/plain":
            return io.TextIOWrapper(file).read()
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT files are allowed.")
    except Exception as e:
        raise ValueError(f"Error parsing file: {e}")


#Example usage
if __name__ == "__main__":
    #Create a dummy file for testing
    with open("test_contract.txt", "w") as f:
        f.write("This is a test contract.\nIt contains some sample text.")

    with open("test_contract.txt", "r") as f:
        text = parse_contract(f)
        print(text)