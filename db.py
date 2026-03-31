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
    fetched_data = cursor.fetchall() if vraci and kolik is None else cursor.fetchmany(int(kolik)) if vraci and int(kolik) > 1 else cursor.fetchone() if vraci and int(kolik) == 1 else None
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

def getMessages() -> list[tuple] | None:
    return provedPrikaz("""
                                SELECT uuid, zprava, read, createdAt, edited, editedAt
                                FROM messages
                                ORDER BY createdAt
                """, vraci=True)

def getMessage(uuid: str) -> tuple[str | int] | None:
    message = provedPrikaz("""
                                SELECT zprava, read, createdAt, edited, editedAt
                                FROM messages
                """, vraci=True, kolik=0)
    return {
        "uuid": uuid,
        "message": message[0],
        "read": message[1],
        "createdAt": message[2],
        "edited": message[3],
        "editedAt": message[3],
    } if message is not None else None

def editMessage(uuid, message):
    provedPrikaz("""
                    UPDATE messages
                    SET zprava = ?, read = ?, edited = ?, editedAt = ?
                    WHERE uuid = ?
                """, (message, 1, 1, time.time(), uuid))

def deleteMessage(uuid: str):
    provedPrikaz("""
                    DELETE messages
                    WHERE uuid = ?
                """, (uuid, ))
    # BTW, tahle čárka    ^    na konci je třeba, protože to udělá z jedné proměnné tuple,
    # kterou ta funkce potřebuje k fungování