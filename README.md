# Personal Identity Redactor
 
A DOCX document redaction tool that detects and replaces personal identity information with consistent synthetic values.
 
The system combines regular expressions, spaCy Named Entity Recognition, contextual heuristics, and document-aware processing to improve detection while minimizing false positives.
 
## Overview
 
The tool is designed to redact sensitive information from real-world DOCX documents while preserving the document structure as much as possible.
 
It processes information found in:
 
- Paragraphs
- Tables
- Hyperlinks
- Embedded images
## Supported Information
 
- Full names
- Email addresses
- Phone numbers
- Company names
- Physical and mailing addresses
- Social Security Numbers (SSNs)
- Credit card numbers
- Dates of birth
- IP addresses
- Director Identification Numbers (DINs)
## Detection Architecture
 
The detector uses multiple complementary techniques rather than relying on a single model.
 
```
                         DOCX Document
                               |
                               v
                    Text / Table Extraction
                               |
                +--------------+--------------+
                |              |              |
                v              v              v
             Regex        spaCy NER     Contextual Rules
                |              |              |
                +--------------+--------------+
                               |
                               v
                       Candidate Filtering
                               |
                               v
                         PII Detection
                               |
                               v
                    Replacement Generation
                               |
                               v
                         Redacted DOCX
```
 
### 1. Regex-Based Detection
 
Regular expressions handle structured information where the format itself provides a strong signal.
 
Examples include:
 
- Email addresses
- Phone numbers
- IP addresses
- SSNs
- Credit card numbers
- Dates of birth
- DINs
- Address patterns
For example, an email such as:
 
```
alice.smith@example.com
```
 
can be detected directly from its structural pattern without requiring a language model.
 
This makes regex detection deterministic and reliable for highly structured identifiers.
 
### 2. spaCy Named Entity Recognition
 
The system uses spaCy's en_core_web_sm model for contextual entity recognition.
 
The model is used primarily for:
 
- PERSON
- ORG
For example:
 
```
Priya Kapoor joined Example Technologies.
```
 
can be interpreted as:
 
```
Priya Kapoor          -> PERSON
Example Technologies  -> ORG
```
 
Unlike regex, NER does not depend on a fixed format. It uses the surrounding language context to determine whether a sequence of words represents a person or organization.
 
This is particularly useful for company names and names that do not follow a predictable pattern.
 
### 3. Generic Name Detection
 
NER models are not perfect and can miss unfamiliar names.
 
To improve recall, the system includes a conservative fallback for likely multi-word names.
 
For example:
 
```
Neeraj Malhotra reviewed the report.
```
 
If the NER model fails to recognize Neeraj Malhotra, the fallback can identify it based on characteristics such as:
 
- Multiple name-like tokens
- Title-case structure
- Word boundaries
- Context
- Exclusion of known company names
The fallback is deliberately conservative because treating every capitalized phrase as a person would create a large number of false positives.
 
### 4. Contextual Filtering
 
Candidate entities are filtered using document context before being treated as personal information.
 
For example, phrases such as:
 
- Server IP
- Phone Number
- Order Number
- Account Number
- Date of Birth
- IP Address
may look like person-name candidates because they contain multiple capitalized words.
 
These are explicitly rejected by the generic-name detection layer.
 
This allows the system to improve name recall while controlling false positives.
 
### 5. Company Detection
 
Organizations can appear repeatedly throughout a business document.
 
The detector identifies company names and uses them during candidate filtering so that organization names are not incorrectly treated as person names.
 
This is particularly useful for documents such as prospectuses where company names may occur hundreds of times.
 
## Entity Replacement
 
Once an entity is detected, the system creates a deterministic replacement mapping.
 
For example:
 
Original:
```
Rashi Patil
rashi.patil@example.com
```
 
becomes:
 
Redacted:
```
Person Zeta
redacted.person001@example.invalid
```
 
If Rashi Patil appears again later in the document, it receives the same replacement:
 
```
Person Zeta
```
 
rather than generating a different name.
 
This maintains consistency throughout the document while removing the original identity.
 
## Document Processing
 
The redactor works at the DOCX level rather than treating the document as plain text.
 
The processing pipeline handles:
 
- Paragraphs
- Tables
- Hyperlinks
- Embedded images
For image content, the system can process embedded images separately and redact detected sensitive regions.
 
This is important because personal information in real documents is not always stored as ordinary paragraph text.
 
## Evaluation
 
The project includes a deterministic evaluation harness in evaluate.py.
 
The evaluation uses the same production detection pipeline as the redaction system.
 
The benchmark contains positive cases covering the supported entity types and negative cases such as:
 
- Order numbers
- Ticket numbers
- Fiscal years
- Percentages
- Page numbers
### Results
 
| Metric | Result |
|---|---|
| True Positives | 10 |
| False Positives | 0 |
| False Negatives | 0 |
| True Negatives | 5 |
| Accuracy | 1.0000 |
| Precision | 1.0000 |
| Recall | 1.0000 |
 
These results represent the current deterministic benchmark and should not be interpreted as a guarantee of performance on arbitrary real-world documents.
 
See evaluation_report.md for the detailed evaluation methodology.
 
## API
 
The redaction engine is exposed through a FastAPI service.
 
```
POST /redact
```
 
The API accepts a DOCX document and returns the redacted document.
 
Interactive API documentation is available at:
 
```
/docs
```
 
## Project Structure
 
```
personal-identity-redactor/
│
├── app.py              # FastAPI application
├── redactor.py         # Detection and DOCX redaction engine
├── evaluate.py         # Evaluation benchmark
├── requirements.txt    # Dependencies
├── render.yaml         # Render deployment configuration
└── .gitignore
```
 
## Extending the Detector
 
The detection pipeline is modular. A new identity type can be introduced by adding:
 
- A detection rule
- A replacement strategy
- Positive evaluation cases
- Negative evaluation cases
This allows the system to be extended with additional country-specific or domain-specific identity formats.
 
## Limitations
 
- NER models can miss uncommon or ambiguous names.
- Regex detection depends on the format of the information.
- Complex DOCX layouts may not preserve every formatting characteristic.
- Image-based detection depends on image quality and OCR accuracy.
- The current evaluation dataset is small and deterministic.
## Future Improvements
 
- Larger human-annotated evaluation datasets
- Per-entity-type precision and recall
- Additional country-specific identity formats
- Multilingual NER support
- Improved OCR for scanned documents
- Confidence scoring for ambiguous detections
- Automated regression testing with larger document corpora
## Technology
 
Python · FastAPI · spaCy · python-docx · Pillow · Regular Expressions · Gunicorn · Render
