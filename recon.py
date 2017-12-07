import sqlite3

from dataset import loader

_conn = sqlite3.connect(":memory:")

def build_db():
    data = loader.csv_load("data.csv")

    c = _conn.cursor()
    c.execute("CREATE TABLE db (Nom text, Contact text, Role text, Responsable text, Niveau text, Equipe text, Competences text, Projets text, Complements text)")

    for row in data:
        c.execute("INSERT INTO db VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            row["Nom"],
            row["Contact"],
            row["Role"],
            row["Responsable"],
            row["Niveau Hierarchique"],
            row["Equipe"],
            row["Competences"],
            row["Projets"],
            row["Complements"]
        ])

    _conn.commit()


def get_answer(question):
    # Extract tags
    # We uses regexps in order to parse a given string


    # Match them in the DB
    pass

if __name__ == "__main__":
    build_db()
    get_answer(input(" > "))
