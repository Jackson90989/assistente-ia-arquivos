
import pandas as pd
from docx import Document

def chunk_text(text, max_len=500):
    # Divide texto em pedaços max_len caracteres
    chunks = []
    current = ""
    for sentence in text.split('. '):
        if len(current) + len(sentence) < max_len:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "
    if current:
        chunks.append(current.strip())
    return chunks

def load_file_and_chunk(filepath):
    ext = filepath.split(".")[-1].lower()
    
    if ext in ["xlsx", "xls"]:
        df = pd.read_excel(filepath)
        text = df.to_csv(index=False)
    elif ext == "csv":
        df = pd.read_csv(filepath)
        text = df.to_csv(index=False)
    elif ext == "txt":
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    elif ext == "docx":
        doc = Document(filepath)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Formato não suportado")
        
    return chunk_text(text)
