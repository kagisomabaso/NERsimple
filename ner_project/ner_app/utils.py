# ner_app/utils.py
import spacy
import pytesseract
from PIL import Image
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_image(image_path):
    """Extracts text from an uploaded image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_entities(text):
    # Process text with spaCy to extract entities
    doc = nlp(text)

    # Specify entity types to extract
    specified_entities = ["ORG", "DATE"]

    # Dictionary to hold extracted entities
    extracted_info = {entity.label_: [] for entity in doc.ents if entity.label_ in specified_entities}

    for entity in doc.ents:
        if entity.label_ in specified_entities:
            extracted_info[entity.label_].append(entity.text)

        # Extract emails using regular expression
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        if emails:
            extracted_info["EMAIL"] = emails

        # Extract locations (GPE: Geopolitical Entity, such as cities, countries)
        locations = [entity.text for entity in doc.ents if entity.label_ == "GPE"]
        if locations:
            extracted_info["GPE"] = locations

    return extracted_info
