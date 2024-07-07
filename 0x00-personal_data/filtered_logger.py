#!/usr/bin/env python3
"""Definition of filter_datum function that returns an obfuscated log message
"""
import re
import logging
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
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text, with redacted
        sensitive information.

        This method overrides the base class method to add functionality
        for redacting specified fields in the log message. It uses the
        filter_datum function to replace sensitive field values with a
        redaction string before formatting the log record.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record as a string with sensitive
            fields redacted.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
