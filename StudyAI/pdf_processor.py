import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_file) -> list:
    """
    Extracts text page by page from an uploaded PDF file.
    Returns a list of dicts: [{"text": str, "page": int, "source": str}]
    """
    reader = PdfReader(pdf_file)
    filename = getattr(pdf_file, 'name', 'Uploaded PDF')
    
    pages_data = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Clean text: reduce multiple spaces/newlines to a single space
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                pages_data.append({
                    "text": text,
                    "page": i + 1,
                    "source": filename
                })
    return pages_data

def chunk_text(pages_data: list, chunk_size: int = 800, overlap: int = 150) -> list:
    """
    Splits the page-by-page text into overlapping chunks, maintaining references.
    Each chunk is a dict: {"text": str, "page": int, "source": str}
    """
    chunks = []
    for page in pages_data:
        text = page["text"]
        page_num = page["page"]
        source = page["source"]
        
        if len(text) <= chunk_size:
            if text.strip():
                chunks.append({
                    "text": text.strip(),
                    "page": page_num,
                    "source": source
                })
            continue
            
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_slice = text[start:end]
            
            # Align end window with a space if possible, so we don't cut words
            if end < len(text):
                last_space = chunk_slice.rfind(' ')
                # If there's a space nearby (within the last 80 chars), break there
                if last_space > chunk_size - 80:
                    chunk_slice = chunk_slice[:last_space]
                    end = start + last_space
            
            chunk_slice = chunk_slice.strip()
            if chunk_slice:
                chunks.append({
                    "text": chunk_slice,
                    "page": page_num,
                    "source": source
                })
            
            start = end - overlap
            # Prevent infinite loops if overlap is configured incorrectly
            if overlap >= chunk_size or start >= len(text):
                break
                
    return chunks
