import logging
import traceback

import psycopg2

from common.CommonResultCode import CommonResultCode
from common.MonterException import MonterException
from common.const import Postgres

logger = logging.getLogger("api.common.pg_connection")


class PostgresUtil:
    def __init__(self):
        try:
            self.conn_credential = f'host={Postgres.ENDPOINT} user={Postgres.USER} password={Postgres.PASSWORD} dbname={Postgres.SCHEMA_NAME}'
            self.conn = psycopg2.connect(self.conn_credential)
        except Exception as err:
            logger.error(f'ERROR: Could not connect to Postgres instance. \n{traceback.format_exc()}')
            self.conn = None

    def get_select_query_result(self, query_string, args) -> map:
        if self.conn is None:
            raise MonterException(CommonResultCode.DB_CONNECTION_ERROR)

        with self.conn.cursor() as cur:
            cur.execute(query_string, args)
            columns = [col[0] for col in cur.description]
            logger.info(columns)
            rows = cur.fetchall()
            cur.close()

        return map(lambda x: dict(zip(columns, x)), rows)

    def insert_and_returning_query(self, query_string, args) -> map:
        if self.conn is None:
            raise MonterException(CommonResultCode.DB_CONNECTION_ERROR)

        with self.conn.cursor() as cur:
            cur.execute(query_string, args)
            self.conn.commit()
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()
            cur.close()

        return map(lambda x: dict(zip(columns, x)), rows)


pg_util = PostgresUtil()


def to_dict_by_relations(row, relation_table):
    result = {}
    join_data = {}
    for k, v in row.items():
        if k.startswith(f"{relation_table}_"):
            attr_name = k.split("_")[1]
            join_data[attr_name] = v
        else:
            result[k] = v

    result[relation_table] = join_data
    return result


