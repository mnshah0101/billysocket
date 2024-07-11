import re
import dotenv
import os
import psycopg2

dotenv.load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def execute_query(query):

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL)

    # Create a cursor
    cur = conn.cursor()

    # Execute the query
    try:
        cur.execute(query)
    except Exception as e:
        print(f'Error: {e}')
        return "There was an error executing the query."

    rows = cur.fetchall()

    cur.close()
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
