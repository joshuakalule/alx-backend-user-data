#!/usr/bin/env python3
"""
Custom logger
"""

import logging
import re
from mysql.connector import connection
from typing import Iterable
import os


PII_FIELDS = ("ssn", "email", "password", "name", "phone")


def get_db() -> connection.MySQLConnection:
    """Connect to a secure database"""
    kwargs = {
        'host': os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.environ.get('PERSONAL_DATA_DB_NAME'),
        'user': os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    }

    return connection.MySQLConnection(**kwargs)


def get_logger() -> logging.Logger:
    """Create a custom logger."""
    logger = logging.getLogger(name='user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def filter_datum(fields: Iterable[str], redaction: str, message: str,
                 separator: str) -> str:
    """Uses a regex to replace occurrences of certain field values"""
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Iterable[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Obfuscate logs based on self.fields"""
        log = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)
