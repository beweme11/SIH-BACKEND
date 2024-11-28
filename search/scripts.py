import os
import json
import uuid
import time
import spacy
from thinc.api import require_gpu, set_gpu_allocator
from PyPDF2 import PdfReader
from search.models import GlobalRegistry, NerData
from django.db import transaction

# Enable GPU
require_gpu()
set_gpu_allocator("pytorch")

# Load the SpaCy model
nlp = spacy.load("en_legal_ner_trf")

# Path to the predefined folder and JSON file
PDF_FOLDER = "03-09-24"
STATUS_FILE = "search/status.json"


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Handle potential None values
    return text.strip()


def perform_ner_on_text(text):
    """
    Perform Named Entity Recognition on text using the SpaCy pipeline.
    Args:
        text (str): Input text for NER.
    Returns:
        dict: Extracted entities categorized by their labels.
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        if label not in entities:
            entities[label] = []
        entities[label].append(ent.text)

    # Convert entity lists to comma-separated strings
    for key in entities:
        entities[key] = ", ".join(entities[key])

    return entities


def save_ner_data_to_db(file_name, entities):
    """
    Save the extracted NER data to the database.
    Args:
        file_name (str): Name of the processed file.
        entities (dict): Extracted entities categorized by their labels.
    """
    with transaction.atomic():
        # Create a GlobalRegistry record
        global_record = GlobalRegistry.objects.create(uuid=uuid.uuid4(), file_name=file_name)

        # Create a NerData record linked to the GlobalRegistry record
        ner_data = NerData.objects.create(
            uuid=global_record,
            case_number=entities.get("CASE_NUMBER", ""),
            court=entities.get("COURT", ""),
            date=entities.get("DATE", ""),
            gpe=entities.get("GPE", ""),
            judge=entities.get("JUDGE", ""),
            lawyer=entities.get("LAWYER", ""),
            org=entities.get("ORG", ""),
            other_person=entities.get("OTHER_PERSON", ""),
            petitioner=entities.get("PETITIONER", ""),
            precedent=entities.get("PRECEDENT", ""),
            provision=entities.get("PROVISION", ""),
            respondent=entities.get("RESPONDENT", ""),
            statute=entities.get("STATUTE", ""),
            witness=entities.get("WITNESS", ""),
        )
        ner_data.save()


def process_pdfs():
    """
    Process all PDFs in the predefined folder, extract NER data, and save it to the database.
    """
    # Load or initialize the status JSON
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as file:
            status = json.load(file)
    else:
        status = {}

    # Iterate over all PDFs in the folder
    for pdf_file in os.listdir(PDF_FOLDER):
        if pdf_file.endswith(".pdf") and pdf_file not in status:
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
            print(f"Processing {pdf_file}...")

            # Extract text from the PDF
            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text:
                print(f"Skipped {pdf_file}: No text extracted.")
                status[pdf_file] = "Skipped"
                continue

            # Perform NER on the extracted text
            entities = perform_ner_on_text(pdf_text)

            # Save the results to the database
            save_ner_data_to_db(pdf_file, entities)

            # Mark the file as processed
            status[pdf_file] = "Processed"
            print(f"Processed {pdf_file} successfully.")

    # Save the updated status JSON
    with open(STATUS_FILE, "w") as file:
        json.dump(status, file, indent=4)


def process_unprocessed_pdfs():
    """
    Process only the PDFs that have not been processed yet.
    """
    process_pdfs()
