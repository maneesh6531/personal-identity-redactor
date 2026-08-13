"""Small deterministic evaluation harness for the PII detector.

The benchmark contains intentionally labeled PII and non-PII examples.
It is separate from the target prospectus so the evaluation is not circular.

The actual detection is delegated to redactor.py so that this evaluation
does not duplicate the detector's regexes, entity patterns, NER logic,
or fallback detection rules.
"""

from redactor import detect_pii_for_evaluation


CASES = [
    (
        "email",
        "Email me at alice.smith@example.com",
        {"EMAIL": ["alice.smith@example.com"]},
    ),
    (
        "phone",
        "Telephone: +91 98765 43210",
        {"PHONE": ["+91 98765 43210"]},
    ),
    (
        "ip",
        "Server IP: 192.0.2.10",
        {"IP": ["192.0.2.10"]},
    ),
    (
        "ssn",
        "SSN: 123-45-6789",
        {"SSN": ["123-45-6789"]},
    ),
    (
        "card",
        "Card: 4111 1111 1111 1111",
        {"CARD": ["4111 1111 1111 1111"]},
    ),
    (
        "dob",
        "Date of Birth: January 15, 1990",
        {"DOB": ["Date of Birth: January 15, 1990"]},
    ),
    (
        "din",
        "Director DIN 87654321",
        {"DIN": ["87654321"]},
    ),
    (
        "person",
        "Contact Person: Alice Johnson",
        {"PERSON": ["Alice Johnson"]},
    ),
    (
        "company",
        "Acme Technologies Limited",
        {"COMPANY": ["Acme Technologies Limited"]},
    ),
    (
        "address",
        "42 Example Road, Pune – 411 001, Maharashtra, India",
        {"ADDRESS": ["42 Example Road, Pune – 411 001, Maharashtra, India"]},
    ),
    (
        "negative-order",
        "Order 123456789 is ready",
        {},
    ),
    (
        "negative-ticket",
        "Ticket 123456789 is closed",
        {},
    ),
    (
        "negative-year",
        "Fiscal 2025 revenue increased",
        {},
    ),
    (
        "negative-percentage",
        "Growth was 12.50%",
        {},
    ),
    (
        "negative-page",
        "See page 420 for details",
        {},
    ),
]


def main():
    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for name, text, gold in CASES:

        # Use the actual production detector from redactor.py.
        predicted = detect_pii_for_evaluation(text)

        pred_spans = {
            (m.kind, m.value)
            for m in predicted
        }

        gold_spans = {
            (kind, value)
            for kind, values in gold.items()
            for value in values
        }

        case_tp = pred_spans & gold_spans
        case_fp = pred_spans - gold_spans
        case_fn = gold_spans - pred_spans

        tp += len(case_tp)
        fp += len(case_fp)
        fn += len(case_fn)

        if not pred_spans and not gold_spans:
            tn += 1

        print("\n------------------------------")
        print(f"CASE: {name}")
        print(f"EXPECTED: {gold_spans}")
        print(f"DETECTED: {pred_spans}")

        if case_fn:
            print(f"MISSED: {case_fn}")

        if case_fp:
            print(f"FALSE POSITIVE: {case_fp}")

        if not case_fn and not case_fp:
            print("PASS")

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    accuracy = (
        (tp + tn) / (tp + tn + fp + fn)
        if tp + tn + fp + fn
        else 0
    )

    print("\n==============================")
    print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"accuracy={accuracy:.4f}")
    print(f"precision={precision:.4f}")
    print(f"recall={recall:.4f}")
    print("==============================")


if __name__ == "__main__":
    main()