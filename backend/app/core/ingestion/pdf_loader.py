import pdfplumber
from pathlib import Path
from typing import List
from backend.app.core.utils.logger import log

def load_pdf(file_path: str | Path) -> List[dict]:
    """Load a PDF and extract text page by page."""
    file_path = Path(file_path)
    log.info(f"Loading PDF: {file_path.name}")
    chunks = []
   
    try:
        with pdfplumber.open(file_path) as pdf:
            log.debug(f"PDF has {len(pdf.pages)} pages")
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
               
                # Extract tables and convert to readable text
                tables = page.extract_tables()
                table_text = ""
                for table in tables:
                    if table:
                        for row in table:
                            cleaned_row = [str(cell or "").strip() for cell in row]
                            table_text += " | ".join(cleaned_row) + "\n"
               
                full_text = text
                if table_text:
                    full_text += "\n[TABLE]\n" + table_text
               
                # Skip pages with no useful content
                clean_text = full_text.strip()
                if len(clean_text) < 20:
                    continue
               
                chunks.append({
                    "text": clean_text,
                    "source": file_path.name,
                    "page": page_num,
                    "file_type": "pdf"
                })
        log.info(f"PDF loaded: {len(chunks)} pages extracted from {file_path.name}")
        return chunks
    except Exception as e:
        log.error(f"Failed to load PDF {file_path.name}: {e}")
        raise