import sqlite3
from datetime import datetime


DATABASE = "sahayak.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        CREATE TABLE IF NOT EXISTS
        scan_results (

            id INTEGER PRIMARY KEY
            AUTOINCREMENT,

            content TEXT NOT NULL,

            risk_score INTEGER,

            risk_level TEXT,

            created_at TEXT

        )

    """)


    connection.commit()

    connection.close()


def save_scan(
    content,
    score,
    risk
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        INSERT INTO scan_results
        (
            content,
            risk_score,
            risk_level,
            created_at
        )

        VALUES (?, ?, ?, ?)

    """, (

        content,
        score,
        risk,
        datetime.now().isoformat()

    ))


    connection.commit()

    connection.close()


def get_scan_history():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT *
        FROM scan_results
        ORDER BY id DESC
        LIMIT 20

    """)


    rows = cursor.fetchall()

    connection.close()


    return [

        dict(row)

        for row in rows

    ]