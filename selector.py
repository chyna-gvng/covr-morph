import pymupdf4llm
import re

# indexed page ranges from the Harvard CV Guide
SAMPLE_GROUPS = [
    [8, 9], [10, 11], [12], [13], [14, 15], [16], [17, 18], [19, 20]
]

def get_context(jd_text: str, harvard_path: str = "data/harvard-cv-formats.pdf") -> dict:
    """
    Selector for Harvard CV guidelines and templates.
    """
    try:
        pages = pymupdf4llm.to_markdown(harvard_path, page_chunks=True)
    except Exception as e:
        raise RuntimeError(f"Failed to load {harvard_path}: {e}")

    advice_context = "\n".join(p["text"] for p in pages[1:7] if p["text"].strip())
    jd_keywords = set(re.findall(r'\w+', jd_text.lower()))
    
    best = {"score": -1, "text": "", "pages": []}
    
    for group in SAMPLE_GROUPS:
        content = "\n".join(pages[pg - 1]["text"] for pg in group)
        sample_words = set(re.findall(r'\w+', content.lower()))
        score = len(jd_keywords & sample_words)
        
        if score > best["score"]:
            best.update({"score": score, "text": content, "pages": group})

    return {
        "context": f"# HARVARD STYLE GUIDELINES\n{advice_context}\n\n# TEMPLATE STRUCTURE\n{best['text']}",
        "metadata": {"pages": best["pages"], "score": best["score"]}
    }
