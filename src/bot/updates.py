from src.data.data import Data


class Updates(Data):
    def __init__(self) -> None:
        super().__init__()

    def get_all_updates(self):
        result = {}

        for i in self.get_server({'updates': {'$exists': True}}):
            result[i['_id']] = [i['updates']['channel']]

            if 'message' in i['updates']:
                result[i['_id']].append(i['updates']['message'])

        return result

    def get_updates(self, server_id):
        for i in self.get_server({'_id': server_id, 'updates': {'$exists': True}}):
            if 'message' in i['updates']:
                return [i['updates']['channel'], i['updates']['message']]

            return [i['updates']['channel']]

        return []

    def remove_updates(self, server_id):
        self.update_server({'_id': server_id}, {'$unset': {'updates': ''}})
        self.check_server_len(server_id)

    def add_channel(self, server_id, channel_id):
        self.update_server({'_id': server_id}, {'$set': {'updates.channel': channel_id}})

    def add_message(self, server_id, message):
        self.update_server({'_id': server_id}, {'$set': {'updates.message': message}})

    def remove_message(self, server_id):
        self.update_server({'_id': server_id}, {'$unset': {'updates.message': ''}})
