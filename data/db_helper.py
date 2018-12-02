import sqlite3, json, time, datetime, os

# Logging functions here:

def log(string, logged=True):
    if not logged:
        return
    print("{}{}".format(datetime.datetime.now().strftime("(%Y-%m-%d)[%H:%M:%S]"), string))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Start of program logic:

class DBHelper():
    """
    The SQLite database helper I wrote in order to make SQLite queries with Python easier.
    
    Check out the code at https://github.com/lickorice/sqlite3-py-utils.

    Args:
        database_path (str): The path to your database, it will print a log message if the database does not exist.
        is_logged (:obj:`bool`, optional): shows verbose logs of the operations.

    Attributes:
        current_db (sqlite.connect): The connection object of the database as initialized with the :meth:`.connect()` method.
        database_path (str): The path to your database, it will print a log message if the database does not exist.
        is_logged (:obj:`bool`, optional): shows verbose logs of the operations.
    """
    def __init__(self, database_path, is_logged=True):
        """
        Args:
            database_path (str): The path to your database, it will print a log message if the database does not exist.
            is_logged (:obj:`bool`, optional): shows verbose logs of the operations.
        """
        self.database_path = database_path
        self.is_logged = is_logged

    def connect(self):
        """This function connects to a database."""
        if not os.path.isfile(self.database_path):
            log("[-ERR-] Database failed to connect. '{}' does not exist.".format(self.database_path), self.is_logged)
            return False
        self.current_db = sqlite3.connect(self.database_path)
        self.current_db.row_factory = dict_factory
        return True

    def close(self):
        """This function closes the connection."""
        self.current_db.close()
        self.current_db = None
        return

    def insert_row(self, table_name, **kwargs):
        """
        This function inserts a row in a table.
        
        Args:
            table_name (str): Name of the table to fetch rows from.
            strict (:obj:`bool`, optional): If the query will use = or LIKE comparators.
                Defaults to True (uses =).
            **kwargs (keyword args): Keyword parameters for initial data values.
        """

        exec_str = 'INSERT INTO {}('+'{}, '*len(kwargs)+') '
        exec_str += 'VALUES ('+'?, '*len(kwargs)+')'
        columns = [i for i in kwargs]
        exec_str = exec_str.format(table_name, *columns)
        exec_str = exec_str.replace(', )', ')')

        input_columns = tuple([kwargs[i] for i in kwargs])

        try:
            self.commit(exec_str, input_columns)
        except sqlite3.OperationalError as e:
            log('[-ERR-] ' + str(e).capitalize())
            return
        except sqlite3.IntegrityError as e:
            log('[-ERR-] ' + str(e).capitalize())
            return

        log("[-DB--] Successfully inserted new row to table '{}'.".format(table_name), self.is_logged)

    def fetch_rows(self, table_name, strict=True, **kwargs):
        """
        This function returns all the matches of a certain row

        Args:
            table_name (str): Name of the table to fetch rows from.
            strict (:obj:`bool`, optional): If the query will use = or LIKE comparators.
                Defaults to True (uses =).
            **kwargs (keyword args): Keyword parameters for pattern matching.
        """

        if strict:
            exec_str = "SELECT * FROM {} WHERE " + "{} = ? AND " * len(kwargs) + "<<"  # marker for removal
        else:
            exec_str = "SELECT * FROM {} WHERE " + "{} LIKE ? AND " * len(kwargs) + "<<"  # marker for removal
        
        columns = [i for i in kwargs]
        exec_str = exec_str.format(table_name, *columns)
        exec_str = exec_str.replace("AND <<", "")

        input_columns = tuple([kwargs[i] for i in kwargs])

        c = self.current_db.cursor()
        c.execute(exec_str, input_columns)
        results = c.fetchall()
        return results

    def fetch_all_rows(self, table_name):
        """
        This function returns all rows of a table
        
        Args:
            table_name (str): Name of the table to fetch rows from.
        """

        exec_str = "SELECT * FROM {}".format(table_name)
        
        c = self.current_db.cursor()
        c.execute(exec_str)
        results = c.fetchall()
        return results

    def remove_rows(self, table_name, **kwargs):
        """
        This function deletes all matches of a certain pattern.
        For safety purposes, LIKE (regex) cannot be used here.
        """

        exec_str = "DELETE FROM {} WHERE " + "{} = ? AND " *len(kwargs) + "<<"

        columns = [i for i in kwargs]
        exec_str = exec_str.format(table_name, *columns)
        exec_str = exec_str.replace("AND <<", "")

        input_columns = tuple([kwargs[i] for i in kwargs])

        self.commit(exec_str, input_columns)
        log("[-DB--] Successfully removed a row in table '{}'".format(table_name), self.is_logged)

    def update_column(self, table_name, column_name, column_value, **kwargs):
        """
        This function updates a column of a certain row given pattern.
        For safety purposes, LIKE (regex) cannot be used here.

        Args:
            table_name (str): Name of the table to fetch rows from.
            column_name (str): Column to update from.
            column_value (str): Value to update to.
            **kwargs (keyword args): Keyword parameters for pattern matching.
        """

        columns = [i for i in kwargs]
        input_columns = tuple([column_value] + [kwargs[i] for i in kwargs])

        exec_str = "UPDATE {} SET {} = ? WHERE ".format(table_name, column_name)
        exec_str += "{} = ? AND " * len(kwargs)
        exec_str += "<<"
        exec_str = exec_str.replace("AND <<", "")
        exec_str = exec_str.format(*columns)
        
        self.commit(exec_str, input_columns)
        log("[-DB--] Successfully updated a row in table '{}'".format(table_name), self.is_logged)

    def commit(self, string, column_tuple):
        """
        **Internally called by the class. Do not call directly.**
        
        This function executes and commits to the database.

        Args:
            string (str): Prepared string for the SQL query.
            column_tuple: Values for the prepared string.
        """
        c = self.current_db.cursor()
        c.execute(string, column_tuple)
        self.current_db.commit()
