import mysql.connector
def get_connection():
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Keerthuma31",
    database="ai_skill_gap_analyzer"
)
    return connection




