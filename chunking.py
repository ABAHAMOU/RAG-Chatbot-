import logging
from pathlib import Path

import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def extraire_et_chunker(pdf_path, chunk_size=500, chunk_overlap=100):
    
    pdf_path = Path(pdf_path)
    texte_par_page = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                texte = page.extract_text()
                if texte:
                    texte_par_page.append((i, texte))
                else:
                    logger.warning(
                        "Page %d de %s sans texte extractible (page vide ou scannée sans OCR)",
                        i, pdf_path.name
                    )
    except Exception:
        logger.exception("Échec de lecture de %s", pdf_path)
        return []

    if not texte_par_page:
        logger.warning("Aucun texte extrait de %s", pdf_path.name)
        return []

    total_caracteres = sum(len(t) for _, t in texte_par_page)
    logger.info("Texte extrait de %s : %d caractères sur %d page(s)",
                pdf_path.name, total_caracteres, len(texte_par_page))

    chunking_model = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []
    for page_num, texte_page in texte_par_page:
        for morceau in chunking_model.split_text(texte_page):
            chunks.append({
                "text": morceau,
                "page": page_num,
                "source": pdf_path.name,
            })

    logger.info("%d chunks générés pour %s", len(chunks), pdf_path.name)
    return chunks