import re
from analyzer.sensitive_detector import PATTERNS

REDACTION_TEXT = "[REDACTED]"

def redact_content(content):

    redacted = content

    for pattern in PATTERNS.values():

        redacted = re.sub(
            pattern,
            REDACTION_TEXT,
            redacted,
            flags=re.IGNORECASE
        )

    return redacted