from duckdb import DuckDBPyConnection
from db import create_db_connection


def load_parquet_data(db: DuckDBPyConnection, file_path: str):
    '''load a parquet file into a duckdb database'''

    db.execute(
        f"CREATE TABLE IF NOT EXISTS cur AS SELECT line_item_unblended_cost, product_servicecode, line_item_line_item_type from '{
            file_path}' where line_item_line_item_type = 'Usage'")


def load_discount_data(db: DuckDBPyConnection, discounts_file_path: str):
    '''load a dictionary of discounts into a duckdb database'''

    db.execute(
        f"CREATE TABLE IF NOT EXISTS discounts AS SELECT * from '{discounts_file_path}'")


def create_db_and_load_data(db_path: str, parquet_file_path: str, discounts_file_path: str):
    '''create a connection to a duckdb database and load data into it'''
    db = create_db_connection(db_path)
    load_parquet_data(db, parquet_file_path)
    load_discount_data(db, discounts_file_path)


if __name__ == "__main__":
    create_db_and_load_data(db_path='data/test.db', parquet_file_path='data/Oct2018-WorkshopCUR-00001.snappy.parquet',
                            discounts_file_path='data/discounts.json')
