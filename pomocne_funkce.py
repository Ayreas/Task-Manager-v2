# Pomocné logické funkce

def odstranit_ukol_podle_id(ukol_id, conn):
    """Pomocná logická funkce pro odstranění úkolu dle ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ukoly WHERE UkolID = %s", (ukol_id,))
        conn.commit()
    
        cursor.execute("SELECT COUNT(*) FROM Ukoly WHERE UkolID = %s", (ukol_id,))
        pocet = cursor.fetchone()[0]

        cursor.close()
        return pocet == 0  

    except Exception as e:
        print(f"❌ Chyba při mazání úkolu: {e}")
        return False


def aktualizovat_ukol_podle_id(ukol_id, novy_stav, conn):
    """Pomocná logická funkce pro změnu stavu úkolu podle ID."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Ukoly SET Stav = %s WHERE UkolID = %s", (novy_stav, ukol_id))
        conn.commit()

        # Ověření 
        cursor.execute("SELECT Stav FROM Ukoly WHERE UkolID = %s", (ukol_id,))
        aktualni_stav = cursor.fetchone()

        cursor.close()
        return aktualni_stav is not None and aktualni_stav[0] == novy_stav

    except Exception as e:
        print(f"❌ Chyba při aktualizaci úkolu: {e}")
        return False