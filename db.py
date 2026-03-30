import sqlite3, uuid, time

def connect():
    return sqlite3.connect("database.db")

def provedPrikaz(cmd: str, params: tuple | None = None, vraci: bool = False, kolik: int | None = None) -> list[tuple] | None:
    conn = connect()
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(cmd, params)
    else:
        cursor.execute(cmd)
    # well, jestli je tady chyba...hodně štěstí s debugováním
    fetched_data = cursor.fetchall() if vraci and kolik is None else cursor.fetchmany(int(kolik)) if vraci and int(kolik) > 0 else None
    conn.commit()
    cursor.close()
    conn.close()
    return fetched_data

def init_db():
    # datové typy v sqlite jsou pouze TEXT, INTEGER, REAL (v Javě jako double),
    # NUMERIC (nepoužil jsem nikdy) a BLOB (taky jsem nikdy nepoužil, ale je to k
    # uložení celého objektu, ale musíš k tomu napsat konvertor a dekonvertor)
    provedPrikaz("""
                    CREATE TABLE IF NOT EXISTS messages (
                        uuid TEXT,
                        zprava TEXT,
                        read INTEGER,
                        createdAt REAL,
                        edited INTEGER,
                        editedAt REAL,
                        PRIMARY KEY("uuid")
                    )
                """)

def createMessage(message):
    # otazníky v tom pžíkazu se používají jako proměnné, které se mají uložit do té databáze.
    # Může se dát přímo do příkazu danná proměnná, ale je to pak náchylné na  cross-site scripting (XSS)
    # a ačkoliv dělám hrozný kód, nenechám ho nezabezpečený
    provedPrikaz("""
                    INSERT INTO messages (
                        uuid, zprava, read, createdAt, edited, editedAt
                    ) VALUES ( ?, ?, ?, ?, ?, ? )
                """, (str(uuid.uuid4()), message, False, time.time(), False, 0))

def getMessages():
    messages = provedPrikaz("""
                                SELECT uuid, zprava, read, createdAt, edited, editedAt
                                FROM messages
                                ORDER BY createdAt
                """, vraci=False)

def editMessage(uuid, message):
    provedPrikaz("""
                    UPDATE messages
                    SET zprava = ?, read = ?, edited = ?, editedAt = ?
                    WHERE uuid = ?
                """, (message, 1, 1, time.time(), uuid))