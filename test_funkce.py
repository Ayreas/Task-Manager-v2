
import pytest
from db import pripojeni_db
from funkce import pridat_ukol
from pomocne_funkce import odstranit_ukol_podle_id, aktualizovat_ukol_podle_id

# Test pozitivní a negativní pro pridat_ukol
def test_pridat_ukol_pozitivni():
    """Test funkce kdy je název i popis validně zadán."""
    pridat_ukol("Test Úkol", "Popis pro test")

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Ukoly WHERE Nazev = %s", ("Test Úkol",))
    result = cursor.fetchone()[0]

    # Úklid po testu (smaže testovací data)
    cursor.execute("DELETE FROM Ukoly WHERE Nazev = %s", ("Test Úkol",))
    conn.commit()

    cursor.close()
    conn.close()

    assert result == 1

def test_pridat_ukol_negativni():
    """"Test funkce kdy je prázdný popis úkolu -> vyhodí chybu"""
    with pytest.raises(TypeError):
        pridat_ukol("Neplatný Úkol", interaktivni=False)  # Zadán jen název, ale je nutný i popis úkolu.

# Test pozitivní a negativní pro aktualizovat_ukol
def test_aktualizovat_ukol_pozitivni():
    """Test pozitivní při kterém aktualizuji úkol podle ID a změním stav na 'Hotovo'"""
    pridat_ukol("Test Aktualizace", "Popis pro aktualizaci")

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT UkolID FROM Ukoly WHERE Nazev = %s", ("Test Aktualizace",))
    vybrane_id = cursor.fetchone()[0]

    aktualizovat_ukol_podle_id(ukol_id=vybrane_id, novy_stav="Hotovo", conn=conn)

    cursor.execute("SELECT Stav FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
    result = cursor.fetchone()[0]

    
    cursor.execute("DELETE FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
    conn.commit()

    cursor.close()
    conn.close()

    assert result == "Hotovo"


def test_aktualizovat_ukol_negativni():
    """Negativní test při kterém je zádáno záporné ID číslo"""
    conn = pripojeni_db()
    with pytest.raises(Exception):
        aktualizovat_ukol_podle_id(ukoly_id=-1, novy_stav="Hotovo", conn=conn)
    conn.close()


# Test pozitivní a negativní pro odstranit_ukol     
def test_odstranit_ukol_pozitivni():
    """Test pozitivní na odstranění úkolu podle ID"""
    pridat_ukol("Test Mazání", "Popis mazání")

    conn = pripojeni_db()
    cursor = conn.cursor()
    cursor.execute("SELECT UkolID FROM Ukoly WHERE Nazev = %s", ("Test Mazání",))
    vybrane_id = cursor.fetchone()[0]

    odstranit_ukol_podle_id(ukol_id=vybrane_id, conn=conn)

    cursor.execute("SELECT COUNT(*) FROM Ukoly WHERE UkolID = %s", (vybrane_id,))
    pocet = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    assert pocet == 0


def test_odstranit_ukol_negativni():
    """Test kdy vstup očekává číslo a jsou zadána písmena"""
    conn = pripojeni_db()
    vysledek = odstranit_ukol_podle_id(ukol_id="abc", conn=conn)  # zadám písmena místo čísel
    conn.close()

    assert vysledek is False

