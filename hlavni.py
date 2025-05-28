# Projekt 2 - Task Manager propojený s Databází - Martin Papež

from db import pripojeni_db
from funkce import pridat_ukol, zobrazit_ukol, aktualizovat_ukol, odstranit_ukol, reset_tabulky

# Vytvoření tabulky pro úkoly
def vytvoreni_tabulky():
    """Vytvoření tabulky Ukoly v databázi UkolyDB"""
    conn = pripojeni_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ukoly (
        UkolID INT PRIMARY KEY AUTO_INCREMENT,
        Nazev VARCHAR(100) NOT NULL,
        Popis VARCHAR(200) NOT NULL,
        Stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
        Datum TIMESTAMP DEFAULT CURRENT_TIMESTAMP                               
    )
    """)
    # Poznámka - kdyz u Datum dám klasický CURDATE() tak to Mysql nepobere a vyhodí chybu.
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tabulka byla úspěšně vytvořena (nebo již existuje!).")

# Definování hlavního menu
def hlavni_menu():
    """Spustí hlavní menu. Možnost volby 1-5, při chybném čísle vypíše chybu."""
    while True:
        print ("\nSprávce úkolů - Hlavní menu 📝") 
        print ("1. Přidat nový úkol")
        print ("2. Zobrazit všechny úkoly")
        print ("3. Aktualizovat úkol")
        print ("4. Odstranit úkol")
        print ("5. Resetovat tabulku")              # Tato volba odstraní data z tabulky a ID opět nastaví od 1!!!
        print ("6. Konec programu")

        volba = input ("Vyberte možnost (1-5): ") 
        if  volba == "1":
            print()     
            while True:
                Nazev = input("Zadej název úkolu: ").strip()
                if Nazev:
                    break
                print("❌ Název úkolu je povinný! Zkus to znovu.")

            while True:
                Popis = input("Zadej popis úkolu: ").strip()
                if Popis:
                    break
                print("❌ Popis úkolu je povinný! Zkus to znovu.")
            pridat_ukol(Nazev, Popis)               
        elif volba == "2":
            print()
            zobrazit_ukol()
        elif volba == "3":
            print()
            aktualizovat_ukol()
        elif volba == "4":
            print()
            odstranit_ukol()
        elif volba == "5":
            print()
            while True:
                potvrzeni = input("⚠️  Opravdu chceš vymazat všechna data z tabulky? Tuto akci nelze vrátit! ⚠️  (a/n): ").lower()
                if potvrzeni == 'a':
                    reset_tabulky()
                    break
                elif potvrzeni == 'n':
                    print("ℹ️  Akce vymazání dat byla zrušena.")
                    break
                else:
                    print("❌ Neplatná volba. Zadej prosím 'a' pro potvrzení nebo 'n' pro zrušení.")
        elif volba == "6":
            print()
            print("Konec programu.👋")
            break
        else:
            print("❌ Neplatná volba. Zkuste to znovu.")


if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()