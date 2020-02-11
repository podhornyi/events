import logging

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from db import init_mysql, close_mysql
from routes import setup_routes

if __name__ == '__main__':
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(init_mysql)
    app.on_cleanup.append(close_mysql)

    logging.basicConfig(level=logging.DEBUG)

    setup_aiohttp_apispec(app)
    app.middlewares.append(validation_middleware)

    web.run_app(app)
