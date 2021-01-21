class Repository:
    _table = ''
    _entity = ''
    _cache = {}

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

    # Fetch one entity by a given id. If already once requested it does not send another SQL to the database
    def fetch_by_id(self, rowid: int):
        if int in self._cache:
            return self._cache[id]

        result = self._database.load_one(
            'SELECT rowid as id, * FROM ' + self.table + ' WHERE rowid=? LIMIT 1',
            [rowid]
        )

        self._cache[id] = self.entity(**dict(result))

        return self._cache[id]

    # Fetches all data for this repository and return a list of entities
    def fetch_all(self) -> list:
        result = self._database.load_all(
            'SELECT rowid as id, * FROM ' + self.table,
            []
        )

        rows = []
        for item in result:
            entity = self.entity(**dict(item))
            self._cache[entity.id] = entity

            rows.append(entity)

        return rows

    # Removes one row from the database by a given id
    def remove(self, rowid: int):
        self._database.delete(
            'DELETE FROM ' + self.table + ' WHERE rowid=?',
            [rowid]
        )

        del self._cache[rowid]

    # Creates a entity by a dictionary, saves it to the database and returns the corresponding entity
    def create(self, attr: dict):
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
            self.table,
            ','.join(list(attr.keys())),
            ','.join(['?'] * len(attr))
        )

        return self.fetch_by_id(
            self._database.insert(sql, list(attr.values()))
        )
