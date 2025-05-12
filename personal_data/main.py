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
