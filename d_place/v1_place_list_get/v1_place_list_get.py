import json
import logging
import os
import traceback

import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PG_DB_NAME = os.environ.get('postgres_db_name', 'monter')
PG_DB_USER = os.environ.get('postgres_db_user', 'dbmasteruser')
PG_DB_PASSWORD = os.environ.get('postgres_db_password', 'W+BybAv~.N!*A0N;x^u}:b0k)j5CPo)$')

PG_DB_ENDPOINT = os.environ.get('postgres_endpoint', 'ls-af27c949e6d172afcaa4afd2d4b03e1a13311fdd.cbdr1wnqf8wg.ap-northeast-2.rds.amazonaws.com')
PG_DB_PORT = os.environ.get('postgres_port', '5432')


def lambda_handler(event, context):
    logger.info('Hello, world! Welcome to CloudWatch')
    try:
        conn_credential = f'host={PG_DB_ENDPOINT} user={PG_DB_USER} password={PG_DB_PASSWORD} dbname={PG_DB_NAME}'
        logger.warning(conn_credential)
        conn = psycopg2.connect(conn_credential)
    except Exception as err:
        logger.error(f'ERROR: Could not connect to Postgres instance. \n{traceback.format_exc()}')

    logger.info('SUCCESS: Connection to RDS Postgres instance succeeded')

    query = '''
        SELECT
            place.id, place.name, place.address, place."zipCode", place."franchiseId", place.latitude, place.longitude, f.*
        FROM place
            LEFT JOIN franchise f 
                ON place."franchiseId" = f.id;
                
    '''
    table_schema = ("id", "name", "")

    with conn.cursor() as cur:
        rows = []
        cur.execute(query)
        for row in cur:
            rows.append(row)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"place_users": rows})
    }


if __name__ == '__main__':
    print(lambda_handler({}, {}))