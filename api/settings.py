import os


class Config:
    API_MYSQL_HOST = os.environ.get('API_MYSQL_HOST')
    API_MYSQL_DATABASE = os.environ.get('API_MYSQL_DATABASE')

    API_MYSQL_MIN = int(os.environ.get('API_MYSQL_MIN'))
    API_MYSQL_MAX = int(os.environ.get('API_MYSQL_MAX'))

    API_MYSQL_ROOT_USER = os.environ.get('API_MYSQL_ROOT_USER')
    API_MYSQL_ROOT_PASSWORD = os.environ.get('API_MYSQL_ROOT_PASSWORD')

    API_MYSQL_USER = os.environ.get('API_MYSQL_USER')
    API_MYSQL_PASSWORD = os.environ.get('API_MYSQL_PASSWORD')
