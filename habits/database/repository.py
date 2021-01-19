class Repository:
    _table = ''
    _entity = ''

    def __init__(self, database, config):
        if self.entity not in config.get('entities'):
            print("TODO Exception")
        self._database = database
        self._config = config

    @property
    def table(self) -> str:
        return self._table

    @property
    def entity(self) -> str:
        return self._entity

    def fetch_by_id(self, rowid: int):
        result = self._database.load_one(
            'SELECT rowid as id, * FROM ' + self.table + ' WHERE rowid=? LIMIT 1',
            [rowid]
        )
        return self.entity(**dict(result))

    def fetch_all(self) -> list:
        result = self._database.load_all(
            'SELECT rowid as id, * FROM ' + self.table,
            []
        )

        rows = []
        for item in result:
            rows.append(self.entity(**dict(item)))

        return rows

    def remove(self, rowid: int):
        self._database.delete(
            'DELETE FROM ' + self.table + ' WHERE rowid=?',
            [rowid]
        )

    def create(self, attr: dict):
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
            self.table,
            ','.join(list(attr.keys())),
            ','.join(['?'] * len(attr))
        )

        return self.fetch_by_id(
            self._database.insert(sql, list(attr.values()))
        )
