#!/usr/bin/env python3
"""
Custom logger
"""

import logging
import re
from mysql.connector.connection import MySQLConnection
from typing import Iterable, List
from os import getenv


PII_FIELDS = ("ssn", "email", "password", "name", "phone")


def get_db() -> MySQLConnection:
    """Connect to a secure database"""
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = getenv("PERSONAL_DATA_DB_NAME")
    return MySQLConnection(user=user, password=pwd, host=host, database=db)


def get_logger() -> logging.Logger:
    """Create a custom logger."""
    logger = logging.getLogger(name='user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Obfuscate logs based on self.fields"""
        log = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def main():
    """Entry point of the program."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")

    headers = [desc[0] for desc in cursor.description]

    logger = get_logger()

    for row in cursor:
        formatted = ';'.join([f"{h}={d}" for h, d in zip(headers, row)])
        logger.info(formatted)

    cursor.close()
    conn.close()
