from aiohttp import web
from aiohttp_apispec import querystring_schema

from models import Event
from schemas import get_event_schema, GetEventSchema


async def healthcheck(request: web.Request):
    async with request.app['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT 1')
            return web.json_response(data={'message': 'Connection to db is active'})


@querystring_schema(get_event_schema())
async def create_event(request: web.Request):
    schema_dict = request['querystring']
    event = Event(
        schema_dict.get('id'),
        schema_dict.get('uid'),
        schema_dict.get('action'),
        schema_dict.get('day'),
        schema_dict.get('month'),
    )

    try:
        async with request.app['db'].acquire() as conn:
            await event.create(conn)
            return web.json_response(data={'message': 'created'}, status=200)
    except:
        return web.json_response(data={'error': 'Failed created event.'}, status=400)


@querystring_schema(GetEventSchema)
async def get_count(request: web.Request):
    schema_dict = request['querystring']
    event = Event(
        schema_dict.get('id'),
        schema_dict.get('uid'),
        schema_dict.get('action'),
        schema_dict.get('day'),
        schema_dict.get('month'),
    )

    try:
        async with request.app['db'].acquire() as conn:
            count = await event.get_count(conn)
            return web.json_response(data=dict(count=count))
    except Exception as e:
        return web.json_response(data={'error': str(e)}, status=400)


@querystring_schema(GetEventSchema)
async def get_stats(request: web.Request):
    schema_dict = request['querystring']
    event = Event(
        schema_dict.get('id'),
        schema_dict.get('uid'),
        schema_dict.get('action'),
        schema_dict.get('day'),
        schema_dict.get('month'),
    )

    try:
        async with request.app['db'].acquire() as conn:
            result = await event.get_stats(conn)
            return web.json_response(data=result)
    except Exception as e:
        return web.json_response(data={'error': str(e)}, status=400)
