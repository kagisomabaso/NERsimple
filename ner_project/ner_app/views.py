# ner_app/views.py
from django.shortcuts import render
from .utils import extract_entities, extract_text_from_image
from django.core.files.storage import default_storage
import os


def ner_view(request):
    extracted_data = {}
    text = None

    if request.method == "POST" and request.FILES.get("uploaded_image"):
        uploaded_image = request.FILES["uploaded_image"]

        # Save the image to media directory
        image_path = default_storage.save("uploads/" + uploaded_image.name, uploaded_image)
        full_image_path = os.path.join("media", image_path)

        # Perform OCR to extract text
        text = extract_text_from_image(full_image_path)

        # Perform NER on extracted text
        extracted_data = extract_entities(text)

    return render(request, "ner_app/ner.html", {"extracted_data": extracted_data, "full_text": text})
