# Definování funkcí z menu

from mysql.connector import Error    # Musím naimportovat Error zvlášť aby fungoval!
from db import pripojeni_db
from pomocne_funkce import odstranit_ukol_podle_id, aktualizovat_ukol_podle_id

def pridat_ukol(Nazev=None, Popis=None, interaktivni=True):
    """Přidá úkol do databáze. Ošetření prazdných vstupů i nečekané události (př: spadne databáze)."""
    if not interaktivni:
        if Nazev is None or not Nazev.strip():
            raise TypeError("❌ Název úkolu je povinný! Zkus to znovu.")
        if Popis is None or not Popis.strip():
            raise TypeError("❌ Popis úkolu je povinný! Zkus to znovu.")

    if not Nazev or not Nazev.strip():
        while True:
            Nazev = input("Zadej název úkolu: ").strip()
            if Nazev:
                break
            print("❌ Název úkolu je povinný! Zkus to znovu.")

    if not Popis or not Popis.strip():
        while True:
            Popis = input("Zadej popis úkolu: ").strip()
            if Popis:
                break
            print("❌ Popis úkolu je povinný! Zkus to znovu.")
 
    conn = pripojeni_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ukoly (Nazev, Popis)VALUES (%s, %s)", (Nazev.strip(), Popis.strip()))
        conn.commit()
        print("✅ Úkol byl úspěšně uložen do databáze.")
        
    except Error as e:
        print(f"❌ Chyba při ukládání úkolu: {e}")

    finally:
        cursor.close()
        conn.close()

def zobrazit_ukol():
    """Zobrazí seznam všech úkolů s informacemi: ID, název, popis, stav, datum vytvoření. Ošetřuje chyby či prázdný seznam v DB."""
    conn = pripojeni_db()
    if conn is None:
        return
    
    try: 
        cursor = conn.cursor()
        cursor.execute("""
            SELECT UkolID, Nazev, Popis, Stav, Datum FROM Ukoly
            WHERE Stav IN ('Nezahájeno', 'Probíhá')
            ORDER BY UkolID
        """)
        ukoly = cursor.fetchall()

        if not ukoly:
            print("❌ Seznam úkolů je prázdný!")
            return
        
        print("📋 Seznam úkolů:")
        for ukol in ukoly:
            print(f"📌 ID: {ukol[0]}, Název: {ukol[1]}, Popis: {ukol[2]}, Stav: {ukol[3]}, Vytvořeno: {ukol[4].date()}")
    
    except Error as e:
        print(f"❌ Chyba při zobrazení úkolů: {e}")
    
    finally:
        cursor.close()
        conn.close()

def aktualizovat_ukol():
    """Změna stavu úkolu, filtr na "Nezahájeno a Probíhá", Hotovo není zahrnuto."""
    conn = pripojeni_db()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    try:
        # Zobrazení úkolu kde je stav Nezahájeno či Probíhá
        cursor.execute("""
            SELECT UkolID, Nazev, Stav FROM Ukoly 
            WHERE Stav IN ('Nezahájeno', 'Probíhá')  
            ORDER BY UkolID
        """)
        ukoly = cursor.fetchall()
        
        if not ukoly:
            print("❌ Seznam úkolů je prázdný!")
            return
        
        print("📋 Seznam úkolů:")
        # Přidání ikonek pro lepši uživatelskou přívětivost
        stav_map = {
        "Nezahájeno": "🛑 Nezahájeno",
        "Probíhá": "⏳ Probíhá"
        }

        for ukol in ukoly:
            stav_text = stav_map[ukol[2]]  
            print(f"📌 ID: {ukol[0]}, Název: {ukol[1]}, Stav: {stav_text}")

    except Error as e:
        print(f"❌ Chyba při zobrazení úkolů: {e}")  

    # Část kde vybírám úkol dle ID 
    while True:
        try:
            vybrane_id = int(input("\nZadej ID úkolu, který chceš aktualizovat: "))
            print()
            cursor.execute("SELECT COUNT(*) FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                print("❌ Toto ID úkolu neexistuje, zkus to prosím znovu.")
                continue
            break
        
        except ValueError:
            print("❌ Zadej prosím platné číslo!")

    # Tímhle si získam původní stav do proměnné puvodni_stav
    cursor.execute("SELECT Stav FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
    puvodni_stav = cursor.fetchone()[0]
    
    # Část kdy měním stav úkolu
    while True:
        try:
            print("📋 Vyber nový stav úkolu: ")
            print("1 - Probíhá ⏳")
            print("2 - Hotovo ✅\n")
            volba = int(input("Tvoje volba: "))

            if volba == 1:
                novy_stav = "Probíhá"
                break

            elif volba == 2:
                novy_stav = "Hotovo"
                break
            else:
                print("❌ Neplatná volba, zadej číslo 1 nebo 2.")
        except ValueError:
            print("❌ Zadej prosím číslo.")

    # Část kdy updatuji databazi
    try:
        uspesne = aktualizovat_ukol_podle_id(vybrane_id, novy_stav, conn)
        if uspesne:
            print("✅ Stav úkolu byl úspěšně aktualizován.\n")
        else:
            print("❌ Nepodařilo se aktualizovat stav úkolu.")
            return

        while True:
            zpet = input("Chceš vrátit změnu? (a/n): ").lower()
            if zpet == 'a':
                aktualizovat_ukol_podle_id(vybrane_id, puvodni_stav, conn)
                print("↩️ Změna byla vrácena zpět.")
                break
    
            elif zpet == 'n':
                print("✅ Změna potvrzena.")
                break
            else:
                print("❌ Neplatná volba. Zadej prosím 'a' pro vrácení nebo 'n' pro potvrzení.")

    except Error as e:
        print(f"❌ Chyba při aktualizaci úkolu: {e}")
    finally:
        cursor.close()
        conn.close()

def odstranit_ukol():
    """Odstranění úkolu z databáze po vybrání ID."""
    conn = pripojeni_db()
    if conn is None:
        return
    
    cursor = conn.cursor()

    # Nejdřív zobrazím úkoly z databáze
    try:
        cursor.execute("SELECT UkolID, Nazev, Stav FROM Ukoly ORDER BY UkolID")
        ukoly = cursor.fetchall()

        if not ukoly:
            print("❌ Nejsou k dispozici žádné úkoly pro odstranění.")
            return        

        print("📋 Seznam úkolů:")
        for ukol in ukoly:
            print(f"📌 ID: {ukol[0]}, Název: {ukol[1]}, Stav: {ukol[2]}")

    except Error as e:
        print(f"❌ Chyba při zobrazení úkolů: {e}")
        return
    
    # Výběr ID úkolu k odstranění
    while True:
        try:
            vybrane_id = int(input("\nZadej ID úkolu, který chceš odstranit: "))
            print()
            cursor.execute("SELECT COUNT(*) FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                print("❌ Toto ID úkolu neexistuje, zkus to prosím znovu.")
                continue
            break

        except ValueError:
            print("❌ Zadej prosím platné číslo!")
    
    while True:
        potvrzeni = input("⚠️  Opravdu chceš úkol odstranit? (a/n): ").lower()
        print()

        if potvrzeni == 'a':
            try:
                uspesne = odstranit_ukol_podle_id(ukol_id=vybrane_id, conn=conn)
                if uspesne:
                    print("🗑️  Úkol byl úspěšně odstraněn.")
                else:
                    print("❌ Úkol se nepodařilo odstranit.")
            except Error as e:
                print(f"❌ Chyba při odstraňování úkolu: {e}")
            break


        elif potvrzeni == 'n':
            print("ℹ️  Odstranění bylo zrušeno.")
            cursor.close()
            conn.close()
            return

        else:
            print("❌ Neplatná volba. Zadej prosím 'a' pro smazání nebo 'n' pro zrušení.")

def reset_tabulky():
    """Vymaže všechna data z tabulky Ukoly a resetuje ID znovu na 1!"""
    conn = pripojeni_db()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Ukoly")                    # Smaže vše z tabulky Ukoly
        cursor.execute("ALTER TABLE Ukoly AUTO_INCREMENT = 1") # Reset ID na 1.
        conn.commit()
        print("🧹 Data v tabulce Ukoly byla vymazána a ID resetováno.")
    
    except Exception as e:
        print(f"❌ Chyba při mazání dat tabulky: {e}")
    
    finally:
        cursor.close()
        conn.close()    