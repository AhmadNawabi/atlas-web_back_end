#!/usr/bin/env python3
"""
Filtered logger module
"""

import os
import re
import logging
import mysql.connector
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns the log message obfuscated.
    """
    for field in fields:
        message = re.sub(
            f"{field}=[^{separator}]*",
            f"{field}={redaction}",
            message
        )

    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Create a new instance of RedactingFormatter.

        Args:
                fields (List[str]): A list of strings representing
                fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum.

        Args:
                record (logging.LogRecord): The log record.

        Returns:
                str: The formatted and obfuscated log record.
        """
        original_formatted_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_formatted_message,
            self.SEPARATOR
        )


# Define the PII_FIELDS constant
PII_FIELDS: tuple = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and returns a Logger object.

    Returns:
            logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Create and return a connector to the database.

    Returns:
            MySQLConnection: The connection to the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )
    return connection


def main():
    """
    Main function that retrieves and displays filtered
    user data.
    """
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor.fetchall():
        to_log = ("name={};email={};phone={};ssn={};password={};"
                  "ip={};last_login={};user_agent={};").format(*row)
        logger.info(filter_datum(PII_FIELDS, "***", to_log, ";"))

    cursor.close()
    db_connection.close()
    if __name__ == "main":
        main()
