import sqlite3, json

db_directory = 'db/'

with open('schema.json') as f:
    schemas_json = json.load(f)

baseExperience, factor = 50, 1.5

def exec_string_generate(schemas):
    """This processes a schema object into CREATE TABLE strings."""
    exec_strings = []
    for schema in schemas:
        exec_str = "CREATE TABLE IF NOT EXISTS {}(".format(schema["TABLE_NAME"])
        exec_str += "id INTEGER PRIMARY KEY,"
        columns = list(schema.keys())
        columns.remove("TABLE_NAME")
        for column in columns:
            exec_str += " {} {}".format(column, schema[column])
            exec_str += ')' if column == columns[-1] else ','
        exec_strings.append(exec_str)
    return exec_strings


def db_gen():
    """This creates a database made from the schema.json"""
    for database in schemas_json:
        exec_strings = exec_string_generate(schemas_json[database])
        target_db = sqlite3.connect('{}{}.db'.format(db_directory, database))
        c = target_db.cursor()
        for exec_str in exec_strings:
            c.execute(exec_str)
            target_db.commit()
        print(exec_strings)
        target_db.close()


def main():
    db_gen()


if __name__ == '__main__':
    main()