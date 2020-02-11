import asyncio
import logging
import random
from datetime import timedelta, date
from itertools import cycle

import aiomysql

from api.settings import Config

ROWS_COUNT_OF_MONTH = 219000
START_YEAR = 2019
END_YEAR = 2020
ACTIONS = [
    'test', 'created', 'disconnected', 'investigate', 'updated',
    'deleted', 'implemented', 'cancelled', 'pending'
]


def generate_events_for_month(count=ROWS_COUNT_OF_MONTH):
    for i in range(0, count):
        _id = random.randrange(0, 1999)
        uid = random.randrange(0, 1999)
        action = random.choice(ACTIONS)
        yield {'id': _id, 'uid': uid, 'action': action}


def date_range(start_date, years_days):
    for day in range(years_days):
        yield start_date + timedelta(day)


def prepare_data_for_insert():
    logger.info('Prepare data before inserting to database.')
    start_year_date = date(START_YEAR, 1, 1)
    end_year_date = date(END_YEAR, 1, 1)
    years_days = int((end_year_date - start_year_date).days)
    step = int(ROWS_COUNT_OF_MONTH / years_days)

    logger.debug('Step count data between days: %s' % step)
    for single_date in date_range(start_year_date, years_days):
        count = 0
        while count < step:
            data = next(cycle(generate_events_for_month()))
            data['date'] = single_date.strftime('%Y-%m-%d')
            yield data
            count += 1


async def insert_data_to_db(conn):
    query_values = (
        (elem.get('id'), elem.get('uid'), elem.get('action'), elem.get('date'))
        for elem in prepare_data_for_insert()
    )
    query = "INSERT INTO metrics.Events (id, uid, action, created_at) VALUES (%s, %s, %s, %s)"

    async with conn.cursor() as cur:
        try:
            await cur.executemany(query, query_values)
            await conn.commit()
        except Exception as e:
            logger.error(e)
            await conn.rollback()


async def main(_loop):
    logger.info("Started insert data to table")
    async with aiomysql.connect(
            host=Config.API_MYSQL_HOST,
            db=Config.API_MYSQL_DATABASE,
            user=Config.API_MYSQL_USER,
            password=Config.API_MYSQL_PASSWORD,
            loop=_loop,
    ) as conn:
        await insert_data_to_db(conn)
        logger.info("Successfully completed.")


def setupLogging():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    logger = setupLogging()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
