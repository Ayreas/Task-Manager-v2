Pokyny pro správné fungování aplikace:

1) Vytvořit si databázi v MySQL s názvem Ukoly DB.
    příkaz v MySQL -> CREATE DATABASE UkolyDB;

2) Vytvořit si .env soubor ve stejné složce jako je projekt s nastavením připojení k databázi.

    vzor:
        DB_HOST=localhost
        DB_USER=root
        DB_PASSWORD=tvojeheslo   # Sem napiš svoje heslo k MySQL
        DB_NAME=UkolyDB

3) Aplikaci spustit v souboru hlavni.py .... případně v terminalu přes  příkaz python hlavni.py

4) Testy spouštět pomocí pytest  (pytest test_funkce.py)

5) Případně doinstalovat:
    - Pytest, příkaz v terminálu -> pip install pytest
    - práce s env, příkaz v terminálu -> pip install python-dotenv
    - MySQL balíček, příkaz v terminálu -> pip install mysql-connector-python

