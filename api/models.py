import calendar
import datetime

FORMAT = '%Y-%m-%d'


class Event:
    def __init__(self, id: int, uid: int, action: str, day: datetime.date, month: datetime.date):
        self.id = id
        self.uid = uid
        self.action = action
        self.day = day
        self.month = month
        self._values = dict()

    async def create(self, conn):
        values = [self.id, self.uid, self.action, datetime.date.today().strftime(format=FORMAT)]
        query = 'INSERT INTO metrics.Events (id, uid, action, created_at) VALUE (%s, %s, %s, %s)'

        async with conn.cursor() as cur:
            try:
                await cur.execute(query, values)
                await conn.commit()
            except:
                await conn.rollback()
                raise

    async def get_count(self, conn):
        query = 'SELECT COUNT(id) FROM metrics.Events WHERE %s' % self._get_where_expression()
        async with conn.cursor() as cur:
            await cur.execute(query, self._values)
            count = await cur.fetchone()
            return count

    async def get_stats(self, conn):
        query_data = '''
                SELECT id, uid, action, DATE_FORMAT(created_at, '%%%%Y-%%%%m-%%%%d')
                FROM metrics.Events 
                WHERE %s
        ''' % self._get_where_expression()
        query_count = '''
                SELECT count(id) as row_count
                FROM metrics.Events 
                WHERE %s
        ''' % self._get_where_expression()
        result = dict()
        result_payload = []
        async with conn.cursor() as cur:
            await cur.execute(query_data, self._values)
            rows_data = await cur.fetchall()

            await cur.execute(query_count, self._values)
            rows = await cur.fetchall()
            for row in rows_data:
                result_payload.append({
                    'id': row[0],
                    'uid': row[1],
                    'action': row[2],
                    'created_at': row[3]
                })
                
            for row in rows_count:
                result['total'] = row[0]
        result['payload'] = result_payload
        return result_payload

    def _get_where_expression(self):
        where_expression = ''
        if self.day:
            where_expression += 'created_at = %(created_at)s'
            self._values['created_at'] = self.day.strftime(FORMAT)
        elif self.month:
            last_day_of_month = calendar.monthlen(self.month.year, self.month.month)
            date_start = self.month.strftime(FORMAT)
            date_end = self.month.replace(day=last_day_of_month).strftime(FORMAT)
            where_expression += f'created_at between %(date_start)s and %(date_end)s'
            self._values['date_start'] = date_start
            self._values['date_end'] = date_end
            
        if self.id:
            where_expression += 'id = %(id)s and '
            self._values['id'] = self.id
        if self.uid:
            where_expression += 'uid = %(uid)s and '
            self._values['uid'] = self.uid
        if self.action:
            where_expression += 'action = %(action)s and '
            self._values['action'] = self.action
       
        return where_expression
