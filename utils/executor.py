import sqlite3
import re


def execute_query(query):

    conn = sqlite3.connect('nfl.db')

    cur = conn.cursor()

    cur.execute(query)

    rows = cur.fetchall()
    conn.close()
    return rows


def extract_sql_query(input_string):
    if 'sql' not in input_string:
        return input_string
    # Use regular expression to find the SQL query within the triple quotes
    match = re.search(r'```sql\n(.*?)\n```', input_string, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None
