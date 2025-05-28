# Připojení k databázi - Vytvořit databázi ručně v MySQL jinak nebude fungovat! Název = UkolyDB

import mysql.connector
from mysql.connector import Error          
from dotenv import load_dotenv
import os

load_dotenv() # načte proměnné ze souboru .env 

def pripojeni_db():
    """Připojení k DB MySQL. Vyhodí chybovou hlášku když se nepodaří připojit a vypíše daný problém"""
    db_name = os.getenv("DB_NAME", "UkolyDB")                   
    try:
        conn = mysql.connector.connect(
            host= os.getenv("DB_HOST", "localhost"),
            user= os.getenv("DB_USER", "root"),
            password= os.getenv("DB_PASSWORD"),   # heslo je načteno z .env
            database= db_name
        )
        if conn.is_connected():
            print("✅ Připojení k databázi bylo úspěšné.\n") 
            return conn
    except Error as e:
        print(f"❌ Nepodařilo se ti připojit k databázi! '{db_name}': {e}")
        return None
