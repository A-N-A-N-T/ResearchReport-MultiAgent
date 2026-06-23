from database.db import get_connection
import sqlite3
import os

# this is for the creating the unique id for each data in sqlite
def generate_research_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM research_history
        ORDER BY id DESC
        LIMIT 1
    """)

    last = cursor.fetchone()

    conn.close()

    if last is None:
        return "RS001"

    number = int(last[0][2:]) + 1

    return f"RS{number:03d}"


# fn that help to save the research into DB
def save_research(
    topic , 
    report , 
    feedback , 
    search_results , 
    pdf_path
):
   research_id = generate_research_id()
   conn = get_connection()

   cursor = conn.cursor()
   cursor.execute(
     """
      INSERT INTO research_history(
         id, 
         topic,
         report,
         feedback,
         search_results,
         pdf_path
      )

      VALUES(?,?,?,?,?,?)
     """,
   
   (
     research_id,
     topic,
     report,
     feedback,
     search_results,
     pdf_path
   ))

   conn.commit()
   conn.close()

   return research_id


# Fn that help to fetch all the research paper from DB
def get_all_research():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        id,
        topic,
        created_at

        FROM research_history

        ORDER BY created_at DESC

    """)

    history = cursor.fetchall()

    conn.close()

    return history


# Fn that get the research data from the DB
def get_research_by_id(research_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM research_history

        WHERE id=?

    """,(research_id,))

    report = cursor.fetchone()

    conn.close()

    return report



# fn that help to delete research the data from sqlite db
def delete_research(research_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT pdf_path

        FROM research_history

        WHERE id=?

    """,(research_id,))

    pdf = cursor.fetchone()

    if pdf and os.path.exists(pdf[0]):
        os.remove(pdf[0])

    cursor.execute("""

        DELETE FROM research_history

        WHERE id=?

    """,(research_id,))

    conn.commit()

    conn.close()


#Fn that help to search the research paper from db
def search_history(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        id,
        topic,
        created_at

        FROM research_history

        WHERE topic LIKE ?

        ORDER BY created_at DESC

    """,(f"%{keyword}%",))

    result = cursor.fetchall()

    conn.close()

    return result


def delete_all_reports():

    conn = sqlite3.connect("database/research_history.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM research_history")

    conn.commit()
    conn.close()
    history = get_all_research()
    print(history)
    print("Database cleaned successfully!")