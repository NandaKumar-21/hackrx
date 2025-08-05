import pdfplumber
import docx
import email
from bs4 import BeautifulSoup

def extract_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_from_email(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_email = f.read()
        msg = email.message_from_string(raw_email)

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    text = part.get_payload(decode=True).decode(errors='ignore')
                    break
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True).decode(errors='ignore')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text = soup.get_text()
                    break
        else:
            text = msg.get_payload(decode=True).decode(errors='ignore')

    except Exception as e:
        print(f"Error reading EML: {e}")
    return text

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_from_docx(file_path)
    elif file_path.endswith(".eml"):
        return extract_from_email(file_path)
    else:
        raise ValueError("Unsupported file type")
