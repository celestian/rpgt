import sqlite3


class DataStorage:

    def __init__(self, data_path):

        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return dict(zip(fields, row))

        self.__connection = sqlite3.connect(":memory:")
        self.__connection.row_factory = dict_factory
        self.__cursor = self.__connection.cursor()

        print("Loading database...")
        db_dir = data_path.joinpath("data")
        for child in db_dir.iterdir():
            if child.is_file() and child.suffix == ".sql":
                with open(child, "r", encoding="utf-8") as f:
                    print(f"  {child}")
                    sql = f.read()
                    self.__cursor.executescript(sql)
                    self.__connection.commit()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()
        print("Database closed.")

    def query(self, sql):
        return self.__cursor.execute(sql)
