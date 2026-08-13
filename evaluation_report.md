# Evaluation Report

## 1. Objective

The purpose of this evaluation is to measure the effectiveness of the Personal Identity Redactor in detecting supported personal identity information while avoiding unnecessary redaction of normal document content.

The evaluation focuses on:

- **Recall:** How many expected PII instances were detected?
- **Precision:** How many detected instances were actually PII?
- **Accuracy:** How many benchmark cases were classified correctly overall?

The evaluation is performed separately from the target prospectus using a small, deterministic benchmark with manually defined expected results.

---

## 2. Evaluation Design

The evaluation is implemented in `evaluate.py`.

The benchmark contains two types of cases:

### Positive cases

These contain known examples of supported personal identity information:

| Category | Example |
|---|---|
| Email | `alice.smith@example.com` |
| Phone | `+91 98765 43210` |
| IP Address | `192.0.2.10` |
| SSN | `123-45-6789` |
| Credit Card | `4111 1111 1111 1111` |
| Date of Birth | `January 15, 1990` |
| DIN | `87654321` |
| Person | `Alice Johnson` |
| Company | `Acme Technologies Limited` |
| Address | `42 Example Road, Pune – 411 001, Maharashtra, India` |

### Negative cases

Negative examples are included to test whether the detector unnecessarily identifies ordinary document information as PII.

The benchmark includes:

```
Order 123456789 is ready
Ticket 123456789 is closed
Fiscal 2025 revenue increased
Growth was 12.50%
See page 420 for details
```

These values are intentionally treated as non-PII for this evaluation.

This is important because a redaction system should not simply redact every number that looks sensitive.

---

## 3. Production Detector Used

The evaluation uses the same detection pipeline used by the actual redaction system.

`evaluate.py` does not contain a second implementation of the detector's regular expressions, NER rules, or contextual heuristics.

The flow is:

```
Evaluation Case
      |
      v
Production Detection Pipeline
      |
      v
Detected Entities
      |
      v
Comparison with Expected Entities
      |
      v
TP / FP / FN / TN
      |
      v
Accuracy / Precision / Recall
```

This ensures that the reported metrics correspond to the actual detector used by the application.

---

## 4. Evaluation Metrics

### True Positive (TP)

A PII entity that was expected and correctly detected.

Example:

```
Expected: EMAIL -> alice.smith@example.com
Detected: EMAIL -> alice.smith@example.com
```

This contributes one true positive.

### False Positive (FP)

An entity is detected as PII even though it is not present in the expected results.

For example, during development the detector initially classified:

```
Server IP
```

as a `PERSON`.

This was a false positive.

The generic-name fallback was then updated to reject common technical and document phrases.

### False Negative (FN)

An expected PII entity is present in the test case but the detector fails to identify it.

For example:

```
Expected: PERSON -> Alice Johnson
Detected: nothing
```

would result in one false negative.

### True Negative (TN)

A negative test case produces no PII detections.

For example:

```
Order 123456789 is ready
```

producing no detection contributes one true negative.

---

## 5. Metric Formulas

### Precision

Precision measures how many detected entities were actually correct.

```
Precision = TP / (TP + FP)
```

### Recall

Recall measures how many expected PII entities were successfully detected.

```
Recall = TP / (TP + FN)
```

### Accuracy

Accuracy measures the overall correctness across the benchmark.

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

---

## 6. Evaluation Run

The evaluation was executed using:

```bash
python evaluate.py
```

The final run produced:

```
TP=10 FP=0 FN=0 TN=5
accuracy=1.0000
precision=1.0000
recall=1.0000
```

### Final Results

| Metric | Result |
|---|---:|
| True Positives | 10 |
| False Positives | 0 |
| False Negatives | 0 |
| True Negatives | 5 |
| Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |

---

## 7. Results by Detection Objective

### PII Detection

All 10 positive benchmark instances were detected successfully.

```
True Positives  = 10
False Negatives = 0
```

Therefore:

```
Recall = 10 / (10 + 0)
       = 1.0000
       = 100%
```

This indicates that none of the PII instances included in the benchmark were missed.

### False Positive Control

None of the five negative cases produced an incorrect PII detection.

```
False Positives = 0
True Negatives  = 5
```

Therefore:

```
Precision = 10 / (10 + 0)
          = 1.0000
          = 100%
```

This indicates that the detector did not incorrectly classify any of the tested non-PII examples.

### Overall Accuracy

```
Accuracy = (10 + 5) / (10 + 0 + 0 + 5)
         = 15 / 15
         = 1.0000
         = 100%
```

All benchmark cases were classified correctly.

---

## 8. False Positive Testing During Development

The evaluation was also useful during development because it exposed an issue in the generic name detection fallback.

The following input:

```
Server IP: 192.0.2.10
```

was initially detected as:

```
IP: 192.0.2.10
PERSON: Server IP
```

The IP address was correct, but `Server IP` was an incorrect person detection.

The generic-name fallback was refined to reject common technical and document phrases, including:

```
Server IP
Client IP
IP Address
Phone Number
Account Number
Order Number
Date of Birth
```

After this change, the same evaluation case produced:

```
Expected:
{('IP', '192.0.2.10')}

Detected:
{('IP', '192.0.2.10')}
```

The false positive was eliminated without changing the expected IP detection.

---

## 9. Interpretation

The final benchmark demonstrates:

- All tested PII instances were detected.
- None of the tested PII instances were missed.
- None of the tested non-PII examples were incorrectly detected.
- The detector achieved perfect scores on the current benchmark.

The results are particularly useful for demonstrating the balance between recall and precision.

A detector with high recall but poor precision could redact large amounts of unrelated document content. Conversely, a highly conservative detector could avoid false positives while missing important personal information.

The current benchmark was designed to test both aspects.

---

## 10. Limitations of the Evaluation

The benchmark is intentionally small and deterministic. It is designed to provide a reproducible sanity check of the detection pipeline rather than serve as a statistically representative dataset.

The evaluation does not currently measure:

- Performance across a large document corpus
- Per-category precision and recall
- Multilingual names
- Country-specific identity formats beyond the implemented patterns
- OCR accuracy across different image qualities
- Complex document layouts
- Ambiguous real-world entities

Therefore, the reported 100% scores should be interpreted as:

> The detector achieved 100% accuracy, precision, and recall on the defined evaluation benchmark.

They should not be interpreted as a guarantee of 100% accuracy on arbitrary real-world documents.

---

## 11. Future Evaluation Improvements

A stronger evaluation framework could include:

- A larger human-annotated document dataset
- Per-entity-type precision and recall
- Separate test sets for different document types
- Multilingual name and organization examples
- Country-specific address and identity formats
- OCR-based test cases
- Regression tests built from previously discovered false positives and false negatives

This would provide a more comprehensive measurement of the detector's generalization to real-world documents.

---

## 12. Conclusion

The final evaluation achieved:

```
Accuracy  = 100%
Precision = 100%
Recall    = 100%
```

with:

```
TP = 10
FP = 0
FN = 0
TN = 5
```

The evaluation confirms that the current production detection pipeline correctly handled all positive and negative cases included in the benchmark while also demonstrating how the evaluation process was used to identify and reduce false positives during development.
