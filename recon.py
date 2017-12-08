import sqlite3
import logging
import re

from random import shuffle
from dataset import loader

_logg = logging.getLogger()
_logg.addHandler(logging.StreamHandler())
_logg.setLevel(logging.DEBUG)

_conn = sqlite3.connect(":memory:")
_c    = _conn.cursor()

DEFAULT_ANSWERS = [
    "Désolé, je n'arrive pas à comprendre, pouvez vous reformuler ?",
    "Ah bah ça alors, je suis encore entrain d'apprendre, pardonnez moi...",
    "Excusez moi, je ne comprend pas"
]

def build_db():
    data = loader.csv_load("data.csv")

    _c.execute("CREATE TABLE db (Nom text, Contact text, Role text, Responsable text, Niveau text, Equipe text, Competences text, Projets text, Complements text)")

    for row in data:
        _logg.debug("DB: loading {}".format(row))
        _c.execute("INSERT INTO db VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            row["Nom"].lower(),
            row["Contact"].lower(),
            row["Role"].lower(),
            row["Responsable"].lower(),
            row["Niveau Hierarchique"].lower(),
            row["Equipe"].lower(),
            row["Competences"].lower(),
            row["Projets"].lower(),
            row["Complements"].lower()
        ])

    _conn.commit()


def get_answer(question):
    # Extract tags
    tags = []

    question = question.lower()

    # We uses regexps in order to parse a given string
    for row in _c.execute("SELECT Nom, Contact, Role, Responsable, Niveau, Equipe, Competences, Projets, Complements FROM db"):
        for subrow in row:
            if re.match(".*" + subrow + ".*", question):
                _logg.info("CORE: {} match \"{}\"".format(subrow, question))
                tags.append(subrow)

    # Get the meaning of our question
    classes = {
            "Nom"         : ".*(qui|nom|appelle).*",
            "Contact"     : ".*(contact|lieu|où|habite).*",
            "Role"        : ".*(fait|role|véhicule|piéton).*",
            "Responsable" : ".*(supérieur|responsable|frère|soeur).*",
            "Niveau"      : ".*(adulte|enfant|niveau).*",
            "Equipe"      : ".*(état|équipe).*",
            "Competences" : ".*(situation|compétence|projet).*",
            "Projets"     : ".*(faire|projets).*",
            "Complements" : ".*(suplémentaires|complément|complète).*"
    }

    classes_found = []

    _logg.debug("CORE: classifying question")

    for key in classes.keys():
        if re.match(classes[key], question):
            _logg.info("CORE: {} has been tagged with {}".format(question, key))
            classes_found.append(key)

    # Si pas de classes trouvées, on return
    if len(classes_found) == 0:
        return shuffle(DEFAULT_ANSWERS)

    # We need each type of tags
    def get_types_for_tag(tag):
        tag_type = []

        for type_tag in ("Nom", "Contact", "Role", "Responsable", "Niveau", "Equipe", "Competences", "Projets", "Complements"):
            # Check if in column
            for row in _c.execute("SELECT group_concat({}, \",\") FROM db".format(type_tag)):
                if tag in row[0].split(","):
                    tag_type.append(type_tag)

        return tag_type

    def extend_sql_query_string(sql_query_str, to_be_added):
        if not sql_query_str.endswith("WHERE "): sql_query_str += " OR "
        sql_query_str += to_be_added

        return sql_query_str

    def build_search_query():
        query = ""

        for query_class in classes_found:
            if query != "": query += ", "
            query += query_class

        return query

    # Build sql query
    sql_query = "SELECT {} FROM db WHERE ".format(build_search_query())

    # Start building via tags
    for tag in tags:
        type_of_tag_list = get_types_for_tag(tag)
        for type_of_tag in type_of_tag_list:
            # TODO: remove duplicates
            sql_query = extend_sql_query_string(sql_query, "{}='{}'".format(type_of_tag, tag))

    for row in _c.execute(sql_query):
        print(row)

    # Match them in the DB
    # So we look for tags in `classes_found`, based on data in `tags`

if __name__ == "__main__":
    build_db()
    get_answer(input(" > "))
