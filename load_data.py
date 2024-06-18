import duckdb


def create_db_connection(path=":memory:"):
    '''create a connection to a duckdb database'''
    con = duckdb.connect(path)
    return con


def load_parquet_data(db, file_path="./Oct2018-WorkshopCUR-00001.snappy.parquet",):
    '''load a parquet file into a duckdb database'''

    db.execute(
        f"CREATE TABLE IF NOT EXISTS cur AS SELECT line_item_unblended_cost, product_servicecode, line_item_line_item_type from '{
            file_path}' where line_item_line_item_type = 'Usage'")


def create_db_and_load_data(db_path=":memory:"):
    '''create a connection to a duckdb database and load data into it'''
    db = create_db_connection(db_path)
    load_parquet_data(db)


if __name__ == "__main__":
    create_db_and_load_data()
