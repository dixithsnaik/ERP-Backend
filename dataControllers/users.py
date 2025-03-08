from dataControllers.cursor import cursor
import logging

def getUsers():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching users: {e}")
        return {"error": str(e)}


