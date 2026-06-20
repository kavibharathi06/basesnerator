import re

def clean_text(text):
    # Split text into original lines first to preserve line structures
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # Remove strange OCR symbols per line
        line = re.sub(r"[^\w\s.,:()\-/%+=\[\]]", " ", line)
        # Remove repeated spaces
        line = re.sub(r"\s+", " ", line).strip()
        
        if not line:
            continue
            
        # Deduplicate consecutive repeated words
        words = []
        previous = ""
        for word in line.split():
            if word.lower() != previous.lower():
                words.append(word)
            previous = word
        
        cleaned_line = " ".join(words)
        if len(cleaned_line) > 0:
            cleaned_lines.append(cleaned_line)

    # Rejoin with clean line breaks so the pipeline knows lines are separate concepts!
    return "\n".join(cleaned_lines)