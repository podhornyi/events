from aiohttp import web

from views import healthcheck, create_event, get_count, get_stats


def setup_routes(app):
    app.router.add_routes([
        web.get('/healthcheck', healthcheck),
        web.post('/event', create_event),
        web.get('/count', get_count),
        web.get('/stats', get_stats),
    ])
