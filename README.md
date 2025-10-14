BookLog API
-----------
BookLog je REST API za vođenje evidencije pročitane literature, uključujući knjige, članke i stripove s mnogim atributima.

Funkcionalnosti
---------------
- CRUD operacije (kreiranje, čitanje, ažuriranje, brisanje) za Knjige (Book), Članke (Article) i Stripove (ComicBook)

- Filtriranje zapisa prema različitim kriterijima poput naslova, autora, žanra, raspoloženja, tagova i sl.

- Enum tipovi za žanr, ocjenu i raspoloženje radi konzistentnosti podataka.

- PostgreSQL nasljeđivanje tablica za učinkovito upravljanje zajedničkim i specifičnim atributima.

Tehnologije
------------
- Python 3.10+

- FastAPI - web framework za razvoj API-ja

- PostgreSQL - relacijska baza podataka

- asyncpg - asinkroni PostgreSQL klijent za Python

- Pydantic - za validaciju i serijalizaciju podataka

- PL/pgSQL - funkcija za računanje prosječne ocjene po žanru u bazi

Struktura repozitorija
-------------------------
- schemas.py - Pydantic modeli i enumeracije koje definiraju validaciju ulaznih podataka

- models.sql - SQL skripta za kreiranje tablica, tipova podataka i funkcija u PostgreSQL-u

- database.py - inicijalizacija asinkronog konekcijskog pool-a prema bazi podataka

- main.py - FastAPI aplikacija sa definiranim endpointim

- create_tables.py - skripta za kreiranje/rekreiranje tablica u bazi pozivanjem models.sql
