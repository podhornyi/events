import argparse
import asyncio

import aiomysql

from api.settings import Config

TABLE_NAME = "Events"


async def engine(_loop):
    pool = await aiomysql.create_pool(
        user=Config.API_MYSQL_ROOT_USER,
        db='mysql',
        host=Config.API_MYSQL_HOST,
        password=Config.API_MYSQL_ROOT_PASSWORD,
        minsize=Config.API_MYSQL_MIN,
        maxsize=Config.API_MYSQL_MAX,
        loop=_loop,
    )
    return pool


async def engine_close(engine):
    engine.close()
    await engine.wait_closed()


async def setup_db(admin_engine):
    db_name = Config.API_MYSQL_DATABASE
    db_user = Config.API_MYSQL_USER
    db_pass = Config.API_MYSQL_PASSWORD

    async with admin_engine.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("CREATE USER IF NOT EXISTS '%s'@'localhost' IDENTIFIED BY '%s'" % (db_user, db_pass))
            await cur.execute("CREATE DATABASE IF NOT EXISTS %s CHARACTER SET UTF8mb4 COLLATE utf8mb4_bin" % db_name)
            await cur.execute("GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost'" % (db_name, db_user))


async def teardown_db(admin_engine):
    db_name = Config.API_MYSQL_DATABASE
    db_user = Config.API_MYSQL_USER

    async with admin_engine.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DROP DATABASE IF EXISTS %s" % db_name)
            await cur.execute("DROP USER IF EXISTS '%s'@'localhost'" % db_user)


async def create_tables(admin_engine):
    db_name = Config.API_MYSQL_DATABASE

    async with admin_engine.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("USE %s" % db_name)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS %s
                (
                    id SMALLINT UNSIGNED NOT NULL,
                    uid SMALLINT UNSIGNED NOT NULL,
                    action VARCHAR(12) NOT NULL,
                    created_at DATE NOT NULL,
                    CONSTRAINT events_id_check CHECK (id < 9999),
                    CONSTRAINT events_uid_check CHECK (uid < 9999),
                    CONSTRAINT events_action_check CHECK (LENGTH(action) > 3 and length(action) < 13),
                    INDEX comb_created_at_action_idx (created_at, action, id, uid)
                );
            """ % TABLE_NAME)


async def drop_tables(admin_engine):
    db_name = Config.API_MYSQL_DATABASE

    async with admin_engine.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("USE %s" % db_name)
            await cur.execute("DROP TABLE IF EXISTS %s" % TABLE_NAME)


async def main(_loop, action):
    admin_engine = await engine(_loop)

    if action == 'init':
        await setup_db(admin_engine)
        await create_tables(admin_engine)
    elif action == 'destroy':
        await drop_tables(admin_engine)
        await teardown_db(admin_engine)

    await engine_close(admin_engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initializing/destroying database')
    parser.add_argument('-a', '--action', help='Actions with database.',
                        choices=['init', 'destroy'], required=True)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, args.action))
