#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list of str): The list of fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log line where fields need to be obfuscated.
        separator (str): The character separating the fields in the log line.

    Returns:
        str: The log message with specified fields obfuscated.

    Example:
        fields = ["name", "email"]
        redaction = "REDACTED"
        message = "name=John Doe; email=john.doe@example.com; age=30"
        separator = "; "

        obfuscated_message = filter_datum(fields, redaction, message,separator)
        # Output: "name=REDACTED; email=REDACTED; age=30"
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
