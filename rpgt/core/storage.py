import logging
import sqlite3
import sys

from rpgt.core.singleton import Singleton

DB_SCHEME = """
    DROP TABLE IF EXISTS modules;
    DROP TABLE IF EXISTS sections;
    DROP TABLE IF EXISTS elements;
    DROP TABLE IF EXISTS questions;
    DROP TABLE IF EXISTS answers;

    CREATE TABLE modules (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        version INTEGER NOT NULL,
        character_name_elememt TEXT NOT NULL
    );

    CREATE TABLE sections (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        after TEXT,
        order_level INTEGER,
        module_id TEXT NOT NULL,
        FOREIGN KEY (module_id) REFERENCES modules(id)
    );

    CREATE TABLE elements (
        id TEXT PRIMARY KEY,
        after TEXT,
        element_type TEXT NOT NULL,
        prompt_type TEXT NOT NULL,
        prompt_count INTEGER,
        condition TEXT NOT NULL,
        action TEXT NOT NULL,
        order_level INTEGER,
        section_id TEXT NOT NULL,
        FOREIGN KEY (section_id) REFERENCES sections(id)
    );

    CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        reference INTEGER,
        element_id INTEGER NOT NULL,
        FOREIGN KEY (element_id) REFERENCES elements(id)
    );

    CREATE TABLE answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        answer TEXT NOT NULL,
        description TEXT,
        reference INTEGER,
        question_id INTEGER NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions(id)
    );
"""


class DataStorage(metaclass=Singleton):

    def __init__(self):

        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return dict(zip(fields, row))

        self.__connection = sqlite3.connect("./rpgt.db")
        self.__connection.row_factory = dict_factory
        self.__cursor = self.__connection.cursor()
        self.__create_scheme()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def _query(self, sql):
        return self.__cursor.execute(sql)

    def __create_scheme(self):
        logging.info("Database scheme created.")
        self.__cursor.executescript(DB_SCHEME)
        self.__connection.commit()

    def __insert(self, table, data):
        fields = ", ".join(data.keys())
        values = ", ".join(["?" for _ in data.keys()])
        sql = f"INSERT INTO {table} ({fields}) VALUES ({values})"
        self.__cursor.execute(sql, tuple(data.values()))
        self.__connection.commit()

    def __order_items(self, items):
        orders = []
        for item in items:
            current = item
            line = [current["id"]]
            while True:
                if current["after"] is not None:
                    save = current
                    current = [x for x in items if x["id"] == current["after"]]
                    if current == []:
                        err_msg = f"Error: Cannot find [{save['after']}]"
                        err_msg += f" referenced in [{save['id']}]"
                        print(err_msg)
                        sys.exit(0)
                    current = current[0]
                    line.append(current["id"])
                else:
                    line.append(current["after"])
                    orders.append({"id": item["id"], "order_level": len(line) - 2})
                    break
        return orders

    def __order_sections(self, sections):
        orders = self.__order_items(sections)
        for order in orders:
            sql = f"UPDATE sections SET order_level = {order['order_level']} "
            sql += f"WHERE id = '{order['id']}'"
            self._query(sql)

    def __order_elements(self, elements):
        orders = self.__order_items(elements)
        for order in orders:
            sql = f"UPDATE elements SET order_level = {order['order_level']} "
            sql += f"WHERE id = '{order['id']}'"
            self._query(sql)

    def process(self):
        modules = self.get_modules()
        for module in modules:
            module_id = module["id"]
            sections = self.get_sections(module_id)
            self.__order_sections(sections)
            for section in sections:
                section_id = section["id"]
                elements = self.get_elements(section_id)
                self.__order_elements(elements)

    def add_module(self, data):
        self.__insert("modules", data)

    def add_section(self, data):
        self.__insert("sections", data)

    def add_element(self, data):
        self.__insert("elements", data)

    def add_question_answers(self, question, answers):
        self.__insert("questions", question)
        last_id = self.__cursor.lastrowid
        for answer in answers:
            answer["question_id"] = last_id
            self.__insert("answers", answer)

    def get_modules(self):
        return self._query("SELECT * FROM modules").fetchall()

    def get_character_name_element(self, module_id):
        return self._query(
            f"SELECT character_name_elememt FROM modules WHERE id = '{module_id}'"
        ).fetchone()["character_name_elememt"]

    def get_sections(self, module_id):
        sql = f"SELECT * FROM sections WHERE module_id = '{module_id}' "
        sql += "ORDER BY order_level, name"
        return self._query(sql).fetchall()

    def get_elements(self, section_id):
        sql = f"SELECT * FROM elements WHERE section_id = '{section_id}' "
        sql += "ORDER BY order_level, id"
        return self._query(sql).fetchall()

    def get_element(self, element_id):
        return self._query(
            f"SELECT * FROM elements WHERE id = '{element_id}'"
        ).fetchone()

    def get_question(self, element_id):
        return self._query(
            f"SELECT * FROM questions WHERE element_id = '{element_id}'"
        ).fetchone()

    def get_answers(self, question_id):
        return self._query(
            f"SELECT * FROM answers WHERE question_id = '{question_id}'"
        ).fetchall()
