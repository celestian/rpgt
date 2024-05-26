import logging
import sqlite3

from rpgt.core.singleton import Singleton

structure = """
    DROP TABLE IF EXISTS modules;
    DROP TABLE IF EXISTS sections;
    DROP TABLE IF EXISTS elements;
    DROP TABLE IF EXISTS questions;
    DROP TABLE IF EXISTS answers;

    CREATE TABLE modules (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        version INTEGER NOT NULL
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
        self.__create_structure()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_structure(self):
        logging.info("Database structure created.")
        self.__cursor.executescript(structure)
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
                    current = [x for x in items if x["id"] == current["after"]][0]
                    line.append(current["id"])
                else:
                    line.append(current["after"])
                    orders.append({"id": item["id"], "order_level": len(line) - 2})
                    break
        return orders

    def __order_sections(self, sections):
        orders = self.__order_items(sections)
        for order in orders:
            sql = "UPDATE sections SET order_level = {} WHERE id = '{}'".format(
                order["order_level"], order["id"]
            )
            self.query(sql)

    def __order_elements(self, elements):
        orders = self.__order_items(elements)
        for order in orders:
            sql = "UPDATE elements SET order_level = {} WHERE id = '{}'".format(
                order["order_level"], order["id"]
            )
            self.query(sql)

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
        return self.query("SELECT * FROM modules").fetchall()

    def get_sections(self, module_id):
        return self.query(
            f"SELECT * FROM sections WHERE module_id = '{module_id}' ORDER BY order_level, name"
        ).fetchall()

    def get_elements(self, section_id):
        return self.query(
            f"SELECT * FROM elements WHERE section_id = '{section_id}' ORDER BY order_level, id"
        ).fetchall()

    def get_question(self, element_id):
        return self.query(
            f"SELECT * FROM questions WHERE element_id = '{element_id}'"
        ).fetchone()

    def get_answers(self, question_id):
        return self.query(
            f"SELECT * FROM answers WHERE question_id = '{question_id}'"
        ).fetchall()

    def query(self, sql):
        return self.__cursor.execute(sql)
