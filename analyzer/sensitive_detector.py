import re

PATTERNS = {

    "email":
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",

    "ip_address":
    r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",

    "api_key":
    r"(?:api[_-]?key|token|secret)[\"'\s:=]+[A-Za-z0-9_\-]{8,}",

    "password":
    r"(?:password|passwd|pwd)[\"'\s:=]+[^\s]+"
}


def detect_sensitive_data(text):

    findings = []

    for name, pattern in PATTERNS.items():

        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:

            findings.append({
                "type": name,
                "value": match
            })

    return findings