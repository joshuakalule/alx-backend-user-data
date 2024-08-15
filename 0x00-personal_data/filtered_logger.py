#!/usr/bin/env python3
"""
Task 0. Regex-ing
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Uses a regex to replace occurrences of certain field values"""
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message
