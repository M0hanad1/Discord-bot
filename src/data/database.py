import pymongo


class Database:
    def __init__(self, host: str, database: str) -> None:
        self.client = pymongo.MongoClient(host, connect=False)
        self.db = self.client[database]
        self.collections = {}

    def remove_database(self):
        self.client.drop_database(self.db)

    def add_collection(self, *collections: str):
        for i in collections:
            self.collections[i] = self.db[i]

    def remove_collection(self, collection: str):
        self.db.drop_collection(self.collections[collection])

    def add_post(self, collection: str, *post: dict):
        self.collections[collection].insert_many([i for i in post])

    def remove_post(self, collection: str, filter: dict):
        self.collections[collection].delete_many(filter)

    def find_post(self, collection: str, filter: dict):
        return (i for i in self.collections[collection].find(filter))

    def update_post(self, collection: str, filter: dict, changes: dict):
        self.collections[collection].update_many(filter, changes, upsert=True)

    def check_post(self, collection: str, filter: dict):
        for _ in self.find_post(collection, filter):
            return True

        return False


# data = Database('localhost', 'discord-bot')
# data.add_collection('servers', 'users')
# test = data.find_post('users', {'score': {'$exists': True}})

# for i in test:
#     print(i['_id'], i['score'])