import duckdb


def create_db_connection(path=":memory:"):
    '''create a connection to a duckdb database'''
    con = duckdb.connect(path)
    return con
