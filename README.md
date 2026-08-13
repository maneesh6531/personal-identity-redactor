# Personal Identity Redactor

A document redaction tool that detects and replaces personal identity information in DOCX documents with consistent synthetic values.

The system combines regular expressions, spaCy Named Entity Recognition, contextual heuristics, and document-aware processing to improve detection while minimizing false positives.

## Overview

Redacting personal information from real-world documents requires more than pattern matching. Names can appear in paragraphs, tables, headers, hyperlinks, and images, while ordinary numbers and capitalized phrases can be incorrectly identified as sensitive information.

This project uses a hybrid detection pipeline designed to handle these cases while preserving the original document structure as much as possible.

## Supported Information

The detector currently handles:

- Full names
- Email addresses
- Phone numbers
- Company names
- Physical and mailing addresses
- Social Security Numbers
- Credit card numbers
- Dates of birth
- IP addresses
- Director Identification Numbers (DIN)

It also processes information found in tables, hyperlinks, and embedded images.

## Detection Approach

```text
DOCX Document
      |
      v
Text and Table Extraction
      |
      v
+-----------------------------+
|       Detection Layer       |
|                             |
|  Regex                      |
|  spaCy NER                  |
|  Contextual Heuristics      |
|  Document-aware Extraction  |
+-----------------------------+
      |
      v
Candidate Filtering
      |
      v
PII Detection
      |
      v
Deterministic Replacement
      |
      v
Redacted DOCX
Regex

Regular expressions are used for structured information such as emails, phone numbers, IP addresses, SSNs, credit cards, dates, and other formatted identifiers.

spaCy NER

spaCy is used to identify person and organization entities that cannot reliably be detected through formatting rules alone.

Contextual Heuristics

NER models can miss unfamiliar names. A conservative fallback identifies likely multi-word names while filtering common document phrases such as:

Server IP
Phone Number
Order Number
Account Number
Date of Birth

This improves recall without unnecessarily redacting normal document content.

Deterministic Replacement

Repeated occurrences of the same entity receive the same replacement throughout the document.

For example:

Rashi Patil
rashi.patil@example.com

becomes:

Person Zeta
redacted.person001@example.invalid

This keeps the resulting document consistent and readable.

Evaluation

The project includes a separate deterministic evaluation harness in evaluate.py.

The evaluation uses the same production detection pipeline as the redaction system and contains both positive and negative examples.

Positive cases cover the supported information types, while negative cases include values such as order numbers, ticket numbers, years, percentages, and page numbers.

Results
Metric	Result
True Positives	10
False Positives	0
False Negatives	0
True Negatives	5
Accuracy	1.0000
Precision	1.0000
Recall	1.0000

The results represent the included deterministic benchmark and should not be interpreted as a guarantee of performance on arbitrary real-world documents.

See evaluation_report.md for the evaluation methodology and detailed results.

Project Structure
personal-identity-redactor/
│
├── app.py
├── redactor.py
├── evaluate.py
├── requirements.txt
├── render.yaml
└── .gitignore
File	Purpose
redactor.py	Core PII detection and DOCX redaction engine
app.py	FastAPI application
evaluate.py	Evaluation benchmark and metrics
requirements.txt	Python dependencies
render.yaml	Render deployment configuration
.gitignore	Excludes virtual environments and generated files
Running Locally

Clone the repository:

git clone https://github.com/maneesh6531/personal-identity-redactor.git
cd personal-identity-redactor

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
python -m spacy download en_core_web_sm

Start the API:

uvicorn app:app --reload

Open the interactive API documentation:

http://localhost:8000/docs

Use the /redact endpoint to upload a DOCX document and receive the redacted output.

Extending the Detector

The detection pipeline is modular, so a new information type can be added by:

Defining its detection rule.
Adding its replacement strategy.
Adding positive and negative evaluation cases.
Measuring its precision and recall.

This allows additional country-specific or domain-specific identity formats to be introduced without redesigning the complete pipeline.

Limitations
NER models can miss uncommon or ambiguous names.
Regex-based detection depends on the format of the information.
Complex DOCX layouts may not preserve every formatting characteristic.
Image-based detection depends on image quality and OCR accuracy.
The current evaluation dataset is intentionally small and deterministic.
Technology

Python, FastAPI, spaCy, python-docx, Pillow, Regular Expressions, Gunicorn, Render.
