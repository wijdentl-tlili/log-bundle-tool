import math
from collections import Counter
import re


def calculate_entropy(text: str) -> float:

    if not text:
        return 0.0

    counter = Counter(text)

    length = len(text)

    entropy = 0.0

    for count in counter.values():

        probability = count / length

        entropy -= probability * math.log2(probability)

    return entropy


def extract_suspicious_strings(text: str, threshold: float = 4.5):

    """
    Detect high entropy strings (possible encoding/obfuscation)
    """

    # extract long strings (common in logs / payloads)
    candidates = re.findall(r"[A-Za-z0-9+/=]{20,}", text)

    findings = []

    for item in candidates:

        entropy = calculate_entropy(item)

        if entropy >= threshold:

            findings.append({

                "value": item,

                "entropy": round(entropy, 2),

                "risk": "HIGH" if entropy > 5 else "MEDIUM"
            })

    return findings