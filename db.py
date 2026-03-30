import sqlite3

def connect():
    return sqlite3.connect("database.db")

def provedPrikaz(cmd: str, params: tuple | None = None, vraci: bool = False) -> list[tuple] | None:
    conn = connect()
    cursor = conn.cursor()
    if params is not None:
        cursor.execute(cmd, params)
    else:
        cursor.execute(cmd)
    fetched_data = cursor.fetchall() if vraci else None
    conn.commit()
    cursor.close()
    conn.close()
    return fetched_data


def init_db():
    provedPrikaz("""
                    CREATE TABLE IF NOT EXISTS messages (
                        uuid TEXT,
                        zprava TEXT,
                        read INTEGER,
                        createdAt INTEGER,
                        edited INTEGER,
                        PRIMARY KEY("Field2")
                    )
                """)
init_db()


# # create a table
# cu.execute("create table lang(name, first_appeared)")

# # insert values into a table
# cu.execute("insert into lang values (?, ?)", ("C", 1972))
# # execute a query and iterate over the result
# for row in cu.execute("select * from lang"):
#     print(row)
