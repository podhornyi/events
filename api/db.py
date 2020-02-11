import aiomysql

from settings import Config


async def init_mysql(app):
    engine = await aiomysql.create_pool(
        user=Config.API_MYSQL_USER,
        db=Config.API_MYSQL_DATABASE,
        host=Config.API_MYSQL_HOST,
        password=Config.API_MYSQL_PASSWORD,
        minsize=Config.API_MYSQL_MIN,
        maxsize=Config.API_MYSQL_MAX,
    )

    app['db'] = engine


async def close_mysql(app):
    app['db'].close()
    await app['db'].wait_closed()
